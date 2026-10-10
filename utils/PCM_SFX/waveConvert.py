import argparse
import numpy
import sys
import resampy
import pathlib
import wave
from tkinter import messagebox

from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from support.outputBundle import OutputBundle

filterValues    = ['kaiser_best','kaiser_fast']
bitdepthValues  = ['5bit']
playerateValues = ['6960','6991','7020','9279','10440','11090','12180','13920','14040','no resample']

class CmdInterface():
    
    def __init__(self,args):
        self.args = args

    def process(self):

        args = self.args
        if args.bitpackPCM or args.alignPCM256 or args.bitDepth != '5bit':
            raise ValueError('Only unpacked 5-bit PCM is supported; alignment and packing options are not implemented')
        
        if not args.filein:
            print("Error: file required for CLI mode")
            sys.exit(1)

        result, convertInfo, pcmHeader, pcmData = WavRead(args.filein).readFile()

        if not result:
            print(f'Error: {convertInfo}')
            sys.exit(1)
        
        print(f'Wav/RIFF Info: {convertInfo}')
        filename = pathlib.Path(args.filein).stem

        saveDir = args.destinationPath
        playbackRate = args.playback
        pcmHeader['resampleFilter'] = args.resampleFilter
        pcmHeader['playbackRate']   = int( (playbackRate,pcmHeader['SamplesPerSec'])[playbackRate in ("no_resample", "no resample") or args.resampleFilter == "no_resample"] )
        print(f"New sample rate: {pcmHeader['playbackRate']}")

        message, newSampleData, eightBitData = ConvertWave().convertPCMData(pcmHeader,pcmData)

        newSampleData = newSampleData + [0x80]


        filename = (args.overridename.strip(),filename)[args.overridename == ""]
        includePath = args.includePath

        writePCM(saveDir, filename, includePath, newSampleData,
                 eightBitData if args.debug else None)
        print('HuPCM file saved.')



class ConvertWave():

    def __init__(self):
        pass

    def convertPCMData(self, sampleObj, sampleData, ):
        sampleDepth     = sampleObj['BitsPerSample']
        sr_orig         = sampleObj['SamplesPerSec']
        playbackRate    = sampleObj['playbackRate']
        resampleFilter  = sampleObj['resampleFilter']

        # promote all sample data to signed 16bit
        if sampleDepth == 16:
            # need to convert any originally signed data back to signed data. Shouldn't affect 8bit samples stored as 16bit data
            sampleData = [ (sample, sample - 0x10000)[sample > 0x7fff] for sample in sampleData ]
        elif sampleDepth == 8:
            sampleData = [ (sample - 128) * 256 for sample in sampleData ]
        else:
            print('error unknown bit depth')
            return 'ERROR: Unknown sample format', [], []

        # Update with corrected values.
        sampleData = [sample * 1.5 for sample in sampleData]
        sampleData = [ (sample, -32767)[sample < -32767] for sample in sampleData]
        sampleData = [ (sample, 32767)[sample > 32767] for sample in sampleData]

        # use resampy to resample down to target frequency
        if sr_orig != playbackRate:
            orgData = numpy.array(sampleData)
            newSampleData = resampy.resample(orgData, sr_orig, playbackRate, filter=resampleFilter)
        else:
            newSampleData = sampleData

        # numpy arrays are great and all, but let's convert this base to a python list
        newSampleData = [ int(sample) for sample in newSampleData ]

        # need to clamp the samples because.. well.. you know.. filters.
        newSampleData = [ (sample, -32767)[sample < -32767] for sample in newSampleData]
        newSampleData = [ (sample, 32767)[sample > 32767] for sample in newSampleData]

        eightbitSampleData = [ ((sample + 32767) >> 8)   for sample in newSampleData ]

        # Convert the data to PCE 5bit format
        newSampleData = [ (sample + 32767) >> 11 for sample in newSampleData ]

        return '', newSampleData, eightbitSampleData


class WavRead():
    """Read only the declared PCM data, accepting RIFF metadata chunks."""
    def __init__(self, filename, debug=False):
        self.filename = filename
        self.debug = debug

    def readFile(self):
        try:
            with wave.open(str(self.filename), 'rb') as source:
                channels = source.getnchannels()
                width = source.getsampwidth()
                rate = source.getframerate()
                frames = source.getnframes()
                if channels != 1 or width not in (1, 2) or rate <= 0:
                    raise ValueError('Expected mono 8-bit or 16-bit PCM with a positive sample rate')
                # Read any partial final frame too, so odd 16-bit data fails.
                data = source.readframes(frames + 1)
                if not frames or len(data) != frames * width:
                    raise ValueError('Empty or truncated PCM data')
                samples = [int.from_bytes(data[i:i+width], 'little')
                           for i in range(0, len(data), width)]
                header = dict(Channels=channels, BitsPerSample=width*8,
                              SamplesPerSec=rate, DataIDsize=len(data), fmtType=1)
                return True, f'{width*8}-bit mono PCM, {rate} Hz, {frames} samples', header, samples
        except (OSError, EOFError, wave.Error, ValueError) as error:
            return False, str(error), {}, []


def writeDebugPCM(saveDir, filename, samples, eightBitData, outputs=None):
    standalone = outputs is None
    outputs = OutputBundle() if standalone else outputs
    folder = pathlib.Path(saveDir or '.')
    for suffix, data in (('8bit', eightBitData),
                         ('5it_as_8bit', [(sample >> 3) << 3 for sample in eightBitData]),
                         ('5bit', samples)):
        with outputs.open(folder / f'{filename}.debug.{suffix}.bin', 'wb') as output:
            output.write(bytes(data))
    if standalone:
        outputs.commit()


def writePCM(saveDir, filename, includePath, samples, eightBitData=None):
    """Use the same bank-safe output for GUI and command line conversion."""
    folder = pathlib.Path(saveDir or '.')
    if not filename or filename in ('.', '..') or any(c in filename for c in '/\\\r\n"'):
        raise ValueError('PCM name must be a file name without directories')
    include = (pathlib.PurePosixPath(includePath.replace('\\', '/')) / (filename+'.data.inc')).as_posix()
    if any(c in include for c in '\r\n"'):
        raise ValueError('Invalid assembly include path')
    outputs = OutputBundle()
    with outputs.open(folder/(filename+'.inc')) as output:
        output.write('  .db bank(.sample)\n  .dw .sample\n  .page 2\n.sample\n'
                     f'  .include "{include}"\n')
    with outputs.open(folder/(filename+'.data.inc')) as output:
        for offset in range(0, len(samples), 16):
            if offset % 4096 == 0:
                output.write('  .page 2\n')
            output.write('  .db '+','.join(f'${value:02x}' for value in samples[offset:offset+16])+'\n')
    if eightBitData is not None:
        writeDebugPCM(saveDir, filename, samples, eightBitData, outputs)
    outputs.commit()


class GuiFrontend():

    def __init__(self, args):
        self.pcmData    = []
        self.pcmHeader  = {}
        self.components = {}
        self.args       = args
        self.filename = ''

    def openWave(self):

        filename = fd.askopenfilename(defaultextension='.wav', filetypes = (("wav files","*.wav"),("all files","*")))
        if filename == '' or filename == None:
            print('Cancel open..')
            return
        
        result, convertInfo, self.pcmHeader, self.pcmData = WavRead(filename).readFile()

        if not result:
            self.componentState(tk.DISABLED)
            self.filename = ''
            messagebox.showerror(title="Failed...", message=convertInfo)
            return
        
        messagebox.showinfo(title="Wav/RIFF Info", message=convertInfo)
        self.componentState(tk.NORMAL)
        self.filename = pathlib.Path(filename).stem
        self.sfxnameVar.set(self.filename)

        return result


    def saveFile(self):

        saveDir = fd.askdirectory()
        if not saveDir:
            return
        try:
            self.exportFile(saveDir)
        except (OSError, ValueError) as error:
            messagebox.showerror(title='PCM export failed', message=str(error))
            return
        messagebox.showinfo(title='Export complete', message='HuPCM assembly files saved.')

    def exportFile(self, saveDir):
        playbackRate = self.components['playback'].get()
        self.pcmHeader['resampleFilter'] = self.components['filter'].get()
        self.pcmHeader['playbackRate']   = int( (playbackRate,self.pcmHeader['SamplesPerSec'])[playbackRate == "no resample"] )

        message, newSampleData, eightBitData = ConvertWave().convertPCMData(self.pcmHeader,self.pcmData)

        # All streams need the end marker, including "no resample" exports.
        newSampleData = newSampleData + [0x80]


        filename = (self.sfxnameVar.get().strip(),self.filename)[self.sfxnameVar.get().strip() == ""]
        includePath = self.includePath.get().strip()

        writePCM(saveDir, filename, includePath, newSampleData,
                 eightBitData if self.components['debug'].get() == 'On' else None)

    def componentState(self, compState):
        for frame in ('subframe1', 'subframe2'):
            for child in self.components[frame].winfo_children():
                state = 'readonly' if compState == tk.NORMAL and isinstance(child, ttk.Combobox) else compState
                child.configure(state=state)
        self.components['bitdepth'].configure(state=tk.DISABLED)
        self.components['bitpack'].configure(state=tk.DISABLED)
        self.components['save'].configure(state=compState)


    def process(self):
        root = tk.Tk()
        self.components['root'] = root
        root.title("Wav/RIFF to HuPCM Converter")


        frame1 = tk.LabelFrame(root,padx=24, pady=24)
        frame1.pack()

        subframe1 = tk.LabelFrame(frame1, padx=4, pady=4)
        subframe1.pack(side=tk.LEFT)
        self.components['subframe1'] = subframe1

        labelTop = ttk.Label(subframe1, text = "Filter Type")
        labelTop.grid(column=0, row=0)
        filterCombo = ttk.Combobox(subframe1, values=filterValues)
        self.components['filter'] = filterCombo
        filterCombo.grid(column=0, row=1)
        # no_resample is represented by the playback selector in the GUI.
        filterCombo.set('kaiser_best' if self.args.resampleFilter == 'no_resample' else self.args.resampleFilter)

        labelTop = ttk.Label(subframe1, text = "Bit Depth")
        labelTop.grid(column=0, row=2)
        bitdepthCombo = ttk.Combobox(subframe1, values=bitdepthValues)
        self.components['bitdepth'] = bitdepthCombo
        bitdepthCombo.grid(column=0, row=3)
        bitdepthCombo.current(0)

        labelTop = ttk.Label(subframe1, text = "Playback Rate")
        labelTop.grid(column=0, row=4)
        playerateCombo = ttk.Combobox(subframe1, values=playerateValues)
        self.components['playback'] = playerateCombo
        playerateCombo.grid(column=0, row=5)
        playerateCombo.set('no resample' if self.args.resampleFilter == 'no_resample'
                          else self.args.playback.replace('_', ' '))

        labelTop = ttk.Label(subframe1, text = "Debug")
        labelTop.grid(column=0, row=6)
        debugCombo = ttk.Combobox(subframe1, values=['Off','On'])
        self.components['debug'] = debugCombo
        debugCombo.grid(column=0, row=7)
        debugCombo.current(int(bool(self.args.debug)))

        labelTop = ttk.Label(subframe1, text = "Bit Pack PCM")
        labelTop.grid(column=0, row=8)
        bitpackCombo = ttk.Combobox(subframe1, values=['Off'])
        self.components['bitpack'] = bitpackCombo
        bitpackCombo.grid(column=0, row=9)
        bitpackCombo.current(0)



        subframe2 = tk.LabelFrame(frame1, padx=4, pady=4)
        subframe2.pack(side=tk.LEFT)
        self.components['subframe2'] = subframe2

        labelTop = ttk.Label(subframe2, text = "Include Path: ")
        labelTop.grid(column=0, row=0)
        self.includePath = tk.StringVar()
        includePath = tk.Entry(subframe2,textvariable=self.includePath)
        self.components['path'] = includePath
        includePath.grid(column=1, row=0)
        labelTop = ttk.Label(subframe2, text = "PCM name: ")
        labelTop.grid(column=0, row=1)
        self.sfxnameVar = tk.StringVar()
        sfxname = tk.Entry(subframe2,textvariable=self.sfxnameVar )
        self.components['sfxname'] = sfxname
        sfxname.grid(column=1, row=1)




        subframe3 = tk.LabelFrame(frame1, padx=4, pady=4)
        subframe3.pack(side=tk.LEFT)
        self.components['subframe3'] = subframe3

        openButton   = tk.Button(subframe3, text='     Open WAV       ', command=self.openWave)
        openButton.grid(row=0, column=0,sticky=tk.W)
        saveButton   = tk.Button(subframe3, text='     Save HuPCM    ', command=self.saveFile)
        self.components['save'] = saveButton
        saveButton.grid(row=2, column=0,sticky=tk.W)


        self.componentState(tk.DISABLED)

        root.mainloop()


#############################################################################################################
#############################################################################################################
#............................................................................................................
#                                                                                                           .
# Main                                                                                                      .
#............................................................................................................

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert WAV to PCE PCM.',
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    runOptionsGroup = parser.add_argument_group('Run options', 'Run options for WAV converter')
    runOptionsGroup.add_argument('--filein',
                                    '-f',
                                    required=False,
                                    default="",
                                    help='File input for CLI mode.')
    runOptionsGroup.add_argument('--overridename',
                                    required=False,
                                    default="",
                                    help='Provides a new file name for the pcm export.')
    runOptionsGroup.add_argument('--destinationPath',
                                    '-destpth',
                                    required=False,
                                    default="",
                                    help='Copies the newly created files to a specific path.')
    runOptionsGroup.add_argument('--includePath',
                                    '-incpth',
                                    required=False,
                                    default="",
                                    help='Relative path prefix for file ".include"')
    runOptionsGroup.add_argument('--NoSongNameSubfolder',
                                    '-nosub',
                                    required=False,
                                    action="store_true",
                                    help=argparse.SUPPRESS)
    runOptionsGroup.add_argument('--bitpackPCM',
                                    '-pack',
                                    action="store_true",
                                    default=False,
                                    help=argparse.SUPPRESS)
    runOptionsGroup.add_argument('--debug',
                                    '-dbg',
                                    default=False,
                                    action="store_true",
                                    help='Write raw 8-bit and 5-bit PCM debug files.')
    runOptionsGroup.add_argument('--alignPCM256',
                                    '-align256',
                                    action="store_true",
                                    default=False,
                                    help=argparse.SUPPRESS)
    runOptionsGroup.add_argument('--resampleFilter',
                                    '-refil',
                                    choices=['kaiser_best','kaiser_fast','no_resample'],
                                    default='kaiser_best',
                                    help='See https://resampy.readthedocs.io/ documentation for info on filters.')
    runOptionsGroup.add_argument('--bitDepth',
                                    '-bdpth',
                                    choices=bitdepthValues,
                                    default='5bit',
                                    help='The bit depth for streaming PCM samples.')
    runOptionsGroup.add_argument('--playback',
                                    '-pb',
                                    choices=['6960','6991','7020','9279','10440','11090','12180','13920','14040','no_resample'],
                                    default='6960',
                                    help='The playback rate for PCM samples.')
    runOptionsGroup.add_argument('--noGui',
                                    '-ng',
                                    action="store_true",
                                    default=False,
                                    help='Forces command line only.')

    args = parser.parse_args()
    if args.bitpackPCM or args.alignPCM256:
        parser.error('Only unpacked 5-bit PCM is supported; packing and alignment options are unavailable.')

    if args.NoSongNameSubfolder:
        parser.error('WAV exports already use destinationPath directly; omit --NoSongNameSubfolder.')

    if not args.noGui:
        GuiFrontend(args).process()
    else:
        try:
            CmdInterface(args).process()
        except (OSError, ValueError) as error:
            parser.exit(1, f"Error: {error}\n")

import argparse
import os
import numpy
import sys
import resampy
import pathlib

from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk

HEXbase = 16
DECbase = 10
INT_MAX = 2**32 - 1
INT_MIN = (INT_MAX) / -2 - 1

runOptions = {}
components = {}
filterValues    = ['kaiser_best','kaiser_fast','sinc_window_32','sinc_window_Hann']
bitdepthValues  = ['5bit']
playerateValues = ['6960','6991','7020','9279','10440','11090','12180','13920','14040','no resample']


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

    def __init__(self, filename, debug=False):
        self.wavHeader      = {}
        self.wavContents    = []
        self.contentIndex   = 0
        self.content        = None
        self.filename       = filename
        self.message        = ''
        self.debug          = debug

    def readFile(self):
        try:
            with open(self.filename,'rb') as f:
                self.content = f.read()
                self.content = [int(item) & 0xff for item in self.content]
        except Exception as e:
            print(f'Error reading contents: {e}')
            return False

        print('File read.')

        result = self.content != None and self.getWavHeader() and self.getWaveData()
        
        return result, self.message, self.wavHeader, self.wavContents


    # ///////////////////////////////////////////////////////////////////////
    def getWavHeader(self):

        RiffID          = self.read4cc()
        RiffIDsize      = self.intReadLE()
        WaveID          = self.read4cc()

        FmtID           = self.read4cc()
        FMTsize         = self.intReadLE()
        fmtType         = self.wordReadLE()

        Channels        = self.wordReadLE()

        SamplesPerSec   = self.intReadLE()
        AvgBytesPerSec  = self.intReadLE()

        BlockAlign      = self.wordReadLE()
        BitsPerSample   = self.wordReadLE()

        DataID          = self.read4cc()
        DataIDsize      = self.intReadLE()

        if RiffID != 'RIFF':
            self.message = "\n Possible incorrect or corrupt wave file. No RIFF ID. \n"
        elif WaveID != 'WAVE':
            self.message = "\n Possible incorrect or corrupt wave file. No WAVE ID. \n"
        elif FmtID != 'fmt ':
            self.message = "\n Possible incorrect or corrupt wave file. No FMT ID. \n"
        elif DataID != 'data':
            self.message = "\n Possible incorrect or corrupt wave file. No DATA ID. \n"
        elif FMTsize != 0x10:
            self.message = "\n Unsupported RIFF FMT format or correct wavefile. \n"
        elif (BitsPerSample!=8) and (BitsPerSample!=16):
            self.message = f"\n Wave file must be 8bit or 16bit in depth. Found: {BitsPerSample}bit\n"
        elif Channels > 1:
            self.message = f"\n More than 1 channel support isn't currently implemented. \n"
        else:
            self.wavHeader = {
                'RiffID'            : RiffID,
                'RiffIDsize'        : RiffIDsize,
                'WaveID'            : WaveID,
                'FMT'               : FmtID,
                'FMTsize'           : FMTsize,
                'fmtType'           : fmtType,
                'Channels'          : Channels,
                'SamplesPerSec'     : SamplesPerSec,
                'AvgBytesPerSec'    : AvgBytesPerSec,
                'BlockAlign'        : BlockAlign,
                'BitsPerSample'     : BitsPerSample,
                'DataID'            : DataID,
                'DataIDsize'        : DataIDsize
            }

            self.message  = f" Bit depth: {BitsPerSample}\n"
            self.message += f" Channels:  {Channels}\n"
            self.message += f" Rate:      {SamplesPerSec}\n"
        
        print(self.message)

        return self.wavHeader != {}

    # ///////////////////////////////////////////////////////////////////////
    def getWaveData(self):

        numChans    = self.wavHeader['Channels']
        pcmSize     = self.wavHeader['BitsPerSample'] // 8
        step        = numChans * pcmSize

        if self.debug:
            print(f' {self.contentIndex}, {len(self.content)}, {step}, {pcmSize}')

        for idx in range(self.contentIndex, len(self.content), step):

            vals = self.content[idx:idx+step]

            for vidx in range(0,len(vals),pcmSize):
                sample = 0
                sample  |= int(vals[vidx]) & 0xff
                if pcmSize == 2:
                    sample |= (int(vals[vidx+1]) & 0xff) << 8
                self.wavContents.append(sample)

        if self.debug:
            with open('debug.bin','wb') as f:
                for val in self.wavContents:
                    if pcmSize == 2:
                        f.write(bytearray([val>>8 & 0xff]))
                    f.write(bytearray([val & 0xff]))

        return self.wavContents != []

    # ///////////////////////////////////////////////////////////////////////
    # Helper functions
    # ///////////////////////////////////////////////////////////////////////

    def read4cc(self):
        data = self.content[self.contentIndex : self.contentIndex+4 ]
        self.contentIndex += 4
        return ''.join([chr(val) for val in data])
    
    def intReadBE(self):
        idx = self.contentIndex
        self.contentIndex += 4
        val  = self.content[idx+0:idx+1][0] << 24
        val |= self.content[idx+1:idx+2][0] << 16
        val |= self.content[idx+2:idx+3][0] <<  8
        val |= self.content[idx+3:idx+4][0] <<  0
        return val

    def intReadLE(self):
        idx = self.contentIndex
        self.contentIndex += 4
        val  = self.content[idx+0:idx+1][0] <<  0
        val |= self.content[idx+1:idx+2][0] <<  8
        val |= self.content[idx+2:idx+3][0] << 16
        val |= self.content[idx+3:idx+4][0] << 24
        return val

    def wordReadBE(self):
        idx = self.contentIndex
        self.contentIndex += 2
        val  = self.content[idx+0:idx+1][0] << 8
        val |= self.content[idx+1:idx+2][0] << 0
        return val

    def wordReadLE(self):
        idx = self.contentIndex
        self.contentIndex += 2
        val  = self.content[idx+0:idx+1][0] << 0
        val |= self.content[idx+1:idx+2][0] << 8
        return val

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

        if not result and tk.messagebox.showerror(title="Failed...", message=convertInfo):
            return
        
        tk.messagebox.showinfo(title="Wav/RIFF Info", message=convertInfo)
        self.componentState(tk.NORMAL)
        self.filename = self.sfxnameVar.set(pathlib.Path(filename).stem)

        return result


    def saveFile(self):

        saveDir = fd.askdirectory()
        playbackRate = self.components['playback'].get()
        self.pcmHeader['resampleFilter'] = self.components['filter'].get()
        self.pcmHeader['playbackRate']   = int( (playbackRate,self.pcmHeader['SamplesPerSec'])[playbackRate == "no resample"] )

        message, newSampleData, eightBitData = ConvertWave().convertPCMData(self.pcmHeader,self.pcmData)

        # TODO, need to add a switch in the GUI for this
        newSampleData = newSampleData + [0x80]

        tk.messagebox.showinfo(title=None, message='HuPCM file saved.')

        filename = (self.sfxnameVar.get().strip(),self.filename)[self.sfxnameVar.get().strip() == ""]
        includePath = self.includePath.get().strip()

        with open(f'{os.path.join(saveDir,filename)}.inc','w') as f:

            # TODO needs to be a GUI option
            f.write(f'\n')
            f.write(f'  .db bank(.sample)\n')
            f.write(f'  .dw .sample\n\n')
            f.write(f'.sample\n\n')
            f.write (f'  .page {2}\n\n')
            f.write(f'  .include \"{os.path.join(includePath,filename)}.data.inc\"\n\n')

        with open(f'{os.path.join(saveDir,filename)}.data.inc','w') as f:
            columnBytes = 0
            sampleCount = 0
            for idx, val in enumerate(newSampleData):
                valString = hex(val)[2:]
                valString = '$'+('','0')[len(valString) == 1] + valString
                if columnBytes == 0:
                    f.write("  .db ")
                f.write(f'{valString}')
                columnBytes += 1
                if columnBytes > 15:
                    f.write("\n")
                    columnBytes = 0
                    if sampleCount >= 16384:
                        f.write(f'\n\n  .page {2}\n\n')
                        sampleCount = 0
                elif idx == len(newSampleData)-1:
                    f.write("\n")
                else:
                    f.write(", ")
                sampleCount += 1

        with open(f'{filename}.debug.8bit.bin','wb') as f:
            f.write(bytearray(eightBitData))

        with open(f'{filename}.debug.5it_as_8bit.bin','wb') as f:
            [ ((sample) >> 3)<<3 for sample in eightBitData ]
            f.write(bytearray([ ((sample) >> 3)<<3 for sample in eightBitData ]))

        with open(f'{filename}.debug.5bit.bin','wb') as f:
            f.write(bytearray(newSampleData))



    def componentState(self, compState):
            for child in self.components["subframe1"].winfo_children():
                child.configure(state=compState)
            for child in self.components["subframe2"].winfo_children():
                child.configure(state=compState)
            self.components["save"].config(state=compState)


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
        filterCombo.current(0)

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
        playerateCombo.current(0)

        labelTop = ttk.Label(subframe1, text = "Debug")
        labelTop.grid(column=0, row=6)
        debugCombo = ttk.Combobox(subframe1, values=['Off','On'])
        self.components['debug'] = debugCombo
        debugCombo.grid(column=0, row=7)
        debugCombo.current(0)

        labelTop = ttk.Label(subframe1, text = "Bit Pack PCM")
        labelTop.grid(column=0, row=8)
        bitpackCombo = ttk.Combobox(subframe1, values=['Off','On'])
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

def auto_int(val):
    val = int(val, (DECbase,HEXbase)['0x' in val])
    return val

parser = argparse.ArgumentParser(description='Convert WAV to PCE PCM.',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

runOptionsGroup = parser.add_argument_group('Run options', 'Run options for DMF converter')
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
                                help='Stops util from using the song name as a sub folder.')
runOptionsGroup.add_argument('--bitpackPCM',
                                '-pack',
                                action="store_true",
                                default=False,
                                help='Bit packs the 5bit the samples.')
runOptionsGroup.add_argument('--debug',
                                '-dbg',
                                default=False,
                                action="store_true",
                                help='Output uncompressed DMF as raw bin and hex s-record.')
runOptionsGroup.add_argument('--alignPCM256',
                                '-align256',
                                action="store_true",
                                default=False,
                                help='Forces all samples to take up a multiple of 256 bytes and block aligns to 256byte boundaries - remaining values will be 0.')
runOptionsGroup.add_argument('--resampleFilter',
                                '-refil',
                                choices=['kaiser_best','kaiser_fast','sinc_window_32','sinc_window_Hann','default'],
                                default='kaiser_best',
                                help='See https://resampy.readthedocs.io/ documentation for info on filters.')
runOptionsGroup.add_argument('--bitDepth',
                                '-bdpth',
                                choices=['4bit','4.5bit','5bit','5.5bit','6bit','6.5bit','7bit'],
                                default='5bit',
                                help='The bit depth for streaming PCM samples.')
runOptionsGroup.add_argument('--playback',
                                '-pb',
                                choices=['6960','6991','7020','9279','10440','11090','12180','13920','14040'],
                                default='6960',
                                help='The playback rate for PCM samples.')
runOptionsGroup.add_argument('--noGui',
                                '-ng',
                                action="store_true",
                                default=False,
                                help='The bit depth for streaming PCM samples.')

args = parser.parse_args()

runOptions['destinationPath'] = args.destinationPath
runOptions['subFolder']       = ('songName','')[args.NoSongNameSubfolder]
runOptions['includePath']     = args.includePath
runOptions['bitpackPCM']      = args.bitpackPCM
runOptions['bitDepth']        = args.bitDepth
runOptions['resampleFilter']  = args.resampleFilter
runOptions['playback']        = args.playback
runOptions['alignPCM256']     = args.alignPCM256
runOptions['debug']           = args.debug

if not args.noGui:
    GuiFrontend(args).process()
else:
    print(f'Only GUI mode is operational')

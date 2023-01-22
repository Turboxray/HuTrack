import argparse
import os
import numpy
import sys
import resampy

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
bitdepthValues  = ['4bit','4.5bit','5bit','5.5bit','6bit','6.5bit','7bit']
playerateValues = ['6960','6991','7020','9279','10440','11090','12180','13920','14040']


class ConvertWave():

    def __init__(self):
        pass

    def convertPCMData(self, sampleObj):
        sampleDepth = sampleObj.sampleDepth
        data        = sampleObj.sampleData
        sampleRate  = sampleObj.sampleRate
        samplePitch = sampleObj.samplePitch
        sampleNum   = sampleObj.sampleNum

        # promote all sample data to signed 16bit
        if sampleDepth == 16:
            # need to convert any originally signed data back to signed data. Shouldn't affect 8bit samples stored as 16bit data
            data = [ (sample, sample - 0x10000)[sample > 0x7fff] for sample in data ]
        elif sampleDepth == 8:
            data = [ (sample - 128) * 256 for sample in data ]
        else:
            print('error unknown bit depth')
            sampleObj.sampleName = 'ERROR: Unknown sample format'
            sampleObj.sampleData = []
            sampleObj.samplePCE  = []
            return

        # Update with corrected values.
        sampleObj.sampleData = data[::]

        data = [sample * 1.5 for sample in data]
        data = [ (sample, -32767)[sample < -32767] for sample in data]
        data = [ (sample, 32767)[sample > 32767] for sample in data]

        # use resampy to resample down to target frequency
        orgData = numpy.array(data)
        sr_orig = RATE_VAL[sampleRate] * PITCH_VAL[samplePitch]
        newSampleData = resampy.resample(orgData, sr_orig, int(self.params['playback']), filter=self.params['resampleFilter'])

        # numpy arrays are great and all, but let's convert this base to a python list
        newSampleData = [ int(sample) for sample in newSampleData ]

        # need to clamp the samples because.. well.. you know.. filters.
        newSampleData = [ (sample, -32767)[sample < -32767] for sample in newSampleData]
        newSampleData = [ (sample, 32767)[sample > 32767] for sample in newSampleData]

        # DEBUG
        # if sampleDepth == 8:
        #     eightbitSampleData = [ ((sample + 32767) >> 8)   for sample in newSampleData ]
            # with open(f'{sampleData.sampleName}.pre.bin','wb') as fout:
            #     fout.write(bytearray(eightbitSampleData))

        if self.params['debug']:
            filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.{sampleNum}.8bit.bin').replace("\\","/")
            with open(os.path.join(runOptions['destinationPath'],filename),'wb') as fout:
                eightbitSampleData = [ ((sample + 32767) >> 8)   for sample in newSampleData ]
                fout.write(bytearray(eightbitSampleData))

        # Convert the data to PCE 5bit format
        newSampleData = [ (sample + 32767) >> 11 for sample in newSampleData ]

        sampleObj.samplePCE = newSampleData[::]

# ///////////////////////////////////////////////////////////////////////
# int get_file_info( FILE *bin )
# {


#             rewind(bin);
#             RiffID=int_read_be(bin);
#             RiffIDsize=int_read_le(bin);
#             WaveID=int_read_be(bin);
#             FMT=int_read_be(bin);
#             WaveIDsize=int_read_le(bin);

#             FormatTag=wrd_read_le(bin);
#             Channels=wrd_read_le(bin);

#             SamplesPerSec=int_read_le(bin);
#             AvgBytesPerSec=int_read_le(bin);

#             BlockAlign=wrd_read_le(bin);
#             BitsPerSample=wrd_read_le(bin);

#             DataID=int_read_be(bin);
#             DataIDsize=int_read_le(bin);


#             if(RiffID!='RIFF')
#               { printf("\n Possible incorrect or corrupt wave file. No RIFF ID. \n"); fclose(bin); exit(-1); }
#             if(WaveID!='WAVE')
#               { printf("\n Possible incorrect or corrupt wave file. No WAVE ID. \n"); fclose(bin); exit(-1); }
#             if(FMT!='fmt ')
#               { printf("\n Possible incorrect or corrupt wave file. No FMT ID. \n"); fclose(bin); exit(-1); }
#             if(DataID!='data')
#               { printf("\n Possible incorrect or corrupt wave file. No DATA ID. \n"); fclose(bin); exit(-1); }
#             if((BitsPerSample!=8) && (BitsPerSample!=16))
#               { printf("\n Wave file must be 8bit or 16bit in depth. \n"); fclose(bin); exit(-1); }

#             printf("\n Bit depth: %d", BitsPerSample);
#             printf("\n Channels: %d", Channels);
#             printf("\n Rate: %dhz", SamplesPerSec);



#       return 0;
# }

def openWave():

    global hutrack, components

    filename = fd.askopenfilename(defaultextension='.dmf', filetypes = (("dmf files","*.dmf"),("all files","*")))
    filename = filename

    if filename == '' or filename == None:
        print('Cancel open..')
        return


def saveFile():
    tk.messagebox.showinfo(title=None, message='HuTrack pce file saved.')


def componentState(compState):
        for child in components["subframe1"].winfo_children():
            child.configure(state=compState)
        for child in components["subframe2"].winfo_children():
            child.configure(state=compState)
        components["export"].config(state=compState)
        components["save"].config(state=compState)

def initGui():
    root = tk.Tk()
    components['root'] = root
    root.title("DMF to HuTrack Converter")


    frame1 = tk.LabelFrame(root,padx=24, pady=24)
    frame1.pack()

    subframe1 = tk.LabelFrame(frame1, padx=4, pady=4)
    subframe1.pack(side=tk.LEFT)
    components['subframe1'] = subframe1

    labelTop = ttk.Label(subframe1, text = "Filter Type")
    labelTop.grid(column=0, row=0)
    filterCombo = ttk.Combobox(subframe1, values=filterValues)
    components['filter'] = filterCombo
    filterCombo.grid(column=0, row=1)
    filterCombo.current(0)

    labelTop = ttk.Label(subframe1, text = "Bit Depth")
    labelTop.grid(column=0, row=2)
    bitdepthCombo = ttk.Combobox(subframe1, values=bitdepthValues)
    components['bitdepth'] = bitdepthCombo
    bitdepthCombo.grid(column=0, row=3)
    bitdepthCombo.current(2)

    labelTop = ttk.Label(subframe1, text = "Playback Rate")
    labelTop.grid(column=0, row=4)
    playerateCombo = ttk.Combobox(subframe1, values=playerateValues)
    components['playback'] = playerateCombo
    playerateCombo.grid(column=0, row=5)
    playerateCombo.current(0)

    labelTop = ttk.Label(subframe1, text = "Debug")
    labelTop.grid(column=0, row=6)
    debugCombo = ttk.Combobox(subframe1, values=['Off','On'])
    components['debug'] = debugCombo
    debugCombo.grid(column=0, row=7)
    debugCombo.current(0)

    labelTop = ttk.Label(subframe1, text = "Bit Pack PCM")
    labelTop.grid(column=0, row=8)
    bitpackCombo = ttk.Combobox(subframe1, values=['Off','On'])
    components['bitpack'] = bitpackCombo
    bitpackCombo.grid(column=0, row=9)
    bitpackCombo.current(0)



    subframe2 = tk.LabelFrame(frame1, padx=4, pady=4)
    subframe2.pack(side=tk.LEFT)
    components['subframe2'] = subframe2

    labelTop = ttk.Label(subframe2, text = "Include Path: ")
    labelTop.grid(column=0, row=0)
    includePath = tk.Entry(subframe2)
    components['path'] = includePath
    includePath.grid(column=1, row=0)
    labelTop = ttk.Label(subframe2, text = "Song name: ")
    labelTop.grid(column=0, row=1)
    songname = tk.Entry(subframe2)
    components['song'] = songname
    songname.grid(column=1, row=1)
    labelTop = ttk.Label(subframe2, text = "dest path: ")
    labelTop.grid(column=0, row=2)
    destpath = tk.Entry(subframe2)
    components['destpath'] = destpath
    destpath.grid(column=1, row=2)
    labelTop = ttk.Label(subframe2, text = "subFolder: ")
    labelTop.grid(column=0, row=2)
    subFolder = tk.Entry(subframe2)
    components['subFolder'] = subFolder
    subFolder.grid(column=1, row=2)


    subframe3 = tk.LabelFrame(frame1, padx=4, pady=4)
    subframe3.pack(side=tk.LEFT)
    components['subframe3'] = subframe3

    openButton   = tk.Button(subframe3, text='     Open DMF       ', command=openWave)
    openButton.grid(row=0, column=0,sticky=tk.W)
    saveButton   = tk.Button(subframe3, text='     Save DMF    ', command=saveFile)
    components['save'] = saveButton
    saveButton.grid(row=2, column=0,sticky=tk.W)


    componentState(tk.DISABLED)

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
                                default=False,
                                help='Bit packs the 5bit the samples.')
runOptionsGroup.add_argument('--debug',
                                '-dbg',
                                default=False,
                                action="store_true",
                                help='Output uncompressed DMF as raw bin and hex s-record.')
runOptionsGroup.add_argument('--alignPCM256',
                                '-align256',
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


initGui()

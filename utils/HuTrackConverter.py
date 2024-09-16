
import argparse
import os
import sys

from support.hutrackLib import HuTrackLib


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
playerateValues = ['6960','6991','9279','10440','11090','12180']
hutrack = None




def openDMF():

    global hutrack, components

    filename = fd.askopenfilename(defaultextension='.dmf', filetypes = (("dmf files","*.dmf"),("all files","*")))
    filename = filename

    if filename == '' or filename == None:
        print('Cancel open..')
        return


    runOptions['filein'] = filename
    print(runOptions['filein'])
    runOptions['songName'] = 'converter'

    print("\n saveHuTrack",runOptions)
    hutrackConv = HuTrackLib(params=runOptions)
    result, hutrack = hutrackConv.importDmf()

    if not result and tk.messagebox.showerror(title=None, message='DMF could not be loaded'):
        componentState(tk.NORMAL)
        components['song'].delete(0,tk.END)
        components['song'].insert(0,"")
        componentState(tk.DISABLED)
    else:
        componentState(tk.NORMAL)
        songname = os.path.split(runOptions['filein'])[-1][0:-4]
        destpath = os.path.join(*os.path.split(runOptions['filein'])[0:-1])
        components['song'].delete(0,tk.END)
        components['song'].insert(0,songname)
        components['destpath'].delete(0,tk.END)
        components['destpath'].insert(0,destpath)
        components['subFolder'].delete(0,tk.END)
        components['subFolder'].insert(0,songname)

    del hutrackConv

def componentState(compState):
        for child in components["subframe1"].winfo_children():
            child.configure(state=compState)
        for child in components["subframe2"].winfo_children():
            child.configure(state=compState)
        components["export"].config(state=compState)
        components["save"].config(state=compState)

def exportHuTrack():
    hutrackConv = HuTrackLib(hutrack=hutrack, params=runOptions)
    content = hutrackConv.exportPceHuTrackFile()
    print('debug')
    filename = fd.asksaveasfilename(defaultextension='.hutrack', filetypes = (("hutrack files","*.hutrack"),("any file","*")))
    if filename == '' or filename == None:
        print('Cancel saveAs..')
        return
    with open (filename,"w") as f:
        for line in content:
            f.write(line)
        print('Hutrack file written.')


def saveHuTrack():
    runOptions['destinationPath'] = components['destpath'].get()
    runOptions['subFolder']       = components['subFolder'].get()
    runOptions['songName']        = components['song'].get()
    runOptions['includePath']     = components['path'].get()


    hutrackConv = HuTrackLib(hutrack=hutrack, params=runOptions)
    hutrackConv.exportHuTrackTextFile()

    tk.messagebox.showinfo(title=None, message='HuTrack pce file saved.')


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
    labelTop.grid(column=0, row=3)
    destpath = tk.Entry(subframe2)
    components['destpath'] = destpath
    destpath.grid(column=1, row=3)
    labelTop = ttk.Label(subframe2, text = "subFolder: ")
    labelTop.grid(column=0, row=2)
    subFolder = tk.Entry(subframe2)
    components['subFolder'] = subFolder
    subFolder.grid(column=1, row=2)


    subframe3 = tk.LabelFrame(frame1, padx=4, pady=4)
    subframe3.pack(side=tk.LEFT)
    components['subframe3'] = subframe3

    openButton   = tk.Button(subframe3, text='     Open DMF       ', command=openDMF)
    openButton.grid(row=0, column=0,sticky=tk.W)
    exportButton = tk.Button(subframe3, text='     Export Hutrack ', command=exportHuTrack)
    components['export'] = exportButton
    exportButton.grid(row=1, column=0,sticky=tk.W)
    saveButton   = tk.Button(subframe3, text='     Save DMF    ', command=saveHuTrack)
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

parser = argparse.ArgumentParser(description='Convert DefleMask DMF to PCE HuTrack format.',
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
                                choices=['6960','6991','9279','10440','11090','12180'],
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

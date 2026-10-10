
import argparse
import sys

from support.hutrackLib import HuTrackLib
from pathlib import Path

from tkinter import filedialog as fd
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk


runOptions = {}
components = {}
filterValues    = ['kaiser_best','kaiser_fast']
bitdepthValues  = ['5bit']
playerateValues = ['6960','6991','9279','10440','11090','12180']
hutrack = None




def openDMF():
    global hutrack
    filename = fd.askopenfilename(defaultextension='.dmf', filetypes = (("dmf files","*.dmf"),("all files","*")))
    if not filename:
        return
    hutrack = None
    source = Path(filename)
    runOptions.update(filein=filename, songName=source.stem,
                      destinationPath=str(source.parent), subFolder=source.stem)
    componentState(tk.NORMAL)
    for key, value in (('song', source.stem), ('destpath', str(source.parent)),
                       ('subFolder', source.stem)):
        components[key].delete(0, tk.END)
        components[key].insert(0, value)
    try:
        hutrack = loadGuiSong()
    except (OSError, ValueError) as error:
        componentState(tk.DISABLED)
        messagebox.showerror(title='DMF could not be loaded', message=str(error))

def componentState(compState):
    for frame in ('subframe1', 'subframe2'):
        for child in components[frame].winfo_children():
            state = 'readonly' if compState == tk.NORMAL and isinstance(child, ttk.Combobox) else compState
            child.configure(state=state)
    # The engine accepts unpacked 5-bit PCM only.
    components['bitdepth'].configure(state=tk.DISABLED)
    components['bitpack'].configure(state=tk.DISABLED)
    components['export'].configure(state=compState)
    components['save'].configure(state=compState)


def loadGuiSong():
    """Re-read the source so changed PCM settings are applied to the samples."""
    runOptions.update(
        destinationPath=components['destpath'].get(),
        subFolder=components['subFolder'].get(),
        songName=components['song'].get(),
        includePath=components['path'].get(),
        no_songname=not bool(components['incsongname'].get()),
        no_author=not bool(components['incauthorname'].get()),
        resampleFilter=components['filter'].get(),
        playback=components['playback'].get(),
        debug=components['debug'].get() == 'On',
        bitDepth='5bit', bitpackPCM=False, alignPCM256=False)
    result, song = HuTrackLib(params=runOptions).importDmf()
    if not result:
        raise ValueError('Check that the file is a supported PC Engine legacy DMF. See the console for details.')
    return song

def exportHuTrack():
    filename = fd.asksaveasfilename(defaultextension='.hutrack', filetypes = (("hutrack files","*.hutrack"),("any file","*")))
    if not filename:
        return
    try:
        song = loadGuiSong()
        content = HuTrackLib(hutrack=song, params=runOptions).exportPceHuTrackFile()
        with open(filename, 'w', encoding='utf-8') as output:
            output.writelines(content)
    except (OSError, ValueError) as error:
        messagebox.showerror(title='Text export failed', message=str(error))
        return
    messagebox.showinfo(title='Export complete', message='HuTrack text dump saved.')


def saveHuTrack():
    try:
        song = loadGuiSong()
        HuTrackLib(hutrack=song, params=runOptions).exportHuTrackTextFile()
    except (OSError, ValueError) as error:
        messagebox.showerror(title='Assembly export failed', message=str(error))
        return
    messagebox.showinfo(title='Export complete', message='HuTrack assembly files saved.')


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
    filterCombo.set(runOptions.get('resampleFilter', 'kaiser_best'))

    labelTop = ttk.Label(subframe1, text = "Bit Depth")
    labelTop.grid(column=0, row=2)
    bitdepthCombo = ttk.Combobox(subframe1, values=bitdepthValues)
    components['bitdepth'] = bitdepthCombo
    bitdepthCombo.grid(column=0, row=3)
    bitdepthCombo.current(0)

    labelTop = ttk.Label(subframe1, text = "Playback Rate")
    labelTop.grid(column=0, row=4)
    playerateCombo = ttk.Combobox(subframe1, values=playerateValues)
    components['playback'] = playerateCombo
    playerateCombo.grid(column=0, row=5)
    playerateCombo.set(runOptions.get('playback', '6960'))

    labelTop = ttk.Label(subframe1, text = "Debug")
    labelTop.grid(column=0, row=6)
    debugCombo = ttk.Combobox(subframe1, values=['Off','On'])
    components['debug'] = debugCombo
    debugCombo.grid(column=0, row=7)
    debugCombo.current(int(bool(runOptions.get('debug', False))))

    labelTop = ttk.Label(subframe1, text = "Bit Pack PCM")
    labelTop.grid(column=0, row=8)
    bitpackCombo = ttk.Combobox(subframe1, values=['Off'])
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

    labelTop = ttk.Label(subframe2, text = "subFolder: ")
    labelTop.grid(column=0, row=2)
    subFolder = tk.Entry(subframe2)
    components['subFolder'] = subFolder
    subFolder.grid(column=1, row=2)

    labelTop = ttk.Label(subframe2, text = "dest path: ")
    labelTop.grid(column=0, row=3)
    destpath = tk.Entry(subframe2)
    components['destpath'] = destpath
    destpath.grid(column=1, row=3)

    incsongname = tk.IntVar()
    incsongname.set(1)
    labelTop = tk.Checkbutton(subframe2, text = "Include Song name", variable = incsongname, onvalue=1, offvalue=0)
    labelTop.grid(column=0, row=4)
    components['incsongname'] = incsongname

    incauthorname = tk.IntVar()
    incauthorname.set(1)
    labelTop = tk.Checkbutton(subframe2, text = "Include Author name", variable = incauthorname, onvalue=1, offvalue=0)
    labelTop.grid(column=1, row=4)
    components['incauthorname'] = incauthorname


    subframe3 = tk.LabelFrame(frame1, padx=4, pady=4)
    subframe3.pack(side=tk.LEFT)
    components['subframe3'] = subframe3

    openButton   = tk.Button(subframe3, text='Open DMF', width=18, command=openDMF)
    openButton.grid(row=0, column=0,sticky=tk.W)
    exportButton = tk.Button(subframe3, text='Export text dump', width=18, command=exportHuTrack)
    components['export'] = exportButton
    exportButton.grid(row=1, column=0,sticky=tk.W)
    saveButton   = tk.Button(subframe3, text='Export assembly', width=18, command=saveHuTrack)
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert DefleMask DMF to PCE HuTrack format.',
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    runOptionsGroup = parser.add_argument_group('Run options', 'Run options for DMF converter')
    runOptionsGroup.add_argument('--filein',
                                    default="",
                                    help='DMF file to convert.')
    runOptionsGroup.add_argument('--destinationPath',
                                    '-destpth',
                                    required=False,
                                    default="",
                                    help='Copies the newly created files to a specific path.')
    runOptionsGroup.add_argument('--songname',
                                    required=False,
                                    default="",
                                    help='Name the song to something specific instead of taken from the filen name.')
    runOptionsGroup.add_argument('--includePath',
                                    '-incpth',
                                    required=False,
                                    default="",
                                    help='Relative path prefix for file ".include"')
    runOptionsGroup.add_argument('--subfolder',
                                    required=False,
                                    default=".=songName=.",
                                    help='Use different subfolder than the song file name.')
    runOptionsGroup.add_argument('--bitpackPCM',
                                    '-pack',
                                    nargs='?', const=True,
                                    default=False,
                                    help=argparse.SUPPRESS)
    runOptionsGroup.add_argument('--debug',
                                    '-dbg',
                                    default=False,
                                    action="store_true",
                                    help='Output uncompressed DMF as raw bin and hex s-record.')
    runOptionsGroup.add_argument('--alignPCM256',
                                    '-align256',
                                    nargs='?', const=True,
                                    default=False,
                                    help=argparse.SUPPRESS)
    runOptionsGroup.add_argument('--resampleFilter',
                                    '-refil',
                                    choices=filterValues,
                                    default='kaiser_best',
                                    help='See https://resampy.readthedocs.io/ documentation for info on filters.')
    runOptionsGroup.add_argument('--bitDepth',
                                    '-bdpth',
                                    choices=bitdepthValues,
                                    default='5bit',
                                    help='The bit depth for streaming PCM samples.')
    runOptionsGroup.add_argument('--playback',
                                    '-pb',
                                    choices=['6960','6991','9279','10440','11090','12180'],
                                    default='6960',
                                    help='The playback rate for PCM samples.')
    runOptionsGroup.add_argument('--no_songname',
                                    action='store_true',
                                    help='Do not store song name in output file.')
    runOptionsGroup.add_argument('--no_author',
                                    action='store_true',
                                    help='Do not store author name in output file.')
    runOptionsGroup.add_argument('--no_gui',
                                    action='store_true',
                                    help='Forces command line only.')

    args = parser.parse_args()
    if args.bitpackPCM or args.alignPCM256:
        parser.error('Only unpacked 5-bit PCM is supported; packing and alignment options are unavailable.')

    runOptions['destinationPath'] = args.destinationPath
    runOptions['subFolder']       = args.subfolder
    runOptions['includePath']     = args.includePath
    runOptions['bitpackPCM']      = args.bitpackPCM
    runOptions['bitDepth']        = args.bitDepth
    runOptions['resampleFilter']  = args.resampleFilter
    runOptions['playback']        = args.playback
    runOptions['alignPCM256']     = args.alignPCM256
    runOptions['debug']           = args.debug
    runOptions['no_songname']     = args.no_songname
    runOptions['no_author']       = args.no_author

    if args.no_gui:
        if args.filein == "":
            print(f'Error: filein argument is required for no-gui mode.')
            sys.exit(1)
        runOptions['filein'] = args.filein
        print(runOptions['filein'])
        runOptions['songName'] = 'converter'

        print("\n saveHuTrack",runOptions)
        hutrackConv = HuTrackLib(params=runOptions)
        result, hutrack = hutrackConv.importDmf()

        if not result:
            print('DMF could not be loaded')
            sys.exit(1)
        else:

            runOptions['subFolder'] = (runOptions['subFolder'], Path(args.filein).stem)[runOptions['subFolder'] == '.=songName=.']
            runOptions['destinationPath'] = (runOptions['destinationPath'], Path(args.filein).parent )[runOptions['destinationPath'] == '']
            runOptions['songName'] = (args.songname, Path(args.filein).stem)[args.songname == '']

            hutrackConv = HuTrackLib(hutrack=hutrack, params=runOptions)
            try:
                hutrackConv.exportHuTrackTextFile()
            except (OSError, ValueError) as error:
                parser.exit(1, f"Error: {error}\n")

            print('\nHuTrack pce file saved.')        
    else:
        initGui()

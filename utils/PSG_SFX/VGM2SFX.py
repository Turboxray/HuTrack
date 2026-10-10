
import argparse
import os
import sys
import tkinter as tk
import traceback

from pathlib import Path
from tkinter import filedialog as fd
from tkinter import messagebox

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from support.outputBundle import OutputBundle

version = "1.0.0"

def hexPrintList(aList):
    return f"{[hex(val)[2:] for val in aList]}"

def decodeWaveformList(waveformlist):

    wf_block = []
    if waveformlist == '':
        return []

    with open(waveformlist,'r') as f_in:
        content = f_in.read()

    wf_block = []
    wf_num = -1
    for line in content.split("\n"):
        if '.wf.block' in line:
            wf_num += 1
            wf_block.append([])
            continue

        if line.strip().startswith(".db"):
            line = line.strip().replace("$",'')
            vals = line.split(".db ")[1].split(",")
            vals = [int(val.strip(),16) for val in vals]
            wf_block[wf_num] += vals

    wf_block = [wf_set[:] for wf_set in wf_block if wf_set != []]

    if len(wf_block)>256 or any(len(w)!=32 or any(v<0 or v>31 for v in w) for w in wf_block):
        raise ValueError('Invalid shared pool: expected at most 256 complete five-bit waveforms')

    return wf_block

class GuiGui():

    def __init__(self, args):
        self.args = args
        self.wf_block = []

    def process(self):
        root = tk.Tk()
        root.minsize(width=450, height=250)
        root.geometry("750x250")
        root.title(f"VGM converter. Ver: {version}")

        subframe1 = tk.LabelFrame(root, text='Select Channels',padx=2, pady=2)
        subframe1.grid(row=0, column=0,sticky=tk.W)

        self.chn = []
        for i in range(6):
            self.chn.append(tk.IntVar())
            self.chn[-1].set((0,1)[i==5])
            tk.Checkbutton(subframe1, text=str(i), variable=self.chn[-1]).grid(row=0, column=i,sticky=tk.W)

        subframe2 = tk.LabelFrame(root, text='Debug',padx=2, pady=2)
        subframe2.grid(row=0, column=1,sticky=tk.W)
        self.outputBin = tk.IntVar()
        self.outputLog = tk.IntVar()
        tk.Checkbutton(subframe2, text="bin", variable=self.outputBin).grid(row=0, column=0,sticky=tk.W)
        tk.Checkbutton(subframe2, text="log", variable=self.outputLog).grid(row=0, column=1,sticky=tk.W)

        tk.Button(root, text='Open VGM', command=self.openVGM, width=25).grid(row=2, column=0,sticky=tk.W)
        tk.Button(root, text='Chose output folder', command=self.setOutput, width=25).grid(row=3, column=0,sticky=tk.W)
        tk.Button(root, text='Waveform list', command=self.openWaveform, width=25).grid(row=6, column=0,sticky=tk.W)
        tk.Button(root, text='Convert', command=self.convert, width=25).grid(row=7, column=0,sticky=tk.W)

        action = (self.args.waveformlist,'(None)')[self.args.waveformlist=='']

        self.l1 = tk.Label(root, text = " VGM: (None)")
        self.l1.grid(row=2, column=1,sticky=tk.W)
        self.l2 = tk.Label(root, text = " Output: (None)")
        self.l2.grid(row=3, column=1,sticky=tk.W)
        self.l3 = tk.Label(root, text = "Include path for assembler/source")
        self.l3.grid(row=4, column=1,sticky=tk.W)
        self.l4 = tk.Label(root, text = "SFX file name")
        self.l4.grid(row=5, column=1,sticky=tk.W)
        self.l5 = tk.Label(root, text = f"Waveform List: {action}")
        self.l5.grid(row=6, column=1,sticky=tk.W)

        self.includePath = tk.StringVar()
        self.includePath.set('')
        inputField = tk.Entry(root,textvariable = self.includePath, font = ('calibre',10,'normal'),width=25)
        inputField.grid(row=4, column=0, sticky=tk.W)

        self.sfxFileName = tk.StringVar()
        self.sfxFileName.set('')
        inputField = tk.Entry(root,textvariable = self.sfxFileName, font = ('calibre',10,'normal'),width=25)
        inputField.grid(row=5, column=0, sticky=tk.W)

        root.mainloop()


    def openVGM(self):
        filenames = fd.askopenfilenames(defaultextension='.png', filetypes = (("VGM files","*.vgm"),("all files","*")))

        if not filenames:
            return
        filename = filenames[0]
        if filename == '' or filename == None:
            print('Cancel open..')
            return
        self.l1.config(text=f' VGM: {filename}')
        print(filename)
        self.args.filein = filename
        # self.args.destfolder = os.path.join(os.getcwd(), f'{Path(filename).stem}')
        self.l2.config(text=f' Output: {self.args.destfolder}')
        self.sfxFileName.set(Path(filename).stem)


    def openWaveform(self):
        filenames = fd.askopenfilenames(defaultextension='.wf.inc', filetypes = ((" files","*.wf.inc"),("all files","*")))

        if not filenames:
            return
        filename = filenames[0]
        if filename == '' or filename == None:
            print('Cancel open..')
            return
        self.args.waveformlist = filename
        self.l5.config(text=f' Waveform List: {self.args.waveformlist}')
        print(self.args.waveformlist)


    def setOutput(self):
        filepath = fd.askdirectory()
        if filepath == '' or filepath == None:
            print('Cancel saveAs..')
            return
        print(filepath)
        self.args.destfolder = filepath
        self.buildPath    = filepath
        self.l2.config(text=f' Output: {filepath}')


    def convert(self):

        if self.args.filein == '':
            messagebox.showerror(title='On VGM', message='No VGM file is loaded.')
            return

        configMsg = f'VGM: {self.args.filein}\n\nFolder: {self.args.destfolder}\n\nFilename: {self.sfxFileName.get()}\n\nInclude path: {self.includePath.get()}'

        if not  messagebox.askyesno(title='Confirmation', message=configMsg):
            return

        self.args.dir = self.includePath.get()
        try:
            chanproc = []
            for i in range(6):
                if self.chn[i].get() == 1:
                    chanproc.append(i)
            self.args.chanproc = chanproc

            self.args.debugBin = self.outputBin.get()==1
            self.args.debugLog = self.outputLog.get()==1

            print(f' log: {self.outputLog.get()}, {self.args.debugLog }. bin: {self.outputBin.get()},{self.args.debugBin}')

            self.wf_block = decodeWaveformList(self.args.waveformlist)

            action = ('append','new')[self.args.waveformlist=='']
            wf_list_file = (self.args.waveformlist,self.args.destfolder+".wf.inc")[self.args.waveformlist=='']
            self.l5.config(text=f' Waveform List: {wf_list_file} ({action})')

            self.args.sfxname = self.sfxFileName.get()

            result = ConvertVGM(self.args).process(self.wf_block)
            if result:
                tk.messagebox.showinfo(title='Finished',message='VGM has been converted. Check debug log for any errors or weidness.')
            else:
                tk.messagebox.showerror(title='Error',message=f'Something went wrong. Check to see if debugLog was generated.')
        except Exception as e:
            print(f'{e}\n{traceback.format_exc()}')
            tk.messagebox.showerror(title='Error',message=f'{e}')


class ConvertVGM():

    def __init__(self, args, guiMode=False):
        self.args     = args
        self.guiMode  = guiMode
        self.debugLog = []
        self.wf_block = []

        if self.args.destfolder == '':
            self.args.destfolder = str(Path(self.args.filein).with_suffix(''))

        self.includPathName = os.path.join(self.args.dir,self.args.sfxname).replace('\\','/')

        self.reg_list = { 0 : [],
                          1 : [],
                          2 : [],
                          3 : [],
                          4 : [],
                          5 : [],
                          'num_frames' : 0
                        }

        self.op_len = {
                        0x90 : 4,
                        0x91 : 4,
                        0x92 : 5,
                        0x93 : 10,
                        0x94 : 1,
                        0x95 : 4,
                        0xB9 : 2,
                        0x62:  0,
                        0x66:  0,
                        0x67:  6
                    }

    def process(self, wf_block=None):
        name = self.args.sfxname
        if not name or name in ('.', '..') or any(c in name for c in '/\\\r\n"'):
            raise ValueError('SFX name must be a file name without directories, quotes or line breaks')
        for value in (self.args.dir, self.args.waveformlist):
            if any(c in value for c in '\r\n"'):
                raise ValueError('Invalid assembly include path')
        if not self.args.chanproc or any(ch not in range(6) for ch in self.args.chanproc):
            raise ValueError('Select at least one HuSFX channel from 0..5')
        self.outputs = OutputBundle()
        if not self._process(wf_block):
            return False
        self.outputs.commit()
        return True

    def _process(self, wf_block=None):
        self.wf_block = [list(wave) for wave in (wf_block or [])]
        if len(self.wf_block)>256 or any(len(w)!=32 or any(v<0 or v>31 for v in w) for w in self.wf_block):
            raise ValueError('Expected at most 256 waveforms of 32 five-bit samples')
        self.reg_list = {ch:[] for ch in range(6)}
        self.reg_list['num_frames'] = 0
        self.debugLog = []
        self.debugPrint(f'Opening [{self.args.filein}] ....')
        content = None
        try:
            with open(self.args.filein,"rb") as f:
                content = f.read()
                content = [int(val) for val in content]
        except:
            error = (f'Error: could not read file {self.args.filein}.')
            if self.guiMode:
                raise ValueError(error)
            return False

        if not content:
            error = (f'Error: file {self.args.filein} is empty.')
            if self.guiMode:
                raise ValueError(error)
            return False

        if len(content) < 0x40:
            error = (f'Error: file {self.args.filein} is too small.')
            if self.guiMode:
                raise ValueError(error)
            return False

        if self.get_string(0,4,content) != "Vgm ":
            error = (f'Error: file {self.args.filein} is not identified as "Vgm".')
            if self.guiMode:
                raise ValueError(error)
            return False

        self.debugPrint(f'[{self.get_int(0x08, content)}]')
        if self.get_int(0x08, content) != 0x00000171:
            self.debugPrint(f'WARNING!!!!!: file {self.args.filein} is not the expected version: 0x0171. Found version: {hex(self.get_int(0x08, content))}.')


        if not self.decode_vgm(content):
            return False

        print(f'debug log: {self.args.debugLog}')
        if self.args.debugLog:
            with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.debugLog.txt",'w') as f:
                for line in self.debugLog:
                    f.write(f'{line}\n')

        return True

    def debugPrint(self, msg):
        if self.args.debugConsole:
            print(msg)
        self.debugLog.append(msg)

    def get_PCM(self, dataOffset, operand, content):
        self.debugPrint(f' pcm operand {operand}')
        pcmLen = self.get_int(2,operand)
        if dataOffset+pcmLen>len(content):raise ValueError('Truncated VGM PCM block')
        data = content[dataOffset : dataOffset + pcmLen]
        self.debugPrint(f'^^^^^^^^^^^^^^^ get PCM {hex(pcmLen)}, {hex(dataOffset)}')
        return data, dataOffset+pcmLen

    def get_PatternInfo(self, dataOffset, operand, content):
        dataLen = self.get_int(2,operand)
        if dataLen<9 or dataOffset+dataLen>len(content):raise ValueError('Invalid VGM pattern block')
        data = content[dataOffset : dataOffset + dataLen]
        self.debugPrint(f' block operand {operand}')
        self.debugPrint(f'^^^^^^^^^^^^^^^ get pattern {hex(dataLen)}, data {hexPrintList(data)}, offset {hex(dataOffset)}')
        return data, dataOffset+dataLen

    def decode_vgm(self, content):

        relative = self.get_int(0x34,content)
        dataOffset = relative + 0x34 if relative else 0x40
        if not 0x40 <= dataOffset < len(content):
            raise ValueError('VGM data offset is outside the file')
        ended = False

        stream_channels = {}
        # We do not simulate PCM completion. A stream remains reserved until
        # an explicit stop, but retriggering the same ID/channel is supported.
        # Furnace configures a fixed stream per PCE channel before playback.
        active_streams = {}
        chan_data = { 0:[], 1:[], 2:[], 3:[], 4:[], 5:[] }


        current_channel = 0

        self.samplePCM = []

        while dataOffset < len(content):

            old_offset = dataOffset
            op, operand, dataOffset = self.get_decodeData(dataOffset, content)

            self.debugPrint(f' DEBUG: op {hex(op)}, operand {[hex(val) for val in operand]}, offset {hex(dataOffset)}, current chan {current_channel}')
            if op in list(self.op_len.keys()):
                if op == 0xB9 and operand[0] == 0x00:
                    current_channel = operand[1]
                    self.debugPrint(f'set channel: [{current_channel}]')
            else:
                error = (f'Error: op [{hex(op)}] is not recognised at offset [{hex(old_offset)}]')
                if self.guiMode:
                    raise ValueError(error)
                print(error)
                return False

            if current_channel > 5:
                error = (f'Error: found channel entry [{current_channel}] at offset {hex(old_offset)}. Channels must be between 0 to 5.')
                if self.guiMode:
                    raise ValueError(error)
                print(error)
                return False

            # No need to store the channel select.
            if op == 0xB9 and operand[0] == 0x00:
                self.debugPrint(f'     B9 NO STORE')
                continue

            if op == 0x67 and operand[1] != 0xFE:
                data, dataOffset = self.get_PCM(dataOffset, operand, content)
                self.samplePCM.append(data)
                self.debugPrint(f'     67 NO STORE: {hexPrintList(operand)}')
                continue

            if op == 0x67 and operand[1] == 0xFE:
                data, dataOffset = self.get_PatternInfo(dataOffset, operand, content)
                self.debugPrint(f'     67 PATTERN NO STORE: {hexPrintList(operand)}')

                # capture pattern num -> store in each channel
                for chn_idx in range(6):
                    reg = 10
                    chan_data[chn_idx].append((reg,data[1]))
                    self.debugPrint(f'    chan [{current_channel}], Data: reg {reg}, val {data}')

                    reg = 11
                    p_num = data[3:][chn_idx]
                    chan_data[chn_idx].append((reg,p_num))
                    self.debugPrint(f'    chan [{current_channel}], Data: reg {reg}, val {data}')

                continue


            if op == 0x90:
                # 90: stream ID, chip type, channel (port), DAC register.
                # Furnace can bind stream 0 to channel 5, for example.
                stream, chip, channel, register = operand
                if stream == 255 or chip != 0x1b or channel > 5 or register != 6:
                    raise ValueError('Unsupported PCM stream setup: expected stream 0..254, first HuC6280 chip, channel 0..5, register 6')
                if stream in active_streams and active_streams[stream] != channel:
                    raise ValueError('Stop the PCM stream before remapping its channel; automatic sample completion is not tracked')
                stream_channels[stream] = channel
                self.debugPrint(f'PCM stream {stream} targets channel {channel}')
                continue

            if op in [0x91, 0x92]:
                self.debugPrint(f'     91 NO STORE')
                continue

            if op in [0x93]:
                error = (f'Error: op {hex(op)} is not supported. Found at offset {hex(dataOffset)}, operand data {operand}.')
                if self.guiMode:
                    raise ValueError(error)
                print(error)
                return False

            if op==0xb9 and operand[0]>9:
                raise ValueError('Unsupported PCE register or second chip')

            if op in (0x94, 0x95):
                stream = operand[0]
                if op == 0x94 and stream == 255:
                    # FF is stop-all, never a channel or an ordinary stream ID.
                    for channel in sorted(set(active_streams.values())):
                        chan_data[channel].append((0x94, 0))
                    active_streams.clear()
                    continue
                if stream in stream_channels:
                    channel = stream_channels[stream]
                elif not stream_channels and stream < 6:
                    # Compatibility with old setup-free HuSFX command files.
                    # Once 90 is used, every referenced stream needs a setup.
                    channel = stream
                else:
                    raise ValueError(f'PCM stream {stream} has no HuC6280 setup')
                if op == 0x94:
                    # An inactive stream may alias another stream's channel.
                    # Stopping it must not stop that channel's actual owner.
                    if stream in active_streams:
                        chan_data[active_streams.pop(stream)].append((op, 0))
                else:
                    # 95: stream ID, little-endian block ID, flags. FC retains
                    # one byte for the ID and one for forward/loop flags.
                    sample_id = operand[1] | (operand[2] << 8)
                    flags = operand[3]
                    if sample_id > 255:
                        raise ValueError('HuSFX PCM sample IDs must fit 0..255')
                    if flags & ~1:
                        raise ValueError('HuSFX PCM supports forward playback and looping, not reverse/other flags')
                    if any(other != stream and target == channel for other, target in active_streams.items()):
                        raise ValueError('Stop the previous PCM stream before starting another ID on its channel; automatic sample completion is not tracked')
                    chan_data[channel].append((op, (flags << 24) | (sample_id << 8)))
                    active_streams[stream] = channel
                self.debugPrint(f'PCM stream {stream}, channel {channel}, command {op:#x}')
                continue

            if op in [0x62, 0x66]:
                self.debugPrint(f"\n\n frame{self.reg_list['num_frames']}, adding {chan_data} \n\n")
                for i in range(6):
                    self.reg_list[i].append(chan_data[i][:])
                chan_data = { 0:[], 1:[], 2:[], 3:[], 4:[], 5:[] }
                self.reg_list['num_frames'] += 1
                # Do not reset the channel on frame end!
                self.debugPrint(f'###  Frame end!  #####$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

                if op == 0x66:
                    ended = True
                    break
                else:
                    continue


            reg, data = operand

            chan_data[current_channel].append((reg,data))
            self.debugPrint(f'    chan [{current_channel}], Data: reg {reg}, val {data}')



        self.debugPrint(f"\n\n\n{self.reg_list}\n\n\n")

        if not ended:
            raise ValueError('Truncated VGM: missing end command')
        waveforms, bin_channels = self.consilidateWFupdates()

        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #
        # waveforms ASM file

        # Write actual PCM blocks
        if self.args.debugBin:
            with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.pcm.bin", 'wb') as f:
                for sample in self.samplePCM:
                    for val in sample:
                        val += 0x20
                        val &= 0x1f
                        f.write(bytearray([val]))


        # Flatten waveform block
        waveform_block = []
        for idx, waveform in enumerate(waveforms):
            waveform = list(waveform)
            waveform_block = waveform_block + [val&0xff for val in waveform]

        if self.args.debugBin:
            with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.wf.bin", 'wb') as f:
                f.write(bytearray(waveform_block))

        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #
        # waveforms ASM file

        waveform_labels = []

        # Write actual waveform blocks
        wf_list_file = (self.args.waveformlist,f"{self.args.destfolder}/{self.args.sfxname}.wf.inc")[self.args.waveformlist=='']
        with self.outputs.open(wf_list_file, 'w') as f:
            for idx,waveform in enumerate(waveforms):
                waveform = list(waveform)
                f.write(f'\n  .page 2\n.wf.block{idx}\n')
                waveform_labels.append(f'.wf.block{idx}')
                output_str = self.asciiWaveform(waveform) + " "
                for idx, val in enumerate(waveform):
                    val = hex(val&0xff)[2:]
                    val = ('','0')[len(val)<2] + val
                    if idx % 8 == 0:
                        output_str = output_str[:-1]
                        output_str += f'\n  .db ${val},'
                    else:
                        output_str += f'${val},'
                output_str = output_str[:-1]+'\n'

                f.write(f'{output_str}')


        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #
        # channel data

        # The output is an SFX stream; optional Furnace pattern markers are retained.

        totalSongdataBinsize = 0
        data_labels = []
        for num, chan_block in bin_channels.items():
            print(f'chan mask: {self.args.chanproc }, {num}')
            if num not in self.args.chanproc:
                continue

            if self.args.debugBin:
                with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.chan{num}.bin",'wb') as f:
                    self.debugPrint(f' saving {num}: {chan_block}')
                    prep_block = self.encodeChannel(chan_block)
                    f.write(bytearray(prep_block))
                print(f' - Chan {num} bin size: {len(prep_block)}.')
                totalSongdataBinsize += len(prep_block)

            wait_frame = 0
            with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.chan{num}.inc",'w') as f:
                output_str = f"\n  .page 2\n.data.chan{num}\n"
                data_labels.append(f".data.chan{num}")
                output_str += f"\n\n;..........................\n; frame 0\n"

                skip_byte  = 0
                for idx, val in enumerate(chan_block):

                    if skip_byte > 0 :
                        skip_byte -= 1
                        continue

                    if val == 0xffff:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, 0 , len(build_str))
                        wait_frame += 1
                        output_str += f"\n\n;..........................\n; frame {wait_frame}\n"
                        skip_byte = 0
                        continue

                    elif val >= 0x00 and val <= 0x1f:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, 0, len(build_str))
                        skip_byte = 0
                    elif val >= 0x20 and val <= 0x3f:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, 0, len(build_str))
                        skip_byte = 0
                    elif val >= 0x40 and val <= 0x5f:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, 0, len(build_str))
                        skip_byte = 0
                    elif val >= 0x80 and val <= 0x9f:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, 0, len(build_str))
                        skip_byte = 0
                    elif val >= 0xA0 and val <= 0xAB:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex(chan_block[idx+1]&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    elif val >= 0xC0 and val <= 0xCf:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex(chan_block[idx+1]&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    elif val == 0xB0:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex(chan_block[idx+1]&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    elif val == 0xFC:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex((chan_block[idx+1]>>8)&0xff)[2:]}'
                        build_str  += f', ${hex((chan_block[idx+1]>>24)&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    elif val == 0xFD:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, 0, len(build_str))
                        skip_byte = 0
                    elif val == 0xFE:
                        build_str   = f'\n  .page 2\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex(chan_block[idx+1]&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    else:
                        error = (f'Error: cannot identify token command: chan {num}, offset {hex(idx)}, val {hex(val)}.')
                        # if self.args.gui:
                        #     raise ValueError(error)
                        print(error)
                        return False

                build_str   = f'\n  .db $fb'
                output_str += build_str
                output_str += self.commentDecode(0xfb, 0x00, len(build_str))
                f.write(output_str)

        print(f' - Total channel bin size: {totalSongdataBinsize} bytes.\n')

        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #
        # Support files

        # Write waveform table file.
        with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.wfTable.inc", 'w') as f:
            f.write(f'\n;'+("#"*75)+'\n')
            f.write(f'\n  .page 2\n.waveform.table\n')
            f.write(f'\n  .dw ${hex(len(waveform_labels)*2)[2:]}       ; offset to bank table\n\n')
            for idx, wf_label in enumerate(waveform_labels):
                f.write(f"  .dw {wf_label}\n")
            f.write(f'\n\n; Banks\n\n')
            for idx, wf_label in enumerate(waveform_labels):
                f.write(f"  .db bank({wf_label})\n")

        # Write data table file.
        with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.dataTable.inc", 'w') as f:
            f.write(f'\n;'+("#"*75)+'\n')
            f.write(f'\n  .page 2\n.data.table\n')
            f.write(f'\n  .dw ${hex(len(data_labels)*2)[2:]}       ; offset to bank table\n\n')
            for idx, wf_label in enumerate(data_labels):
                f.write(f"  .dw {wf_label}\n")
            f.write(f'\n\n; Banks\n\n')
            for idx, wf_label in enumerate(data_labels):
                f.write(f"  .db bank({wf_label})\n")


        # Separate waveform inc
        with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.sfx_wf.inc","w") as f:
            f.write(f' .include "{self.includPathName+".wfTable.inc"}"\n')
            f.write(f' .include "{(self.args.waveformlist.replace("\\","/") if self.args.waveformlist else self.includPathName+".wf.inc")}"\n')

        # Separate data inc
        with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.sfx_data.inc","w") as f:
            f.write(f' .include "{self.includPathName+".dataTable.inc"}"\n')
            for num in range(6):
                if num not in self.args.chanproc:
                    continue
                f.write(f' .include "{self.includPathName}.chan{num}.inc"\n')

        with self.outputs.open(f"{self.args.destfolder}/{self.args.sfxname}.sfx_main.inc","w") as f:
            f.write(f' .include "{self.includPathName+".sfx_wf.inc"}"\n')
            f.write(f' .include "{self.includPathName+".sfx_data.inc"}"\n')




        self.debugPrint(f'Done')
        return True

    @staticmethod
    def encodeChannel(chan_block):
        """Serialize internal tokens, whose packed FC operand is not one byte."""
        output = []
        index = 0
        while index < len(chan_block):
            op = chan_block[index]
            index += 1
            if op == 0xffff:
                output.append(0xff)
                continue
            output.append(op)
            if op == 0xfc:
                if index == len(chan_block):
                    raise ValueError('Missing packed FC operand')
                packed = chan_block[index]
                output.extend(((packed >> 8) & 0xff, (packed >> 24) & 0xff))
                index += 1
            elif 0xa0 <= op <= 0xab or op == 0xb0 or 0xc0 <= op <= 0xcf or op == 0xfe:
                if index == len(chan_block):
                    raise ValueError(f'Missing operand for {op:#x}')
                output.append(chan_block[index] & 0xff)
                index += 1
            elif not (0 <= op <= 0x5f or 0x80 <= op <= 0x9f or op == 0xfd):
                raise ValueError(f'Unknown HuSFX token {op:#x}')
        output.append(0xfb)
        return output

    def asciiWaveform(self, waveform):

        if self.args.disablecomment:
            return ""

        waveform_array = []
        for idx, val in enumerate(waveform):
            column_array = []
            val = val&0xff

            if val == 0:
                column_array = [" " for i in range(15)] + [":"]
            elif val == 31:
                column_array = [":" for i in range(16)]
            else:
                column_array = [":" for i in range(((val+1)//2))] + [(" ",".")[val % 2 == 0]]
                column_array = column_array + [" " for i in range(16-len(column_array)) ]
                column_array = column_array[::-1]

            waveform_array.append(column_array[:])

        graphString = ""
        for row in range(16):
            graphString += "\n;    "
            for col in range(32):
                graphString += f'{waveform_array[col][row]}'*2
            graphString += f"   {(' ','')[row>7]+hex(row<<1)[2:]}  ;"

        graphString +="\n\n;     0 1 2 3 4 5 6 7 8 9 A B C D E F 0 1 2 3 4 5 6 7 8 9 A B C D E F   ;"

        return graphString + "\n"


    def commentDecode(self, val, opr, length):
        if self.args.disablecomment:
            return ""

        output_str  = (48-length)*" "
        if val == 0xffff:
            output_str += f" ; Wait vblank"
        elif val >= 0x00 and val <= 0x1f:
            output_str += f" ; 804 -> ${hex(val)[2:]}"
        elif val >= 0x20 and val <= 0x3f:
            output_str += f" ; 804 -> ${hex(val-0x20+0xC0)[2:]}"
        elif val >= 0x40 and val <= 0x5f:
            output_str += f" ; 804 -> ${hex(val)[2:]}"
        elif val >= 0x80 and val <= 0x9f:
            output_str += f" ; 804 -> ${hex(val)[2:]}"
        elif val >= 0xA0 and val <= 0xA9:
            output_str += f" ; 80{hex(val)[2:][-1]} -> ${hex(opr)[2:]}"
        elif val == 0xAA:
            output_str += f" ; Pattern Index # {opr}"
        elif val == 0xAB:
            output_str += f" ; Pattern # {opr}"
        elif val >= 0xC0 and val <= 0xCf:
            output_str += f" ; 802 -> ${hex(opr)[2:]}, 803 -> ${hex(val & 15)[2:]}"
        elif val == 0xB0:
            output_str += f" ; Waveform update #${hex(opr)[2:]}"
        elif val == 0xFB:
            output_str += f" ; End of channel stream"
        elif val == 0xFC:
            output_str += f" ; Play fixed sample # {(opr>>8)&0xff} @ flag {hex((opr>>24)&0xff)}"
        elif val == 0xFD:
            output_str += f" ; Stop sample"
        elif val == 0xFE:
            output_str += f" ; Wait vblank {opr} frames."
        else:
            error = (f'Error: cannot identify token command {val} .')
            if self.guiMode:
                raise ValueError(error)
            print(error)
            return False

        return output_str

    def consilidateWFupdates(self):

        self.prep_reg_list = {  0 : {},
                                1 : {},
                                2 : {},
                                3 : {},
                                4 : {},
                                5 : {},
                                'num_frames' : 0 }

        for chan in range(6):
            control = 0
            for frame, entries in enumerate(self.reg_list[chan]):
                output = []
                pending = []
                def flush():
                    if len(pending)==32 and not control&0x40:
                        output.append({'reg':6, 'data':pending[:]})
                    else:
                        output.extend({'reg':6, 'data':[value]} for value in pending)
                    pending.clear()
                for reg, value in entries:
                    if reg in (10,11):
                        continue # Furnace pattern metadata is not a PSG write.
                    if reg==6:
                        pending.append(value&31)
                        if len(pending)==32:flush()
                    else:
                        flush()
                        output.append({'reg':reg,'data':[value]})
                        if reg==4:control=value
                flush()
                self.prep_reg_list[chan][frame]=output
        self.prep_reg_list['num_frames']=self.reg_list['num_frames']

        self.debugPrint(f"############################################### waveform prep\n\n ")

        waveform_list = self.wf_block[:]

        self.debugPrint(f' PRE PRE PRE wf_list:' )
        for a_list in waveform_list:
            self.debugPrint(a_list)

        temp_list = []
        for chan,data_set in self.prep_reg_list.items():
            if chan == 'num_frames':
                continue

            for frame, data_frame in data_set.items():
                if data_frame == []:
                    continue

                for data_pair in data_frame:
                    reg = data_pair['reg']
                    data = data_pair['data']
                    if reg == 0x06 and len(data) == 32:
                        waveform = [val&0xff for val in data]
                        if not self.waveformCheck(waveform, waveform_list):
                            temp_list.append(waveform[:])
                            waveform_list.append(waveform[:])


        # B0 has one byte for its waveform index. The ASM writer masks values
        # to a byte, so an overflowing shared pool would silently select wave 0.
        if len(waveform_list) > 256:
            raise ValueError(f'HuSFX supports at most 256 shared waveforms; found {len(waveform_list)}')

        self.debugPrint(f'temp_list: ' )
        for a_list in temp_list:
            self.debugPrint(a_list)
        self.debugPrint(f'wf_list:' )
        for a_list in waveform_list:
            self.debugPrint(a_list)

        self.debugPrint(f'waveform list len {len(waveform_list)}')

        self.debugPrint(f"############################################### waveform list\n\n ")


        # assign waveform call
        for chan,data_set in self.prep_reg_list.items():
            if chan == 'num_frames':
                continue

            for frame, data_frame in data_set.items():
                if data_frame == []:
                    continue

                for idx,data_pair in enumerate(data_frame):
                    reg = data_pair['reg']
                    data = data_pair['data']
                    if reg == 0x06 and len(data) == 32:
                        waveform = [val&0xff for val in data]
                        waveform_index = self.getWaveformIndex(waveform, waveform_list)
                        self.prep_reg_list[chan][frame][idx] = { 'reg' : 0x10, 'data' : [waveform_index] }




        # Only adjacent low/high period writes may be combined. Isolated low
        # writes remain raw register commands; duplicate control/DDA writes can
        # have hardware side effects and must not be discarded.
        for chan in range(6):
            for frame, entries in self.prep_reg_list[chan].items():
                output=[]
                index=0
                while index<len(entries):
                    entry=entries[index]
                    if entry['reg']==2 and index+1<len(entries) and entries[index+1]['reg']==3:
                        output.append({'reg':2,'data':[entry['data'][0],entries[index+1]['data'][0]&15]})
                        index+=2
                    else:
                        output.append(entry)
                        index+=1
                self.prep_reg_list[chan][frame]=output

        bin_output = { 0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
        bin_test = []
        for chan,data_set in self.prep_reg_list.items():
            if chan == 'num_frames':
                continue

            previous_bin_frame = []
            empty_frame_run = False
            previous_frame_empty = False
            empty_frame_count = 0
            for frame, data_frame in data_set.items():
                if data_frame == []:
                    bin_output[chan].append(0xffff)
                    self.debugPrint(f'@@@@@@@@@ reg convert: ** empty ** , frame {frame}, chan {chan}')
                    continue

                for idx,data_pair in enumerate(data_frame):
                    reg = data_pair['reg']
                    data = data_pair['data']

                    self.debugPrint(f'@@@@@@@@@ reg convert: reg {hex(reg)} , data {data}, frame {frame}, chan {chan}')
                    alt_volume = False
                    if reg == 0x04:
                        reg = data[0]
                        if reg >=0 and reg <= 0x1f:
                            pass
                        elif reg >=0x40 and reg <= 0x5f:
                            pass
                        elif reg >=0x80 and reg <= 0x9f:
                            pass
                        elif reg >=0xC0 and reg <= 0xDf:
                            reg = reg - 0xc0 + 0x20
                        else:
                            print(f"ERROR ERROR ERROR: reg value for volume is unknown: reg {hex(data_pair['reg'])} , data {hex(data_pair['data'][0])}, frame {frame}, chan {chan}")
                            self.debugPrint(f'Leaving it as is. Hope it works.')
                            reg  = 0xA4
                            data = data[0]
                            alt_volume = True

                        bin_output[chan].append(reg)
                        bin_test.append(reg)
                        if alt_volume:
                            alt_volume = False
                            bin_output[chan].append(data)
                            bin_test.append(data)
                    elif reg == 0x94:
                        reg = 0xFD
                        bin_output[chan].append(reg)
                        bin_test.append(reg)
                    elif reg == 0x95:
                        reg = 0xFC
                        data = data[0]
                        bin_output[chan].append(reg)
                        bin_output[chan].append(data)
                        bin_test.append(reg)
                        bin_test.append(data)
                    elif reg == 0x02 and len(data)==2:
                        reg = data[1] + 0xC0
                        data = data[0]
                        bin_output[chan].append(reg)
                        bin_output[chan].append(data)
                        bin_test.append(reg)
                        bin_test.append(data)
                    else:
                        reg  = reg + 0xA0
                        data = data[0]
                        bin_output[chan].append(reg)
                        bin_output[chan].append(data)
                        bin_test.append(reg)
                        bin_test.append(data)
                    self.debugPrint(f'       reg convert: reg {hex(reg)} , data {data}')

                bin_output[chan].append(0xffff)

        self.debugPrint(f'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% bin len {len(bin_test)} , {len(bin_test)+(len(waveform_list)*32)}')
        self.debugPrint(f'{len(bin_output[0])}')

        #Print out data for debug
        for chan,data_set in self.prep_reg_list.items():
            if chan == 'num_frames':
                continue

            self.debugPrint(f'Channel: {chan}\n\n')
            for frame, data_frame in data_set.items():
                self.debugPrint(f'    Frame: {frame}')
                if data_frame == []:
                    self.debugPrint(f'        ... empty')
                    continue

                for data_pair in data_frame:
                    reg = data_pair['reg']
                    data = data_pair['data']
                    self.debugPrint(f'            Reg: {reg}, data: {[hex(val) for val in data]}')


        return (waveform_list[:], bin_output)

    def getWaveformIndex(self, waveform, waveform_list):
        # try all 32 rotations
        for wf_idx, cmp_wf in enumerate(waveform_list):
            for i in range(32):
                if self.compare_wf(cmp_wf, self.rotateWF(waveform, i) ):
                    return wf_idx

        return False         

    def waveformCheck(self, waveform, waveform_list):

        # try all 32 rotations\
        for cmp_wf in waveform_list:
            for i in range(32):
                if self.compare_wf(cmp_wf, self.rotateWF(waveform, i) ):
                    return True

        return False            

    def compare_wf(self, wf_1, wf_2):
        wf_1 = list(wf_1)
        wf_2 = list(wf_2)
        result = True
        for i in range(32):
            result &= wf_1[i] == wf_2[i]

        return result

    def rotateWF(self,waveform, idx):
        waveform = list(waveform)
        new_wf = waveform[-idx:] + waveform[:-idx]
        return new_wf

    def get_decodeData(self, offset, content):
        if not 0<=offset<len(content):
            raise ValueError('Truncated VGM command')
        op = content[offset]


        if op not in list(self.op_len.keys()):
            error  = f'failed on decodedata: op [{hex(op)}], offset [{hex(offset)}]'
            error += f'Error: opcode [{content[offset]}] at address {offset} is not recognised.'
            print(error)
            raise ValueError(error)

        if offset+1+self.op_len[op]>len(content):
            raise ValueError(f'Truncated VGM operand at {offset:#x}')
        operand = content[offset + 1 : offset + 1 + self.op_len[op]]
        offset += len(operand)+1

        return (op, operand, offset)

    def get_int(self, offset, content):
        return content[offset+3]<<24 | content[offset+2]<<16 | content[offset+1]<<8 | content[offset+0]

    def get_word(self, offset, content):
        return content[offset+1]<<8 | content[offset+0]

    def get_string(self, offset, length, content):
        if length+offset > len(content):
            error = f'Error: internal error - string offset and length exceeds file length.'
            print(error)
            raise ValueError(error)

        return ''.join([ f'{chr(val)}' for val in content[offset:offset+length]])


#.....................................
# END CLASS


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=f'Convert VGM files to PCEAS source as Data. Ver: {version}',
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    runOptionsGroup = parser.add_argument_group('Run options', 'Run options for TMX converter')
    runOptionsGroup.add_argument('--filein',
                                 '-in',
                                 default='',
                                 help='Source VMG file')
    runOptionsGroup.add_argument('--destfolder',
                                 '-df',
                                 default='',
                                 type=str,
                                 help='path/name for output files')
    runOptionsGroup.add_argument('--sfxname',
                                 default='',
                                 type=str,
                                 help='path/name for output files')
    runOptionsGroup.add_argument('--dir',
                                 '-d',
                                 default='',
                                 type=str,
                                 help='the "include" path for the source generation')
    runOptionsGroup.add_argument('--chanproc',
                                 '-cp',
                                 choices=[0,1,2,3,4,5],
                                 default=[5],
                                 type=int,
                                 nargs="+",
                                 help='Channel number to process. Default: only process channel # 5.')
    runOptionsGroup.add_argument('--disablecomment',
                                 '-dc',
                                 default=False,
                                 action="store_true",
                                 help='Disables comments in the source generation')
    runOptionsGroup.add_argument('--gui',
                                 '-g',
                                 default=False,
                                 action="store_true",
                                 help='Run tool in GUI mode.')
    runOptionsGroup.add_argument('--debugLog',
                                 '-dlog',
                                 default=False,
                                 action="store_true",
                                 help='Output debug log.')
    runOptionsGroup.add_argument('--debugBin',
                                 '-dbin',
                                 default=False,
                                 action="store_true",
                                 help='Output debug binaries.')
    runOptionsGroup.add_argument('--waveformlist',
                                 '-wf',
                                 default="",
                                 help='Use waveform list for SFX processing. Will append if waveforms don\'t exists.')
    runOptionsGroup.add_argument('--debugConsole',
                                 '-dbgOut',
                                 default=False,
                                 action="store_true",
                                 help='Not recommended to turn this on. It will slow down the conversion. Check the debug log which is always generated.')

    args = parser.parse_args()

    args.chanproc = [val for val in args.chanproc if val < 6]

    args.chanproc = list(set(args.chanproc))

    if args.gui:
        sys.exit( GuiGui(args).process() == False )
    elif args.filein != '':
        args.sfxname = (args.sfxname,Path(args.filein).stem)[args.sfxname=='']
        if args.destfolder:
            args.destfolder = os.path.join(args.destfolder)
        sys.exit( ConvertVGM(args).process(decodeWaveformList(args.waveformlist)) == False)
    else:
        print(f'Error: Use --gui or supply a filename for --filein')
        sys.exit(1)

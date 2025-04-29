
import argparse
import os
import sys
import tkinter as tk
import traceback

import json

from pathlib import Path
from tkinter import filedialog as fd
from tkinter import messagebox
from functools import partial

HEXbase = 16
DECbase = 10
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

    wf_block_check = [len(wf_set) for wf_set in wf_block if len(wf_set) != 32]

    if wf_block_check:
        print(f"Error: failed to decode full waveform sets. Found {len(wf_block_check)} sets with incorrect size.")
        for num, wf_set in enumerate(wf_block):
            print(f'Wave set {num} is len {len(wf_set)}')

    wf_block = [wf_set[:] for wf_set in wf_block]
    # print(f'debug - {wf_block}')

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

        configMsg = f'VGM: {self.args.filein}\n\nFolder: {self.buildPath}\n\nFilename: {self.sfxFileName.get()}\n\nInclude path: {self.includePath.get()}'

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

            self.wf_block = decodeWaveformList(args.waveformlist)

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
            self.args.destfolder = self.args.filein

        self.includPathName = os.path.join(self.args.dir,Path(self.args.destfolder).name)

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

        self.op_chan = {
                        0x90 : 2,
                        0xB9 : 0,
                    }

        self.op_reg = {
                        0xB9 : 0,
                        0x94 : 0,
                        0x95 : 0,
                    }

        self.op_reg_data = {
                        0xB9 : 1,
                        0x94 : 1,
                        0x95 : 4
                    }


    def process(self, wf_block=[]):

        if wf_block != []:
            self.wf_block = [[val for val in wf_set] for wf_set in wf_block]
        self.debugPrint(f'Opening [{self.args.filein}] ....')
        content = None
        try:
            with open(self.args.filein,"rb") as f:
                content = f.read()
                content = [int(val) for val in content]
        except:
            error = (f'Error: could not read file {self.args.filein}.')
            if self.args.guiMode:
                raise(error)
            return False

        if not content:
            error = (f'Error: file {self.args.filein} is empty.')
            if self.args.guiMode:
                raise(error)
            return False

        if not len(content) > 0x100:
            error = (f'Error: file {self.args.filein} is too small.')
            if self.args.guiMode:
                raise(error)
            return False

        if self.get_string(0,3,content) != "Vgm":
            error = (f'Error: file {self.args.filein} is not identified as "Vgm".')
            if self.args.guiMode:
                raise(error)
            return False

        self.debugPrint(f'[{self.get_int(0x08, content)}]')
        if self.get_int(0x08, content) != 0x00000171:
            self.debugPrint(f'WARNING!!!!!: file {self.args.filein} is not the expected version: 0x0171. Found version: {hex(self.get_int(0x08, content))}.')


        if not self.decode_vgm(content):
            return False

        print(f'debug log: {self.args.debugLog}')
        if self.args.debugLog:
            with open(f"{self.args.destfolder}/{self.args.sfxname}.debugLog.txt",'w') as f:
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
        data = content[dataOffset : dataOffset + pcmLen]
        self.debugPrint(f'^^^^^^^^^^^^^^^ get PCM {hex(pcmLen)}, {hex(dataOffset)}')
        return data, dataOffset+pcmLen

    def get_PatternInfo(self, dataOffset, operand, content):
        dataLen = self.get_int(2,operand)
        data = content[dataOffset : dataOffset + dataLen]
        self.debugPrint(f' block operand {operand}')
        self.debugPrint(f'^^^^^^^^^^^^^^^ get pattern {hex(dataLen)}, data {hexPrintList(data)}, offset {hex(dataOffset)}')
        return data, dataOffset+dataLen

    def decode_vgm(self, content):

        dataOffset = self.get_int(0x34,content) + 0x34

        channelCount = []
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
                if self.args.guiMode:
                    raise(error)
                print(error)
                return False

            if current_channel > 5:
                #print(f'op: [{hex(op)}], operand: {[hex(val) for val in operand]}, data offset: [{hex(dataOffset)}], chan offset {hex(self.op_chan[op])}')
                error = (f'Error: found channel entry [{hex(operand[self.op_chan[op]])}] at offset {hex(old_offset)}. Channels must be between 0 to 5.')
                if self.args.guiMode:
                    raise(error)
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
                channelCount.append(operand[self.op_chan[op]])
                self.debugPrint(f'     90 NO STORE')
                continue

            if op in [0x91, 0x92]:
                self.debugPrint(f'     91 NO STORE')
                continue

            if op in [0x93]:
                error = (f'Error: op {hex(op)} is not supported. Found at offset {hex(dataOffset)}, operand data {operand}.')
                if self.args.guiMode:
                    raise(error)
                print(error)
                return False

            if op in [0x94]:
                self.debugPrint(f'&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& found op {hex(op)} at offset {hex(dataOffset)}, {operand}, chan {current_channel}')
                reg = 0x94
                data = 0
                chan_data[operand[0]].append((reg,data))
                self.debugPrint(f'PCM PCM PCM    chan [{operand[0]}], Data: {reg}, {data}')
                continue

            if op in [0x95]:
                self.debugPrint(f'&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& found op {hex(op)} at offset {hex(dataOffset)}, {operand}, chan {current_channel}')
                reg = 0x95
                data = 0x01<<24
                data |= operand[1]<<16
                data |= operand[2]<<8
                data |= operand[3]<<0
                chan_data[operand[0]].append((reg,data))
                self.debugPrint(f'PCM PCM PCM    chan [{operand[0]}], Data: {reg}, {data}')
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
                    break
                else:
                    continue


            reg = operand[self.op_reg[op]]
            data = operand[self.op_reg_data[op]]

            chan_data[current_channel].append((reg,data))
            self.debugPrint(f'    chan [{current_channel}], Data: reg {reg}, val {data}')



        self.debugPrint(f"\n\n\n{self.reg_list}\n\n\n")

        waveforms, bin_channels =  self.consilidateWFupdates()

        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #
        # waveforms ASM file

        # Write actual PCM blocks
        if self.args.debugBin:
            with open(f"{self.args.destfolder}/{self.args.sfxname}.pcm.bin", 'wb') as f:
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
            with open(f"{self.args.destfolder}/{self.args.sfxname}.wf.bin", 'wb') as f:
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
        with open(wf_list_file, 'w') as f:
            for idx,waveform in enumerate(waveforms):
                waveform = list(waveform)
                f.write(f'\n.wf.block{idx}\n')
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


        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        encode_delta_bin = self.firstPassPrep(bin_channels, noEncode=False)

        json_string = json.dumps(encode_delta_bin, indent=4)
        with open(self.args.sfxname+'_ENC_chan.txt', 'w') as f:
            f.write(json_string)

        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        frame_rle_eof_data = self.compressFrameEOF(encode_delta_bin)

        json_string = json.dumps(frame_rle_eof_data, indent=4)
        with open(self.args.sfxname+'_RLE-EOF_chan.txt', 'w') as f:
            f.write(json_string)

        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        RLE_bin_channels = self.compressFrameRLE(frame_rle_eof_data)


        json_string = json.dumps(RLE_bin_channels, indent=4)
        with open(self.args.sfxname+'_RLE_chan.txt', 'w') as f:
            f.write(json_string)

        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        no_pattern_compress = False
        if no_pattern_compress:
            new_bin_pattern_channels = RLE_bin_channels
        else:
            new_bin_pattern_channels, chan_playlist, pattern_list_by_index = self.compressPatterns(RLE_bin_channels)

            json_string = json.dumps(new_bin_pattern_channels, indent=4)
            with open(self.args.sfxname+'_pattern-comp_chan.txt', 'w') as f:
                f.write(json_string)

            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            no_consolidate_pattern_chunk = False
            if no_consolidate_pattern_chunk:
                pass
            else:
                new_bin_pattern_channels = self.consolidatePatternBlocks(RLE_bin_channels, chan_playlist, pattern_list_by_index)



        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        totalSongdataBinsize = 0
        data_labels = []
        # Convert any negative numbers into 2's compliment 8bit val
        for num, chan_block in new_bin_pattern_channels.items():
            if num not in self.args.chanproc:
                continue
            for frame_num, frame_block in enumerate(chan_block):
                for frame_idx, val in enumerate(frame_block):
                    if val < 0:
                        val = val * -1
                        val = (val ^ 0xff) + 1
                        new_bin_pattern_channels[num][frame_num][frame_idx] = val

            # Output full binary of song data per channel
            if self.args.debugBin:
                with open(f"{self.args.destfolder}/{self.args.sfxname}.chan{num}.bin",'wb') as f:
                    self.debugPrint(f' saving {num}: {chan_block}')
                    prep_block = []
                    [[prep_block.append(val) for val in frame] for frame in chan_block]
                    try:
                        f.write(bytearray(prep_block))
                    except Exception as e:
                        print(e)
                        print(prep_block)
                    f.write(bytearray([0xFB]))
                print(f' - Chan {num} bin size: {len(prep_block)+1}.')
                totalSongdataBinsize += len(prep_block)+1

        # Separate patterns
        # for num, chan_block in new_bin_pattern_channels.items():
        #     if num not in self.args.chanproc:
        #         continue
        #     pattern_idx = -1
        #     chan_patterns = []
        #     new_data=False
        #     for frame_num, frame_block in enumerate(chan_block):
        #         if frame_block[0] == 0xAA:
        #             pattern_idx +=1
        #             if pattern_idx == 0:
        #                 chan_patterns = chan_patterns + frame_block[:]
        #                 continue
        #             new_data=False
        #             with open(f"{self.args.destfolder}/{self.args.sfxname}.chan{num}.pattern{pattern_idx}.pbin",'wb') as f:
        #                 f.write(bytearray(chan_patterns))
        #             print(f' Chan {num}: pattern {pattern_idx}. size: {len(chan_patterns)}')
        #             chan_patterns = []
        #         else:
        #             chan_patterns = chan_patterns + frame_block[:]
        #             new_data = True
        #     if new_data:
        #         with open(f"{self.args.destfolder}/{self.args.sfxname}.chan{num}.pattern{pattern_idx}.pbin",'wb') as f:
        #             f.write(bytearray(chan_patterns))

        # output full binary of song data
        if self.args.debugBin:
            with open(f"{self.args.destfolder}/{self.args.sfxname}.full.bin",'wb') as f:
                for num, chan_block in new_bin_pattern_channels.items():
                    if num not in self.args.chanproc:
                        continue

                    prep_block = []
                    [[prep_block.append(val) for val in frame] for frame in chan_block]
                    try:
                        f.write(bytearray(prep_block))
                    except Exception as e:
                        print(e)
                        print(prep_block)
                    f.write(bytearray([0xFB]))


        for num, chan_block in new_bin_pattern_channels.items():
            print(f'chan mask: {self.args.chanproc }, {num}')
            if num not in self.args.chanproc:
                continue

            wait_frame = 0
            with open(f"{self.args.destfolder}/{self.args.sfxname}.chan{num}.inc",'w') as f:
                output_str = f"\n.data.chan{num}\n"
                data_labels.append(f".data.chan{num}")

                for frame_num, frame_block in enumerate(chan_block):
                    # print(f"frame num: {frame_num}.Size: {len(frame_block)}")
                    output_str += f"\n\n;..........................\n; frame {frame_num}\n"
                    skip_byte = 0
                    for frame_idx, val in enumerate(frame_block):
                        # print(f"     frame idx: {frame_idx}")
                        if skip_byte > 0 :
                            skip_byte -= 1
                            continue

                        if val >= 0x00 and val <= 0x1f:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, 0, len(build_str))
                            skip_byte = 0
                        elif val >= 0x20 and val <= 0x3f:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, 0, len(build_str))
                            skip_byte = 0
                        elif val >= 0x40 and val <= 0x5f:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, 0, len(build_str))
                            skip_byte = 0
                        elif val >= 0x60 and val <= 0x7f:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, 0, len(build_str))
                            skip_byte = 0
                        elif val >= 0x80 and val <= 0x9f:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, 0, len(build_str))
                            skip_byte = 0
                        elif val >= 0xA0 and val <= 0xAB:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            build_str  += f', ${hex(frame_block[frame_idx+1]&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, frame_block[frame_idx+1], len(build_str))
                            skip_byte = 1
                        elif val >= 0xAC and val <= 0xAF:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, 0, len(build_str))
                            skip_byte = 0
                        elif val == 0xB0:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            build_str  += f', ${hex(frame_block[frame_idx+1]&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, frame_block[frame_idx+1], len(build_str))
                            skip_byte = 1
                        elif val >= 0xB1 and val <= 0xBF:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, 0, len(build_str))
                            skip_byte = 0
                        elif val >= 0xC0 and val <= 0xCF:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            build_str  += f', ${hex(frame_block[frame_idx+1]&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, frame_block[frame_idx+1], len(build_str))
                            skip_byte = 1
                        elif val >= 0xD0 and val <= 0xDF:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            build_str  += f', ${hex(frame_block[frame_idx+1]&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, frame_block[frame_idx+1], len(build_str))
                            skip_byte = 1
                        elif val == 0xF0:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            build_str  += f', ${hex(frame_block[frame_idx+1]&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, frame_block[frame_idx+1], len(build_str))
                            skip_byte = 1
                        elif val >= 0xF1 and val <= 0xF8:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, 0, len(build_str))
                            skip_byte = 0
                        elif val == 0xFC:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            build_str  += f', ${hex((frame_block[frame_idx+1]>>8)&0xff)[2:]}'
                            build_str  += f', ${hex((frame_block[frame_idx+1]>>24)&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, frame_block[frame_idx+1], len(build_str))
                            skip_byte = 1
                        elif val == 0xFD:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, frame_block[frame_idx+1], len(build_str))
                            skip_byte = 0
                        elif val == 0xFE:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            build_str  += f', ${hex(frame_block[frame_idx+1]&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, frame_block[frame_idx+1], len(build_str))
                            skip_byte = 1
                        elif val == 0xFF:
                            build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                            output_str += build_str
                            output_str += self.commentDecode(val, 0, len(build_str))
                            skip_byte = 0
                        else:
                            error = (f'Error: cannot identify token command: chan {num}, offset {hex(frame_idx)}, val {hex(val)}.')
                            # if self.args.gui:
                            #     raise(error)
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
        with open(f"{self.args.destfolder}/{self.args.sfxname}.wfTable.inc", 'w') as f:
            f.write(f'\n;'+("#"*75)+'\n')
            f.write(f'\n.waveform.table\n')
            f.write(f'\n  .dw ${hex(len(waveform_labels)*2)[2:]}       ; offset to bank table\n\n')
            for idx, wf_label in enumerate(waveform_labels):
                f.write(f"  .dw {wf_label}\n")
            f.write(f'\n\n; Banks\n\n')
            for idx, wf_label in enumerate(waveform_labels):
                f.write(f"  .db bank({wf_label})\n")

        # Write data table file.
        with open(f"{self.args.destfolder}/{self.args.sfxname}.dataTable.inc", 'w') as f:
            f.write(f'\n;'+("#"*75)+'\n')
            f.write(f'\n.data.table\n')
            f.write(f'\n  .dw ${hex(len(data_labels)*2)[2:]}       ; offset to bank table\n\n')
            for idx, wf_label in enumerate(data_labels):
                f.write(f"  .dw {wf_label}\n")
            f.write(f'\n\n; Banks\n\n')
            for idx, wf_label in enumerate(data_labels):
                f.write(f"  .db bank({wf_label})\n")


        # Separate waveform inc
        with open(f"{self.args.destfolder}/{self.args.sfxname}.sfx_wf.inc","w") as f:
            f.write(f' .include "{self.includPathName+".wfTable.inc"}"\n')
            f.write(f' .include "{self.includPathName+".wf.inc"}"\n')

        # Separate data inc
        with open(f"{self.args.destfolder}/{self.args.sfxname}.sfx_data.inc","w") as f:
            f.write(f' .include "{self.includPathName+".dataTable.inc"}"\n')
            for num in range(6):
                if num not in self.args.chanproc:
                    continue
                f.write(f' .include "{self.includPathName}.chan{num}.inc"\n')

        with open(f"{self.args.destfolder}/{self.args.sfxname}.sfx_main.inc","w") as f:
            f.write(f' .include "{self.includPathName+".sfx_wf.inc"}"\n')
            f.write(f' .include "{self.includPathName+".sfx_data.inc"}"\n')




        self.debugPrint(f'Done')
        return True

    def firstPassPrep(self, bin_channels, noEncode=False):
        totalSongdataBinsize = 0
        RLE_frame = 0
        curr_frame = []
        prev_frame = []
        new_bin_chan_data = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        reg_state_chan_data = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        reg_chan_data = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }

        json_string = json.dumps(bin_channels, indent=4)
        with open(self.args.sfxname+'_bin_chan.txt', 'w') as f:
            f.write(json_string)

        # Group data into frames
        raw_total_size = 0
        for num, chan_block in bin_channels.items():
            if num not in self.args.chanproc:
                continue
            print(f'   --- (FP-pre) chan {num} RAW size: {len(chan_block)}')
            raw_total_size += len(chan_block)
        print(f'   --- (FP-pre) TOTAL RAW size: {raw_total_size}')

        # Convert to Reg updates and group as frames
        for num, chan_block in bin_channels.items():
            print(f' (FP-1) chan {num}')
            if num not in self.args.chanproc:
                print(f' - Skipping channel {num}')
                continue

            skip_byte = 0
            for idx, val in enumerate(chan_block):

                if skip_byte > 0 :
                    skip_byte -= 1
                    continue

                if val == 0xffff:
                    reg_chan_data[num].append(curr_frame[:])
                    curr_frame = []
                else:

                    if val >= 0x00 and val <= 0x1f:
                        curr_frame.append( { hex(0x804)[2:] : hex(val) } )
                        skip_byte = 0
                    elif val >= 0x20 and val <= 0x3f:
                        curr_frame.append( { hex(0x804)[2:] : hex(val) } )
                        skip_byte = 0
                    elif val >= 0x40 and val <= 0x5f:
                        curr_frame.append( { hex(0x804)[2:] : hex(val) } )
                        skip_byte = 0
                    elif val >= 0x80 and val <= 0x9f:
                        curr_frame.append( { hex(0x804)[2:] : hex(val) } )
                        skip_byte = 0
                    elif val >= 0xA0 and val <= 0xA9:
                        curr_frame.append( { hex(0x800 | (val & 0x0f))[2:] : hex(chan_block[idx+1]) } )
                        skip_byte = 1
                    elif val == 0xAA:
                        curr_frame.append( { hex(0x80A)[2:] : hex(chan_block[idx+1]) } )
                        skip_byte = 1
                    elif val == 0xAB:
                        curr_frame.append( { hex(0x80B)[2:] : hex(chan_block[idx+1]) } )
                        skip_byte = 1
                    elif val >= 0xC0 and val <= 0xCf:
                        curr_frame.append( { hex(0x802)[2:] : hex(val & 0x0f) } )
                        curr_frame.append( { hex(0x803)[2:] : hex(chan_block[idx+1]) } )
                        skip_byte = 1
                    elif val == 0xB0:
                        curr_frame.append( { hex(0x80C)[2:] : hex(chan_block[idx+1]) } )
                        skip_byte = 1
                    elif val == 0xFC:
                        print(f' ***** WARNING 0xFC ****** offset {idx}')
                        curr_frame.append( { hex(0x80D)[2:] : hex(chan_block[idx+1] + chan_block[idx+2]<<8) } )
                        skip_byte = 2
                    elif val == 0xFD:
                        curr_frame.append( { hex(0x80E)[2:] : hex(-1) } )
                        skip_byte = 0
                    else:
                        error = (f'Error: cannot identify token command: chan {num}, offset {hex(idx)}, val {hex(val)}.')
                        print(error)
                        return False

        # get reg "final state" in frame
        final_reg_block = { ('frame_num' if i==-1 else 'r'+hex(0x800 + i)[2:]) : ('-0x2') for i in range (-1,16,1) }
        last_reg_frame = final_reg_block
        frame_counter = 0
        for num, chan_block in reg_chan_data.items():
            print(f' (FP-2) chan {num}')
            if num not in self.args.chanproc:
                print(f' - Skipping channel {num}')
                continue

            for frame_idx, reg_block in enumerate(chan_block):

                for entry_num, container in enumerate(reg_block):
                    for reg_key, reg_val in container.items():
                        final_reg_block['r'+reg_key] = reg_val
                curr_reg_frame = { reg : val for reg, val in final_reg_block.items() }
                curr_reg_frame['frame_num'] = frame_counter
                chan_block[frame_idx].append( { 'final_reg' : curr_reg_frame } )
                chan_block[frame_idx].append( { 'diff_frame' : self.frame_reg_diff(curr_reg_frame, last_reg_frame) })
                last_reg_frame = curr_reg_frame
                frame_counter += 1

        json_string = json.dumps(reg_chan_data, indent=4)
        with open(self.args.sfxname+'_json.txt', 'w') as f:
            f.write(json_string)

        json_string = json.dumps(self.onlyRegFrame(reg_chan_data), indent=4)
        with open(self.args.sfxname+'_reg_frame___1.txt', 'w') as f:
            f.write(json_string)

        final_reg_block = { ('frame_num' if i==-1 else 'r'+hex(0x800 + i)[2:]) : ('-0x2') for i in range (-1,16,1) }
        frame_counter = 0
        for num, chan_block in reg_chan_data.items():
            print(f' (FP-3) chan {num}')
            if num not in self.args.chanproc:
                print(f' - Skipping channel {num}')
                continue

            for frame_idx, frame_block in enumerate(chan_block):

                reg_writes = []
                diff_frame = {}
                state_frame = {}
                for entry_num, reg_block in enumerate(frame_block):

                    for reg_key, reg_val in reg_block.items():
                        if reg_key == 'diff_frame':
                            diff_frame = reg_val
                        elif reg_key == 'final_reg':
                            state_frame = reg_val
                        else:
                            reg_writes.append( [reg_key,reg_val] )
                diff_frame_keys = list({ key[1:]: val for key,val in diff_frame.items() if val != '' }.keys())
                new_frame = []
                for key, val in reg_writes:
                    if key == '80a':
                        new_frame = [{key : val} for key, val in reg_writes]
                        break
                    if key in diff_frame_keys:
                        new_frame.append({key : val})
                for item in new_frame:
                    for rkey, rval in item.items():
                        final_reg_block['r'+rkey] = rval
                curr_reg_frame = { reg : val for reg, val in final_reg_block.items() }
                curr_reg_frame['frame_num'] = frame_counter
                new_frame.append( { 'final_reg' : curr_reg_frame } )
                # new_frame.append( { 'diff_frame' : diff_frame })
                reg_chan_data[num][frame_idx] = new_frame[:]
                frame_counter += 1

        json_string = json.dumps(reg_chan_data, indent=4)
        with open(self.args.sfxname+'_json___2.txt', 'w') as f:
            f.write(json_string)

        json_string = json.dumps(self.onlyRegFrame(reg_chan_data), indent=4)
        with open(self.args.sfxname+'_reg_frame___2.txt', 'w') as f:
            f.write(json_string)


        # Re-encode

        prev_state_frame = { ('frame_num' if i==-1 else 'r'+hex(0x800 + i)[2:]) : ('-0x2') for i in range (-1,16,1) }
        chan_size = 0
        total_size = 0
        frame_counter = 0
        encoded_chan_data = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        return_for_RLE = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        for num, chan_block in reg_chan_data.items():
            print(f' (FP-3) chan {num}')
            if num not in self.args.chanproc:
                print(f' - Skipping channel {num}')
                continue
            chan_size = 0
            for frame_idx, frame_block in enumerate(chan_block):

                reg_writes = []
                state_frame = {}
                new_frame = []
                for entry_num, reg_block in enumerate(frame_block):

                    # all entries in the frame block
                    for reg_key, reg_val in reg_block.items():
                        if reg_key == 'final_reg':
                            state_frame = reg_val
                        else:
                            reg_writes.append( [reg_key,reg_val] )
                if state_frame == {}:
                    print(f' $$$$$$$$$ Error: no frame reg found!')
                    sys.exit(1)

                reg_writes = self.encodeLevel2(reg_writes, state_frame, prev_state_frame, noEncode)
                encoded_chan_data[num] = encoded_chan_data[num] + reg_writes[:]
                return_for_RLE[num].append(reg_writes[:])
                chan_size += len(reg_writes)
                new_frame.append( [hex(val)[3:] if val <0 else hex(val)[2:] for val in reg_writes] )
                curr_frame = self.decodeFrame(reg_writes, prev_state_frame)
                curr_frame['frame_num'] = frame_counter
                new_frame.append( { 'final_reg' : curr_frame } )
                reg_chan_data[num][frame_idx] = new_frame[:]
                prev_state_frame = state_frame
                frame_counter += 1
            total_size += chan_size
            print(f' ############# (FP-3) chan {num} size: {chan_size}')
        print(f' ############## ----(FP-3) total size: {total_size}')

        json_string = json.dumps(reg_chan_data, indent=4)
        with open(self.args.sfxname+'_json___3.txt', 'w') as f:
            f.write(json_string)

        json_string = json.dumps(self.onlyRegFrame(reg_chan_data), indent=4)
        with open(self.args.sfxname+'_reg_frame___3.txt', 'w') as f:
            f.write(json_string)

        json_string = json.dumps(encoded_chan_data, indent=4)
        with open(self.args.sfxname+'_____encode_bin.txt', 'w') as f:
            f.write(json_string)

        # flatten chan data for return
        return return_for_RLE #encoded_chan_data

    def decodeFrame(self, encodedFrame, prev_state_frame):

        diff_frame  = { ('frame_num' if i==-1 else 'r'+hex(0x800 + i)[2:]) : ('-0x2') for i in range (-1,16,1) }
        state_frame = { reg : (val if reg=='frame_num' else int(val,16)) for reg,val in prev_state_frame.items() }     #deep copy

        skipbyte = 0
        for idx,val in enumerate(encodedFrame):
            if skipbyte > 0:
                skipbyte -= 1
                continue

            if val >= 0x00 and val <=0x5f:
                state_frame['r804'] = val
                skipbyte = 0
            elif val >= 0x60 and val <=0x7f:
                state_frame['r804'] = val | 0xC0
                skipbyte = 0
            elif val >= 0x80 and val <=0x9f:
                state_frame['r804'] = val
                skipbyte = 0
            elif val >= 0xA0 and val <=0xA9:
                state_frame['r80'+hex(val&0x0f)[2:]] = encodedFrame[idx+1]
                skipbyte = 1
            elif val == 0xAA:
                state_frame['r80a'] = encodedFrame[idx+1]
                skipbyte = 1
            elif val == 0xAB:
                state_frame['r80b'] = encodedFrame[idx+1]
                skipbyte = 1
            elif val == 0xB0:
                state_frame['r80c'] = encodedFrame[idx+1]
                skipbyte = 1
            elif val >= 0xB1 and val <=0xBf:
                state_frame['r804'] = state_frame['r804'] + self.signed4bit(val & 0x0f)
                skipbyte = 0
            elif val >= 0xC0 and val <=0xCf:
                state_frame['r802'] = val & 0x0f
                state_frame['r803'] = encodedFrame[idx+1]
                skipbyte = 1
            elif val >= 0xD0 and val <=0xDf:
                state_frame['r804'] = state_frame['r804'] + self.signed4bit(val & 0x0f)
                period = (state_frame['r802']<<8) + state_frame['r803']
                period += self.signed8bit(encodedFrame[idx+1])
                state_frame['r802'] = (period >> 8) & 0x0f
                state_frame['r803'] = (period) & 0xff
                skipbyte = 1
            elif val == 0xF0:
                pass
                skipbyte = 1
            elif val >= 0xF1 and val <=0xF8:
                pass
                skipbyte = 0
            elif val == 0xFb:
                pass
                skipbyte = 0
            elif val == 0xFc:
                state_frame['r80c'] = (encodedFrame[idx+1]<<8) + encodedFrame[idx+2]
                skipbyte = 2
            elif val == 0xFd:
                state_frame['r80e'] = -1
                skipbyte = 0
            elif val == 0xFe:
                pass
                skipbyte = 1
            elif val == 0xFf:
                pass
                skipbyte = 0

        return { reg : (val if reg=='frame_num' else hex(val)) for reg,val in state_frame.items() }

    def signed4bit(self, val):
        if val <=7:
            return val
        return (((val ^ 0xff) + 1) & 0x0f) * -1

    def signed8bit(self, val):
        if val <=127:
            return val
        return ((val ^ 0xff) + 1) * -1

    def onlyRegFrame(self, bin_channel):
        reg_chan_data = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        for num, chan_block in bin_channel.items():
            if num not in self.args.chanproc:
                continue
            for frame_idx, frame_block in enumerate(chan_block):
                state_frame = {}
                for entry_num, reg_block in enumerate(frame_block):
                    try:
                        for reg_key, reg_val in reg_block.items():
                            if reg_key == 'final_reg':
                                state_frame = reg_val
                                break
                    except:
                        pass
                reg_chan_data[num].append({reg: val for reg,val in state_frame.items()})

        return reg_chan_data

    def encodeLevel2(self, reg_writes, state_frame, prev_state_frame, noEncode=False):

        found_regs = { '801':[], '802':[], '803':[], '804':[], '805':[], '807':[], '808':[], '809':[], '80a':[], '80b':[], '80c':[], '80d':[],'80e':[] }

        output = []
        embedded_exit = False

        for reg, val in reg_writes:
            found_regs[reg].append(int(val,16))
        prev_state_frame = { reg : (val if reg=='frame_num' else int(val,16)) for reg,val in prev_state_frame.items() }

        # check for start of new pattern
        if found_regs['80a'] != []:
            # Do not encode as relative ops

            output = output + [0xaa, found_regs['80a'][-1]]
            output = output + [0xab, found_regs['80b'][-1]]

            if found_regs['80d']:
                upper = 0xFC
                fist   = found_regs['80d'][-1]>>8 & 0xff
                second = found_regs['80d'][-1] & 0xff
                output = output + [upper, fist, second]

            if found_regs['80e']:
                upper = 0xFD
                output = output + [upper]

            if found_regs['80c']:
                upper = 0xB0
                lower = found_regs['80c'][-1]
                output = output + [upper, lower]

            if found_regs['805']:
                upper = 0xA5
                lower = found_regs['805'][-1]
                output = output + [upper, lower]

            if found_regs['801']:
                upper = 0xA1
                lower = found_regs['801'][-1]
                output = output + [upper, lower]

            if found_regs['807']:
                upper = 0xA7
                lower = found_regs['807'][-1]
                output = output + [upper, lower]

            if found_regs['808']:
                upper = 0xA8
                lower = found_regs['808'][-1]
                output = output + [upper, lower]

            if found_regs['809']:
                upper = 0xA9
                lower = found_regs['809'][-1]
                output = output + [upper, lower]

            if found_regs['802'] or found_regs['803']:
                upper = ( found_regs['802'][-1] & 0x0f ) | 0xC0
                lower = found_regs['803'][-1]
                output = output + [upper, lower]

            if found_regs['804']:
                vol = found_regs['804'][-1]
                if vol>= 0xC0 and vol <= 0xDF:
                    vol = (vol - 0xC0) + 0x60
                output = output + [vol]
        elif noEncode:
            if found_regs['80d']:
                upper = 0xFC
                fist   = found_regs['80d'][-1]>>8 & 0xff
                second = found_regs['80d'][-1] & 0xff
                output = output + [upper, fist, second]

            if found_regs['80e']:
                upper = 0xFD
                output = output + [upper]

            if found_regs['80c']:
                upper = 0xB0
                lower = found_regs['80c'][-1]
                output = output + [upper, lower]

            if found_regs['805']:
                upper = 0xA5
                lower = found_regs['805'][-1]
                output = output + [upper, lower]

            if found_regs['801']:
                upper = 0xA1
                lower = found_regs['801'][-1]
                output = output + [upper, lower]

            if found_regs['807']:
                upper = 0xA7
                lower = found_regs['807'][-1]
                output = output + [upper, lower]

            if found_regs['808']:
                upper = 0xA8
                lower = found_regs['808'][-1]
                output = output + [upper, lower]

            if found_regs['809']:
                upper = 0xA9
                lower = found_regs['809'][-1]
                output = output + [upper, lower]

            if found_regs['802'] or found_regs['803']:
                # upper = ( found_regs['802'][-1] & 0x0f ) | 0xC0
                # lower = found_regs['803'][-1]
                if found_regs['802'] == []:
                    upper = prev_state_frame['r802']
                else:
                    upper = found_regs['802'][-1]

                if found_regs['803'] == []:
                    lower = prev_state_frame['r803']
                else:
                    lower = found_regs['803'][-1]

                upper = ( upper & 0x0f ) | 0xC0
                # lower = found_regs['803'][-1]

                output = output + [upper, lower]

            if found_regs['804']:
                vol = found_regs['804'][-1]
                if vol>= 0xC0 and vol <= 0xDF:
                    vol = (vol - 0xC0) + 0x60
                output = output + [vol]
        else:
            # Encode to relative ops

            skip_vol = False

            if found_regs['801']:
                upper = 0xA1
                lower = found_regs['801'][-1]
                output = output + [upper, lower]

            #..........................................................
            if found_regs['80d']:
                upper = 0xFC
                fist   = found_regs['80d'][-1]>>8 & 0xff
                second = found_regs['80d'][-1] & 0xff
                output = output + [upper, fist, second]

            #..........................................................
            if found_regs['80e']:
                upper = 0xFD
                output = output + [upper]

            #..........................................................
            if found_regs['80c']:
                upper = 0xB0
                lower = found_regs['80c'][-1]
                output = output + [upper, lower]

            #..........................................................
            if found_regs['805']:
                upper = 0xA5
                lower = found_regs['805'][-1]
                output = output + [upper, lower]

            #..........................................................
            if found_regs['807']:
                upper = 0xA7
                lower = found_regs['807'][-1]
                output = output + [upper, lower]

            #..........................................................
            if found_regs['808']:
                upper = 0xA8
                lower = found_regs['808'][-1]
                output = output + [upper, lower]

            #..........................................................
            if found_regs['809']:
                upper = 0xA9
                lower = found_regs['809'][-1]
                output = output + [upper, lower]

            #..........................................................
            if found_regs['802'] or found_regs['803']:

                delta = 0xffff
                if found_regs['802'] == []:
                    upper = prev_state_frame['r802']
                else:
                    upper = found_regs['802'][-1]

                if found_regs['803'] == []:
                    lower = prev_state_frame['r803']
                else:
                    lower = found_regs['803'][-1]

                prev_upper = prev_state_frame['r802']
                prev_lower = prev_state_frame['r803']

                if lower < 0:
                    print(f" ===== Error: 803 is invalid: {lower}")
                    sys.exit(1)
                if upper < 0:
                    print(f" ===== Error: 802 is invalid: {upper}")
                    sys.exit(1)

                if prev_lower < 0 and prev_upper < 0:
                    # can't do relative encoding
                    upper = ( upper & 0x0f ) | 0xC0
                    lower = found_regs['803'][-1]
                    output = output + [upper, lower]
                    delta = 0xffff
                else:
                    prev_period = (prev_upper<<8) + prev_lower
                    period = (upper<<8) + lower
                    delta = period - prev_period

                if delta != 0xffff:
                    if delta >= -128 and delta <= 127:

                        delta_period = delta
                        delta_vol = None

                        if found_regs['804']:
                            vol = found_regs['804'][-1]
                            if prev_state_frame['r804'] < 0:
                                if vol>= 0xC0 and vol <= 0xDF:
                                    vol = (vol - 0xC0) + 60
                                output = output + [vol]
                                skip_vol = True
                            else:
                                vol_detla = vol - prev_state_frame['r804']
                                if vol_detla >= -8 and vol_detla <= 7:
                                    delta_vol = vol_detla

                        if delta_vol != None:
                            upper = 0xD0 + (delta_vol & 0x0F)
                            lower = delta_period
                            output = output + [upper, lower]
                            skip_vol = True
                            embedded_exit = True
                        else:
                            # Do the volume update first, because the delta freq update is an embedded exit op
                            if found_regs['804']:
                                vol = found_regs['804'][-1]
                                if vol>= 0xC0 and vol <= 0xDF:
                                    vol = (vol - 0xC0) + 60
                                output = output + [vol]
                                skip_vol = True
                            upper = 0xD0
                            lower = delta_period
                            output = output + [upper, lower]
                            embedded_exit = True
                    else:
                        # can't do relative encoding
                        upper = ( upper & 0x0f ) | 0xC0
                        output = output + [upper, lower]
                        skip_vol = False

            #..........................................................
            if found_regs['804'] and skip_vol == False:
                vol = found_regs['804'][-1]
                if prev_state_frame['r804'] < 0:
                    # No delta available
                    if vol>= 0xC0 and vol <= 0xDF:
                        vol = (vol - 0xC0) + 60
                    output = output + [vol]
                else:
                    vol_detla = vol - prev_state_frame['r804']
                    if vol_detla == 0:
                        pass
                    if vol_detla >= -8 and vol_detla <= 7:
                        vol = 0xB0 | (vol_detla & 0x0F)
                        embedded_exit = True
                    elif vol>= 0xC0 and vol <= 0xDF:
                        vol = (vol - 0xC0) + 60
                    output = output + [vol]

        output = output + ([0xFF],[])[embedded_exit == True]

        return output

    def frame_reg_diff(self, curr_frame, last_frame):
        diff_frame = { 'r'+hex(0x800 + i)[2:] : '' for i in range (16) }
        for reg_key, val in curr_frame.items():
            if val != last_frame[reg_key]:
                diff_frame[reg_key] = val

        return diff_frame

    def compressFrameEOF(self, bin_channels):
        RLE_frame = 0
        curr_frame = []
        prev_frame = []
        new_bin_chan_data = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        final_bin_chan_data = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        chan_size = 0
        raw_chan_size = 0
        raw_total_size = 0
        total_size = 0
        for num, chan_block in bin_channels.items():
            if num not in self.args.chanproc:
                continue

            RLE_frame = 0

            chan_size = 0
            raw_chan_size = 0
            for frame in chan_block:

                curr_frame = frame[:]
                raw_chan_size += len(curr_frame)
                if len(curr_frame) == 1 and curr_frame[0] == 0xff:
                    RLE_frame += 1
                    if RLE_frame == 5:
                        new_bin_chan_data[num].append([0xAC+(RLE_frame-2)])
                        RLE_frame = 0
                else:

                    if RLE_frame > 0:
                        if RLE_frame == 1:
                            new_bin_chan_data[num].append([0xFF])
                            chan_size += 1
                        # write original pending, then RLE frame
                        elif RLE_frame < 6:
                            new_bin_chan_data[num].append([0xAC+(RLE_frame-2)])
                            chan_size += 1
                        else:
                            print(f' ERROR!!! Internal EOF RLE pass limit!')
                            sys.exit(1)

                    new_bin_chan_data[num].append(curr_frame[:])
                    chan_size += len(curr_frame[:])
                    RLE_frame = 0
            total_size += chan_size
            raw_total_size += raw_chan_size

            print(f'  --- Chan block raw size: {raw_chan_size}')
            print(f' Post RLE_EOF Chan {num} size: {chan_size}')

        # print(f'  PRE Total size: {raw_total_size}')
        # print(f' POST RLE_EOF Total size: {total_size}')

        # for num, chan_block in new_bin_chan_data.items():
        #     if num not in self.args.chanproc:
        #         continue
        #     for frame_idx, frame in enumerate(chan_block):
        #         curr_frame = frame[:]
        #         if len(curr_frame) == 1 and curr_frame[0] == 0xff:
        #             if frame_idx > 0 and chan_block[frame_idx][-1] == 0xff:
        #                 # print(chan_block[frame_idx-1])
        #                 new_bin_chan_data[num][frame_idx-1][-1] = 0xAC+2
        #                 new_bin_chan_data[num][frame_idx] = []

        # chan_size = 0
        # total_size = 0
        # for num, chan_block in new_bin_chan_data.items():
        #     if num not in self.args.chanproc:
        #         continue
        #     chan_size = 0
        #     for frame_idx, frame in enumerate(chan_block):
        #         curr_frame = frame[:]
        #         if curr_frame != []:
        #             final_bin_chan_data[num].append(curr_frame)
        #             chan_size += len(frame)
        #     total_size += chan_size

        #     print(f' Final RLE_EOF Chan {num} size: {chan_size}')
        # print(f' Final RLE_EOF Total size: {total_size}')


        return new_bin_chan_data

    def compressFrameRLE(self, bin_channels):

        RLE_frame = 0
        curr_frame = []
        prev_frame = []
        new_bin_chan_data = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        chan_size = 0
        raw_chan_size = 0
        raw_total_size = 0
        total_size = 0
        # print(json.dumps(bin_channels, indent=4))
        for num, chan_block in bin_channels.items():
            print(f'chan mask: {self.args.chanproc }, {num}')
            if num not in self.args.chanproc:
                print(f' - Skipping channel {num}')
                continue

            curr_frame = []
            prev_frame = []
            RLE_frame = 0

            chan_size = 0
            raw_chan_size = 0
            for frame in chan_block:

                curr_frame = frame[:]
                raw_chan_size += len(curr_frame)
                if self.compareFrames(curr_frame, prev_frame):
                    RLE_frame += 1
                    prev_frame = curr_frame[:]
                    curr_frame = []
                else:

                    if RLE_frame > 0:
                        # write original pending, then RLE frame
                        if RLE_frame > 8:
                            new_bin_chan_data[num].append([0xF0, RLE_frame])
                            chan_size += 2
                        else:
                            new_bin_chan_data[num].append([0xF0 + RLE_frame])
                            chan_size += 1
                        prev_frame = []
                    else:
                        prev_frame = curr_frame[:]

                    new_bin_chan_data[num].append(curr_frame[:])
                    chan_size += len(curr_frame[:])
                    RLE_frame = 0
                    curr_frame = []
            total_size += chan_size
            raw_total_size += raw_chan_size

            print(f'  --- Chan block raw size: {raw_chan_size}')
            print(f' Post RLE Chan {num} size: {chan_size}')

        print(f'  RAW Total size: {raw_total_size}')
        print(f' POST RLE Total size: {total_size}')

        return new_bin_chan_data

    def compareFrames(self, alist, blist):
        if len(alist) != len(blist):
            return False
        for a,b in zip(alist,blist):
            if a != b:
                return False
        return True

    def consolidatePatternBlocks(self, bin_channels, chan_playList, pattern_list_by_index):
        new_bin_chan_data = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        new_chan_playlist = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        block_chan_playlist = { 0 : {}, 1: {}, 2 : {}, 3 : {}, 4 : {}, 5 : {} }
        new_block_chan_playlist = { 0 : {}, 1: {}, 2 : {}, 3 : {}, 4 : {}, 5 : {} }
        clean_block_chan_playlist = { 0 : {}, 1: {}, 2 : {}, 3 : {}, 4 : {}, 5 : {} }

        chan_playList[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 17, 17, 17, 17, 17, 17, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 9, 10, 11, 12, 17,13, 14, 15, 16]

        for num, playList in chan_playList.items():
            playList = [[0xffff,idx,val] for idx,val in enumerate(playList)]
            marker = 0
            for idx,ptrn in enumerate(playList):
                new_found_match = False
                for prev_idx, prev_ptrn in enumerate(playList[:idx]):
                    if prev_ptrn[0] < 0:
                        continue        # don't reference a reference
                    if ptrn[2] == prev_ptrn[2]:
                        ptrn[0] = -1 * prev_idx
                        ptrn[1] = prev_idx
                        if prev_ptrn[0] == 0xffff:
                            prev_ptrn[0] = marker
                            new_found_match = True
                if not new_found_match:
                    marker += 1
            new_chan_playlist[num] = playList

        # for num, playList in new_chan_playlist.items():
            # print(f'COS - chan {num}: {playList}\n\n')

        print("\n\n\n\n")

        marker += 1000
        for num, playList in new_chan_playlist.items():
            for idx,ptrn in enumerate(playList):
                if ptrn[0] == 0xFFFF:
                    ptrn[0] = marker
                else:
                    marker += 1

        for num, playList in new_chan_playlist.items():
            marker_repeat = -1
            for idx,ptrn in enumerate(playList):
                if ptrn[0] < 0:
                    ptrn[0] = marker_repeat
                else:
                    marker_repeat -= 1

        for num, playList in new_chan_playlist.items():
            for idx, ptrn in enumerate(playList):
                if ptrn[0] < 0:
                    try:
                        block_chan_playlist[num][ptrn[0]].append(ptrn[2])
                    except:
                        block_chan_playlist[num][ptrn[0]] = [ptrn[2]]
                else:
                    try:
                        block_chan_playlist[num][ptrn[0]].append(ptrn[2])
                    except:
                        block_chan_playlist[num][ptrn[0]] = [ptrn[2]]


        # for num, playList in new_chan_playlist.items():
        #     # playList = [[0xffff,idx,val] for idx,val in enumerate(playList)]
        #     print(f'COS - chan {num}: {playList}\n\n')

        for num, playList in new_chan_playlist.items():
            # playList = [[0xffff,idx,val] for idx,val in enumerate(playList)]
            print(f'COS - chan {num}: {block_chan_playlist[num]}\n\n')

        for num, chanblock in block_chan_playlist.items():

            for key, plist in chanblock.items():
                if key > -1:
                    new_block_chan_playlist[num][key] = plist[:]
                else:
                    # watch through the list of references
                    found_match = False
                    for s_key, s_plist in new_block_chan_playlist[num].items():
                        if s_key > -1:
                            if plist[0] == s_plist[0]:
                                if len(s_plist) > len(plist):
                                    print(f'Error: s:{s_plist}, p:{plist}')
                                    sys.exit(1)
                                elif len(s_plist) == len(plist):
                                    if sum(1 for v1,v2 in zip(s_plist,plist) if v1 == v2) == len(s_plist):
                                        print(f' chan {num}. Found match. s:{s_plist}, p:{plist}')
                                        new_block_chan_playlist[num][key] = [plist[0] * -1]
                                        found_match = True
                                        break
                                else:

                                    print(f' chan {num}. NO match. s:{s_plist}, p:{plist}')
                    if not found_match:
                        new_block_chan_playlist[num][key] = plist[:]

        for num, playList in new_block_chan_playlist.items():
            # playList = [[0xffff,idx,val] for idx,val in enumerate(playList)]
            print(f'pre step COS - chan {num}: {new_block_chan_playlist[num]}\n\n')

        update_marker = -1000
        for num, chanblock in new_block_chan_playlist.items():
            for key, plist in chanblock.items():
                if key > -1 or ( key < 0 and plist[0] < 0 ):
                    # we already processed this.. just store it and move on.
                    clean_block_chan_playlist[num][key] = plist[:]
                else:
                    # watch through the list of references
                    found_match = False
                    print(f'Checking: {plist}')
                    save_plist = plist[:]
                    while plist != []:
                        found_match = False
                        for s_key, s_plist in new_block_chan_playlist[num].items():
                            if s_key > -1:
                                print(f' searching: {s_key}, {s_plist}')
                                min_pair = min(len(s_plist),len(plist))
                                count_match = 0
                                for i in range(min_pair):
                                    if plist[i] == s_plist[i]:
                                        count_match += 1
                                    else:
                                        if count_match == 0:
                                            break
                                        found_match = True
                                        clean_block_chan_playlist[num][key + update_marker] = [plist[0] * -1]
                                        plist = plist[count_match:]
                                        print(f'Match: partial {clean_block_chan_playlist[num][key + update_marker]}, left over{plist}')
                                        update_marker += -1000
                                        break
                                if count_match > 0 and found_match == False:
                                    clean_block_chan_playlist[num][key + update_marker] = [plist[0] * -1]
                                    plist = plist[count_match:]
                                    print(f'Match: partial {clean_block_chan_playlist[num][key + update_marker]}, left over{plist}')
                                    update_marker += -1000
                        if len(save_plist) == len(plist):
                            print(f'Error: ')
                            sys.exit(1)

        # Give the literal blocks an actual reference number
        pre_final = { 0 : {}, 1: {}, 2 : {}, 3 : {}, 4 : {}, 5 : {} }
        for num, chanblock in clean_block_chan_playlist.items():
            update_marker = 0
            for key, plist in chanblock.items():
                if key > -1:
                    # we already processed this.. just store it and move on.
                    pre_final[num][update_marker] = plist[:]
                    update_marker += 1
                else:
                    pre_final[num][key] = plist[:]

        # Update reference blocks to match new literal IDs
        for num, chanblock in pre_final.items():
            update_marker = 0
            for key, plist in chanblock.items():
                if key < 0:
                    for s_key, s_plist in pre_final[num].items():
                        if s_key > -1 and (plist[0]*-1) == s_plist[0]:
                            pre_final[num][key] = [s_key]

        for num, playList in pre_final.items():
            # playList = [[0xffff,idx,val] for idx,val in enumerate(playList)]
            print(f'pre - final COS - chan {num}: {pre_final[num]}\n\n')


        final_list = { 0 : [], 1: [], 2 : [], 3 : [], 4 : [], 5 : [] }
        for num, chanblock in pre_final.items():
            for key, plist in chanblock.items():
                if key < 0:
                    final_list[num].append(plist[0])
                else:
                    final_list[num].append(key)



        for num, playList in final_list.items():
            # playList = [[0xffff,idx,val] for idx,val in enumerate(playList)]
            print(f'final COS - chan {num}: {playList}\n\n')



        sys.exit(1)

        # for num, chan_block in bin_channels.items():
        #     if num not in self.args.chanproc:
        #         continue
        #     pattern_idx = -1
        #     chan_patterns = []
        #     new_data=False
        #     for frame_num, frame_block in enumerate(chan_block):
        #         if frame_block[0] == 0xAA:
        #             pattern_idx +=1
        #             if pattern_idx == 0:
        #                 chan_patterns = chan_patterns + frame_block[:]
        #                 continue
        #             new_data=False
        #             with open(f"{self.args.destfolder}/{self.args.sfxname}.chan{num}.pattern{pattern_idx}.pbin",'wb') as f:
        #                 f.write(bytearray(chan_patterns))
        #             print(f' Chan {num}: pattern {pattern_idx}. size: {len(chan_patterns)}')
        #             chan_patterns = []
        #         else:
        #             chan_patterns = chan_patterns + frame_block[:]
        #             new_data = True
        #     if new_data:
        #         with open(f"{self.args.destfolder}/{self.args.sfxname}.chan{num}.pattern{pattern_idx}.pbin",'wb') as f:
        #             f.write(bytearray(chan_patterns))        

    def compressPatterns(self, bin_channels):

        print("######################################################################################")
        print("Processing compressed pattern sizes:")
        channelPatterData = {}
        pattern_index = { 0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : [] }
        final_playlist = { 0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : [] }
        pattern_compressed = { 0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : [] }
        chan_size = 0
        total_size = 0
        for num, chan_block in bin_channels.items():
            if num not in self.args.chanproc:
                continue

            if chan_block[0][0] != 0xaa:
                print(f'\nVGM does not have Pattern index markers.\n')
                self.debugPrint(f'\nVGM does not have Pattern index markers.\n')
                return

            for frame_idx, frame in enumerate(chan_block):
                    if frame[0] == 0xAA:
                        # print(frame)
                        pattern_index[num].append([frame[1],frame[3],frame_idx])

        for num, pattern_info in pattern_index.items():
            print(f'  Chan {num} pattern list: {[block[1] for block in pattern_info]}. Size: {len(pattern_info)}')
            final_playlist[num] = [block[1] for block in pattern_info]
            pattern_track = []
            chan_size = 0
            for idx, ( play_inc, playorder_idx, pattern_idx) in enumerate(pattern_info):
                if playorder_idx not in pattern_track:
                    pattern_track.append(playorder_idx)

                    try:
                        next_idx = pattern_info[idx+1][2]
                    except:
                        next_idx = len(bin_channels[num])
                    # print(f' p_index: {pattern_idx}. next: {next_idx}')
                    for frame_idx in range(pattern_idx,next_idx,1):
                        chan_size += len(bin_channels[num][frame_idx])
                        pattern_compressed[num].append( bin_channels[num][frame_idx][:] )
            total_size += chan_size
            print(f" New RLE chan {num} size: {chan_size}")
        print(f" New RLE total size: {total_size}")

        return pattern_compressed, final_playlist, pattern_index

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
        if val == 0xff or val == 0xffff:
            output_str += f" ; Wait vblank"
        elif val >= 0x00 and val <= 0x1f:
            output_str += f" ; 804 -> ${hex(val)[2:]}"
        elif val >= 0x20 and val <= 0x3f:
            output_str += f" ; 804 -> ${hex(val-0x20+0xC0)[2:]}"
        elif val >= 0x40 and val <= 0x5f:
            output_str += f" ; 804 -> ${hex(val)[2:]}"
        elif val >= 0x60 and val <= 0x7f:
            output_str += f" ; 804 -> ${hex(val|0xC0)[2:]}"
        elif val >= 0x80 and val <= 0x9f:
            output_str += f" ; 804 -> ${hex(val)[2:]}"
        elif val >= 0xA0 and val <= 0xA9:
            output_str += f" ; 80{hex(val)[2:][-1]} -> ${hex(opr)[2:]}"
        elif val == 0xAA:
            output_str += f" ; Pattern Index # {opr}"
        elif val == 0xAB:
            output_str += f" ; Pattern # {opr}"
        elif val >= 0xAC and val <= 0xAF:
            output_str += f" ; Wait vblank {(val-0xAC)+2} frames."
        elif val >= 0xC0 and val <= 0xCF:
            output_str += f" ; 802 -> ${hex(val)[2:][-1]}, 803 -> ${hex(opr)[2:]}"
        elif val >= 0xD0 and val <= 0xDF:
            output_str += f" ; 802:803 delta -> signed ${hex(opr)[2:][-1]}, 804 detla -> signed ${hex(val&0x0f)[2:]}"
        elif val == 0xB0:
            output_str += f" ; Waveform update #${hex(opr)[2:]}"
        elif val >= 0xB1 and val <= 0xBF:
            output_str += f" ; 804 detla -> signed ${hex(val&0x0f)[2:]} ({self.signed4bit(val & 0x0f)})"
        elif val == 0xF0:
            output_str += f" ; Repeat last 'frame' for {opr} number of frames."
        elif val >= 0xF1 and val <= 0xF8:
            output_str += f" ; Repeat last 'frame' for {val & 0x0f} number of frames."
        elif val == 0xFB:
            output_str += f" ; End of channel stream"
        elif val == 0xFC:
            output_str += f" ; Play fixed sample # {(opr>>8)&0xff} @ flag {hex((opr>>24)&0xff)}"
        elif val == 0xFD:
            output_str += f" ; Stop sample"
        elif val == 0xFE:
            output_str += f" ; Wait vblank {opr} frames."
        else:
            error = (f'Error: cannot identify token command {val} for comment.')
            if self.args.guiMode:
                raise(error)
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

        # First thing is to consolidate 806 waveform buffer writes
        for chan,data_set in self.reg_list.items():

            if chan == 'num_frames':
                self.prep_reg_list['num_frames'] = data_set
                continue

            _806_run = []

            for frame, data_frame in enumerate(data_set):
                if data_frame == []:
                    if frame not in list(self.prep_reg_list[chan].keys()):
                        self.prep_reg_list[chan][frame] = []
                    continue

                for data_pair in data_frame:

                    reg_data = data_pair

                    try:
                        reg = reg_data[0]
                        data = reg_data[1]
                    except:
                        error = f'failed pair: {reg_data}'
                        print(error)
                        if self.Guimode:
                            raise Exception(error)
                        sys.exit(1)
                    self.debugPrint(f'reg    [{reg}], channel [{chan}]')
                    if reg == 0x06:
                        _806_run.append(data)
                    elif reg != 0x06 and _806_run != []:
                        if frame not in list(self.prep_reg_list[chan].keys()):
                            self.prep_reg_list[chan][frame] = []
                        self.prep_reg_list[chan][frame].append({'reg':0x06, 'data': _806_run})
                        self.prep_reg_list[chan][frame].append({'reg':reg, 'data': [data]})
                        _806_run = []
                    else:
                        if frame not in list(self.prep_reg_list[chan].keys()):
                            self.prep_reg_list[chan][frame] = []
                        self.prep_reg_list[chan][frame].append({'reg':reg, 'data': [data]})


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




        # combine period updates
        for chan,data_set in self.prep_reg_list.items():
            if chan == 'num_frames':
                continue

            for frame, data_frame in data_set.items():
                if data_frame == []:
                    continue

                found_02 = False
                period_02 = 0
                for idx,data_pair in enumerate(data_frame):
                    reg = data_pair['reg']
                    data = data_pair['data']
                    if reg == 0x02:
                        found_02 = True
                        period_02 = data[0]
                        prev_idx = idx
                        continue
                    if reg == 0x03 and found_02:
                        self.prep_reg_list[chan][frame][idx] = { 'reg' : 0x02, 'data' : [period_02, data[0]] }
                        self.prep_reg_list[chan][frame].pop(prev_idx)

                    found_02 = False

        # remove duplicate reg writes
        for chan,data_set in self.prep_reg_list.items():
            if chan == 'num_frames':
                continue

            for frame, data_frame in data_set.items():
                if data_frame == []:
                    continue

                rle_reg = []
                rle_idx = []
                for idx,data_pair in enumerate(data_frame):
                    reg = data_pair['reg']
                    data = data_pair['data']
                    pair_set = set([(idx+1)<<8|val for idx, val in enumerate(data+[reg])])

                    if rle_reg == []:
                        rle_reg.append(pair_set)
                        rle_idx = [idx]
                        continue

                    if pair_set in rle_reg:
                        rle_idx.append(idx)
                        continue

                    for remove_idx in rle_idx[1:]:
                        self.prep_reg_list[chan][frame].pop(remove_idx)
                        rle_reg.append(pair_set)
                        rle_reg = []
                        rle_idx = []

                    rle_reg = [pair_set]
                    rle_idx = [idx]


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
                        elif reg >=40 and reg <= 0x5f:
                            pass
                        elif reg >=80 and reg <= 0x9f:
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
                    elif reg == 0x02:
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
        op = content[offset]


        if op not in list(self.op_len.keys()):
            error  = f'failed on decodedata: op [{hex(op)}], offset [{hex(offset)}]'
            error += f'Error: opcode [{content[offset]}] at address {offset} is not recognised.'
            print(error)
            if self.Guimode:
                raise Exception(error)
            sys.exit(1)

        operand = content[offset + 1 : offset + 1 + self.op_len[op]]
        offset += len(operand)+1

        return (op, operand, offset)

    def get_int(self, offset, content):
        return content[offset+3]<<24 | content[offset+2]<<16 | content[offset+1]<<8 | content[offset+0]

    def get_word(self, offset, content):
        return content[offset+1]<<8 | content[offset+0]

    def get_string(self, offset, length, content):
        if length+offset > len(content) - 1:
            error = f'Error: internal error - string offset and length exceeds file length.'
            print(error)
            if self.Guimode:
                raise Exception(error)
            sys.exit(1)

        return ''.join([ f'{chr(val)}' for val in content[offset:offset+length]])


#.....................................
# END CLASS


def auto_int(val):
    val = int(val, (DECbase,HEXbase)['0x' in val])
    return val

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


import argparse
import os
import sys
import tkinter as tk

from pathlib import Path
from tkinter import filedialog as fd
from tkinter import messagebox
from functools import partial

HEXbase = 16
DECbase = 10
version = "1.0.0"

class GuiGui():

    def __init__(self, args):
        self.args = args

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
        tk.Button(root, text='Convert', command=self.convert, width=25).grid(row=6, column=0,sticky=tk.W)

        self.l1 = tk.Label(root, text = " VGM: ")
        self.l1.grid(row=2, column=1,sticky=tk.W)
        self.l2 = tk.Label(root, text = " Output: ")
        self.l2.grid(row=3, column=1,sticky=tk.W)
        self.l3 = tk.Label(root, text = "Include path for assembler/source")
        self.l3.grid(row=4, column=1,sticky=tk.W)
        self.l4 = tk.Label(root, text = "SFX file name")
        self.l4.grid(row=5, column=1,sticky=tk.W)

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
        self.args.fileout = os.path.join(os.getcwd(), f'{Path(filename).stem}')
        self.l2.config(text=f' Output: {self.args.fileout}')
        self.sfxFileName.set(Path(filename).stem)


    def setOutput(self):
        filepath = fd.askdirectory()
        if filepath == '' or filepath == None:
            print('Cancel saveAs..')
            return
        print(filepath)
        self.args.fileout = filepath + '/'+ self.sfxFileName.get()
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
            chanMask = 0
            for i in range(6):
                chanMask |= (0,1)[self.chn[i].get()] << (5-i)
            self.args.chanMask = chanMask

            self.args.debugBin = self.outputBin.get()==1
            self.args.debugLog = self.outputLog.get()==1

            print(f' log: {self.outputLog.get()}, {self.args.debugLog }. bin: {self.outputBin.get()},{self.args.debugBin}')

            result = ConvertVGM(self.args).process()
            if result:
                tk.messagebox.showinfo(title='Finished',message='VGM has been converted. Check debug log for any errors or weidness.')
            else:
                tk.messagebox.showerror(title='Error',message=f'Something went wrong. Check to see if debugLog was generated.')
        except Exception as e:
            print(f'{e}')
            tk.messagebox.showerror(title='Error',message=f'{e}')


class ConvertVGM():

    def __init__(self, args, guiMode=False):
        self.args     = args
        self.guiMode  = guiMode
        self.debugLog = []

        if self.args.fileout == '':
            self.args.fileout = self.args.filein

        self.includPathName = os.path.join(self.args.dir,Path(self.args.fileout).name)

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


    def process(self):

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
            with open(self.args.fileout+'.debugLog.txt','w') as f:
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
                self.debugPrint(f'     NO STORE')
                continue

            if op == 0x67:
                data, dataOffset = self.get_PCM(dataOffset, operand, content)
                self.samplePCM.append(data)
                self.debugPrint(f'     NO STORE')
                continue

            if op == 0x90:
                channelCount.append(operand[self.op_chan[op]])
                self.debugPrint(f'     NO STORE')
                continue

            if op in [0x91, 0x92]:
                self.debugPrint(f'     NO STORE')
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
                # This is wrong! Do not reset the channel
                # current_channel = 0
                self.debugPrint(f'###  Frame end!  #####$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                print(f"frame end: {self.reg_list['num_frames'] }")

                if op == 0x66:
                    break
                else:
                    continue


            reg = operand[self.op_reg[op]]
            data = operand[self.op_reg_data[op]]

            chan_data[current_channel].append((reg,data))
            self.debugPrint(f'    chan [{current_channel}], Data: {reg}, {data}')



        self.debugPrint(f"\n\n\n{self.reg_list}\n\n\n")

        waveforms, bin_channels =  self.consilidateWFupdates()

        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #
        # waveforms ASM file

        # Write actual waveform blocks
        if self.args.debugBin:
            with open(self.args.fileout+".pcm.bin", 'wb') as f:
                for sample in self.samplePCM:
                    for val in sample:
                        val += 0x20
                        val &= 0x1f
                        f.write(bytearray([val]))


        # Flatten waveform block
        waveform_block = []
        for idx, waveform in enumerate(waveforms):
            waveform = sorted(list(waveform))
            waveform_block = waveform_block + [val&0xff for val in waveform]

        if self.args.debugBin:
            with open(self.args.fileout+".wf.bin", 'wb') as f:
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
        with open(self.args.fileout+".wf.inc", 'w') as f:
            for idx,waveform in enumerate(waveforms):
                waveform = sorted(list(waveform))
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

        data_labels = []
        for num, chan_block in bin_channels.items():
            print(f'chan mask: {self.args.chanMask }, {((self.args.chanMask >> (5-num)) & 0x01)}')
            if ((self.args.chanMask >> (5-num)) & 0x01) == 0:
                continue

            if self.args.debugBin:
                with open(self.args.fileout+f".chan{num}.bin",'wb') as f:
                    self.debugPrint(f' saving {num}: {chan_block}')
                    prep_block = [val&0xff for val in chan_block]
                    f.write(bytearray(prep_block))
                    f.write(bytearray([0xFB]))

            wait_frame = 0
            with open(self.args.fileout+f'.chan{num}.inc','w') as f:
                output_str = f"\n.data.chan{num}\n"
                data_labels.append(f".data.chan{num}")
                output_str += f"\n\n;..........................\n; frame 0\n"

                skip_byte  = 0
                for idx, val in enumerate(chan_block):

                    if skip_byte > 0 :
                        skip_byte -= 1
                        continue

                    if val == 0xffff:
                        build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, 0 , len(build_str))
                        wait_frame += 1
                        output_str += f"\n\n;..........................\n; frame {wait_frame}\n"
                        if skip_byte > 0:
                            error = (f'Error converting channel block {num}, offset {idx}.')
                            if self.args.guiMode:
                                raise(error)
                            print(error)
                            return False
                        skip_byte = 0
                        continue

                    elif val >= 0x00 and val <= 0x1f:
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
                    elif val >= 0x80 and val <= 0x9f:
                        build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, 0, len(build_str))
                        skip_byte = 0
                    elif val >= 0xA0 and val <= 0xA9:
                        build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex(chan_block[idx+1]&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    elif val >= 0xC0 and val <= 0xCf:
                        build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex(chan_block[idx+1]&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    elif val == 0xB0:
                        build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex(chan_block[idx+1]&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    elif val == 0xFC:
                        build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex((chan_block[idx+1]>>8)&0xff)[2:]}'
                        build_str  += f', ${hex((chan_block[idx+1]>>24)&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    elif val == 0xFD:
                        build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 0
                    elif val == 0xFE:
                        build_str   = f'\n  .db ${hex(val&0xff)[2:]}'
                        build_str  += f', ${hex(chan_block[idx+1]&0xff)[2:]}'
                        output_str += build_str
                        output_str += self.commentDecode(val, chan_block[idx+1], len(build_str))
                        skip_byte = 1
                    else:
                        error = (f'Error: cannot identify token command: chan {num}, offset {hex(idx)}, val {hex(val)}.')
                        if self.args.guiMode:
                            raise(error)
                        print(error)
                        return False

                build_str   = f'\n  .db $fb'
                output_str += build_str
                output_str += self.commentDecode(0xfb, 0x00, len(build_str))
                f.write(output_str)



        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #...........................................................................................................................
        #
        # Support files

        # Write waveform table file.
        with open(self.args.fileout+".wfTable.inc", 'w') as f:
            f.write(f'\n;'+("#"*75)+'\n')
            f.write(f'\n.waveform.table\n')
            f.write(f'\n  .dw ${hex(len(waveform_labels)*2)[2:]}       ; offset to bank table\n\n')
            for idx, wf_label in enumerate(waveform_labels):
                f.write(f"  .dw {wf_label}\n")
            f.write(f'\n\n; Banks\n\n')
            for idx, wf_label in enumerate(waveform_labels):
                f.write(f"  .db bank({wf_label})\n")

        # Write data table file.
        with open(self.args.fileout+".dataTable.inc", 'w') as f:
            f.write(f'\n;'+("#"*75)+'\n')
            f.write(f'\n.data.table\n')
            f.write(f'\n  .dw ${hex(len(data_labels)*2)[2:]}       ; offset to bank table\n\n')
            for idx, wf_label in enumerate(data_labels):
                f.write(f"  .dw {wf_label}\n")
            f.write(f'\n\n; Banks\n\n')
            for idx, wf_label in enumerate(data_labels):
                f.write(f"  .db bank({wf_label})\n")


        # Separate waveform inc
        with open(self.args.fileout+".sfx_wf.inc","w") as f:
            f.write(f' .include "{self.includPathName+".wfTable.inc"}"\n')
            f.write(f' .include "{self.includPathName+".wf.inc"}"\n')

        # Separate data inc
        with open(self.args.fileout+".sfx_data.inc","w") as f:
            f.write(f' .include "{self.includPathName+".dataTable.inc"}"\n')
            for num in range(6):
                if ((self.args.chanMask >> (5-num)) & 0x01) == 0:
                    continue
                f.write(f' .include "{self.includPathName}.chan{num}.inc"\n')

        with open(self.args.fileout+".sfx_main.inc","w") as f:
            f.write(f' .include "{self.includPathName+".sfx_wf.inc"}"\n')
            f.write(f' .include "{self.includPathName+".sfx_data.inc"}"\n')




        self.debugPrint(f'Done')
        return True

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
        elif val >= 0xC0 and val <= 0xCf:
            output_str += f" ; 802 -> ${hex(val)[2:][-1]}, 803 -> ${hex(opr)[2:]}"
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

            # if chan > 1:
            #     continue
            _806_run = []

            #self.debugPrint(f' data set @ chan [{chan}]: {data_set}')

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
                    #self.debugPrint(f'reg    [{reg}], channel [{chan}]')
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

        waveform_list = []
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
                        self.debugPrint(f'{data}')
                        waveform = set([idx<<8|val for idx,val in enumerate(data)])
                        self.debugPrint(f'{waveform}')
                        if not self.waveformCheck(waveform, waveform_list):
                            waveform_list.append(waveform)


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
                        waveform = set([idx<<8|val for idx,val in enumerate(data)])
                        waveform_index = self.getWaveformIndex(waveform_list, waveform)
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
                        #print(f"found 0x02: {period_02}")
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
                #self.debugPrint(f'Frame {frame} ........................................................................................')
                for idx,data_pair in enumerate(data_frame):
                    reg = data_pair['reg']
                    data = data_pair['data']
                    pair_set = set([(idx+1)<<8|val for idx, val in enumerate(data+[reg])])

                    #print(idx)
                    if rle_reg == []:
                        rle_reg.append(pair_set)
                        rle_idx = [idx]
                        #self.debugPrint(f'init reg pair:::::::: {[hex(val) for val in pair_set]},,,, {hex(reg)}, {[hex(val) for val in data]}')
                        continue

                    if pair_set in rle_reg:
                        rle_idx.append(idx)
                        #self.debugPrint(f'found reg pair:::::::: {[hex(val) for val in pair_set]},,,, {hex(reg)}, {[hex(val) for val in data]}')
                        continue

                    for remove_idx in rle_idx[1:]:
                        self.prep_reg_list[chan][frame].pop(remove_idx)
                        #self.debugPrint(f'Removing IDX: {remove_idx}')
                        rle_reg.append(pair_set)
                        rle_reg = []
                        rle_idx = []

                    rle_reg = [pair_set]
                    rle_idx = [idx]
                    #self.debugPrint(f'init reg pair:::::::: {[hex(val) for val in pair_set]},,,, {hex(reg)}, {[hex(val) for val in data]}')


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
                            #sys.exit(1)

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

        #print(f"\n\n\n{self.prep_reg_list}\n\n\n")

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
                    # self.debugPrint(f'data pair : {data_pair}')
                    reg = data_pair['reg']
                    data = data_pair['data']
                    self.debugPrint(f'            Reg: {reg}, data: {[hex(val) for val in data]}')


        return (waveform_list, bin_output)

    def getWaveformIndex(self, waveform_list, waveform):
        # try all 32 rotations
        for wf_idx, cmp_wf in enumerate(waveform_list):
            for i in range(32):
                if cmp_wf == self.rotateWF(waveform, i):
                    return wf_idx

        return False         

    def waveformCheck(self, waveform, waveform_list):

        # try all 32 rotations
        for cmp_wf in waveform_list:
            for i in range(32):
                if cmp_wf == self.rotateWF(waveform, i):
                    return True

        return False            

    def rotateWF(self,waveform, idx):
        waveform = list(waveform)
        new_wf = waveform[idx:] + waveform[:idx]
        return set(new_wf)

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
    runOptionsGroup.add_argument('--fileout',
                                 '-out',
                                 default='',
                                 type=str,
                                 help='path/name for output files')
    runOptionsGroup.add_argument('--dir',
                                 '-d',
                                 default='',
                                 type=str,
                                 help='the "include" path for the source generation')
    runOptionsGroup.add_argument('--chanMask',
                                 '-cm',
                                 default=0x3f,
                                 type=int,
                                 help='Default is 0x3f or 00111111b. Bit set = process channel, clear = ignore channel.')
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
    runOptionsGroup.add_argument('--debugConsole',
                                 '-dbgOut',
                                 default=False,
                                 action="store_true",
                                 help='Not recommended to turn this on. It will slow down the conversion. Check the debug log which is always generated.')

    args = parser.parse_args()

    if args.gui:
        sys.exit( GuiGui(args).process() == False )
    elif args.filein != '':
        sys.exit( ConvertVGM(args).process() == False)
    else:
        print(f'Error: Use --gui or supply a filename for --filein')
        sys.exit(1)

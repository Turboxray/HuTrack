import argparse
import sys

def outputHex(val):
    return hex(val)

def outputDec(val):
    return str(val)

parser = argparse.ArgumentParser(description ='Refactor a PCEAS/HuC symbol file')
parser.add_argument('--filein',
                    '-in',
                    required=True,
                    help ='Input symbol file')
parser.add_argument('--fileout',
                    '-out',
                    default="",
                    help ='Input symbol file')
parser.add_argument('--removeLocal',
                    '-rl',
                    action='store_true',
                    help ='Strip out local variables')
parser.add_argument('--doSize',
                    '-ds',
                    action='store_true',
                    help ='Calculate size of each entry')
parser.add_argument('--removeHucLL',
                    '-rLL',
                    action='store_true',
                    help ='Strip out references to HuC "LLxx" labels')
parser.add_argument('--decsize',
                    '-dec',
                    action='store_true',
                    help ='use decimal for size')
parser.add_argument('--csv',
                    action='store_true',
                    help ='use decimal for size')


 
args = parser.parse_args()

outputSize =(outputHex, outputDec)[args.decsize]

content = None
try:
    with open(args.filein,'r') as f:
        content = f.read()
except Exception as e:
    print(e)
    sys.exit(1)

if not content:
    print(f'File {args.filein} is empty.')
    sys.exit(1)

symTable = []
symHeader = []
for line, item in enumerate(content.split("\n")):
    item = item.strip()
    if line == 0 or line == 1:
        symHeader.append(item)
    else:
        if item[7:].strip().startswith(".") and args.removeLocal:
            continue
        if item[7:].strip().startswith("LL") and args.removeHucLL and not item[7:].strip().startswith("LL0"):
            continue

        if item.strip() == "":
            continue
        bank = int(item[0:2].strip(),16)
        info = item[2:].strip().replace("\t\t\t","\t").replace("\t\t","\t").replace("\t","  ")
        symTable.append((bank,info))

symTable = sorted(symTable, key = lambda x : (x[0], x[1][0:4]),reverse=False)

if args.doSize:
    symHeader[0] = symHeader[0].replace("\t\t","\t").replace("\t","  ")
    symHeader[1] = symHeader[1].replace("\t\t","\t").replace("\t","  ")

    symHeader[0] = symHeader[0] + ' '*(80 - len(symHeader[0])) + "Size"
    symHeader[1] = symHeader[1] + ' '*(80 - len(symHeader[1])) + "----"

    temp = []
    bank = -1
    for line, item in enumerate(symTable):
        if line == 0:
            continue

        val0 = int(symTable[line-1][1][0:4],16) & 0x1fff
        val1 = int(symTable[line-0][1][0:4],16) & 0x1fff

        diff = val1 - val0 + ( (symTable[line][0] - symTable[line-1][0]) * 0x2000)
        info = symTable[line-1][1].replace("\t\t\t","\t").replace("\t\t","\t").replace("\t","  ")

        if symTable[line][0] == 0xF8 and symTable[line-1][0] == 0xF8:
            if val0 <= 0xff and val1 >= 0x100:
                diff = 0x100 - val0
                symTable[line-1] = (symTable[line-1][0], info + ' '*(74 - len(info)) + f'{outputSize(diff)} (????)' )
                continue
            if val0 >= 0x100 and val0 < 0x200 and val1 < 0x200:
                symTable[line-1] = (symTable[line-1][0], info + ' '*(74 - len(info)) + f'{outputSize(diff)} (STACK)' )
                continue
            if val0 >= 0x100 and val0 < 0x200 and val1 >= 0x200:
                diff = 0x200 - val0
                symTable[line-1] = (symTable[line-1][0], info + ' '*(74 - len(info)) + f'{outputSize(diff)} (STACK)' )
                continue


        if symTable[line][0] != 0xF0 and symTable[line-1][0] != 0xF0:
            symTable[line-1] = (symTable[line-1][0], info + ' '*(74 - len(info)) + f'{outputSize(diff)}' )
        elif symTable[line][0] == 0xF0 and symTable[line-1][0] != 0xF0:
            diff = 0x2000 - val0
            symTable[line-1] = (symTable[line-1][0], info + ' '*(74 - len(info)) + f'{outputSize(diff)} (????)' )
        else:
            symTable[line-1] = (symTable[line-1][0], info + ' '*(74 - len(info)) + f'....' )

try:
    ext = (".txt",".csv")[args.csv]
    args.fileout = (args.fileout,args.filein + ext)[args.fileout == ""]
    with open(args.fileout,'w') as f:

        if args.csv:
            header = ','.join([item for item in symHeader[0].split(" ") if item != ""])
            f.write(f'{header}\n')            
            for item in symTable:
                bank = [hex(item[0])]
                info = bank + [i for i in item[1].split(" ") if i != ""]
                info[1] = f'0x{info[1]}'  # make this a string for excel
                line = ','.join(info)
                f.write(f'{line}\n')
        else:
            f.write(f'{symHeader[0]}\n')
            f.write(f'{symHeader[1]}\n')
            for item in symTable:
                bank = hex(item[0])[2:]
                bank = " "*(2-len(bank)) + bank
                f.write(f'  {bank}  {item[1]}\n')
except Exception as e:
    print(e)
    sys.exit(1)


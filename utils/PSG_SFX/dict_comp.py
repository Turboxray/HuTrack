import heapq
import argparse
import sys
from collections import defaultdict


def hex_byte(val):
    val = hex(val)[2:]
    val = '0'*(2-len(val)) + val
    return val

def createDict(content, byte_length):
    curr_dict = {}
    for i in range(0,len(content)-byte_length,1):
        if sum(1 for idx in range(byte_length) if content[i+idx] > 0xff ) > 0:
            continue
        key = ''.join([ hex_byte(content[i+idx]) for idx in range(byte_length)])
        try:
            curr_dict[key] += 1
        except:
            curr_dict[key] = 1


    return curr_dict

def compDict(curr_dict, content, op, level, range_idx):

    curr_dict = list(curr_dict.keys())
    # print(f' dict-{range_idx} keys: {curr_dict}')
    print(f' Pre size: {len(content)}')

    new_content = []
    count_instances = 0
    i = 0
    while i < len(content):
        if len(content) - i >= range_idx:
            key = ''.join([ hex_byte(content[i+idx]) for idx in range(range_idx)])
            # print(f' Checking key: {key}')
            if key in curr_dict:
                key_idx = curr_dict.index(key)
                # print(f' $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n match found. {key}, idx {key_idx}, idx {i} \n')
                if level == 1:
                    new_content.append((op + key_idx)  | 0x1000)
                elif level == 2:
                    new_content.append((op)  | 0x1000)
                    new_content.append(key_idx | 0x1000)
                else:
                    print("Error: only level 1 or 2 allowed. Exiting..")
                    sys.exit(1)
                i += range_idx
                count_instances += 1
            else:
                new_content.append(content[i])
                i += 1
        else:
            new_content.append(content[i])
            i += 1
    content = new_content[:]
    print(f' Post dict-{range_idx} size: {len(new_content)}. instances {count_instances}')
    return content

def main(args):

    # Read binary file and build a dictionary from chunks of 2, 3, 4, and 5 bytes

    # File path (replace with your actual binary file path)
    binary_file_path = args.filein

    content = []
    with open(binary_file_path, "rb") as binary_file:
        content = binary_file.read()

    content = [int(val) for val in content]

    byte_occur_map = {}
    range_map = set(content)
    for val in content:
        try:
            byte_occur_map[val] += 1
        except:
            byte_occur_map[val] = 1

    print(f' range map size: {len(range_map)}')


    dict_occr = { 2 : {}, 3 : {}, 4 : {}, 5: {} }

    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    dict_num = 16
    curr_dict = createDict(content, dict_num)
    curr_dict = dict(sorted(curr_dict.items(), key=lambda item: item[1]))
    curr_dict = dict(list(curr_dict.items())[-8:])
    print(f' Dict {dict_num}: {curr_dict}')
    dict_occr[dict_num] = curr_dict
    content = compDict(dict_occr[dict_num],content,0xD0,2,dict_num)

    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    dict_num = 8
    curr_dict = createDict(content, dict_num)
    curr_dict = dict(sorted(curr_dict.items(), key=lambda item: item[1]))
    curr_dict = dict(list(curr_dict.items())[-16:])
    print(f' Dict {dict_num}: {curr_dict}')
    dict_occr[dict_num] = curr_dict
    content = compDict(dict_occr[dict_num],content,0xD0,2,dict_num)



    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    dict_num = 4
    curr_dict = createDict(content, dict_num)
    curr_dict = dict(sorted(curr_dict.items(), key=lambda item: item[1]))
    curr_dict = dict(list(curr_dict.items())[-16:])
    print(f' Dict {dict_num}: {curr_dict}')
    dict_occr[dict_num] = curr_dict
    content = compDict(dict_occr[dict_num],content,0xD0,2,dict_num)

    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    dict_num = 3
    curr_dict = createDict(content, dict_num)
    curr_dict = dict(sorted(curr_dict.items(), key=lambda item: item[1]))
    curr_dict = dict(list(curr_dict.items())[-32:])
    print(f' Dict {dict_num}: {curr_dict}')
    dict_occr[dict_num] = curr_dict
    content = compDict(dict_occr[dict_num],content,0xD0,2,dict_num)


    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    # ............................................................................................
    dict_num = 2
    curr_dict = createDict(content, dict_num)
    curr_dict = dict(sorted(curr_dict.items(), key=lambda item: item[1]))
    curr_dict = dict(list(curr_dict.items())[-16:])
    print(f' Dict {dict_num}: {curr_dict}')
    dict_occr[dict_num] = curr_dict
    content = compDict(dict_occr[dict_num],content,0xE0,1,dict_num)



    for i in range(len(content)):
        if content[i] > 0x0ff:
            content[i] = content[i] & 0xff

    with open('dict_test.bin','wb') as f:
        f.write(bytearray(content))

    # # dict_occr[2] = sorted(dict_occr[2], key=lambda x: x[1])
    # dict_occr[2] = dict(sorted(dict_occr[2].items(), key=lambda item: item[1]))
    # dict_occr[3] = dict(sorted(dict_occr[3].items(), key=lambda item: item[1]))
    # dict_occr[4] = dict(sorted(dict_occr[4].items(), key=lambda item: item[1]))



    # dict_two_byte = {}
    # for key2, val2 in dict_occr[2]:
    #     for key3, val3 in dict_occr[2]:
    #         pass
    #     for key4, val4 in dict_occr[2]:
    #         pass
    #     for key5, val5 in dict_occr[2]:
    #         pass

    # dict_occr[5] = dict(list(dict_occr[5].items())[:16])

    # dict_occr[2] = {key : val for key, val in dict_occr[2].items() if val > 5}
    # dict_occr[3] = {key : val for key, val in dict_occr[3].items() if val > 5}
    # dict_occr[4] = {key : val for key, val in dict_occr[4].items() if val > 5}
    # dict_occr[5] = {key : val for key, val in dict_occr[5].items() if val > 5}

    # print(f' Dict 2: {dict_occr[2]}\n\n')
    # print(f' Dict 3: {dict_occr[3]}\n\n')
    # print(f' Dict 4: {dict_occr[4]}\n\n')
    # print(f' Dict 5: {dict_occr[5]}\n\n')

    # print(f' Dict 2 size : {len(list(dict_occr[2].keys()))}\n\n')
    # print(f' Dict 3 size : {len(list(dict_occr[2].keys()))}\n\n')
    # print(f' Dict 4 size : {len(list(dict_occr[2].keys()))}\n\n')
    # print(f' Dict 5 size : {len(list(dict_occr[2].keys()))}\n\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f'Convert VGM files to PCEAS source as Data. Ver: 1',
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    runOptionsGroup = parser.add_argument_group('Run options', 'Run options for TMX converter')
    runOptionsGroup.add_argument('--filein',
                                 '-in',
                                 required=True,
                                 help='Source file')
    # runOptionsGroup.add_argument('--fileout',
    #                              '-out',
    #                              required=True,
    #                              help='Compressed file')

    args = parser.parse_args()

    main(args)

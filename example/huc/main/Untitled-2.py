

def compress2(data):
    lit_store = []
    rle_store = []
    output    = []
    lastVal     = 0
    byte_run    = 0

    for idx, currVal in enumerate(data):

        if byte_run == 0:
            lastVal = currVal
            byte_run   = 1
            lit_store = []
            rle_store = []

            lit_store.append(currVal)

        # if we have a repeat instance
        elif lastVal == currVal:

            # Are we in the middle of a literal run? Cancel it if so..
            if len(lit_store) > 1:
                # Don't include the last literal value, because that's the start of the new RLE
                output += [len(lit_store)-1]
                output += lit_store[:-1]
                lit_store = []
                rle_store = []
                rle_store.append(lastVal)
            else:
                lit_store = []
                # Nope, just keep adding to the RLE pile
                rle_store.append(lastVal)

            byte_run += 1

            # run length reached a byte limit boundary?
            if byte_run == 30:
                print("byte run limit!!!!!!!!!!!!! RLE")
                output += [len(rle_store) + 1 | 0x80]
                output += [rle_store[0]]
                byte_run = 0
            # run length meet max length?
            elif len(rle_store) == 0x7f:
                output += [len(rle_store) | 0x80]
                output += [rle_store[0]]
                rle_store = []
                lit_store = []
                lit_store.append(currVal)
            
        else:

            # Are we in the middle of an RLE run?
            if len(rle_store) > 0:
                output += [len(rle_store) + 1  | 0x80]
                output += [rle_store[0]]
                rle_store = []
                lit_store = []
                lit_store.append(currVal)
            else:
                lit_store.append(currVal)

            lastVal = currVal
            byte_run += 1

            # run length reached a byte limit boundary?
            if byte_run == 30:
                print("byte run limit!!!!!!!!!!!!! LIT")
                output += [len(lit_store)]
                output += lit_store
                byte_run = 0
            # run length meet max length?
            elif len(lit_store) == 0x7f:
                output += [len(lit_store)]
                output += lit_store
                rle_store = []
                lit_store = []
                lit_store.append(currVal)

    
    print(len(data), "bytes compresed to", len(output))
        
    return output

def decompress2(compData):
    output = []
    idx = 0
    while idx < len(compData):
        rle = compData[idx]
        if rle > 0x7f:
            val = compData[idx+1]
            idx += 2
            for runLen in range(rle & 0x7f):
                output.append(val)
        else:
            for runLen in range(rle):
                output.append(compData[(idx+1)+runLen])
            idx += 1 + rle

    return output

def compareDataSets(data1, data2):
    results = False

    if len(data1) != len(data2):
        print('Arrays are different sizes')
    else:
        results = True
        for val1, val2 in zip(data1,data2):
            if val1 != val2:
                reults = False
                break


    print(("Arrays are NOT identical","Arrays are identical")[results])

    return results
        #  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 
myData = [ 
           1, 2, 3, 4, 5, 4, 5, 5, 4, 4, 4, 5, 6, 7, 8, 7, 6, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 4, 5, 4, 5, 5, 4, 4, 4, 5, 6, 7, 8, 7, 6, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
           5, 2, 3, 4, 5, 4, 5, 5, 4, 4, 4, 5, 6, 7, 8, 7, 6, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

print("\n\n")
print(myData)
compressedData = compress2(myData)
print(compressedData)

decompData = decompress2(compressedData)
print("\n\n myData")
print(myData)
print("Decomp data")
print(decompData)
print("\n\n")

compareDataSets(myData, decompData)



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
                output = output + [len(lit_store[:-1]), lit_store[:-1]] # Don't include the last literal value, because that's the start of the new RLE
                lit_store = []
                rle_store = []
                rle_store.append(lastVal,lastVal)
            else:
                # Nope, just keep adding to the RLE pile
                rle_store.append(lastVal)

            byte_run   += 1

            # run length reached a byte limit boundary?
            if byte_run == 30:
                output += [len(rle_store)|0x80,rle_store[0]]
                byte_run   = 0
            # run length meet max length?
            elif len(rle_store) == 0x7f:
                output += [len(rle_store)|0x80,rle_store[0]]
                rle_store = []
                lit_store = []
                lit_store.append(currVal)
            
        else:

            # Are we in the middle of an RLE run?
            if len(rle_store) > 0:
                output += [len(rle_store),rle_store[0]]
                rle_store = []
                lit_store = []
                lit_store.append(currVal)

            lastVal = currVal
            byte_run += 1

            # run length reached a byte limit boundary?
            if byte_run == 30:
                output += [len(lit_store),lit_store]
                byte_run   = 0
            # run length meet max length?
            elif len(lit_store) == 0x7f:
                output += [len(lit_store),lit_store]
                rle_store = []
                lit_store = []
                lit_store.append(currVal)

    
    print(len(data), "bytes compresed to", len(output))
        
    return output

def compress(data):
    bytesFormat = []
    lastVal     = 0
    rle_count   = 0
    col_run     = 0

    for idx, currVal in enumerate(data):

        if col_run == 0:
            lastVal = currVal
            rle_count = 1
            col_run   = 1

        # if we have a repeat run
        elif lastVal == currVal:
            rle_count += 1
            col_run   += 1

            # run length reached a column boundary?
            if col_run == 30:
                bytesFormat.append(bytes([rle_count]))
                bytesFormat.append(bytes([lastVal]))
                rle_count = 1
                col_run   = 0
            # run length meet max length?
            elif rle_count == 255:
                bytesFormat.append(bytes([rle_count]))
                bytesFormat.append(bytes([lastVal]))
                rle_count = 1

            # else keep counting..
            
        # run/RLE has broke
        else:

            #Did we have a previous run?
            bytesFormat.append(bytes([rle_count]))
            bytesFormat.append(bytes([lastVal]))
            rle_count = 1
            lastVal = currVal

            if col_run < 30:
                col_run += 1
            else:
                col_run = 1
    
    print(len(data), "bytes compresed to", len(bytesFormat))
        
    return bytesFormat

def decompress(compData):
    compData = [int.from_bytes(val, "big")for val in compData]
    output = []
    for idx in range(0, len(compData), 2):
        rle = compData[idx]
        val = compData[idx+1]
        for runLen in range(rle):
            output.append(val)

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

compressedData = compress(myData)
print([int.from_bytes(val, "big")for val in compressedData])

decompData = decompress(compressedData)
print("\n\n")
print(myData)
print(decompData)
print("\n\n")

compareDataSets(myData, decompData)

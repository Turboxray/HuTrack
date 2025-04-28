import heapq
import argparse
from collections import defaultdict

# Function to build frequency dictionary
def calculate_frequency(data):
    frequency = defaultdict(int)
    for byte in data:
        frequency[byte] += 1
    return frequency

# Function to build Huffman tree
def build_huffman_tree(frequency):
    heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[1]), p))

# Function to compress data using Huffman coding
def huffman_compress(data, huffman_codes):
    compressed_data = "".join([huffman_codes[byte] for byte in data])
    return compressed_data

# Function to pad the compressed data to make it byte-aligned
def pad_compressed_data(compressed_data):
    padding_length = 8 - len(compressed_data) % 8
    padded_data = compressed_data + "0" * padding_length
    padding_info = "{:08b}".format(padding_length)
    return padding_info + padded_data

# Function to save compressed data to a file
def save_to_file(filename, compressed_data):
    byte_data = bytearray()
    for i in range(0, len(compressed_data), 8):
        byte = compressed_data[i:i+8]
        byte_data.append(int(byte, 2))
    size = len(byte_data)
    with open(filename, "wb") as file:
        file.write(byte_data)
    return size

# Main function
def main(args):
    input_filename = args.filein  # Replace with your binary file name
    output_filename = args.fileout

    # Read binary data
    with open(input_filename, "rb") as file:
        data = file.read()

    raw_size = len(data)
    # Generate frequency dictionary
    frequency = calculate_frequency(data)
    print(frequency)
    # sorted_dictionaries = sorted(frequency, key=lambda x: x[''])
    pairs = [(key,val) for key,val in frequency.items()]
    pairs = sorted(pairs, key=lambda x: x[1])
    print(pairs)

    # Build Huffman tree and codes
    huffman_tree = build_huffman_tree(frequency)
    huffman_codes = {symbol: code for symbol, code in huffman_tree}
    print(huffman_tree)

    # Compress data using Huffman coding
    compressed_data = huffman_compress(data, huffman_codes)

    # Pad compressed data and save to file
    padded_data = pad_compressed_data(compressed_data)
    # comp_size = len(padded_data)
    comp_size = save_to_file(output_filename, padded_data)
    print(f"File compressed and saved to {output_filename}. Raw: {raw_size}, Comp: {comp_size}, ratio: {comp_size/raw_size}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f'Convert VGM files to PCEAS source as Data. Ver: 1',
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    runOptionsGroup = parser.add_argument_group('Run options', 'Run options for TMX converter')
    runOptionsGroup.add_argument('--filein',
                                 '-in',
                                 required=True,
                                 help='Source file')
    runOptionsGroup.add_argument('--fileout',
                                 '-out',
                                 required=True,
                                 help='Compressed file')

    args = parser.parse_args()

    main(args)

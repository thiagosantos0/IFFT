
# Main file for IFTT linter

import sys
import os

from ifft_core.ifft_parser import *

def main():
    results = scan_files()

    for file, blocks in results.items():
        for block in blocks:
            print(f"Changed identified inside a IFFT block in {file}:\n\n {block['block_content']}")
            print(f"Modified lines within the block: {block['modified_lines_within_block']}")
            print(f"Should also modify: {block['associated_file_name']}\nBlock label: {block['associated_file_label']}\n")

if __name__ == "__main__":
    main()


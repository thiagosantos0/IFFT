# Main file for IFTT linter

import sys
import os

from ifft_core.ifft_parser import scan_file

def main():
    results = scan_file()

if __name__ == "__main__":
    main()


# Main file for IFTT linter

import sys
import os

from ifft_core.ifft_parser import *

def main():
    results = analyze_repo()
    print(f"Scan results: \n {results}")

if __name__ == "__main__":
    main()


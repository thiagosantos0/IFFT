# Main file for IFTT linter

import sys
import os

from ifft_core.ifft_parser import *

def main():
    results = analyze_repo()

    # Changes in IFFT blocks 
    print(f"Changed identified inside a IFFT block:\n\n {results['app.py'][0][0]}")
    print(f"Should also modify: {results['app.py'][0][1]}\nBlock label: {results['app.py'][0][2]}")



if __name__ == "__main__":
    main()


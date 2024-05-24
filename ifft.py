import argparse
import json
import logging
import os
from ifft_core.ifft_parser import scan_files

def main(auto_mode=False):
    logging.debug("Starting IFFT scan.")
    
    config_path = os.path.join(os.path.dirname(__file__), 'ifft_config.json')
    logging.debug(f"Config path: {config_path}")
    
    if os.path.exists(config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
            auto_mode = config.get('auto_mode', auto_mode)
            logging.debug(f"Auto mode set to: {auto_mode}")
    
    results = scan_files(auto_mode=auto_mode)
    
    if not results:
        logging.debug("No results found from scan_files.")
    else:
        logging.debug(f"Results found: {results}")
    
    changes_detected = False
    for file, blocks in results.items():
        for block in blocks:
            logging.debug(f"Changed identified inside a IFFT block in {file}:\n\n {block['block_content']}")
            print(f"Modified lines within the block: {block['modified_lines_within_block']}")
            if block['modified_lines_within_block'] != []:
                print(f"Should also modify: {block['associated_file_name']}\nBlock label: {block['associated_file_label']} \n")
                changes_detected = True
                if auto_mode:
                    # Error code that indicate changes detected
                    return 1
    
    if changes_detected:
        return 1
    
    print("No changes detected in IFFT blocks")
    # Error code for successfull execution
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run IFFT tool.")
    parser.add_argument("--auto", action="store_true", help="Run in automatic mode")
    args = parser.parse_args()
    
    exit(main(auto_mode=args.auto))


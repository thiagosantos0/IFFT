import argparse
import json
import logging
import os
from block_manager.block_manager_class import BlockManager
from ifft_core.ifft_parser import scan_files

def load_config():
    """Load the IFFT configuration file."""
    config_path = os.path.join(os.path.dirname(__file__), 'ifft_config.json')
    if os.path.exists(config_path):
        with open(config_path) as config_file:
            return json.load(config_file)
    return {}


def main(auto_mode=False):
    
    # Parsing the configuration file
    config = load_config()
    logging.debug(f"Configurations loaded: {config}")

    # Tool opt-in configs
    debug_mode = config.get('debug_mode', False)
    auto_mode = config.get('auto_mode', False)
    show_active_blocks = config.get('show_active_blocks', False)

    if debug_mode:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode enabled.")
    

    # Remove this code section once config logic is implemented
    config_path = os.path.join(os.path.dirname(__file__), 'ifft_config.json')
    logging.debug(f"Config path: {config_path}")
    
    # if os.path.exists(config_path):
    #     with open(config_path) as config_file:
    #         config = json.load(config_file)
    #         auto_mode = config.get('auto_mode', auto_mode)
    #         logging.debug(f"Auto mode set to: {auto_mode}")
    

    logging.debug("Starting IFFT scan.")
    results = scan_files(auto_mode=auto_mode)


    
    if not results:
        logging.debug("No results found from scan_files.")
    else:
        logging.debug(f"Results found: {results}")


    # All options besides debug_mode will be disabled in auto_mode version
    if not auto_mode:
        # Create a block manager object to manage the blocks
        block_manager = BlockManager(show_active_blocks=show_active_blocks)


        # ---------------------------------------------------
        # Feature: Get total active blocks in the project
        if show_active_blocks:
            block_manager.get_block_count()

    
    changes_detected = False
    for file, blocks in results.items():
        for block in blocks:
            logging.debug(f"Change identified inside an IFFT block in {file}:\n\n {block.block_content}")
            print(f"Modified lines within the block: {block.modified_lines}")
            if block.modified_lines != []:
                print(f"Should also modify: {block.associated_file_name}\nBlock label: {block.associated_file_label} \n")
                changes_detected = True
                if auto_mode:
                    return 1

    if changes_detected:
        return 1

    print("No changes detected in IFFT blocks")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run IFFT tool.")
    parser.add_argument("--auto", action="store_true", help="Run in automatic mode")
    args = parser.parse_args()
    
    exit(main(auto_mode=args.auto))


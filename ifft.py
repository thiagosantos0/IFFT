import argparse
import json
import logging
import os
import time
from block_manager.block_manager_class import BlockManager
from ifft_core.ifft_parser import scan_files
from ifft_core.ifft_parser import scan_file
from ifft_core.ifft_parser import save_results_to_file 

def load_config():
    """Load the IFFT configuration file."""
    config_path = os.path.join(os.path.dirname(__file__), 'ifft_config.json')
    if os.path.exists(config_path):
        with open(config_path) as config_file:
            return json.load(config_file)
    return {}

def get_project_root():
    """Retrieve the project root directory from the configuration."""
    config = load_config()
    project_root = config.get("project_root", "mock_project")
    return os.path.abspath(project_root)  # Ensure it's an absolute path

def list_python_files(project_root=None, metadata_dir="block_metadata", excluded_folders=None):
    """
    List all Python files in the project root, using metadata as a fallback.

    Args:
        project_root (str): The root directory of the project.
        metadata_dir (str): The directory where metadata files are stored.
        excluded_folders (list): List of folder names or paths to exclude.

    Returns:
        list: A list of Python file paths.
    """
    # Fallback to dynamically retrieve project root if not provided
    if not project_root:
        project_root = get_project_root()

    python_files = []
    excluded_folders = excluded_folders or []

    print(f"Project root: {project_root}")
    print(f"Metadata_Dir: {metadata_dir}")
    # Option 1: Use metadata directory to find tracked files
    metadata_path = os.path.join(project_root, metadata_dir)
    if os.path.exists(metadata_path):
        for metadata_file in os.listdir(metadata_path):
            if metadata_file.endswith(".json"):
                python_file = os.path.join(project_root, metadata_file.replace(".json", ".py"))
                if os.path.isfile(python_file):
                    python_files.append(python_file)

    # Option 2: Fallback to scanning the project root if no metadata files are found
    if not python_files:
        for root, dirs, files in os.walk(project_root):
            # Exclude specified folders
            if any(excluded in root for excluded in excluded_folders):
                continue

            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

    return python_files


def validate_excluded_folders(project_root, excluded_folders):
    """
    Validate that excluded folders exist within the project root.

    Args:
        project_root (str): The root directory of the project.
        excluded_folders (list): List of folder names or paths to validate.

    Returns:
        list: A list of valid excluded folders.
    """
    valid_folders = []
    for folder in excluded_folders:
        folder_path = os.path.join(project_root, folder)
        if os.path.isdir(folder_path):
            valid_folders.append(folder)
        else:
            logging.warning(f"Excluded folder '{folder}' does not exist.")
    return valid_folders



def main(auto_mode=False):
    # Parsing the configuration file
    config = load_config()
    logging.debug(f"Configurations loaded: {config}")

    # Tool opt-in configs
    debug_mode = config.get('debug_mode', False)
    auto_mode = config.get('auto_mode', False)
    show_active_blocks = config.get('show_active_blocks', False)
    extract_ifft_content = config.get('extract_ifft_blocks_content', False)
    ifft_disabled = config.get('disable_ifft', False)
    restore_ifft = config.get('re_enable_ifft', False)
    excluded_folders = config.get('excluded_folders', [])
    excluded_folders = validate_excluded_folders(config.get('project_root'), excluded_folders)



    if debug_mode:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode enabled.")
    
    project_root = get_project_root()
    logging.debug(f"Project root: {project_root}")


    results = scan_files(auto_mode=auto_mode, project_path=project_root)
    if not results:
        logging.debug("No results found from scan_files.")
    else:
        logging.debug(f"Results found: {results}")
        # Save results to be consumed by UI API's
        path = os.path.join(project_root, "..", "IFFT_WEB/data/", "ifft_results.json")
        save_results_to_file(results, output_file=path)
        


    # All options besides debug_mode will be disabled in auto_mode version
    if not auto_mode:
        # Create a block manager object to manage the blocks
        block_manager = BlockManager(show_active_blocks=show_active_blocks)


        # ---------------------------------------------------
        # Feature: Get total active blocks in the project
        if show_active_blocks:
            block_manager.get_block_count()


        # ---------------------------------------------------
        # Feature: Extract IFFT block content and save it to a "storage_file"
        # default name is "ifft_blocks.json"

        if extract_ifft_content:
            print("[ Extract Content Mode ]")
            print("Extracting IFFT block content...")
            time.sleep(1)
            logging.debug("Extracting IFFT block content...")
            python_files = list_python_files(project_root, excluded_folders=excluded_folders)
            for file_name in python_files:
                blocks = scan_file(project_root, file_name, set())
                print(f"[INFO] blocks: {blocks}")
                if blocks:
                    block_manager.extract_blocks(file_name, blocks)
            return 0

        # ---------------------------------------------------
        # Feature: Disable IFFT mode. This option will remove all IFFT blocks from the project
        if ifft_disabled:
            print("[ Disable IFFT Mode ]")
            print("Cleaning up IFFT blocks trace...")
            time.sleep(1)
            logging.debug("All blocks removed with success.")
            python_files = list_python_files(project_root, excluded_folders=excluded_folders)
            for file_name in python_files:
                block_manager.remove_ifft_trace(file_name)
            return 0

        # ---------------------------------------------------
        # Feature: Restore IFFT mode
        if restore_ifft:
            print("[ Restore IFFT Mode ]")
            print("Restoring IFFT blocks...")
            time.sleep(1)
            logging.debug("Restoring IFFT blocks...")
            python_files = list_python_files(project_root, excluded_folders=excluded_folders)
            for file_name in python_files:
                print(f"[INFO] Restoring blocks for {file_name}")
                block_manager.restore_ifft_blocks(file_name)
            logging.debug("All blocks restored successfully.")
            return 0



    
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


import json
import re
import logging
from colorama import Fore, Style
import os

from helpers.helpers import resolve_path


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

def list_python_files(project_root=None, metadata_dir="block_metadata"):
    """
    List all tracked Python files in the user-specified project.
    First checks the block_metadata directory, and falls back to scanning the project root.

    Args:
        project_root (str): Root path of the project (default: None).
        metadata_dir (str): Directory where metadata is stored.

    Returns:
        List[str]: List of Python file paths.
    """
    if not project_root:
        project_root = get_project_root()

    python_files = []

    # Option 1: Use metadata directory to find tracked files
    metadata_path = os.path.join(project_root, metadata_dir)
    if os.path.exists(metadata_path):
        for metadata_file in os.listdir(metadata_path):
            if metadata_file.endswith(".json"):
                python_files.append(os.path.join(project_root, metadata_file.replace(".json", ".py")))

    # Option 2: Fallback to scanning the project root
    if not python_files:
        for root, _, files in os.walk(project_root):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

    return python_files

class BlockManager:
    def __init__(self, storage_dir="block_metadata", show_active_blocks=False):
       self.storage_dir = storage_dir
       self.show_active_blocks = show_active_blocks
       self.block_data = {}

       # Load metadata into block_data
       self._load_metadata()

       if self.show_active_blocks:
           self._display_active_blocks()

    def _load_metadata(self):
        """Load all metadata from the block_metadata directory."""
        if not os.path.exists(self.storage_dir):
            logging.warning(f"Metadata directory '{self.storage_dir}' does not exist.")
            return

        for metadata_file in os.listdir(self.storage_dir):
            if metadata_file.endswith(".json"):
                file_path = os.path.join(self.storage_dir, metadata_file)
                try:
                    with open(file_path, "r") as f:
                        file_data = json.load(f)
                        self.block_data[metadata_file] = file_data
                except json.JSONDecodeError:
                    logging.error(f"[ERROR] Invalid JSON in {file_path}. Skipping this file.")
                except Exception as e:
                    logging.error(f"[ERROR] Could not load metadata from {file_path}: {e}")


    def _display_active_blocks(self):
        """Display active blocks (for visualization purposes)."""
        if not self.block_data:
            print(f"{Fore.YELLOW}No active blocks found.{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}Active Blocks:{Style.RESET_ALL}")
        for file_name, blocks in self.block_data.items():
            print(f"File: {file_name}")
            for block in blocks:
                print(f"  Block Label: {block['associated_file_label']}")
                print(f"  Block Start: {block['block_start']}")
                print(f"  Block End: {block['block_end']}")


    def save_metadata(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.block_data, f, indent=4)

    def get_block_count(self):
        """Count the total number of active IFFT blocks in the project."""
        total_blocks = 0
        for file, blocks in self.block_data.items():
            # Counting only blocks with associated_file_name and associated_file_label
            if (blocks[0]['associated_file_name'] == "" or blocks[0]['associated_file_label'] == ""):
                logging.warning(f"{Fore.YELLOW} A block in file '{file}' does not have 'associated_file_name' or 'associated_file_label'. Skipping it.{Style.RESET_ALL}")
                continue

            total_blocks += len(blocks)
        print(f"{Fore.GREEN}Total active IFFT blocks in the project: {total_blocks}")
        return total_blocks

    def extract_blocks(self, file_name, blocks):
        """
        Extract IFFT blocks from a file and store their metadata in the block_metadata directory.
        The original file content is not modified.
        
        Args:
            file_name (str): The name of the file to extract blocks from.
            blocks (list): A list of block information (start, end, content, etc.) for the file.
        """
        logging.info(f"Extracting IFFT blocks for {file_name}...")
        file_prefix = file_name.split("/")[-1].split(".")[0]

        # Ensure the block_metadata directory exists
        metadata_dir = os.path.join(get_project_root(), "..", "block_metadata")
        os.makedirs(metadata_dir, exist_ok=True)

        # Construct the metadata file path
        metadata_file_path = os.path.join(metadata_dir, f"{file_prefix}.json")

        # Prepare metadata to store
        metadata = []
        for block in blocks:
            metadata.append({
                "block_start": block.block_start,
                "block_end": block.block_end,
                "block_content": block.block_content,
                "associated_file_name": block.associated_file_name,
                "associated_file_label": block.associated_file_label
            })

        # Write metadata to the JSON file
        with open(metadata_file_path, "w") as f:
            json.dump(metadata, f, indent=4)
        
        logging.info(f"Metadata for {file_name} stored in {metadata_file_path}.")

    

    def remove_ifft_trace(self, file_name):
        """
        Remove IFFT annotations from the file and store metadata in the block_metadata directory.
        """
        # getting only the filename without the extension
        # from a pattern like this: /home/thiagosan/Área de Trabalho/IFFT/block_manager/block_manager_class.py
        file_prefix = file_name.split("/")[-1].split(".")[0]

        script_file_name = file_prefix + ".py"
        metadata_file_name = file_prefix + ".json"

        logging.info(f"Removing IFFT blocks from {script_file_name}")
        source_file_path = resolve_path(script_file_name)

        if not os.path.exists(source_file_path):
            logging.error(f"Source file {script_file_name} not found.")
            return

        metadata_path = os.path.join(self.storage_dir, f"{file_prefix}.json")
        metadata = []

        with open(source_file_path, "r") as source_file:
            lines = source_file.readlines()

        # Scan the file and extract metadata for IFFT blocks
        in_block = False
        block_content = ""
        block_start = None
        block_end = None
        associated_file_name = ""
        associated_file_label = ""

        for line_number, line in enumerate(lines):
            if line.strip().startswith("#IFFT.If"):
                in_block = True
                block_start = line_number + 1  # 1-based index
                block_content += line

            elif line.strip().startswith("#IFFT.Then"):
                if in_block:
                    block_end = line_number + 1  # 1-based index
                    block_content += line
                    # Extract associated file and label
                    parts = re.search(r"#IFFT.Then\(\"(.*?)\", \"(.*?)\"\)", line)
                    if parts:
                        associated_file_name = parts.group(1)
                        associated_file_label = parts.group(2)

                    # Store metadata
                    metadata.append({
                        "block_start": block_start,
                        "block_end": block_end,
                        "block_content": block_content,
                        "associated_file_name": associated_file_name,
                        "associated_file_label": associated_file_label
                    })

                    # Reset block
                    in_block = False
                    block_content = ""

            elif in_block:
                block_content += line

        # Write metadata to file
        os.makedirs(self.storage_dir, exist_ok=True)
        with open(metadata_path, "w") as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

        print(f"{Fore.YELLOW}[INFO] Metadata written to {metadata_path}")

        # Remove IFFT annotations from the source file
        lines = [
            line for line in lines
            if not line.strip().startswith("#IFFT.If") and not line.strip().startswith("#IFFT.Then")
        ]

        with open(source_file_path, "w") as source_file:
            source_file.writelines(lines)

        print(f"{Fore.YELLOW}[INFO] Removed IFFT blocks from {script_file_name}.")


    def restore_ifft_blocks(self, file_name_prefix):
        """
        Restore IFFT annotations and metadata from the JSON file to the original code.
        Handles edge cases where blocks span the last line of the file.
        """

        file_prefix = file_name_prefix.split("/")[-1].split(".")[0]
        print(f"{Fore.YELLOW}[INFO] Restoring IFFT blocks for file: {Style.RESET_ALL}", file_prefix)

        # Construct the path to the metadata file
        metadata_path = os.path.join("block_metadata", f"{file_prefix}.json")
        logging.info(f"Metadata path: {metadata_path}")

        if not os.path.exists(metadata_path):
            print(f"{Fore.RED}[ERROR] Metadata file for {file_prefix} not found.")
            return

        # Load metadata
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        filename = f"{file_prefix}.py"
        # Read the target file
        target_file_path = os.path.join(get_project_root(), filename)
        if not os.path.exists(target_file_path):
            print(f"{Fore.RED}[ERROR] Target file {filename} not found.{Style.RESET_ALL}")
            return

        with open(target_file_path, "r") as f:
            lines = f.readlines()

        # Restore each block in reverse order
        for block in sorted(metadata, key=lambda b: -b["block_start"]):
            block_start = block["block_start"] - 1
            block_end = block["block_end"] - 1

            # Insert the opening marker if it does not already exist
            if block_start < len(lines) and not lines[block_start].strip().startswith("#IFFT.If"):
                lines.insert(block_start, f"#IFFT.If({block['associated_file_label']})\n")

            # Insert the closing marker if it does not already exist
            if block_end >= len(lines):  # Handle edge case for last line
                lines.append(f"#IFFT.Then(\"{block['associated_file_name']}\", \"{block['associated_file_label']}\")\n")
            elif not any(line.strip().startswith("#IFFT.Then") and block["associated_file_label"] in line for line in lines[block_end:]):
                lines.insert(block_end + 1, f"#IFFT.Then(\"{block['associated_file_name']}\", \"{block['associated_file_label']}\")\n")

        # Write back to the target file
        with open(target_file_path, "w") as f:
            f.writelines(lines)

        print(f"{Fore.YELLOW}[INFO] Successfully restored IFFT blocks to {filename}")


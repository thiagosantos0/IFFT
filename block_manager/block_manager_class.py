import json
import re
import logging
from colorama import Fore, Style
import os

from helpers.helpers import resolve_path

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
        print(f"[adesk5] called '_load_metadata' function")
        if not os.path.exists(self.storage_dir):
            logging.warning(f"Metadata directory '{self.storage_dir}' does not exist.")
            return

        for metadata_file in os.listdir(self.storage_dir):
            if metadata_file.endswith(".json"):
                file_path = os.path.join(self.storage_dir, metadata_file)
                try:
                    with open(file_path, "r") as f:
                        file_data = json.load(f)  # Attempt to load JSON
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
            total_blocks += len(blocks)
        print(f"Total active IFFT blocks in the project: {total_blocks}")
        return total_blocks

    
    def extract_blocks(self, file_name, blocks):
        """
        Extract the content of IFFT blocks and store it in the metadata JSON.
        Does not remove the blocks from the code.
        """
        if file_name not in self.block_data:
            self.block_data[file_name] = []


        for block in blocks:
            # Getting the full_path of the file in "block.file_path" field
            with open(block.file_path, "r") as file:
                lines = file.readlines()

                block_start = block.block_start - 1  # Convert to zero-based index
                block_end = block.block_end - 1

                block_content = "".join(lines[block_start:block_end + 1])
                self.block_data[file_name].append({
                    "associated_file_label": block.associated_file_label,
                    "block_start": block.block_start,
                    "block_end": block.block_end,
                    "block_content": block_content
                })

        self.save_metadata()
        print(f"Extracted {len(blocks)} blocks from {file_name}.")

    def remove_ifft_trace(self, file_name):
        """
        Remove IFFT annotations from the file and store metadata in the block_metadata directory.
        """
        # getting only the filename without the extension
        # from a pattern like this: /home/thiagosan/Área de Trabalho/IFFT/block_manager/block_manager_class.py
        file_prefix = file_name.split("/")[-1].split(".")[0]

        script_file_name = file_prefix + ".py"
        metadata_file_name = file_prefix + ".json"

        print(f"[adesk5] file_prefix is: {file_prefix}")

        print(f"[DEBUG] Removing IFFT blocks from {script_file_name}")
        source_file_path = resolve_path(script_file_name)
        print(f"[adesk5] source_file_path is: {source_file_path}")

        if not os.path.exists(source_file_path):
            logging.error(f"Source file {script_file_name} not found.")
            return

        metadata_path = os.path.join(self.storage_dir, f"{file_prefix}.json")
        print(f"[adesk5] metadata_file_name is: {metadata_file_name}")
        print(f"[adesk5] metadata_path is: {metadata_path}")
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

        print(f"[INFO] Metadata written to {metadata_path}")

        # Remove IFFT annotations from the source file
        lines = [
            line for line in lines
            if not line.strip().startswith("#IFFT.If") and not line.strip().startswith("#IFFT.Then")
        ]

        with open(source_file_path, "w") as source_file:
            source_file.writelines(lines)

        print(f"[INFO] Removed IFFT blocks from {script_file_name}.")


    def restore_ifft_blocks(self, file_name):
        """
        Restore IFFT annotations and metadata from the JSON file to the original code.
        Uses adjusted indices to account for removed lines.
        """
        if file_name not in self.block_data:
            print(f"No stored blocks for {file_name}.")
            return

        with open(file_name, "r") as file:
            lines = file.readlines()

        # Restore each block in reverse order to avoid shifting lines
        for block in sorted(self.block_data[file_name], key=lambda x: -x["block_start"]):
            block_start = block["block_start"] - 1
            block_end = block["block_end"] - 1

            # Validate indices
            if block_start < 0 or block_start >= len(lines):
                print(f"Skipping block {block['associated_file_label']} in {file_name}: start index {block_start + 1} out of bounds.")
                continue
            if block_end < 0 or block_end >= len(lines):
                print(f"Skipping block {block['associated_file_label']} in {file_name}: end index {block_end + 1} out of bounds.")
                continue

            # Insert IFFT annotations back
            if not lines[block_start].strip().startswith("#IFFT.If"):
                lines.insert(block_start, f"#IFFT.If({block['associated_file_label']})\n")
            if not lines[block_end].strip().startswith("#IFFT.Then"):
                lines.insert(block_end + 1, f"#IFFT.Then(\"{block['associated_file_label']}\")\n")

        with open(file_name, "w") as file:
            file.writelines(lines)

        print(f"Restored IFFT blocks to {file_name}.")


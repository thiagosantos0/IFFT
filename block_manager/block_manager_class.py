import json
import logging
from colorama import Fore, Style
import os

class BlockManager:
    def __init__(self, show_active_blocks, storage_file="ifft_blocks.json", mock_storage_file="mock_ifft_blocks.json"):
        self.storage_file = storage_file
        self.mock_storage_file = mock_storage_file
        self.show_active_blocks = show_active_blocks

        if self.show_active_blocks:
            # Checking if there is existing metadata
            if os.path.exists(self.storage_file):
                logging.info(f"{Fore.GREEN} Loading metadata from {self.storage_file}. {Style.RESET_ALL}")
                with open(self.storage_file, "r") as f:
                    self.block_data = json.load(f)

            else:
                print(f"{Fore.YELLOW} No metadata file found at {self.storage_file} or {self.storage_file} don't exists. {Style.RESET_ALL}")
                # Asking if user want to load mock metadata
                answer = input("Do you want to load mock metadata? (y/n): ")
                if answer.lower() == "y":
                    logging.warning(f"{Fore.YELLOW} Trying to load mock metadata from {self.mock_storage_file}. {Style.RESET_ALL}")
                    if os.path.exists(self.mock_storage_file):
                        with open(self.mock_storage_file, "r") as f:
                            self.block_data = json.load(f)
                    else:
                        logging.warning(f"{Fore.YELLOW} No mock metadata file found at {self.mock_storage_file}. {Style.RESET_ALL}")
                        logging.warning(f"{Fore.YELLOW} Exiting the program. {Style.RESET_ALL}")
                        exit()

                else:
                    print(f"{Fore.YELLOW} Exiting the program. {Style.RESET_ALL}")
                    exit()

        else:
            print(f"{Fore.YELLOW} Active blocks will not be shown. {Style.RESET_ALL}")
            self.block_data = {}


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

    #def remove_ifft_trace(self, file_name, blocks):
    #    """
    #    Remove only the IFFT comments from the code, keeping the block content intact.
    #    """
    #    with open(file_name, "r") as file:
    #        lines = file.readlines()

    #    for block in blocks:
    #        block_start = block.block_start - 1
    #        block_end = block.block_end - 1

    #        for i in range(block_start, block_end + 1):
    #            if lines[i].strip().startswith("#IFFT"):
    #                lines[i] = ""  # Remove the annotation

    #    with open(file_name, "w") as file:
    #        file.writelines(lines)

    #    print(f"Removed IFFT traces from {file_name}.")

    def remove_ifft_trace(self, file_name, blocks):
        """
        Remove only the IFFT comments from the code, keeping the block content intact.
        Adjusts the block_start and block_end indices to account for removed lines.
        """

        line_offset = 0
        for block in blocks:
            with open(block.file_path, "r") as file:
                lines = file.readlines()
                block_start = block.block_start - 1 - line_offset  # Adjust for previous removals
                block_end = block.block_end - 1 - line_offset

                # Remove opening IFFT comment
                if lines[block_start].strip().startswith("#IFFT.If"):
                    lines[block_start] = ""
                    line_offset += 1

                # Remove closing IFFT comment
                if lines[block_end].strip().startswith("#IFFT.Then"):
                    lines[block_end] = ""
                    line_offset += 1

                # Adjust the stored line numbers for this block
                block.block_start -= 1 if lines[block_start].strip() == "" else 0
                block.block_end -= 1 if lines[block_end].strip() == "" else 0

        with open(file_name, "w") as file:
            file.writelines(lines)

        # Save the updated block metadata
        self.save_metadata()

        print(f"Removed IFFT traces from {file_name}.")


    #def restore_ifft_blocks(self, file_name):
    #    """
    #    Restore IFFT annotations and metadata from the JSON file to the original code.
    #    """
    #    if file_name not in self.block_data:
    #        print(f"No stored blocks for {file_name}.")
    #        return

    #    with open(file_name, "r") as file:
    #        lines = file.readlines()

    #    # Get the total number of lines in the file
    #    total_lines = len(lines)

    #    # Restore each block in reverse order to avoid shifting lines
    #    for block in sorted(self.block_data[file_name], key=lambda x: -x["block_start"]):
    #        block_start = block["block_start"] - 1  # Convert to zero-based index
    #        block_end = block["block_end"] - 1

    #        # Validate indices
    #        if block_start < 0 or block_start >= total_lines or block_end < 0 or block_end >= total_lines:
    #            print(f"Warning: Block with start {block['block_start']} and end {block['block_end']} "
    #                  f"is out of bounds for {file_name}. Skipping...")
    #            continue

    #        block_content = block["block_content"].splitlines(keepends=True)

    #        # Insert IFFT annotations back
    #        if not lines[block_start].strip().startswith("#IFFT.If"):
    #            block_content.insert(0, f"#IFFT.If({block['block_label']})\n")
    #        if not lines[block_end].strip().startswith("#IFFT.Then"):
    #            block_content.append(f"#IFFT.Then(\"{block['block_label']}\")\n")

    #        lines = lines[:block_start] + block_content + lines[block_end + 1:]

    #    # Write the updated file
    #    with open(file_name, "w") as file:
    #        file.writelines(lines)

    #    print(f"Restored IFFT blocks to {file_name}.")

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


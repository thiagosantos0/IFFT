'''
    This class will be used to represent a IFFT block object will all required data.

    Improved Code Readability:

'''

class IFFTBlock:
    def __init__(self, file_path, block_content, associated_file_name, associated_file_label, block_start, block_end, modified_lines):
        self.file_path = file_path
        self.block_content = block_content
        self.associated_file_name = associated_file_name
        self.associated_file_label = associated_file_label
        self.block_start = block_start
        self.block_end = block_end
        self.modified_lines = modified_lines

    def __repr__(self):
        return (f"IFFTBlock(file_path={self.file_path}, block_start={self.block_start}, block_end={self.block_end}, "
                f"associated_file_name={self.associated_file_name}, associated_file_label={self.associated_file_label})")


# ifft_core/iftt_parser.py

from git import Repo, InvalidGitRepositoryError, NoSuchPathError
import os
import logging
from colorama import Fore, Style
from dotenv import load_dotenv

file_dir = os.path.dirname(__file__)
dir_path_mock_project = os.path.join(file_dir, '..', 'mock_project')

load_dotenv()
log_level = os.getenv("LOG_LEVEL")
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')


def validate_associated_file(associated_file_name: str) -> bool:
    """
        Validate if the associated file specified in IFFT block exists.

        Example:
            >>>validate_associated_file("foo_file.py")
            True

            >>>validate_associated_file("foo_file2.py")
            False

        Args:
            associated_file_name (String): A string corresponding to the file beeing
                verified.

        Returns:
            bool: A boolean that indicate whether the specified file is valid or not.
    """

    project_path = os.path.join(dir_path_mock_project)
    associated_file_name = associated_file_name.replace('"', '')
    file_path = os.path.join(project_path, associated_file_name)
    if not os.path.isfile(file_path):
        logging.error(f"{Fore.RED} Associated file: {associated_file_name} not found {Style.RESET_ALL}")
        logging.error(f"{Fore.RED} Associated file path: {file_path} {Style.RESET_ALL}")
        return False
    logging.info(f"{Fore.YELLOW} Associated file: {associated_file_name} found {Style.RESET_ALL}")
    return True

def get_modified_lines(repo: str, filename: str) -> set:
    """
        Get a set of modified lines for the given filename.

        Example:
            >>>file1.py:\n
                + line1\n
                + line2\n
                + line3

            >>>get_modified_lines(repo, file1.py)\n
            {'line1', 'line2', 'line3'}

        Args:
            repo (str): A string corresponding to the repository.
            filename (str): A string corresponding to the filename.

        Returns:
            set: A set of modified lines.

    """
    modified_lines = set()
    diff_text = repo.git.diff(None, filename)
    for line in diff_text.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            modified_lines.add(line[1:].strip())
    print(f"{Fore.GREEN} Modified lines: {modified_lines} {Style.RESET_ALL}")
    return modified_lines

def scan_file(project_path: str, filename: str, modified_lines_set: set) -> list:
    """
        Scan the file for IFFT blocks and return the results.

        Example:
            >>>file1.py:\n
                #IFFT.If\n
                    + line1\n
                    + line2\n
                    + line3
                #IFFT.Then("foo_file.py", "foo_label")
                
            >>>scan_file(project_path, file1.py, {'line1', 'line2', 'line3'})\n
                [{'block_content': '...',
                  'associated_file_name': 'foo_file.py',
                  'associated_file_label': 'foo_label',
                  'modified_lines_within_block': {'line1', 'line2', 'line3'}}]

        Args:
            project_path (str): A string corresponding to the project path.
            filename (str): A string corresponding to the filename.
            modified_lines_set (set): A set of modified lines.

        Returns:
            list: A list of results.

    """

    results = []
    in_block = False
    block_content = ""
    associated_file = ""
    block_start = 0
    block_end = 0
    modified_lines_within_blocks = []

    logging.debug(f"{Fore.GREEN} Scanning file: {filename} {Style.RESET_ALL}")
    file_path = os.path.join(project_path, filename)
    logging.debug(f"{Fore.GREEN} File path: {file_path} {Style.RESET_ALL}")

    lines = open(file_path).readlines()

    for line_number, line in enumerate(lines):
        if line.strip().startswith("#IFFT.If"):
            logging.debug(f"{Fore.GREEN} Entering IFFT block {line} {Style.RESET_ALL}")
            in_block = True
            block_start = line_number
            block_content += line
        elif line.strip().startswith("#IFFT.Then"):
            logging.info(f"{Fore.YELLOW} Exiting IFFT block {line} + {Style.RESET_ALL}")
            associated_file = line.strip().split('(')[1].split(')')[0]
            associated_file_name = associated_file.split(',')[0]
            associated_file_label = associated_file.split(',')[1].strip()
            valid_associated_file = validate_associated_file(associated_file_name)
            if not valid_associated_file:
                associated_file_name = ""
                associated_file_label = ""
            logging.info(f"{Fore.YELLOW} Associated file name: {associated_file_name} {Style.RESET_ALL}")
            logging.info(f"{Fore.YELLOW} Associated file label: {associated_file_label} {Style.RESET_ALL}")
            block_end = line_number

            results.append({
                "block_content": block_content,
                "associated_file_name": associated_file_name,
                "associated_file_label": associated_file_label,
                "modified_lines_within_block": modified_lines_within_blocks
            })

            logging.info(f"{Fore.YELLOW} Block content: \n{block_content} {Style.RESET_ALL}")
            logging.info(f"{Fore.YELLOW} Block end found at line: {block_end} {Style.RESET_ALL}")
            in_block = False
            block_content = ""
            modified_lines_within_blocks = []
        elif in_block:
            block_content += line
            if line.strip() in modified_lines_set:
                modified_lines_within_blocks.append(line.strip())

    return results

def scan_files(project_path: str = dir_path_mock_project) -> dict:
    """
        Scan the repository for modified Python files and return the results in a dictionary.
        
        Example:
            >>>file1.py:\n
                #IFFT.If\n
                    + line1\n
                    + line2\n
                    + line3
                #IFFT.Then("foo_file.py", "foo_label")
            >>>file2.py:\n
                #IFFT.If\n
                    + line4\n
                    + line5\n
                    + line6
                #IFFT.Then("foo_file2.py", "foo_label2")

            >>>scan_files(project_path)\n
                {'file1.py': [{'block_content': '...',
                               'associated_file_name': 'foo_file.py',
                               'associated_file_label': 'foo_label',
                               'modified_lines_within_block': {'line1', 'line2', 'line3'}}]
                    'file2.py': [{'block_content': '...',
                                'associated_file_name': 'foo_file2.py',
                               'associated_file_label': 'foo_label2',
                               'modified_lines_within_block': {'line4', 'line5', 'line6'}}]}
        
        Args:
            project_path (str): A string corresponding to the project path.

        Returns:
            dict: A dictionary of results.

    """

    results_dict = {}
    try:
        repo = Repo(project_path)
    except NoSuchPathError:
        logging.error(f"{Fore.RED} The path '{project_path}' does not exist. {Style.RESET_ALL}")
        return results_dict
    except InvalidGitRepositoryError:
        logging.error(f"{Fore.RED} The path '{project_path}' is not a valid Git repository. {Style.RESET_ALL}")
        return results_dict
    except Exception as e:
        logging.error(f"{Fore.RED} Failed to load repository: {e} {Style.RESET_ALL}")
        return results_dict

    unstaged_files = [item.a_path for item in repo.index.diff(None)]

    for filename in unstaged_files:
        if filename.endswith(".py"):
            modified_lines_set = get_modified_lines(repo, filename)
            results_dict[filename] = scan_file(project_path, filename, modified_lines_set)

    return results_dict


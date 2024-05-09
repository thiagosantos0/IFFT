from git import Repo
from dotenv import load_dotenv
import os
import logging
from colorama import Fore, Back, Style

file_dir = os.path.dirname(__file__)
dir_path_mock_project = os.path.join(file_dir, '..', './mock_project/')

load_dotenv()
log_level = os.getenv("LOG_LEVEL")
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')


def validate_associated_file(associated_file_name):
    '''
        Validate the associated file name and label.
    '''
    # starting from the root of the project
    project_path = os.path.join(dir_path_mock_project)
    associated_file_name = associated_file_name.replace('"', '')
    file_path = os.path.join(project_path, associated_file_name)
    if not os.path.isfile(file_path):
        logging.error(f"{Fore.RED} Associated file: {associated_file_name} not found {Style.RESET_ALL}")
        logging.error(f"{Fore.RED} Associated file path: {file_path} {Style.RESET_ALL}")
        return False
    logging.info(f"{Fore.YELLOW} Associated file: {associated_file_name} found {Style.RESET_ALL}")

    return True

def analyze_repo(project_path=dir_path_mock_project):
    '''
        Analyse the git repository and perform a scan for IFFT blocks on 
        staged and unstaged files.
    '''
    project_path = project_path 
    print(f"{Fore.BLUE} Project path: {project_path} {Style.RESET_ALL}")
    logging.info(f"{Fore.YELLOW} Checking staged and unstaged changes in: {project_path} {Style.RESET_ALL}")
    

    try:
        repo = Repo(project_path)

    except Exception as error:
        logging.error(f"{Fore.RED} Failed to load repository: {error} {Style.RESET_ALL}")
        return []

    staged_files = [item.a_path for item in repo.index.diff("HEAD")]
    #logging.info("Staged files: {}".format(' '.join(map(str, staged_files))))
    logging.info(Fore.YELLOW+ "Staged files: {}".format(' '.join(map(str, staged_files))) + Style.RESET_ALL)
    if not staged_files:
        logging.debug(f"{Fore.GREEN} No staged files found {Style.RESET_ALL}")

    unstaged_files = [item.a_path for item in repo.index.diff(None)]
    logging.info(Fore.YELLOW + "Unstaged files: {}".format(' '.join(map(str, unstaged_files))) + Style.RESET_ALL)
    if not unstaged_files:
        logging.debug(f"{Fore.GREEN} No unstaged files found {Style.RESET_ALL}")

    results = scan_files(project_path)

    return results


def scan_file(project_path, filename):
    '''
        Scan through a file and find out the content inside the IFTTs blocks.
    '''
    results = []
    in_block = False
    block_content = ""
    associated_file = ""
    block_start = 0
    block_end = 0

    logging.debug(f"{Fore.GREEN} Scanning file: {filename} {Style.RESET_ALL}")
    file_path = project_path + filename
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
            print(f"{Fore.BLUE} Associated file: {associated_file} {Style.RESET_ALL}")
            associated_file_name = associated_file.split(',')[0]
            print(f"{Fore.BLUE} Associated filename: {associated_file_name} {Style.RESET_ALL}")
            associated_file_label = associated_file.split(',')[1].strip()
            # Check if the associated file exists
            valid_associated_file = validate_associated_file(associated_file_name)
            if not valid_associated_file:
                associated_file_name = ""
                associated_file_label = ""
            logging.info(f"{Fore.YELLOW} Associated file name: {associated_file_name} {Style.RESET_ALL}")
            logging.info(f"{Fore.YELLOW} Associated file label: {associated_file_label} {Style.RESET_ALL}")
            block_end = line_number
            results.append((block_content, associated_file_name, associated_file_label))
            logging.info(f"{Fore.YELLOW} Block content: \n{block_content} {Style.RESET_ALL}")
            logging.info(f"{Fore.YELLOW} Block end found at line: {block_end} {Style.RESET_ALL}")
            in_block = False
            block_content = ""

        elif in_block:
            block_content += line

    return results

def scan_files(project_path=dir_path_mock_project):
    '''
        Scan through the files of a repository and find out the content inside the IFTTs blocks.
    '''
    project_path = project_path


    results_dict = {}

    # scanning_files
    for filename in os.listdir(project_path):
        if filename.endswith(".py"):
            results_dict[filename] = scan_file(project_path, filename)


    print(f"Results dict: {results_dict}")
    # Returning the results of the first IFFT block found in the file
    return results_dict 

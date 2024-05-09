from git import Repo
from dotenv import load_dotenv
import os
import logging

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
        logging.error(f"Associated file: {associated_file_name} not found")
        logging.info(f"Associated file path: {file_path}")
        return False
    logging.info(f"Associated file: {associated_file_name} found")

    return True

def analyze_repo(project_path=dir_path_mock_project):
    '''
        Analyse the git repository and perform a scan for IFFT blocks on 
        staged and unstaged files.
    '''
    project_path = project_path 
    print(f"Project path: {project_path}")
    logging.info("Checking staged and unstaged changes in: {}".format(project_path))
    

    try:
        repo = Repo(project_path)

    except Exception as error:
        logging.error("Failed to load repository: ", error)
        return []

    staged_files = [item.a_path for item in repo.index.diff("HEAD")]
    logging.info("Staged files: {}".format(' '.join(map(str, staged_files))))
    if not staged_files:
        logging.debug("No staged files found")

    unstaged_files = [item.a_path for item in repo.index.diff(None)]
    logging.info("Unstaged files: {}".format(' '.join(map(str, unstaged_files))))
    if not unstaged_files:
        logging.debug("No unstaged files found")

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

    logging.debug("Scanning file: " + filename)
    file_path = project_path + filename
    logging.debug("File path: " + file_path)
    lines = open(file_path).readlines()


    for line_number, line in enumerate(lines):
        if line.strip().startswith("#IFFT.If"):
            logging.debug("Entering IFFT block" + line)
            in_block = True
            block_start = line_number
            block_content += line

        elif line.strip().startswith("#IFFT.Then"):
            logging.info("Exiting IFFT block" + line)
            associated_file = line.strip().split('(')[1].split(')')[0]
            print(f"Associated file: {associated_file}")
            associated_file_name = associated_file.split(',')[0]
            print(f"Associated filename: {associated_file_name}")
            associated_file_label = associated_file.split(',')[1].strip()
            # Check if the associated file exists
            valid_associated_file = validate_associated_file(associated_file_name)
            if not valid_associated_file:
                associated_file_name = ""
                associated_file_label = ""
            logging.info(f"Associated file name: {associated_file_name}")
            logging.info(f"Associated file label: {associated_file_label}")
            block_end = line_number
            results.append((block_content, associated_file_name, associated_file_label))
            logging.info(f"Block content: \n{block_content}")
            logging.info("Block end found at line: {}".format(block_end))
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

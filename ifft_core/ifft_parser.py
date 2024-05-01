from git import Repo
import os
import logging

file_dir = os.path.dirname(__file__)
dir_path_mock_project = os.path.join(file_dir, '..', './mock_project/')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')


def analyze_repo(project_path=''):
    '''
        Analyse the git repository and perform a scan for IFFT blocks on 
        staged and unstaged files.
    '''
    project_path = dir_path_mock_project

    print("Checking staged and unstaged changes in: ", str(project_path))

    try:
        repo = Repo(project_path)

    except Exception as error:
        logging.error("Failed to load repository: ", error)
        return []

    staged_files = [item.a_path for item in repo.index.diff("HEAD")]
    print("Staged files: ", str(staged_files))
    if not staged_files:
        logging.debug("No staged files found")

    unstaged_files = [item.a_path for item in repo.index.diff(None)]
    print("Unstaged files: ", str(unstaged_files))
    if not unstaged_files:
        logging.debug("No unstaged files found")

    results = scan_files(project_path)

    return results


def scan_files(project_path=''):
    '''
        Scan through the files of a repository and find out the content inside the IFTTs blocks.
    '''
    project_path = dir_path_mock_project
    in_block = False
    block_content = ""


    results = []

    # scanning_files
    for filename in os.listdir(project_path):
        if filename.endswith(".py"):
            logging.debug("Scanning file: " + filename)
            file_path = project_path + filename
            lines = open(file_path).readlines()
        

            for line in lines:
                if line.strip().startswith("#IFFT.If"):
                    logging.debug("Entering IFFT block" + line)
                    in_block = True
                    block_content += line
        
                elif line.strip().startswith("#IFFT.Then"):
                    logging.debug("Exiting IFFT block" + line)
                    in_block = False

                    # TO-DO: Add logic to wrap-up the block content process after
                    # it comes out of the block.
                    pass

                elif in_block:
                    block_content += line
    
    #return results
    return block_content

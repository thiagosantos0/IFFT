from git import Repo
import os
import logging

file_dir = os.path.dirname(__file__)
dir_path_mock_project = os.path.join(file_dir, '..', './mock_project/')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

def scan_file(project_path='', file_path=''):
    '''
        Scan through the file and find out the content inside the IFTT block.
    '''
    project_path = dir_path_mock_project
    file_path = dir_path_mock_project + "app.py"

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
        
                elif line.strip().startswith("#IFFT.Then"):
                    logging.debug("Exiting IFFT block" + line)
    

    return results


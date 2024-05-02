from dotenv import load_dotenv
import os
import sys
import pytest
load_dotenv()

project_path = os.getenv('PYTHONPATH')
if project_path not in sys.path:
    sys.path.append(project_path)

file_dir = os.path.dirname(__file__)
dir_path_mock_project = os.path.join(file_dir, '..', 'mock_project/')

from ifft_core.ifft_parser import scan_files

def test_content_parse_ifft():
    filepath = dir_path_mock_project
    results_dict = scan_files(filepath)
    # Getting one of the files in the projmock_project as example
    assert results_dict['file1.py'][0][0] == "#IFFT.If This is a test comment\n\nprint('Hello world!')\n\n"

def test_filepath_parse_ifft():
    filepath = dir_path_mock_project
    results_dict = scan_files(filepath)
    assert results_dict['file1.py'][0][1] == "path_to_associated_file"

def test_filelabel_parse_ifft():
    filepath = dir_path_mock_project
    results_dict = scan_files(filepath)
    assert results_dict['file1.py'][0][2] == "associated_file_ifft_label"

def test_scan_repositoty_files():
    repo_path = dir_path_mock_project
    results_dict = scan_files(repo_path)
    files_identified = list(results_dict.keys())

    files = os.listdir(repo_path)
    python_files = [file for file in files if file.endswith('.py')]
    
    assert set(python_files) == set(files_identified)




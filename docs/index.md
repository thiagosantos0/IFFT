# IFFT 

IFFT is a Python linter to help you handle correlated changes across your codebase.

<!--- Adding a image of the tool banner -->


## Commands

* `python3 ifft.py` - Run IFFT tool in manual mode.

## Project structure 
```
  ├── banner.py
  ├── docs
  ├── block_metadata 
  ├── helpers 
  │   ├── ...
  ├── IFFT_WEB 
  │   ├── ...
  ├── ifft_core
  │   ├── ifft_parser.py # File with tool helper methods
  │   └── __init__.py
  ├── ifft_block 
  │   ├── ifft_block_class.py
  │   └── __init__.py
  ├── ifft_block_manager
  │   ├── block_manager_class.py
  │   └── __init__.py
  ├── ifft.py # Main file that triggers the tool
  ├── mkdocs.yml
  ├── mock_project # Mock project to test the tool
  ├── README.md
  ├── requirements.txt
  ├── site # Documentation
  ├── surfaces
  │   └── library
  │       └── filler_file
  └── tests
      ├── filler_file
      └── test_ifft_core.py
```

## Reccomended project structure

```
  ── IFFT 
      ├── ifft_core 
          └── ... 
      ├── ... 
      ├── ifft.py
      └── your_project 
```


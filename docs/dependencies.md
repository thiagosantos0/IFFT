# Installing Project Dependencies
To set up the project environment, follow these steps:

## Step 1: Create a Virtual Environment (Optional but Recommended)
It is recommended to create a virtual environment to keep project dependencies isolated.

Run the following command to create and activate a virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Linux/MacOS)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate
```

## Step 2: Install Dependencies
Use the `requirements.txt` file to install all necessary packages:

```bash
# Installing dependencies 
pip3 install -r requirements.txt
```

## Step 3: Verify Installation
Check if all dependencies were installed correctly:

```bash
# Checking 
pip3 check 
```

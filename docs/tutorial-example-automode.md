This section of documentaion consists in step-by-step example of the code usage **in mock project** using *automode*.
The idea here is to give a glimpse of how the tool can be used in a real project.

Here is the following `mock project` structure:

```
../mock_project/
├── app.py
├── file1.py
└── README.md
```
The content of the files are as follows:

#### **app.py**
```python
import os

file_dir = os.path.dirname(__file__)


#IFFT.If(foo1 block)
def foo1(number1: int, number2: int) -> int:
    # Adding a change for testing purposes
    return number1 + number2

# Adding a change for testing purposes

def foo5(number1: int, number2: int) -> int:
    return number1 ** number2

def foo6(number1: int, number2: int) -> int:
    return number1 % number2

def foo7(number1: int, number2: int) -> int:
    return number1 // number2

#IFFT.Then("file1.py", "foo1_related_block")

def foo2(number1: int, number2: int) -> int:
    return number1 - number2

def foo3(number1: int, number2: int) -> int:
    return number1 * number2

def foo4(number1: int, number2: int) -> int:
    return number1 / number2

def foo8(number1: int, number2: int) -> int:
    return 2*number1 + number2

# main

print(foo1(1, 2))
print(foo2(1, 2))
print(foo3(1, 2))

```


#### **file1.py**
```python
#IFFT.If This is a test comment

print('Hello world!')

#IFFT.Then (path_to_associated_file, associated_file_ifft_label)
```


### **Step 0**: pre-commit configuration 
In order to use IFFT in *automode* all you have to do is create a pre-commit file for your project. You can find a pre-filled template that should cover the great majority of the use cases:

```bash
#!/bin/bash

# This is a pre-commit template configuration that can be used for any project with
# just minor changes

PROJECT_DIR=$(pwd)

# Path to the IFFT script 
IFFT_SCRIPT_PATH="../ifft.py"

# Checking for Python files in staging area
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

# If we don't have any staged files, the program can end
if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# Now going to the project directory
cd "$PROJECT_DIR"

# Running IFFT script with auto_mode flag and getting the output
OUTPUT=$(python3 "$IFFT_SCRIPT_PATH" --auto 2>&1)
IFFT_EXIT_CODE=$?

# Show the output
echo "$OUTPUT"

# Check IFFT output
# If auto_mode is beeing used and a change is identified inside a IFFT block
# the program will ask (before commit - this is the reason why this bash script
# is for pre-commit hook) if he wants to continue with te commit or abort.
if [ $IFFT_EXIT_CODE -ne 0 ]; then
    echo "IFFT check detected changes in the blocks."

    read -p "Changes detected in IFFT blocks. Do you want to continue with the commit? (y/n): " CONTINUE_COMMIT < /dev/tty

    if [[ "$CONTINUE_COMMIT" != "y" && "$CONTINUE_COMMIT" != "Y" ]]; then
        echo "Commit aborted."
        exit 1
    fi
fi

# Succesfull execution
exit 0

```

If you project structure is following the recommended pattern (can be found documentation main page), all you have to fill out is the path to ifft script and it's all setup.

<!--- Sections with use cases -->

### **Step 1**: Checking if the "auto-mode" is enabled
*You can run the following command on your terminal or alternatively, you can open it in any
text editor.*

```bash
$ cat ifft_config.json
```
You should see something like this:
![image1](https://i.postimg.cc/sgJv0z51/ifft-confi.png)

This is where IFFT configuration can be changed, as this tutorial aims to show how *automode*
works I will switch it to *true*.

### **Step 2**: Triggering the tool
The main idea of *automode* is to run IFFT automatically. More especifically just before the 
creation of a commit. In *automode* IFFT will run every time a new commit is created and will
give you one of the two outputs:
  - A message saying that none change was found inside a IFFT block.
    - Commit is made normally.
  
  - A message saying that changes were found inside IFFT blocks and asking you
    if you want to continue with the commit anyways or to abort:
    - If you take (y) as option (anything different of (n or N) actually) the commit action
      will happen normally.

Thats the process in summary. Now, follow the practical examples:


### **Step 1**: Making a change outside a IFFT block:
We'll add a new function inside the `app.py` file, outside any IFFT block. The new function is as follows:
```python
import os
file_dir = os.path.dirname(__file__)

#IFFT.If(foo1 block)

...

#IFFT.Then("file1.py", "foo1_related_block")

...

def outsideFunction() -> None:
    print("This is a new function added outside of any IFFT block!")

# main

...
```

After the change addition, we have the following as the output for *git status* command:
```bash
$ git status 
```
![image2](https://i.postimg.cc/2yfYDbDY/git-status.png)


As mentioned before, we need to proceed to do a commit in order to have the tool automatically
triggered, this is done as follow:

```bash
$ git add app.py
$ git commit -m "Commit message"
```
As soon as we run the commit command, we should have the feature triggering automatically and,
in this case, we should have something like this:
![image3](https://i.postimg.cc/9F6djc4p/git-commit.png)

Note that the change cannot be found in the debug output, since it is not inside an IFFT block.
For this reason the program just show a empty list of modified lines inside IFFT block and says
that *"No changes detected in IFFT blocks"*. 

**Note 1**: *You can ignore this .env file for this example.*
**Note 2**: *Please note that the commit is done normally in this case.*

### **Step 2**: Making a change inside a IFFT block:
Now, we'll add a new function inside the `app.py` file, inside the `foo1` IFFT block. The new function is as follows:

Just a reminder before we proceed. In this stage, we have already commited the first change (outside one) so it will not appear in the diff for this section.

![image4](https://i.postimg.cc/fL1cTs2D/git-diff.png)

```python
import os
file_dir = os.path.dirname(__file__)

#IFFT.If(foo1 block)

...

def insideFunction() -> None:
    print("This is a new function added inside of an IFFT block!")

#IFFT.Then("file1.py", "foo1_related_block")

...

```

Again, doing the same process of the last example (git add followed by git commit command)
we have the following:

![image5](https://i.postimg.cc/tJtsQG8r/ifft-output.png)

Note that now the tool detected the change and now recommends the developer to take a look at the associated file `file1.py` (more specefically in `foo1_related_block`) to see if any changes are needed.

Not only that, now the tool also asks the developer if he wants to go on with his commit or abort
the commit. If it's the case where the developer didn't know that those two files are related or
forgot about it, normally he will at least check if everything is ok, so he'll probably abort it
at first. After take a look in the code and change what is necessary or he came to an conclusion
that a change is not necessary, he can go on with the commit.

<!--- Ending the tutorial section -->

### **Final message**
This is the end of the tutorial. The tool can be used in a real project to help developers to keep track of the changes and to make sure that the changes are propagated to the associated files. This tutorial isn't a exact one but it should be enough to give a glimpse of how the tool can be used in a real project.

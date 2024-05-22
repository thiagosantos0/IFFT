This section of documentaion consists in step-by-step example of the code usage **in mock project**.
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



<!--- Sections with use cases -->

### **Step 1**: Running the tool before any changes:
```bash
$ python3 ifft.py "path/to/project"
```

As expected, we should not see any output, since the project is not changed yet. The following image
illustrates this cases:

![step1_image](https://i.postimg.cc/KvN4B8z0/Captura-de-tela-de-2024-05-21-19-42-59.png)

**Note**: *The default project is the "mock_project", so the [dir_name] parameter was not passed.*

### **Step 2**: Making a change outside a IFFT block:
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

Given that the code was added outside the IFFT block, again, the tool should not output anything, as shown in the image below:

![step2_image](https://i.postimg.cc/8ccYbVrJ/Captura-de-tela-de-2024-05-21-21-00-12.png)


Note that the change cannot be found in the debug output, since it is not inside an IFFT block.

**Note 1**: *The program executed in debug mode. In the release version, these messages won't appear.*

**Note 2**: *Even though a function was added as a change for this tutorial, any code could be added instead.*

### **Step 3**: Making a change inside a IFFT block:
Now, we'll add a new function inside the `app.py` file, inside the `foo1` IFFT block. The new function is as follows:

Just a reminder before we proceed. For this example, I already have submmited the code added in the previous step.
As you can see in this 'diff' below, after the commit, we have only the new change:

![step3,1_image](https://i.postimg.cc/52QSS2KW/Captura-de-tela-de-2024-05-21-21-07-25.png)

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

After the change, we should see the following output (actually, a similar one given that this is the debug mode):

![step3,2_image](https://i.postimg.cc/ZKprWMWJ/Captura-de-tela-de-2024-05-21-21-11-38.png)

Note that now the tool detected the change and now recommends the developer to take a look at the associated file `file1.py` (more specefically in `foo1_related_block`) to see if any changes are needed.


<!--- Ending the tutorial section -->

### **Final message**
This is the end of the tutorial. The tool can be used in a real project to help developers to keep track of the changes and to make sure that the changes are propagated to the associated files. This tutorial isn't a exact one but it should be enough to give a glimpse of how the tool can be used in a real project.

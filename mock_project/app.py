import os

file_dir = os.path.dirname(__file__)


#IFFT.If(foo1 block)
def foo1(number1: int, number2: int) -> int:
    # Adding a change for testing purposes
    return number1 + number2

# Adding a change for testing purposes

#IFFT.Then("file1.py", "foo1_related_block")

def foo2(number1: int, number2: int) -> int:
    return number1 - number2




# main

print(foo1(1, 2))
print(foo2(1, 2))

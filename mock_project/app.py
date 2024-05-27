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

def outsideFunction() -> None:
    print("This is a new function added outside of any IFFT block!")

# main

print(foo1(1, 2))
print(foo2(1, 2))
print(foo3(1, 2))

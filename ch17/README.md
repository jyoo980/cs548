# Exercise 17.2

> Print out information. Change the example program so that it prints out the following information in the beginning of each function:
>    My name is <function name>
>       my locals are <k1=v1, k2=v2, k3=v3, ...>
>       and I’m being called from  <name of
>       caller function>
>Additional constraint: these messages should be printed as the result of a call to a function named print_info() with no arguments.

This exercise required me to leverage Python's incredibly detailed introspection techniques. I inspected the value of the
call stack in the `print_info()` method to gain access to what the caller of the function is, in addition to the local
variables of the caller and the caller of the caller (call stack 2-levels deep).

```Python
def print_info():
    # who called this method (print_info)
    caller_name = inspect.stack()[1][3]
    # local variables of the caller of this method
    caller_locals = inspect.stack()[1].frame.f_locals
    # name of the caller who called the method who called this method
    # e.g. foo() calls bar() calls print_info() -> print 'foo''
    caller_of_caller_name = inspect.stack()[2][3]
    print(f"My name is: {caller_name}")
    print(f"    my locals are: {caller_locals}")
    print(f"    and I am being called from: {caller_of_caller_name}")
```
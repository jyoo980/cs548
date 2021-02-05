# Exercise 14.3

> Type checks. Use the decorator presented in this chapter in order to check the types of parameters passed to certain constructors and methods. Feel free to refactor the original example program in order to make type checking more meaningful. Turn in two versions of your new program, one that type checks and one that fails type checking.

The initial decorator was given as below:

```python
class TypeCheck():

    def __init__(self, *args):
        self._args = args

    def __call__(self, f):
        def wrapped_fn(*args):
            for i in range(len(self._args)):
                if self._args[i] == "primitive" and type(args[i + 1]) in (str, int, float, bool):
                    continue
                if not isinstance(args[i + 1], globals()[self._args[i]]):
                    raise TypeError("Wrong type")
            f(*args)
        return wrapped_fn
```

While this decorator provided broad typechecking, it did not enable the developer to provide fine-grained type information.
For example, if a method took in values `str, bool, float, int`, the decorator took in the string "primitive". This meant
that a methods incorrectly called with primitive values, e.g. a method called with `int` when it is supoosed to be called 
with `float`, would still pass typechecking. 

I augmented the decorator by enabling a finer grained level of type checking, where methods called with primitive types would
be subject to actual typechecking, i.e. if you decorate a method with an `int` type check, it better fail if I call it with
`bool`.

```python
# Type checker added for exercise 14.3
class TypeCheck():

    def __init__(self, *args):
        self._args = args
        self._primitives = (str, int, float, bool)

    def __call__(self, f):
        def wrapped_fn(*args):
            for i in range(len(self._args)):
                # if it is a primitive value, check whether it belongs to the array we have
                # Note, it's args[i + 1] since the first element is always 'self'. 
                # Nice going, Python
                expected_type_str = self._args[i]
                actual_type_str = type(args[i + 1]).__name__
                if type(args[i + 1]) in self._primitives and actual_type_str == expected_type_str:
                    continue
                if type(args[i + 1]).__name__ != expected_type_str:
                    raise TypeError(f"Expected type: {expected_type_str}, found actual type: {actual_type_str}")
                # if it's not a primitive, check whether it's of some type we defined
                if not isinstance(args[i + 1], globals()[self._args[i]]):
                    raise TypeError("Wrong type")
            f(*args)
        return wrapped_fn
```
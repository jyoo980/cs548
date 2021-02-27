# Exercise 24.2

> Return. The AcceptTypes decorator of the example program works only for the input arguments of functions. Write another decorator called ReturnTypes that does a similar thing for the return value(s) of functions.

This is a way to add _some_ semblance of typechecking to the return values of Python methods. Like argument typechecking,
this was achieved by creating a decorator (`@AcceptTypes`) that intercepts a method call to assert that the correct
type is being returned. The implementation is below:

```Python
class ReturnTypes():

    def __init__(self, *args):
        self._args = args

    def __call__(self, f):
        def wrapped_f(*args):
            expected_ret_type = self._args[0].__name__
            actual_ret_type = self._actual_ret_type(f, args[0])
            if expected_ret_type != actual_ret_type:
                err_message = f"Expected type: {expected_ret_type}, but got: {actual_ret_type}"
                raise TypeError(err_message)
            return f(*args) 
        return wrapped_f
    
    def _actual_ret_type(self, fn, arg):
        ret_val = fn(arg)
        actual_ret_type = type(ret_val).__name__
        return actual_ret_type
```
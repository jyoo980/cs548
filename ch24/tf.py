#!/usr/bin/env python
import sys, re, operator, string, inspect

#
# Decorating for encorcing types of return values from method calls
#
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

#
# Decorator for enforcing types of arguments in method calls
#
class AcceptTypes():
    def __init__(self, *args):
        self._args = args

    def __call__(self, f):
        def wrapped_f(*args):
            for i in range(len(self._args)):
                if type(args[i]) != self._args[i]:
                    raise TypeError("Expecting %s got %s" % (str(self._args[i]), str(type(args[i]))))
            return f(*args)
        return wrapped_f
#
# The functions
#
@AcceptTypes(str)
@ReturnTypes(list)
def extract_words(path_to_file):
    with open(path_to_file) as f:
        str_data = f.read()
    pattern = re.compile(r'[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

@AcceptTypes(list)
@ReturnTypes(dict)
def frequencies(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

@AcceptTypes(dict)
@ReturnTypes(list)
def sort(word_freq):
    return sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)

word_freqs = sort(frequencies(extract_words(sys.argv[1])))
for (w, c) in word_freqs[0:25]:
    print(w, '-', c)

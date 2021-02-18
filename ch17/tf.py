#!/usr/bin/env python
import sys, re, operator, string, inspect


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

def read_stop_words():
    """ This function can only be called from a function 
        named extract_words."""
    # Meta-level data: inspect.stack()
    print_info()
    if inspect.stack()[1][3] != 'extract_words':
        return None

    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return stop_words

def extract_words(path_to_file):
    # Meta-level data: locals()
    print_info()
    with open(locals()['path_to_file']) as f:
        str_data = f.read()
    pattern = re.compile(r'[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    stop_words = read_stop_words()
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    # Meta-level data: locals()
    print_info()
    word_freqs = {}
    for w in locals()['word_list']:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freq):
    # Meta-level data: locals()
    # print_info()
    return sorted(locals()['word_freq'].items(), key=operator.itemgetter(1), reverse=True)

def main():
    word_freqs = sort(frequencies(extract_words(sys.argv[1])))
    for (w, c) in word_freqs[0:25]:
        print(w, '-', c)

if __name__ == "__main__":
    main()

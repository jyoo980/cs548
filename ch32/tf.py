#!/usr/bin/env python
import sys, re, operator, string
from functools import reduce
#
# Functions for map reduce
#
def partition(data_str, nlines):
    """
    Partitions the input data_str (a big string)
    into chunks of nlines.
    """
    lines = data_str.split('\n')
    for i in range(0, len(lines), nlines):
        yield '\n'.join(lines[i:i+nlines])

def split_words(data_str):
    """
    Takes a string, returns a list of pairs (word, 1),
    one for each word in the input, so
    [(w1, 1), (w2, 1), ..., (wn, 1)]
    """
    def _scan(str_data):
        pattern = re.compile('[\W_]+')
        return pattern.sub(' ', str_data).lower().split()

    def _remove_stop_words(word_list):
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]

    # The actual work of the mapper
    result = []
    words = _remove_stop_words(_scan(data_str))
    for w in words:
        result.append((w, 1))
    return result

# At worst, this is linear time. I could make this O(1)
# by hashing each letter to its range, but I'm not really
# down to make a hashmap with 26 key-value pairs.
def find_key_of(word):
    letters = list(string.ascii_lowercase)
    first_char = word[0]
    key = ""
    if first_char in letters[0:5]:
        key = "a-e"
    elif first_char in letters[5:10]:
        key = "f-j"
    elif first_char in letters[10:15]:
        key = "k-o"
    elif first_char in letters[15:20]:
        key = "p-t"
    else:
        key = "u-z"
    return key

def regroup(pairs_list):
    """
    Takes a list of lists of pairs of the form
    [[(w1, 1), (w2, 1), ..., (wn, 1)],
     [(w1, 1), (w2, 1), ..., (wn, 1)],
     ...]
    and returns a dictionary mapping each unique word to the
    corresponding list of pairs, so
    { a-e: [(w1, 1), (w1, 1)...],
      f-j: [(w2, 1), (w2, 1)...],
      ...}
    """
    mapping = {}
    for pair in pairs_list:
        for p in pair:
            word = p[0]
            key = find_key_of(word)
            if key in mapping:
                mapping[key].append(p)
            else:
                mapping[key] = [p]
    return mapping

def count_words(target, mappings):
    counts = sum([freq for word, freq in mappings if word == target])
    return (target, counts)

def map_over_bucket(mapping):
    # given the second part of "a-e": [ (w1, 1), (w2, 2) ... ]
    unique_words = { w for w, _ in mapping }
    return [count_words(word, mapping) for word in unique_words]

#
# Auxiliary functions
#
def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data

def sort(word_freq):
    return sorted(word_freq, key=operator.itemgetter(1), reverse=True)

#
# The main function
#
splits = map(split_words, partition(read_file(sys.argv[1]), 200))
splits_per_word = regroup(splits)

buckets = splits_per_word.items()
counted_buckets = []
for _, words in buckets:
    counted_buckets.extend(map_over_bucket(words))

word_freqs = sort(counted_buckets)

for (w, c) in word_freqs[0:25]:
    print(w, '-', c)

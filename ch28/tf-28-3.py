#!/usr/bin/env python
import sys, operator, string

def line_iterator(filename):
    lines = [line for line in open(filename)]
    return iter(lines)

def all_words_iterator(filename):
    line_iter = line_iterator(filename)
    words = []
    at_end = False
    while not at_end:
        line = next(line_iter, None)
        if line is not None:
            words.extend(line.split(" "))
        else:
            at_end = True
    return iter([w for w in words if w.isalnum()])

def non_stop_words_iter(filename):
    stopwords = set(open('../stop_words.txt').read().split(',')  + list(string.ascii_lowercase))
    word_iter = all_words_iterator(filename)
    valid_words = []
    at_end = False
    while not at_end:
        word = next(word_iter, None)
        if word is not None and word not in stopwords:
            valid_words.append(word)
        elif word is None:
            at_end = True
    return iter(valid_words)

def count_and_sort_iter(filename):
    freqs, i = {}, 1
    words_iter = non_stop_words_iter(filename)
    at_end = False
    while not at_end:
        word = next(words_iter, None)
        if word is not None:
            freqs[word] = freqs.get(word, 0) + 1
            if i % 5000 == 0:
                sorted_entries = sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
                return iter(sorted_entries)
            i = i + 1
        else:
            at_end = True
    sorted_entries = sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
    return iter(sorted_entries)

#
# The main function
#
word_freq_iter = count_and_sort_iter(sys.argv[1])
for _ in range(0, 26):
    (w, c) = next(word_freq_iter)
    print(f"{w}-{c}")
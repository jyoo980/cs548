#!/usr/bin/env python
import sys, operator, string

def lines(filename):
    for line in open(filename):
        yield line

def all_words(filename):
    words = []
    for line in lines(filename):
        whitespace_filtered = [w for w in line.split(' ') if w.isalnum()]
        words.extend(whitespace_filtered)
    for word in words:
        yield word

def non_stop_words(filename):
    stopwords = set(open('../stop_words.txt').read().split(',')  + list(string.ascii_lowercase))
    for w in all_words(filename):
        if not w in stopwords:
            yield w

def count_and_sort(filename):
    freqs, i = {}, 1
    for w in non_stop_words(filename):
        freqs[w] = 1 if w not in freqs else freqs[w]+1
        if i % 5000 == 0:
            yield sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
        i = i+1
    yield sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
#
# The main function
#
for word_freqs in count_and_sort(sys.argv[1]):
    print("-----------------------------")
    for (w, c) in word_freqs[0:25]:
        print(w, '-', c)

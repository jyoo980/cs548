#!/usr/bin/env python
import sys, re, operator, string, os

#
# Two down-to-earth things
#
stops = set(open("../stop_words.txt").read().split(",") + list(string.ascii_lowercase))

def frequencies_imp(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

#
# Extract Python code from a given file, plug it into our implementation
# 
def extract_word_impl(path):
    f = open(path)
    content = ''.join(f.readlines())
    f.close()
    return content

#
# Let's write our functions as strings.
#
if len(sys.argv) > 1:
    implementation_file = sys.argv[2]
    extract_words_func = extract_word_impl(implementation_file)
    frequencies_func = "lambda wl : frequencies_imp(wl)"
    sort_func = "lambda word_freq: sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)"
    filename = sys.argv[1]
else:
    extract_words_func = "lambda x: []"
    frequencies_func = "lambda x: []"
    sort_func = "lambda x: []"
    filename = os.path.basename(__file__)
#
# So far, this program isn't much about term-frequency. It's about
# a bunch of strings that look like functions.
# Let's add our functions to the "base" program, dynamically.
#
exec('extract_words = ' + extract_words_func)
exec('frequencies = ' + frequencies_func)
exec('sort = ' + sort_func)

#
# The main function. This would work just fine:
#  word_freqs = sort(frequencies(extract_words(filename)))
#
word_freqs = locals()['sort'](locals()['frequencies'](locals()['extract_words'](filename)))

for (w, c) in word_freqs[0:25]:
    print(w, '-', c)


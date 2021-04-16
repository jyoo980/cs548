#!/usr/bin/env python
import re, sys, operator, queue, threading, string

# Two data spaces
word_space = queue.Queue()
freq_space = queue.Queue()

stopwords = set(open('../stop_words.txt').read().split(','))

# Worker function that consumes words from the word space
# and sends partial results to the frequency space
def process_words():
    word_freqs = {}
    while True:
        try:
            word = word_space.get(timeout=1)
        except queue.Empty:
            break
        if not word in stopwords:
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1
    freq_space.put(word_freqs)

# Let's have this thread populate the word space
for word in re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower()):
    word_space.put(word)

# Let's create the workers and launch them at their jobs
workers = []
for i in range(5):
    workers.append(threading.Thread(target = process_words))
[t.start() for t in workers]

# Let's wait for the workers to finish
[t.join() for t in workers]


# Data spaces for the alphabet
a_e_space = queue.Queue()
f_j_space = queue.Queue()
k_o_space = queue.Queue()
p_t_space = queue.Queue()
u_z_space = queue.Queue()

word_freqs = {}
def process_freqs():
    freqs = freq_space.get()
    for k, v in freqs.items():
        if k in word_freqs:
            count = sum(item[k] for item in [freqs, word_freqs])
        else:
            count = freqs[k]
        word_freqs[k] = count
        put_in_space(k, count)

def put_in_space(word, count):
    space_to_put = find_key_of(word)
    to_put = [word, count]
    if space_to_put == "a-e":
        a_e_space.put(to_put)
    elif space_to_put == "f-j":
        f_j_space.put(to_put)
    elif space_to_put == "k-o":
        k_o_space.put(to_put)
    elif space_to_put == "p-t":
        p_t_space.put(to_put)
    else:
        u_z_space.put(to_put)


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

# Collect frequencies in parallel
workers = []
for _ in range(5):
    workers.append(threading.Thread(target = process_freqs))
[t.start() for t in workers]

[t.join() for t in workers]

collected_freqs = {}
def collect_freqs(space):
    while not space.empty():
        (word, freq) = space.get()
        collected_freqs[word] = freq

spaces = [a_e_space, f_j_space, k_o_space, p_t_space, u_z_space]
for space in spaces:
    collect_freqs(space)

for (w, c) in sorted(collected_freqs.items(), key=operator.itemgetter(1), reverse=True)[:25]:
    print(w, '-', c)


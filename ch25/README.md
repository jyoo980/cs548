# Exercise 25.4

> _True to the style_. The goal of this style is to coerce programmers into isolating their IO code from the rest. Two of the three IO- infected functions in the example program, namely extract words and remove stop words, end up doing more than just IO. Refactor the program so that it does a better job at separating IO code from the rest.

This exercise challenges the programmer to enforce a stronger separation of concerns between "effectful" IO code (e.g. 
reading a file), and and pure code that has no side-effects. The difficulty of this was mainly working with Python's `.bind`
function, which only enables each function to consume one argument. This meant that if I wanted to pass through more than one
"piece" of data, I had to construct a tuple containing them.

The first thing I did was to extract the file IO from `extract_words` to a dedicated `read_file` function. This made
`extract_words` effectively pure.

```Python
# IO function added to read file, given a path
def read_file(path):
    f = open(path, "r")
    return f.read()

def extract_words(data):
    pattern = re.compile(r'[\W_]+')
    word_list = pattern.sub(' ', data).lower().split()
    return word_list
```

I then added `read_file` to the function composition pipeline:

```Python
TFQuarantine(get_input)\
.bind(read_file)\
.bind(extract_words)\
.bind(read_stop_words)\
# ...
```

A similar pattern was followed in the other method that had file IO, `remove_stop_words`:

```Python
# Newly added IO-function
def read_stop_words(word_list):
    f = open('../stop_words.txt', 'r')
    stop_words = f.read().split(',')
    return [word_list, stop_words]

def remove_stop_words(word_list_stop_words):
    word_list, stop_words = (word_list_stop_words[0], word_list_stop_words[1])
    # add single-letter words
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]
```
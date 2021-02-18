# Exercise 18.2

> From a file. Modify the example program so that the implementation of extract words is given by a file. Provide at least two alternative implementations of that function (i.e. two files) that make the program work correctly. 

The main focus of this exercise was to exploit reflection and metaprogramming to dynamically assign an implementation
to a Python function at runtime. This was achieved by writing the _body_ of a function to an external file, which was then
read via the function below:

```Python
def extract_word_impl(path):
    f = open(path)
    content = ''.join(f.readlines())
    f.close()
    return content
```

The files which contained the file were called `ext1.py` and `ext2.py` respectively, and are shown below:

```Python
# Contents of ext1.py
lambda name : [x.lower() for x in re.split('[^a-zA-Z]+', open(name).read()) if len(x) > 0 and x.lower() not in stops]
```

```Python
# Contents of ext2.py
lambda name : [x.lower() for x in read_and_split_file(name) if is_valid_word(x)]

def read_and_split_file(name):
    return re.split('[^a-zA-Z]+', open(name).read())

def is_valid_word(x):
    return len(x) > 0 and x.lower() not in stops
```

The content of the files above were then saved to a local variable in the code, like so:

```Python
if len(sys.argv) > 1:
    implementation_file = sys.argv[2]
    extract_words_func = extract_word_impl(implementation_file)
    # other implementation
```
# Exercise 28.2

> Lines vs. characters. The example program, in its eagerness to demonstrate data flows of all kinds, ends up doing something monolithic – the function all words (yuk!). It would be much better to use Python’s facilities to handle words (e.g. split). Change the program, without changing the style, so that the first generator yields an entire line, and the second yields words from those lines using the proper library functions.

In this exercise, I needed to rewrite two methods: `characters` and `all_words`. The rewrite of `characters` was significant enough
to warrant a rename to `lines`, since we now wanted this method to yield all _lines_ of the text file as opposed to each character.
The implementation of this method is below:

```python
def lines(filename):
    for line in open(filename):
        yield line
```

The `all_words` method was immediately downstream from this. It was previously implemented with the assumption that it would be working
with each individual character of the file. Rewriting `all_words` yielded (ha) a program that was easier to understand:

```python
def all_words(filename):
    words = []
    for line in lines(filename):
        whitespace_filtered = [w for w in line.split(' ') if w.isalnum()]
        words.extend(whitespace_filtered)
    for word in words:
        yield word
```

The most interesting part of this method is likely the list-comprehension:

```python
[w for w in line.split(' ') if w.isalnum()]
```

This line of code basically takes each line, tokenizes it based on the space character `' '`, and filters out any token that is not
an alphanumeric character. The equivalent in lisp would be:

```clojure
(filter is-alphanumeric? (string-split line " "))
```
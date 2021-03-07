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
# Exercise 28.3

>  Iterators. Some languages that don’t support generators support their more verbose cousins, iterators (e.g. Java). Python supports both. Change the example program so that it uses iterators instead of gener- ators.

This exercise was a matter of refactoring the example program such that all the methods that `yield`-ed some value now returned an iterator.
In the end, this led to code that was much more difficult compose. It turns out that Python's standard `Iterator` implementation does not
have a `hasNext()`-like construct. It instead throws an exception because that's obviously more ergonomic. All levity aside, I actually don't
understand the design rationale behind this. That said, Python does let you define a optional value that's returned when an iterator is empty
that you can check for instead of throwing an exception, but then this begs the question of why there isn't a simple `has_next()` method in the
first place.

Below is an example of a iterator-based method I wrote for this exercise:

```python
def all_words_iterator(filename):
    line_iter = line_iterator(filename)
    words = []
    # This variable basically acts as a hand-rolled has_next()
    at_end = False
    while not at_end:
        line = next(line_iter, None)
        if line is not None:
            words.extend(line.split(" "))
        else:
            at_end = True
    return iter([w for w in words if w.isalnum()])
```
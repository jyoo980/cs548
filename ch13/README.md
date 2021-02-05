# Exercise 13.2

>  Add method. Delete the last three lines of the example program, and replace the printing of the information with the following. Add a new method to the word freqs obj called top25 which sorts its freqs data and prints the top 25 entries. Then call that method. Constraint: The program cannot be changed at all until line #46 – your additions should come after that line.

The idea here was to leverage Python's first-class function capabilities to encapsulate the lines of code that performed
sorting + printing into a function, and set the key in the `word_freqs_obj` to the function pointer. The solution is below

```python
# defining our method 
def top25():
    for w, c in word_freqs_obj["sorted"]()[0:25]:
        print(f"{w}-{c}")

# adding a method to our object prototype
word_freqs_obj["top25"] = lambda: top25()

# calling our method
word_freqs_obj["top25"]()
```
# Exercise 30.2

Taking a suggestion from the book, I first identified the "data spaces"
in which the threads execute, shown below

```python
# Data spaces for the alphabet
a_e_space = queue.Queue()
f_j_space = queue.Queue()
k_o_space = queue.Queue()
p_t_space = queue.Queue()
u_z_space = queue.Queue()
```

Next was definining a method that each thread could execute in parallel
without running into resource contention issues. This was already taken 
care of in the creation of data spaces, so all I needed to do was write
a function that each thread could execute with the illusion that it was
the only thread operating on it

```python
def process_freqs():
    freqs = freq_space.get()
    for k, v in freqs.items():
        if k in word_freqs:
            count = sum(item[k] for item in [freqs, word_freqs])
        else:
            count = freqs[k]
        word_freqs[k] = count
        put_in_space(k, count)
```

Next we created our threads, and fired them off to work

```python
# Collect frequencies in parallel
workers = []
for _ in range(5):
    workers.append(threading.Thread(target = process_freqs))
[t.start() for t in workers]

[t.join() for t in workers]
```

The final step was to collect results from all the data spaces

```python
spaces = [a_e_space, f_j_space, k_o_space, p_t_space, u_z_space]
for space in spaces:
    collect_freqs(space)
```

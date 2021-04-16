lambda xs: show_frequency(xs)

def show_frequency(xs):
    freq = {}
    for x in xs:
        freq[x] = freq.get(x, 0) + 1
    sorted_freq = sort_freqs(freq)
    display(sorted_freq)
    
def sort_freqs(frequency_map):
    elements = frequency_map.items()
    sorted(elements, key=lambda x: x[1])
    return elements

def display(freqs):
    for k, v in freqs:
        print(f"{k} - {v}")


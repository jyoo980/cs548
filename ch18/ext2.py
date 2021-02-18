lambda name : [x.lower() for x in read_and_split_file(name) if is_valid_word(x)]

def read_and_split_file(name):
    return re.split('[^a-zA-Z]+', open(name).read())

def is_valid_word(x):
    return len(x) > 0 and x.lower() not in stops

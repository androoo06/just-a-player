import math

### file io stuff ###
def open_file(file, method):
    f = None
    try:
        f = open(file, method)
    except:
        print("Problem opening file", file)
        return None
    return f

def read_file_as_list(file):
    f = open_file(file, "r")
    if (f):
        list = f.read().splitlines()
        f.close()
        return list

def write_list_to_file(list, file):
    f = open_file(file, "w")
    if (f):
        for element in list:
            if (element != "") and (element != None):
                f.write(element+"\n")
        f.close()

### other general fns ###
def try_number(s):
    try:
        float(s)
        return round(float(s), 2)
    except ValueError:
        return s

def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n

def get_num_spaces(num):
    # for spacing the numbers in 'display_playlist' (update_song_display()) in main.py
    
    n = int(num)
    if (n == 0):
        return 0
    
    return int(math.log10(n))
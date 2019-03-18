import random
import string
from arctic import Arctic
def random_name(name_length):
    return ''.join([random.choice(string.ascii_letters) for n in range(name_length)])

def random_library(arctic_db):
    lib_name = random_name(6)
    while lib_name in arctic_db.list_libraries():
        lib_name = random_name(6)
    return lib_name





import random
import string
from itertools import permutations

#USERNAME_PREFIX= '0000'
USERNAME_PREFIX = '000053'
USERNAME_LENGTH = 10
CHARSET = string.octdigits


def generate_username(prefix=USERNAME_PREFIX,
                      length=USERNAME_LENGTH):
    """This generator structure lets us combine the timing attack with a
    best-effort brute force search. This gets us the best of both
    worlds...
    """
    suffix_length = length - len(prefix)
    perms_iterable = list(CHARSET * suffix_length)
    # this shuffle is not numerically necessary assuming a truly random
    # username, but it makes people feel more comfortable with the
    # approach.
    random.shuffle(perms_iterable)
    perms_iterable = ''.join(perms_iterable)
    # keep going even after we've done all the combinations, in case
    # of other failure elsewhere in the program
    while True:  
        for suffix in permutations(perms_iterable, suffix_length):
            yield prefix + ''.join(suffix)


def charset():
    """ returns the charset in a random order """
    return random.sample(CHARSET, len(CHARSET))

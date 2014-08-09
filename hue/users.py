import random
import string
from itertools import permutations

USERNAME_PREFIX = '0000'
#USERNAME_PREFIX = '00004367'
USERNAME_LENGTH = 10
CHARSET = string.octdigits


def generate_username(prefix=USERNAME_PREFIX,
                      length=USERNAME_LENGTH):
    """This generator structure lets us combine the timing attack with a
    best-effort brute force search. This gets us the best of both
    worlds...
    """
    suffix_length = length - len(prefix)
    perms_iterable = list('0' + CHARSET + '7') # don't ask
    # this shuffle is not numerically necessary assuming a truly random
    # username, but it makes people feel more comfortable with the
    # approach.
    random.shuffle(perms_iterable)
    perms_iterable = ''.join(perms_iterable)

    # keep going even after we've done all the combinations, in case
    # of other failure elsewhere in the program
    count = 0
    while True:
        for suffix in permutations(perms_iterable, suffix_length):
            yield prefix + ''.join(suffix)


def charset():
    """ returns the charset in a random order """
    return random.sample(CHARSET, len(CHARSET))

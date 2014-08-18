import random
import string
from itertools import product

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
    # this shuffle is not numerically necessary assuming a truly random
    # username, but it makes people feel more comfortable with the
    # approach.
    product_input = [charset() for x in range(suffix_length)]

    # keep going even after we've done all the combinations, in case
    # of other failure elsewhere
    count = 0
    while True:
        for suffix in product(*product_input):
            yield prefix + ''.join(suffix)


def charset():
    """ returns the charset in a random order """
    return random.sample(CHARSET, len(CHARSET))

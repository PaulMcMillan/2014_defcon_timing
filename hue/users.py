import random
import string

USERNAME_PREFIX= '000'
USERNAME_LENGTH = 10
CHARSET = string.octdigits


def generate_username(prefix=USERNAME_PREFIX,
                      length=USERNAME_LENGTH):
    return prefix + ''.join(
        [random.choice(CHARSET) for x in range(length - len(prefix))])


def charset():
    """ returns the charset in a random order """
    return random.sample(CHARSET, len(CHARSET))

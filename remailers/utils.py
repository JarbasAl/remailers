import string
import random


# TODO os.urandom
def generate_iv(key_lenght=8):
    """Generate a random string of letters and digits """
    valid_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(valid_chars) for i in range(key_lenght)).encode("utf-8")


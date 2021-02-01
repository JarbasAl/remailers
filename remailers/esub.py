try:
    # pycryptodomex
    from Cryptodome.Cipher import Blowfish
except ImportError:
    # pycrypto + pycryptodome
    from Crypto.Cipher import Blowfish

from hashlib import md5
from remailers.utils import generate_iv


def create_esub(text, key, iv=None):
    """Produce a 192bit Encrypted Subject. The first 64 bits are the
    Initialization vector used in the Blowfish CFB Mode.  The Subject text
    is MD5 hashed and then encrypted using an MD5 hash of the Key."""
    texthash = md5(text.encode("utf-8")).digest()
    keyhash = md5(key.encode("utf-8")).digest()
    if iv is None:
        iv = generate_iv(8)
    crypt1 = Blowfish.new(keyhash,
                          Blowfish.MODE_OFB, iv).encrypt(texthash)[:8]
    crypt2 = Blowfish.new(keyhash,
                          Blowfish.MODE_OFB, crypt1).encrypt(texthash[8:])
    return (iv + crypt1 + crypt2).hex()


def match_esub(text, key, esub):
    """Extract the IV from a passed eSub and generate another based on it,
    using a passed Subject and Key.  If the resulting eSub collides with
    the supplied one, return True."""
    # All eSubs should be 48 bytes long
    if len(esub) != 48:
        return False
    # The 64bit IV is hex encoded (16 digits) at the start of the esub.
    try:
        iv = bytes.fromhex(esub[:16])
    except TypeError:
        return False
    return create_esub(text, key, iv) == esub


if __name__ == "__main__":
    key = "key"
    subject = "text"
    # new IV for each esub
    esubs = [create_esub(subject, key) for i in range(10)]
    for sub in esubs:
        print(sub, match_esub(subject, key, sub))

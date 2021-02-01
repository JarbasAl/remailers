from hashlib import sha256
from remailers.utils import generate_iv


def create_hsub(text, iv=None, hsublen=48):
    """Create an hSub (Hashed Subject). This is constructed as:
    --------------------------------------
    | 64bit iv | 256bit SHA2 'iv + text' |
    --------------------------------------"""
    # Generate a 64bit random IV if none is provided.
    if iv is None:
        iv = generate_iv()
    if isinstance(iv, str):
        iv = iv
    hashed = sha256(iv + text.encode("utf-8")).digest()
    # Concatenate our IV with a SHA256 hash of text + IV.
    hsub = iv + hashed
    return hsub.hex()[:hsublen]


def match_hsub(hsub, subject):
    """Create an hSub using a known iv, (stripped from a passed hSub).  If
    the supplied and generated hSub's collide, the message is probably for
    us."""
    # We are prepared to check variable length hsubs within boundaries.
    # The low bound is the current Type-I esub length.  The high bound
    # is the 256 bits within SHA2-256.
    hsublen = len(hsub)
    # 48 digits = 192 bit hsub, the smallest we allow.
    # 80 digits = 320 bit hsub, the full length of SHA256 + 64 bit IV
    if hsublen < 48 or hsublen > 80:
        return False
    iv = iv_from_hsub(hsub)
    if not iv:
        return False
    # Return True if our generated hSub collides with the supplied
    # sample.
    return create_hsub(subject, iv, hsublen) == hsub


def iv_from_hsub(hsub, digits=16):
    """Return the decoded IV from an hsub.  By default the IV is the first
    64bits of the hsub.  As it's hex encoded, this equates to 16 digits."""
    # We don't want to process IVs of inadequate length.
    if len(hsub) < digits:
        return False
    try:
        return bytes.fromhex(hsub[:digits])
    except:
        # Not all Subjects are hSub'd
        return False


if __name__ == "__main__":
    subject = "captain dolphin"
    print("Subject: " + subject)
    print("Should return True:  %s" % match_hsub(create_hsub(subject),
                                                 subject))
    print("Should return False: %s" % match_hsub(create_hsub("subject"),
                                                 subject))

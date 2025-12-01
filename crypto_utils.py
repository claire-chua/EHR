from Crypto.Random import get_random_bytes
import os
from dotenv import load_dotenv
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode
from Crypto.Cipher import AES

#contains functions that encrypts and decrypts the data with AES-256 CFB, as well as the inital function used to generate a key (that has been commented out)

load_dotenv()

#generate a 256 bit key in base64 format
#key = get_random_bytes(32)
#print(b64encode(key).decode())

key_base64 = os.environ["AES_SECRET_KEY"]

#load base64-encoded AES key from .env and return 32-bytes key
def load_key():
    key = b64decode(key_base64)
    if len(key) != 32:
        raise RuntimeError("Key must have been generated and decoded to 32 bytes")
    return key

#encrypt string using AES-256 CFB, which returns base64 string with IV + ciphertext
def encrypt_text(plaintext: str):
    
    key = load_key()
    #convert plaintext to bytes object
    data = plaintext.encode('utf-8')

    #create cipher
    cipher = AES.new(key, AES.MODE_CFB)
    ciphertext= cipher.encrypt(data)

    #combine iv and ciphertext
    combined = cipher.iv + ciphertext

    #encode to base64
    return b64encode(combined).decode("utf-8")

#decrypt a base64 string
def decrypt_text(cipher_b64: str):

    key = load_key()

    raw = b64decode(cipher_b64)

    #Extract IV to 
    iv = raw[:16]
    #Extract cipher text
    ciphertext = raw[16:]

    #recreate cipher with iv
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    plaintext_bytes = cipher.decrypt(ciphertext)

    return plaintext_bytes.decode("utf-8")
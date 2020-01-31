#!/usr/bin/python3


import os
import sys
import random
# pip install pycryptodome
from Crypto.Cipher import AES
from hashlib import sha256

__all__ = ["encrypt", "decrypt", "getconfig"]

__configpath = None

if sys.platform == "win32":
    filename = "config.encrypted"
    dir = os.path.realpath(os.path.dirname(__file__))
    __configpath = os.path.join(dir, filename)
elif sys.platform == "linux":
    __configpath = "/etc/DnsPod/config.encrypted"


def getconfig():
    return __configpath


def _randomstr(length):
    string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    pad = ""
    for i in range(length):
        pad += random.choice(string)
    return pad



def encrypt(msg, key):
    if len(key) < 16:
        padlen = 16 - len(key)
        key += key[:padlen]
    elif len(key) > 16:
        key = key[0:16]
    cipher = AES.new(key.encode("utf-8"), AES.MODE_GCM)
    mac = sha256((key + sha256(msg.encode("utf-8")).hexdigest()).encode("utf-8")).hexdigest()
    mac = mac.encode("utf-8")
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode("utf-8"))
    nonce = cipher.nonce
    data = b''
    for value in (ciphertext, tag, nonce, mac):
        data += len(value).to_bytes(2, byteorder="big")
        data += value
    return data


def decrypt(data, key):
    if len(key) < 16:
        padlen = 16 - len(key)
        key += key[:padlen]
    elif len(key) > 16:
        key = key[0:16]
    index = 0
    d = []
    for i in range(4):
        length = int.from_bytes(data[index:index+2], byteorder="big")
        index += 2
        d.append(data[index:index+length])
        index += length
    ciphertext = d[0]
    tag = d[1]
    nonce = d[2]
    mac = d[3].decode("utf-8")
    cipher = AES.new(key.encode("utf-8"), AES.MODE_GCM, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        return False
    curr_mac = sha256((key + sha256(plaintext).hexdigest()).encode("utf-8")).hexdigest()
    if mac != curr_mac:
        return False
    return plaintext.decode("utf-8")


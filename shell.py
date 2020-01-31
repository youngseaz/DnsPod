#!/usr/bin/python3

import os
import sys
import logging
from getpass import getpass
from crypto import encrypt, decrypt, getconfig


__all__ = ["check_py_version", "gettoken", "savetoken"]


def check_py_version():
    info = sys.version_info
    if info.major != 3 and info.micro < 5:
        logging.critical("Check your Python version please, Python 3.5+ is required.")
        sys.exit(1)


def file_accessable(path):
    if os.path.exists(path):
        if os.access(path, os.O_WRONLY):
            return True
    return False


def savetoken(login_token):
    def get():
        key = getpass("password is needed to encrypt token.\nyour password: ")
        confirm = getpass("confirm password:")
        if key != confirm:
            print("tow passwords are abhorrent.")
            return False
        else:
            if len(key) < 8:
                print("password too short.")
                return False
            return key

    def write(file, key):
        data = encrypt(login_token, key)
        try:
            f = open(file, "wb+")
        except Exception:
            logging.info("Fail to save login token to the file.")
            return
        f.write(data)
        f.close()
        logging.info("save login token to the file successfully.")

    file = getconfig()
    if file_accessable(file):
        count = 0
        while True:
            count += 1
            cmd = input("configure file exist, cover it?(yes/no)")
            if cmd.lower() in ("yes", ""):
                while True:
                    key = get()
                    if key:
                        write(file, key)
                        break
            elif cmd.lower() == "no":
                break
            elif count > 3:
                print("return after 3 times ")
                break
            else:
                print("invalid option, try again!")
    else:
        while True:
            key = get()
            if key:
                write(file, key)
                break


def gettoken():
    def save(token):
        count = 0
        while True:
            cmd = input("save login token to the file?(yes/no) ")
            if cmd.lower() in ["yes", ""]:
                savetoken(token)
                break
            elif cmd.lower() == "no":
                break
            elif count > 3:
                break
            else:
                print("invalid command.")

    def input_token():
        n = 0
        while True:
            n += 1
            try:
                if n > 3:
                    break
                id = getpass("your id: ")
                token = getpass("your token: ")
            except Exception:
                print("try again.")
                continue
            if len(id) < 3 or len(token) < 10:
                print("invalid id and token. id length less than 3 or token length less than 10.")
                sys.exit(1)
            login_token = id + "," + token
            return login_token

    file = getconfig()
    if file_accessable(file):
        key = getpass("Password is needed to activate program.\npassword: ")
        f = open(file, "rb")
        data = f.read()
        f.close()
        login_token = decrypt(data, key)
        if login_token:
            logging.info("activate program successfully.")
            return login_token
        else:
            login_token = input_token()
            save(login_token)
            return login_token
    else:
        login_token = input_token()
        save(login_token)
        return login_token



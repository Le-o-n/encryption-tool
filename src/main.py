import sys
import hashlib
import os 


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
KEY_HASH = b"_M\xcc;Z\xa7e\xd6\x1d\x83'\xde\xb8\x82\xcf\x99"
TARGET_PATH = dir_path + "/../target/"


def hash(string: str) -> str:
    return hashlib.md5(string.encode()).digest()


def main():
    '''
    Main entrypoint in program
    '''

    key = input("Key: ")
    option = input("(d)ecode or (e)ncode: ")
    
    print(hash(key))
    if (hash(key) == KEY_HASH):
        print("Correct key ")
    else:
        print("incorrect key")



if __name__ == "__main__":
    main()

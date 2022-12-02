import sys
import hashlib
import os 
from cryptography.fernet import Fernet
import base64


def read_file_bytes(path: str)-> bytes:
    b: bytes = b''
    
    with open(path, 'rb') as f:
        b = f.read()

    return b     

def generate_fernet_key(b: bytes):
    return convert_bytes_to_base64(b).ljust(32, b'P')

def convert_bytes_to_base64(b: bytes):
    return base64.b64encode(b) 

def collect_all_file_paths(dir_path: str)-> list:
    '''
    Overview:
        Collects all file paths for all files in the directory and all subdirectories
    Parameters:
        dir_path    (str)   =   path to directory being decryptd
    Returns:
        returns a list of all paths to files in directory and all subdirectories
    
    '''
    file_paths: list = []
    for path, subdirs, files in os.walk(dir_path):
        for name in files:
            
            file_paths.append(os.path.join(path, name))
    return file_paths

def input_validate(print_string: str, validInputs: list, validFunc = lambda x:x.decode("utf-8")) -> str:
    '''
    Overview:
        Gets user input until valid input recieved

    Parameters:
        print_string    (str)       =   string to be displayed as a prompt each time the user inputs a string
        validInputs     (list)      =   array of valid inputs the user can enter, user will be prompted until
                                        they enter one of these inputs
        validFunc       (function)  =   applying a function to the user input before comparing it with the valid
                                        input. By default this function is a mapping to itself
    Return:
        Returns the valid user input 
    '''
    userInput: str = ""
    while not validFunc(str.encode(userInput)) in validInputs:
        print(print_string, end="")
        userInput = input("")
    return userInput

def hash_md5(string: bytes) -> bytes:
    '''
    Overview:
        Hashes the string using MD5 and returns the binary
    Parameters:
        string      (str)   =   the string that will get hashed
    Returns:
        Returns hashed string as binary
    '''
    return hashlib.md5(string.decode("utf-8").encode("utf-8") ).digest()


def decrypt(en_path: str, key: bytes)-> bool:
    '''
    Overview:
        decrypts file at path using the key as the decrypt key.
    Parameters:
        path    (str)   =   path to file that will be decryptd
        key     (str)   =   key used for the decoding
    Returns:
        returns bool to show if the operation has been successfull   
    
    '''
    fernet_key = key
    fernet : Fernet = Fernet(fernet_key)
    en_path_split = en_path.split("/")
    dir, en_filename = "/".join(en_path_split[0:-1]), en_path_split[-1]
    if (en_filename.split(".")[-1] == ENCRYPTED_EX[1:].decode("utf-8")):
        filename = (fernet.decrypt(str.encode(en_filename))).decode("utf-8")
        path = f"{dir}/{filename}" 

        with open(en_path, 'rb') as file:
            en_data = file.read()
        
        data = fernet.decrypt(en_data)
        
        with open(path, 'wb') as file:
            file.write(data)

        os.remove(en_path)
        
        return True

def encrypt(path: str, key: bytes)-> bool:
    '''
    
    Overview:
        encrypts file at path using the key as the encoding key.
    Parameters:
        path    (str)   =   path to file that will be encryptd
        key     (str)   =   key used for the encoding
    Returns:
        returns bool to show if the operation has been successfull   
    
    '''
    fernet_key = key
    fernet : Fernet = Fernet(fernet_key)
    path_split = path.split("/")
    dir, filename = "/".join(path_split[0:-1]), path_split[-1]
    en_filename = (fernet.encrypt(str.encode(filename)) + ENCRYPTED_EX).decode("utf-8")
    en_path = f"{dir}/{en_filename}" 

    with open(path, 'rb') as file:
        data = file.read()
     
    en_data = fernet.encrypt(data)
    
    
    with open(en_path, 'wb') as en_file:
        en_file.write(en_data)

    os.remove(path)
    
    return True

    

def decrypt_files(file_paths: list, key: bytes) -> bool:
    '''
    Overview:
        decrypts all files within the dir_path directory including any sub directories
        using the key as the decoding key.
    Parameters:
        file_paths  (str)   =   paths to all files that will be decryptd
        key         (str)   =   key used for the decoding
    Returns:
        returns bool to show if the operation has been successfull   
    
    '''

    for path in file_paths:
        if (decrypt(path, key)):
            print(f"successfully decryptd {path}")
        else:
            print(f"error while decoding  {path}")




    return True

def encrypt_files(file_paths: list, key: bytes) -> bool:
    '''
    Overview:
        decrypts all files within the dir_path directory including any sub directories
        using the key as the decoding key.
    Parameters:
        file_paths  (str)   =   paths to all files that will be decryptd
        key         (str)   =   key used for the decoding
    Returns:
        returns bool to show if the operation has been successfull   
    
    '''

    for path in file_paths:
        if (encrypt(path, key)):
            print(f"successfully encryptd {path}")
        else:
            print(f"error while encoding  {path}")




    return True


DIR_PATH: str                   = os.path.dirname(os.path.realpath(__file__))
TARGET_PATH: str                = DIR_PATH + "/../target/"
FUNC_MAP: dict                  = {"e": encrypt_files, "d": decrypt_files}
ENCRYPTED_EX                    = b".encrypted"
ENCRYPTION_KEY                  = b"jpM6DUtu__ySm4CK78w79BLvspPOAWaWnZqtU-Vkcsg="
ENCRYPTION_KEY_HASH: bytes      = read_file_bytes(DIR_PATH + "/key_hash.txt")



def main():
    '''
    Main entrypoint in program
    '''
    option: str = input_validate(print_string = "(d)ecode or (e)ncode: ", 
                                validInputs  = ["d", "e"])

    key: bytes    = str.encode(input_validate(print_string = "Enter Key: ", 
                                validInputs  = [ENCRYPTION_KEY_HASH],
                                validFunc    = hash_md5))

    
    
    file_paths: list = collect_all_file_paths(TARGET_PATH)  

    options_func = FUNC_MAP[option]
    options_func(file_paths, key)
    
   



if __name__ == "__main__":
    main()

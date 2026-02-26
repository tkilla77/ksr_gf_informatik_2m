### requires: pip install pycryptodome
 
### DON'T CHANGE CODE FROM HERE ...
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
 
encoding = 'utf-8' # 'latin-1'
 
data_encrypted = [
    {
        "pw_hashed" : "4ae81572f06e1b88fd5ced7a1a000945432e83e1551e6f721ee9c00b8cc33260",
        "message_encrypted" : b'\xa5\x8a\xb6i\xfb\xe4\x1c\xeeN [\xcb\xb8\xe9\x85-'
    },
    {
        "pw_hashed" : "ccc09a134cf88bae7be3f6d62cf24b9476a044c375a76d53b78eef18ea772f5f",
        "message_encrypted" : b'\x98I\x10\xb3\xbaW\x03V\x9e\x96;\xb0\xb2#\xc7\x04AA\xf4S\xf9H\x10\xf6\x9c\x8e\xd3jf\xfa\x17\xa1\xba\xb5\xae\xc5\n\xc0\xd4\xc8\x02,U\x10\xc2\xd62\xbe\xa6!l\x82\x82Hs\xde\xb7\x97\xf6\x0c\xa6\x85\xf2\xd0'
    },
    {
        "pw_hashed" : "516a8d1c497179956af1feddc603960155d26aad82fa8c184dd27a14fc59da82",
        "message_encrypted" : b'\x89\xd55H\xb3\xab\x0b\x99\x19oW\x00\xfd\xc9*\xdc`\xb2\xb0N\xf7+m\xce\x8c\xf7\xd7k\xc5\x01\xec\xbf+f\x94\xd0\xb1\x04\xcd\xd2$Z\xf6\xdf\xee\xca\xa5V\xf6b\xce\n\x1f\xbc\x1c\xe4\x00zi\xe8:\xcb\x000'
    },
    {
        "pw_hashed" : "1f40dc75353dade02cab2a64cc014d058bc16b3eec3b52b723dc1db5cfdc7875",
        "message_encrypted" : b'\x0c\xe0hb%\xe9E\xdb\x97\x10I\x17\xc2\xdbH4\x03\xf3M\xb20_\xa3\x13\xbd\x87\xd5\xe0\xc8\xcb\xab+\x89\r\x938@2\x0b.{t\x1a3\x85u\x14\xd3'
    },
    {
        "pw_hashed" : "cb059e3e1d77a76665eaaeb7d289f54936ecb301a5ede2a0ac887c204b7bd4e4",
        "message_encrypted" : b'\x0fr\xbd~\x0b C\xd1\xdc\x83y\x0e\xf5Im\xf3U\x94\x7f\xd6\x8e\xde\xb6\xf5\x97\xf6\x06\x16\xd8o\xc4Q<F\x05:)\xe6\xf0\x1b\xb3\xe2b\xe0\xcf\xb4\x84Z\x11\x8f>\x12[k%\xcf\xb2\x14\xea)Zi/e\x1buX?\xc4\x0e\xf9\\\xf9\xa5\xfb\x1e5\xecPi\xe8\x89Ty63`4\x89\x87\x08\x9b\xccj\xcd1y/\xc5\xdc#\x1fS\xa8\xe99\x07\x85\xda\xf5:\xd5'
    }
]
 
def normalize_key(key):
    if len(key) < 16:
        key = key + (16-len(key)) * "a"
    elif len(key) < 64:
        key = key + (16-len(key)) * "a"
    else:
        key = key[:64]
    return key
 
def encrypt(key: str, message: str):
    key = normalize_key(key).encode(encoding)
    cipher = AES.new(key, AES.MODE_ECB)  # Using ECB mode
    padded_message = pad(message.encode(encoding), AES.block_size)  # Pad message
    encrypted_message = cipher.encrypt(padded_message)  # Encrypt the data
    return encrypted_message
 
def decrypt(key: str, message: bytes):
    key = normalize_key(key).encode(encoding)
    cipher = AES.new(key, AES.MODE_ECB)  # Using ECB mode
    decrypted_message = cipher.decrypt(message)
    decrypted_unpadded_message = unpad(decrypted_message, AES.block_size)
    return decrypted_unpadded_message.decode(encoding)  # Decode bytes to string
 
def hashme(s):
    return hashlib.sha256(s.encode(encoding)).hexdigest()
 
def check_pw(pw):
    pw = ''.join(pw)
    for data in data_encrypted:
        if hashme(pw) == data['pw_hashed']:
            return 201,decrypt(pw,data["message_encrypted"]),pw
    return None
 
### ... UNTIL HERE
##############################################
### WRITE YOUR CODE BELOW:
 
from multiprocessing import Pool
from tqdm.auto import tqdm
import time

def hack_password():
    import string, itertools
    
    alphabet = string.ascii_uppercase

    with Pool(processes=4) as pool:
        for l in range(4, 7):
            yield from (response for response in tqdm(pool.imap_unordered(check_pw, itertools.product(alphabet, repeat=l), chunksize=1000), total=len(alphabet)**l) if response)

def hack_password2():
    import string, itertools
    with open('woerter_top10000de_upper.txt') as f:
        words = [line.strip() for line in f]
        with Pool(processes=4) as pool:
            yield from (response for response in tqdm(pool.imap_unordered(check_pw, itertools.product(words, repeat=2), chunksize=1000), total=len(words)**2) if response)

if __name__ == '__main__':
    start = time.time()
    code, message, pw = next(hack_password2())
    elapsed = time.time() - start
    print(f"Code: {code}, Message: {message}, Password: {pw}, Elapsed: {elapsed:.1f}s")

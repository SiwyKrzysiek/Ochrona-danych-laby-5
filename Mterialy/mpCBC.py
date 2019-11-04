import multiprocessing
import time
import ctypes

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

def xor64(a, b):
    block = bytearray(a, 'utf-8')
    for j in range(8):
        block[j] = ord(a[j]) ^ b[j]
    return block

def encrypt_CBC_serial(key, plain_text, iv):
    vector = bytearray(plain_text, 'utf-8')
    des = DES.new(key)
    for i in range(no_blocks):
        offset = i*block_size
        block = plain_text[offset:offset+block_size]
        intermediate = bytes(xor64(block, iv))
        for j in range(1000):
           encrypted = des.encrypt(intermediate)
           intermediate = encrypted
        vector[offset:offset+block_size] = bytearray(encrypted)
        iv = encrypted
    return bytes(vector)        


plain_text = "alamakot"*1000
key = "haslo123"
iv = get_random_bytes(8)
block_size = 8
no_blocks = int(len(plain_text)/block_size)

starttime = time.time()
encryptedCBC = encrypt_CBC_serial(key, plain_text, iv)
print('CBC Encrypt time serial: ', (time.time() - starttime))
#print("Encrypted CBC: ", encryptedCBC)


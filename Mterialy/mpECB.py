import multiprocessing
import time
import ctypes

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

# Xor two bytearrays[8]
# Not used in ECB!
def xor64(a, b):
    block = bytearray(a, 'utf-8')
    for j in range(8):
        block[j] = ord(a[j]) ^ b[j]
    return block

def encrypt_ECB_serial(key, plain_text):
    vector = bytearray(plain_text, 'utf-8')
    des = DES.new(key)

    for i in range(no_blocks):
        # Select right block
        offset = i*block_size
        block = plain_text[offset:offset+block_size]

        # Why this is done 1000 times?
        for j in range(1000):
            encrypted = des.encrypt(block)
            block = encrypted
        vector[offset:offset+block_size] = bytearray(encrypted)
    return bytes(vector)       

def decrypt_ECB_serial(key, encrypted_block):
    vector = bytearray(encrypted_block)
    des = DES.new(key)
    for i in range(no_blocks):
        offset = i*block_size
        block = encrypted_block[offset:offset+block_size]
        for j in range(1000):
            decrypted = des.decrypt(block)
            block = decrypted
        vector[offset:offset+block_size] = bytearray(decrypted)
    return bytes(vector)       


plain_text = "alamakot"*1000
key = "haslo123"

# iv is not used in ECB!
iv = get_random_bytes(8)
block_size = 8
no_blocks = int(len(plain_text)/block_size)

starttime = time.time()
encryptedECB = encrypt_ECB_serial(key, plain_text)
print('ECB Encrypt time serial: ', (time.time() - starttime))

starttime = time.time()
decrypted = decrypt_ECB_serial(key, encryptedECB)
print('ECB Decrypt time serial: ', (time.time() - starttime))

def mapper(i):
    offset = i*block_size
    block = bytes(shared_data[offset:offset+block_size])
    for j in range(1000):
        decrypted = des.decrypt(block)
        block = decrypted
    output_data[offset:offset+block_size] = bytearray(decrypted)
    return i

des = DES.new(key)
shared_data = multiprocessing.RawArray(ctypes.c_ubyte, encryptedECB)
output_data = multiprocessing.RawArray(ctypes.c_ubyte, encryptedECB)
pool = multiprocessing.Pool(4)
starttime = time.time()
pool.map(mapper, range(no_blocks))
print('ECB Decrypt time parallel: ', (time.time() - starttime))
decrypted = bytes(output_data)

    
    

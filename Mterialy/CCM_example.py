#pip3 install pycryptodomex

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


def encrypt_CCM(data, key, nonce):
	cipher = AES.new(key, AES.MODE_CCM, nonce)
	ciphertext = cipher.encrypt(data)
	tag = cipher.digest()
	return ciphertext, tag

def decrypt_CCM(ciphertext,key,nonce,tag):
	cipher = AES.new(key, AES.MODE_CCM, nonce)

	plaintext = cipher.decrypt(ciphertext)

	try:
		cipher.verify(tag)
	except ValueError:
		return False

	return plaintext


message = b'\xe1~\x8a\xd1\x96\x84\xc38v\xc7\x8e\x04\x1f\x12\x96p#\xaa\x11t\x17\x9b\x93(/\x7fg\xfa\x9b.\xdd\xe3\x02\xef<\xca\xe7\xac'

key = get_random_bytes(16)
nonce = get_random_bytes(11)
ciphertext,tag = encrypt_CCM(message,key,nonce)


corrupted_nonce = get_random_bytes(11)

#odszyfrowanie z błędną "solą""
decrypted = decrypt_CCM(ciphertext,key,corrupted_nonce,tag)

#odszyfrowanie poprawne
#decrypted = decrypt_CCM(ciphertext,key,nonce,tag)

if decrypted: 
	print("Odszyfrowano! Twoja wiadomość:")
	print(decrypted)
else:
	print("Niepoprawne odszyfrowanie!")


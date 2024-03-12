# Use algoritmos com tamanhos de chave diferentes. Você deve informar o
# algoritmo e os parâmetros na variável cipher_suite. Pesquise como fazer isso
# na documentação da biblioteca Cipher. O tempo de processamento aumenta
# ou diminui?

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import sys
import timeit

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().encode("utf-8")

file_path = '../bacon-ipsum-dolor-amet-pancetta-rib.txt'
data = read_file(file_path)

#  Você deve informar o algoritmo e os parâmetros na variável cipher_suite.

cipher_suite = {
    'AES_128': {'algorithm': AES, 'key_size': 16},
    'AES_192': {'algorithm': AES, 'key_size': 24},
    'AES_256': {'algorithm': AES, 'key_size': 32}
}


for algorithm in cipher_suite:
    chosen_algorithm = algorithm
    
    aes_key = get_random_bytes(cipher_suite[chosen_algorithm]['key_size'])
    hmac_key = get_random_bytes(16)

    cipher = cipher_suite[chosen_algorithm]['algorithm'].new(aes_key, AES.MODE_CTR)
    ciphertext = cipher.encrypt(data)

    hmac = HMAC.new(hmac_key, digestmod=SHA256)
    tag = hmac.update(cipher.nonce + ciphertext).digest()

    with open("encrypted.bin", "wb") as f:
        f.write(tag)
        f.write(cipher.nonce)
        f.write(ciphertext)

    # Share securely aes_key and hmac_key with the receiver
    # encrypted.bin can be sent over an unsecure channel

    with open("encrypted.bin", "rb") as f:
        tag = f.read(32)
        nonce = f.read(8)
        ciphertext = f.read()

    try:
        hmac = HMAC.new(hmac_key, digestmod=SHA256)
        tag = hmac.update(nonce + ciphertext).verify(tag)
    except ValueError:
        print("A mensagem foi modificada!")
        sys.exit(1)

    cipher = cipher_suite[chosen_algorithm]['algorithm'].new(aes_key, AES.MODE_CTR, nonce=nonce)
    message = cipher.decrypt(ciphertext)
    print("Chave encriptada para {}: {}".format(algorithm, aes_key.hex()))

    print("Tempo de criptografia para {}: {}".format(algorithm, timeit.timeit("AES.new(aes_key, AES.MODE_CTR).encrypt(data)", setup="from Crypto.Cipher import AES; from Crypto.Random import get_random_bytes; aes_key = get_random_bytes({}); data = b'I met aliens in UFO. Here is the map.'".format(cipher_suite[chosen_algorithm]['key_size']), number=1000)))
print("Message:", message.decode())


# from Crypto.Cipher import AES
# from Crypto.Hash import HMAC, SHA256
# from Crypto.Random import get_random_bytes
# import sys

# data = 'secret data to transmit'.encode()

# aes_key = get_random_bytes(16)
# hmac_key = get_random_bytes(16)

# cipher = AES.new(aes_key, AES.MODE_CTR)
# ciphertext = cipher.encrypt(data)

# hmac = HMAC.new(hmac_key, digestmod=SHA256)
# tag = hmac.update(cipher.nonce + ciphertext).digest()

# with open("encrypted.bin", "wb") as f:
#     f.write(tag)
#     f.write(cipher.nonce)
#     f.write(ciphertext)

# # Share securely aes_key and hmac_key with the receiver
# # encrypted.bin can be sent over an unsecure channel

# with open("encrypted.bin", "rb") as f:
#     tag = f.read(32)
#     nonce = f.read(8)
#     ciphertext = f.read()

# try:
#     hmac = HMAC.new(hmac_key, digestmod=SHA256)
#     tag = hmac.update(nonce + ciphertext).verify(tag)
# except ValueError:
#     print("The message was modified!")
#     sys.exit(1)

# cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
# message = cipher.decrypt(ciphertext)
# print("Message:", message.decode())
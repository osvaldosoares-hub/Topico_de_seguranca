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

def split_into_blocks(data, block_size):
    return [data[i:i+block_size] for i in range(0, len(data), block_size)]

def encrypt_with_block_size(data, key, block_size):
    cipher = AES.new(key, AES.MODE_CTR, nonce=b'0000000000')
    encrypted_blocks = [cipher.encrypt(block) for block in split_into_blocks(data, block_size)]
    return b''.join(encrypted_blocks)

for algorithm in cipher_suite:
    chosen_algorithm = algorithm
    
    aes_key = get_random_bytes(cipher_suite[chosen_algorithm]['key_size'])
    hmac_key = get_random_bytes(16)

    print("Chave encriptada para {}: {}".format(algorithm, aes_key.hex()))

    for block_size in [16, 24, 32]:
        ciphertext = encrypt_with_block_size(data, aes_key, block_size)

        hmac = HMAC.new(hmac_key, digestmod=SHA256)
        tag = hmac.update(ciphertext).digest()

        with open("encrypted.bin", "wb") as f:
            f.write(tag)
            f.write(ciphertext)

        # Compartilhando aes_key e hmac_key com o receptor de forma segura
        # encrypted.bin pode ser enviado por um canal não seguro

        with open("encrypted.bin", "rb") as f:
            tag = f.read(32)
            ciphertext = f.read()

        try:
            hmac = HMAC.new(hmac_key, digestmod=SHA256)
            tag = hmac.update(ciphertext).verify(tag)
        except ValueError:
            print("A mensagem foi modificada!")
            sys.exit(1)

        decrypted_data = encrypt_with_block_size(ciphertext, aes_key, block_size)

        print("Tempo de criptografia para {} com tamanho de bloco {}: {}".format(algorithm, block_size, timeit.timeit("encrypt_with_block_size(data, aes_key, {})".format(block_size), setup="from __main__ import encrypt_with_block_size, data, aes_key", number=1000)))
        

print("Message:", decrypted_data.decode())


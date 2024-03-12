# Use algoritmos com tamanhos de chave diferentes. Você deve informar o
# algoritmo e os parâmetros na variável cipher_suite. Pesquise como fazer isso
# na documentação da biblioteca Cipher. O tempo de processamento aumenta
# ou diminui?
# Pesquise como alterar o tamanho do bloco de criptografia do algoritmo.

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import sys
import timeit

# Aqui nós definimos o dado quer queremos criptografar
data = 'I met aliens in UFO. Here is the map.'.encode("utf-8")

#  Como requisitado estamos informando o algoritmo e os parâmetros, como tamanhos e chaves diferentes, na variável cipher_suite.
cipher_suite = {
    'AES_128': {'algorithm': AES, 'key_size': 16},
    'AES_192': {'algorithm': AES, 'key_size': 24},
    'AES_256': {'algorithm': AES, 'key_size': 32}
}

# Função que divide os dados em blocos do tamanho especificado, ela foi necessária pois o counter na biblioteca Crypto não aceita explicitamente a modificação do tamanho do bloco.
def split_into_blocks(data, block_size):
    #essa função divide data em vários blocos do tamanho definido em block_size e depois retorna uma lista que contém todos os blocos criados
    return [data[i:i+block_size] for i in range(0, len(data), block_size)]


# Já essa função é para criptografar os dados com o tamanho de bloco especificado
def encrypt_with_block_size(data, key, block_size):
    # Cria um objeto de cifra AES em modo CTR
    cipher = AES.new(key, AES.MODE_CTR, nonce=b'0000000000')
    # Criptografa cada bloco dos dados
    encrypted_blocks = [cipher.encrypt(block) for block in split_into_blocks(data, block_size)]
    # Concatena os blocos criptografados em um único valor
    return b''.join(encrypted_blocks)

# como quero ver o tempo de criptografia para vários tamanhos de bloco em cada uma das keys, por isso fiz esse for
for algorithm in cipher_suite:
    chosen_algorithm = algorithm

    # Gera uma chave aleatória com o tamanho especificado
    aes_key = get_random_bytes(cipher_suite[chosen_algorithm]['key_size'])
    hmac_key = get_random_bytes(16)

    print("Chave encriptada para {}: {}".format(algorithm, aes_key.hex()))

    # Loop cumprir o requisito de diferentes tamanhos de bloco
    for block_size in [16, 24, 32]:

        # Criptografa os dados com o tamanho de bloco especificado
        ciphertext = encrypt_with_block_size(data, aes_key, block_size)
        hmac = HMAC.new(hmac_key, digestmod=SHA256)
        tag = hmac.update(ciphertext).digest()

        # Aqui a gente escreve os dados criptografados e o HMAC em um arquivo binário
        with open("encrypted.bin", "wb") as f:
            f.write(tag)
            f.write(ciphertext)

        # Aqui nós lemos os dados criptografados do arquivo binário
        with open("encrypted.bin", "rb") as f:
            tag = f.read(32)
            ciphertext = f.read()

        try:
            # Inicializa um novo objeto HMAC para verificar a integridade
            hmac = HMAC.new(hmac_key, digestmod=SHA256)
            # Verifica se o HMAC dos dados recebidos corresponde ao HMAC original
            tag = hmac.update(ciphertext).verify(tag)
        # Caso não seja correspondente significa que a mensagem foi modificada
        except ValueError:
            print("A mensagem foi modificada!")
            sys.exit(1)
        
        # Aqui nós descriptografamos os dados recebidos
        decrypted_data = encrypt_with_block_size(ciphertext, aes_key, block_size)
        
        # E imprimimos o tempo de criptografia para o algoritmo com o tamanho de bloco especificado, a fim de verificar a diferença no tempo de criptografia
        print("Tempo de criptografia para {} com tamanho de bloco {}: {}".format(algorithm, block_size, timeit.timeit("encrypt_with_block_size(data, aes_key, {})".format(block_size), setup="from __main__ import encrypt_with_block_size, data, aes_key", number=1000)))
        
# Por fim, imprimimos os dados descriptografados
print("Message:", decrypted_data.decode())


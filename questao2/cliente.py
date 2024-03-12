import socket
import sys
from cryptography.fernet import Fernet

def decifrando_texto(chave):
    with open('chave_secreta_cifrado.txt', 'rb') as arquivo_cifrado:
        cipher_suite = Fernet(chave)
        texto_cifrado = arquivo_cifrado.read()
        texto_decifrado = cipher_suite.decrypt(texto_cifrado)
    with open('chave_secreta_decifrado.txt', 'wb') as file:
        file.write(texto_decifrado)    
    return texto_decifrado

def client(name):
    server_address = ('127.0.0.1',  5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    print(f'ola, {name}. vamos iniciar o chat!')
    MSG=""

    s.sendall(name.encode('utf-8'))
    data = s.recv(1024)
    peer_name = data.decode('utf-8')
    chave = s.recv(1024)
   
   
    
    texto_decifrado = decifrando_texto(chave)

    
    print("Texto decifrado :" +texto_decifrado.decode('utf-8'))
    #while MSG != 'fim':
    #    MSG = input(f"{name}: ")
        
    #    s.sendall(MSG.encode('utf-8'))
    #    data = s.recv(1024)
    #    if(data.decode('utf-8') == 'fim'):
    #        break

    #    print(f"{peer_name}:", data.decode('utf-8'))
    s.close()
    
def main(name):
    client(name)  

if __name__ == '__main__':
    user_name = sys.argv[1]
    main(user_name)


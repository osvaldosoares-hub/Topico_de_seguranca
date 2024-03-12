import socket
import sys
from cryptography.fernet import Fernet


def encripitando_aquivo(key):
    with open('chave_secreta.txt', 'rb') as arquivo:
        texto = arquivo.read()
        cipher_suite = Fernet(key)
        texto_cifrado = cipher_suite.encrypt(texto)
        print(texto_cifrado)
    with open('chave_secreta_cifrado.txt','wb') as arquivo_cifrado:
        arquivo_cifrado.write(texto_cifrado)

    



def server(name):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 5000)
    s.bind(server_address)
    s.listen(1)
    print(f'ola, {name}. Servidor aguardando conexao')
    connection, address = s.accept()
    MSG=""

    data = connection.recv(1024)
    peer_name = data.decode('utf-8')
    connection.sendall(name.encode('utf-8'))
    
    chave = Fernet.generate_key()
    encripitando_aquivo(chave)
    connection.sendall(chave)
    
    
   
    
    
    #while MSG !='fim':
    #   data = connection.recv(1024)

    #   if data.decode('utf-8') == 'fim':
    #       break

    #   print(f"{peer_name}: ",data.decode('utf-8'))
    #   if not data:
    #      connection.sendall(data)
    #      MSG = input(f"{name}: ")
    #      connection.sendall(MSG.encode('utf-8'))

    connection.close()
    s.close()




def main(name):
   
        server(name)
    
          

if __name__ == '__main__':
    user_name = sys.argv[1]
    main(user_name)
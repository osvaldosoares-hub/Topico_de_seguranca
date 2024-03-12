import socket
import sys
from cryptography.fernet import Fernet

chave = Fernet.generate_key()
cipher_suite = Fernet(chave)    
print(cipher_suite)
def ler_chave_secreta():
    with open('chave_secreta.txt', 'rb') as file:
        texto = file.read()
        texto_cifrado = cipher_suite.encrypt(texto)
        return texto_cifrado



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
    
    chave_secreta = ler_chave_secreta()
    
    connection.sendall(chave_secreta)
   
   
    print("chave secreta: " + chave_secreta.decode('utf-8'))
    

    connection.close()
    s.close()


def client(name):
    server_address = ('127.0.0.1',  5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    print(f'ola, {name}. vamos iniciar o chat!')
    MSG=""

    s.sendall(name.encode('utf-8'))
    data = s.recv(1024)
    peer_name = data.decode('utf-8')

    chave_secreta = s.recv(1024).decode('utf-8')
    print(f"Chave secreta recebida: {chave_secreta}")
   
   
    
    s.close()

def main(peer,name):
    if peer== 'server':
        server(name)
    if peer == 'cliente':
        client(name)    

if __name__ == '__main__':
    peer_type = sys.argv[1]
    user_name = sys.argv[2]
    main(peer_type,user_name)
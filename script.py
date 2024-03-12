import hashlib
import timeit
def calcular_hash(arquivo):
    sha256= hashlib.sha256()
    with open(arquivo,"rb") as f:
        for bloco in iter(lambda: f.read(4096),b""):
            sha256.update(bloco)
    return sha256.hexdigest()
def salvar_hash(arquivo, hash_calculado):
    with open(arquivo+"_hash.txt",'w')as f:
        f.write(hash_calculado)

def verificar_integridade(arquivo,hash_salvo):
    hash_calculado = calcular_hash(arquivo)
    print(f"hash calculado:\t {hash_calculado}")
    print(f"hash salvo:\t {hash_salvo}")
    return hash_calculado == hash_salvo
def main():
    arquivo_original = "exemplo.txt"
    hash_calculado = calcular_hash(arquivo_original)
    salvar_hash(arquivo_original,hash_calculado)
    print('hash salvo em arquivo')
    #arquivo_original = "exemplo.txt"
    hash_salvo = open(arquivo_original+"_hash.txt").read()
    if verificar_integridade(arquivo_original,hash_salvo):
        print("a integridade do arquivo foi preservada.")
    else:
        print('atenção o arquivo foi modificado.')


tempo= timeit.timeit(main,number=1)
print(tempo)
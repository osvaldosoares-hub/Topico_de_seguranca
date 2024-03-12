
text = input('digite o texto que deseja criptografar: ')
distancia = int(input('digite a distancia que deseja usar '))
cripto=''
for letra in text:
    numero= ord(letra)
    numero=numero+distancia
    letra = chr(numero)
    cripto=cripto+letra

print("o texto criptografado é " +cripto)
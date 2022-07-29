from base64 import b64encode, b64decode
import jks
import os
from Crypto.Cipher import ChaCha20, ChaCha20_Poly1305
from Crypto.Util.Padding import pad, unpad

#Conseguimos la clave necesaria del keystore
path=os.path.dirname(__file__)
parent_path=os.path.dirname(path)
keystore=parent_path + "/KeyStorePracticas"
ks = jks.KeyStore.load(keystore, "123456")

for alias, sk in ks.secret_keys.items():
    if sk.alias == 'cifrado-sim-chacha20-256':
        key =  bytes.fromhex("".join("{:02x}".format(b) for b in bytearray(sk.key)))


#Generamos las variables
texto_plano = bytes('Este curso es de lo mejor que podemos encontrar en el mercado', 'utf-8')
nonce = bytes(b64decode('9Yccn/f5nJJhAt2S'))
#Creamos el cifrador y ciframos el texto
cipher = ChaCha20.new(key=key, nonce=nonce)
texto_cifrado = cipher.encrypt(texto_plano)
#Imprimimos texto cifrado
print('Mensaje cifrado en HEX = ', texto_cifrado.hex())
print('Mensaje cifrado en B64 = ', b64encode(texto_cifrado).decode())

#Añadimos mejora de poly1305
#Creamos el cifrador y los datos asociados al mismo
datos_asociados = bytes('Estos datos verifican la integridad del mensaje', 'utf-8')
cipher2 = ChaCha20_Poly1305.new(key=key, nonce=nonce)
cipher2.update(datos_asociados)
texto_cifrado_y_autenticado, tag = cipher2.encrypt_and_digest(texto_plano)
print('Mensaje cifrado y autenticado en HEX = ', texto_cifrado_y_autenticado.hex())
print('Mensaje cifrado y autenticado en B64 = ', b64encode(texto_cifrado_y_autenticado).decode())
print('El tag que firma la integridad en B64 = ', b64encode(tag).decode())
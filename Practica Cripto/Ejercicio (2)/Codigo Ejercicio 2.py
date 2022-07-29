from base64 import b64decode
import jks
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad



#Conseguimos la clave necesaria del keystore
path=os.path.dirname(__file__)
parent_path=os.path.dirname(path)
keystore=parent_path + "/KeyStorePracticas"
ks = jks.KeyStore.load(keystore, "123456")

for alias, sk in ks.secret_keys.items():
    if sk.alias == 'cifrado-sim-aes-256':
        key =  "".join("{:02x}".format(b) for b in bytearray(sk.key))
key = bytes.fromhex(key)

#Desciframos el texto
iv = bytes.fromhex('00000000000000000000000000000000')
texto_cifrado = b64decode('zcFJxR1fzaBj+gVWFRAah1N2wv+G2P01ifrKejICaGpQkPnZMiexn3WXlGYX5WnNIosyKfkNKG9GGSgG1awaZg==')
cipher = AES.new(key, AES.MODE_CBC, iv)
texto_descifrado_pad = cipher.decrypt(texto_cifrado)
#Imprimimos el texto sin quitar el padding
print ('En hex y sin quitar el padding: ', texto_descifrado_pad.hex())
#Quitamos el padding
texto_descifrado_unpad = unpad(texto_descifrado_pad, AES.block_size, style="pkcs7")
print("En hex sin padding: ", texto_descifrado_unpad.hex())
print("El texto en claro es: ", texto_descifrado_unpad.decode("utf-8"))

#Usamos el padding x923
try:
    texto_descifrado_pad_x923 = unpad(cipher.decrypt(texto_cifrado), AES.block_size, style="x923")
except (ValueError, KeyError) as error:
    print('Problemas para descifrar....')
    print("El motivo del error es: ", error) 
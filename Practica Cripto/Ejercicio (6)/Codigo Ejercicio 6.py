import jks
import os
from Crypto.Hash import HMAC, SHA256


#Conseguimos la clave necesaria del keystore
path=os.path.dirname(__file__)
parent_path=os.path.dirname(path)
keystore=parent_path + "/KeyStorePracticas"
ks = jks.KeyStore.load(keystore, "123456")

for alias, sk in ks.secret_keys.items():
    if sk.alias == 'hmac-sha256':
        key =  "".join("{:02x}".format(b) for b in bytearray(sk.key))

secret = bytes.fromhex(key)

#Generación el hmac
texto= bytes('Siempre existe más de una forma de hacerlo, y más de una solución válida.', 'utf-8')
hash = HMAC.new(secret, msg=texto, digestmod=SHA256)
print(hash.hexdigest())
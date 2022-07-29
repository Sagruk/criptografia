from pprint import pprint
import jwt
import hashlib
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import json



##################### PETICION RECIBIDA ##################################
print ('Peticion Recibida')
clave_jwt = 'KeepCoding'
encoded_jwt = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZFVzdWFyaW8iOiJNUT09IiwidXN1YXJpbyI6Im9obWtiMk41djVmSC9SbTJDVDhxNEhOQUk2NEI4Zy9NUlQzWXlTWU1ldDA9IiwidGFyamV0YSI6Ii91RFRnS3d5RGh0L0Iva1pJaGZlNjVxZTZKS2s5alZQZ1N3eDFxWUtRakE9In0.1-dDFwXjDC4PAkqLm8vhOMJ2Dbk2zAL3MmXw_CSUCXw')

try:
    decoded_jwt = jwt.decode(jwt=encoded_jwt, key=clave_jwt, algorithms='HS256')
    print('El JWT recibido y decodificado es:', decoded_jwt)
    id_usuario_64 = decoded_jwt['idUsuario']
    usuario_cifrado_b64 = decoded_jwt['usuario']
    tarjeta_cifrada_b64 = decoded_jwt['tarjeta']
    id_usuario = b64decode(id_usuario_64).decode()
    usuario_cifrado = b64decode(usuario_cifrado_b64)
    tarjeta_cifrada = b64decode(tarjeta_cifrada_b64)
    print('Presentacion de los datos:')
    print('El id de usuario es  :',id_usuario)
    print('El usuario cifrado es:',usuario_cifrado.hex())
    print('La tarjeta cifrada es:',tarjeta_cifrada.hex())

except jwt.exceptions.InvalidSignatureError:
    print("El mensaje no ha sido validado")


#El servidor realizaria la busqueda en la base de datos
#Y responderia con la información solicitada


print ('\n')
##################### RESPUESTA ENVIADA ##################################
print ('Respuesta Enviada')
#Recuperamos los datos que debemos enviar
mov_tarjeta = [{
    'id':1, 
    'comercio':'Comercio Juan', 
    'importe': 5000
    },
    {
    'id':2,
    'comercio':'Rest Paquito',
    'importe': 6000
    }]
moneda = 'EUR'
saldo = '23400'

mensaje_plano = json.dumps({'idUsuario':id_usuario, 'movTarjeta':mov_tarjeta, 'Moneda':moneda, 'Saldo':saldo})

#Creamos el cifrador
clave_EAS = bytes.fromhex('d47361b1377fab9886c3e97424b5357e')
nonce = bytes.fromhex('47e6831df094b7a6')
datos_asociados = bytes('Datos enviados por FJ', 'utf-8')
cifrador = AES.new(clave_EAS, AES.MODE_GCM,nonce=nonce)
cifrador.update(datos_asociados)
mensaje_plano_bytes = bytes(mensaje_plano, 'utf-8')
mensaje_cifrado, tag = cifrador.encrypt_and_digest(mensaje_plano_bytes)
print('El mensaje cifrado es: ', mensaje_cifrado.hex())
print('El tag es: ', tag.hex())

#Codificamos los datos en b64
nonce_b64 = b64encode(nonce).decode()
datos_asociados_64 = b64encode(datos_asociados).decode()
mensaje_cifrado_b64 = b64encode(mensaje_cifrado).decode()
tag_64 = b64encode(tag).decode()

respuesta_enviada = json.dumps({'nonce':nonce_b64, 'datos asociados':datos_asociados_64, 'tag':tag_64, 'texto cifrado':mensaje_cifrado_b64})
print('La respuesta enviada es: ', respuesta_enviada)
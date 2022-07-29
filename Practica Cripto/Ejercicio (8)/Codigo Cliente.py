from bs4 import Tag
import jwt
import hashlib
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import json

###################### PETICION ENVIADA ########################
print ('Peticion Enviada')
#Creamos los datos que vamos a mandar
id_usuario = '1'
usuario_plano = bytes('José Manuel Barrio Barrio', 'utf-8')
tarjeta_plano = bytes('4231212345676891', 'utf-8')

#Creamos el metodo de hash

#Ciframos los datos que se deben cifrar
usuario_cifrado = hashlib.sha256(string=usuario_plano)
tarjeta_cifrada = hashlib.sha256(string=tarjeta_plano)
print('El id de usuario es  :', id_usuario)
print('El usuario cifrado es:', usuario_cifrado.digest().hex())
print('La tarjeta cifrada es:', tarjeta_cifrada.digest().hex())


#Codificamos variables en B64
id_usuario_b64 = b64encode(bytes(id_usuario, 'utf-8')).decode()
usuario_cifrado_b64 = b64encode(usuario_cifrado.digest()).decode()
tarjeta_cifrada_b64 = b64encode(tarjeta_cifrada.digest()).decode()

#Montamos mensaje con los datos
mensaje = {'idUsuario':id_usuario_b64, 'usuario':usuario_cifrado_b64, 'tarjeta':tarjeta_cifrada_b64 }

#Montamos el jwt que deseamos enviar
clave_jwt = 'KeepCoding'
encoded_jwt = jwt.encode(mensaje, key=clave_jwt, algorithm='HS256')
print('El JWT enviado es    :', encoded_jwt)


print ('\n')
###################### RESPUESTA RECIBIDA ########################
print ('Respuesta Recibida')

#Leemos la respuesta recibida
respuesta_recibida_64 = '{"nonce": "R+aDHfCUt6Y=", "datos asociados": "RGF0b3MgZW52aWFkb3MgcG9yIEZK", "tag": "odyaK4IoW2MRSe86V2IMDw==", "texto cifrado": "DoZXgSMAssirJSw9B1VTLceE7oWiIetXr6yU7DqG1JzUnf7fI+X7fWWNjk2ryoQKLXKpnXqBRnDVUKtzwrNlsS1bVnT0JmGKsUL8LiJXJbJ4ARY+HHZ7Y1BFCVcglQlrH1PsjBn0eZ78531VS3j8FDUXNWS37k8IxiARBWk8dREjSwCppSmZ0kaAzYW7iryVMefSzsu7cxVooZIyg39o0/jmAB2kG1FF1QHhRI2YLx4cZUeCKTk="}'
print('La respuesta recibida es: ', respuesta_recibida_64)
respuesta_recibida = json.loads(respuesta_recibida_64)
nonce = b64decode(respuesta_recibida['nonce'])
datos_asociados = b64decode(respuesta_recibida['datos asociados'])
tag = b64decode(respuesta_recibida['tag'])
texto_cifrado = b64decode(respuesta_recibida['texto cifrado'])

#Desencriptamos la respuesta recibida
clave_EAS = bytes.fromhex('d47361b1377fab9886c3e97424b5357e')
descifrador = AES.new(clave_EAS, AES.MODE_GCM, nonce=nonce)
descifrador.update(datos_asociados)
mensaje_descifrado = descifrador.decrypt_and_verify(texto_cifrado,tag)
print('La respuesta descifrada es: ', mensaje_descifrado.decode('utf-8'))

#Desenpaquetamos la respuesta para que se lea bien
print('Presentación de los datos:')
mensaje_descifrado_plano = json.loads(mensaje_descifrado.decode('utf-8'))
print('idUsuario: ',mensaje_descifrado_plano['idUsuario'])
print('movTarjeta: ',mensaje_descifrado_plano['movTarjeta'][0])
print('movTarjeta: ',mensaje_descifrado_plano['movTarjeta'][1])
print('Saldo: ',mensaje_descifrado_plano['Saldo'])
print('Moneda: ',mensaje_descifrado_plano['Moneda'])

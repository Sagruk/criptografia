import jwt
import json
from base64 import b64decode

#Creamos el mensaje entero
encoded_jwt = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c3VhcmlvIjoiRmVsaXBlIFJvZHJcdTAwZWRndWV6Iiwicm9sIjoiaXNOb3JtYWwifQ.-KiAA8cjkamjwRUiNVHgGeJU8k2wiErdxQP_iFXumM8'

#Decodificamos la cabecea para ver el algoritmo usado
header = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
header_plano = json.loads(b64decode(header).decode('utf-8'))
algoritmo = header_plano['alg']
print ('El algoritmo usado es:' , algoritmo)

#Decodificamos el mensaje conociendo la clave y el algoritmo usado
decode_jwt = jwt.decode(encoded_jwt, 'KeepCoding', algorithms=algoritmo)

#Imprimimos el mensaje
print(decode_jwt)

#Creamos el segundo mensaje
encoded_jwt2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c3VhcmlvIjoiRmVsaXBlIFJvZHJcdTAwZWRndWV6Iiwicm9sIjoiaXNBZG1pbiJ9.-KiAA8cjkamjwRUiNVHgGeJU8k2wiErdxQP_iFXumM8'

#Decodificamos el mensaje conociendo la clave y el algoritmo usado
try:
  decode_jwt2 = jwt.decode(encoded_jwt2, algorithms=algoritmo)
  print("Mensaje validado ok")
except jwt.exceptions.InvalidSignatureError:
  print("Mensaje no validado")

#Para que funcione al estar modificado debemos quitar la verificacion de firma
decode_jwt2 = jwt.decode(encoded_jwt2, algorithms='HS256', options={"verify_signature": False})
print(decode_jwt2)
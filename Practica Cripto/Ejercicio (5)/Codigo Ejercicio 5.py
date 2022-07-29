import hashlib

texto = 'En KeepCoding aprendemos cómo protegernos con criptografía.'

#Creamos el hash
hash = hashlib.sha3_256()

#Pasamos el texto por el hash
hash.update(bytes(texto, 'utf-8'))

print(hash.hexdigest())
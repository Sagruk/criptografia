#Creamos la funcion XOR de dos datos:
def xor(binary_data_1, binary_data_2):
    return bytes([b1^b2 for b1, b2 in zip(binary_data_1, binary_data_2)])
#Los datos deben pasarlese en formato bytes.

#Cramos las variables en formato bytes de las clave en hexadecimal
k_fija = bytes.fromhex('A1EF2ABFE1AAEEFF')
k_final_desarrollo = bytes.fromhex('B1AA12BA21AABB12')
#Creamos la variable que es la clave que nos falta pasandole las dos anteriores por la funcion creada
k_manager_desarrollo = xor(k_fija,k_final_desarrollo)
#Imprimimos por pantalla en formato hexadecimal la clave resultante
print("La clave k_manager_desarrollo en hexadecimal es: ", k_manager_desarrollo.hex())

#En produccion nos facilitan la clave del manager
k_manager_produccion = bytes.fromhex('B98A15BA31AEBB22')
#Hacemos el XOR para obtener la clave final
k_final_produccion = xor(k_fija,k_manager_produccion)
#Imprimimos la clave final
print("La clave k_final_produccion en hexadecimal es: ", k_final_produccion.hex())
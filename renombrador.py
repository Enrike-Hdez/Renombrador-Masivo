__version__ = "0.2.4"

import os
import ctypes
import functools
from pathlib import Path

# Pedir al usuario la ruta y el nombre para los documentos
try:
    rute = Path(input("Ingrese la ruta donde se encuentran los archivos: "))
    name = input("Ingrese el nombre que desea para los archivos: ")

except Exception as e:
    print(f"Error al ingresar la ruta o el nombre: {e}")
    exit()

# Parte principal del programa
try:
    if rute.exists():

        # Lista para almacenar los nombres
        old_names = [f for f in os.listdir(rute) if os.path.isfile(os.path.join(rute, f))]

        # Pedir al usuario el número de inicio y final para la numeración
        try:
            try:
                selection = input("Pulse 1 para seleccionar todos los archivos o pulse 2 para seleccionar un rango específico: ")

                if selection == "1":
                    start = 1
                    end = len(old_names)
                else:
                    start = int(input("Ingrese el número de inicio para la numeración: "))
                    end = int(input("Ingrese el número final para la numeración: "))

                if start > end or start < 0 or end < 0 or end - start >= len(old_names):
                    print("El número de inicio debe ser menor o igual al número final y debe coincidir con la cantidad de archivos.")
                    exit()
            
            except ValueError:
                print("Debe ingresar un número entero para la numeración.")
                exit()
        
        except ValueError:
            print("Debe ingresar un número entero para la numeración.")
            exit()

        # Función para transformar la función de comparación de StrCmpLogicalW
        # en una función que python pueda usar para ordenar de forma natural
        # porque al parecer no hay otra forma de hacer esto sin meterte en los
        # metadatos de los archivos COMO SI FUERA YO A HACKEAR UN PUTO COMIC PARA RENOMBRARLO
        natSort = functools.cmp_to_key(ctypes.windll.shlwapi.StrCmpLogicalW)

        # Ordenando los nombres viejos de forma natural gracias a la conversón
        old_names.sort(key=natSort)          
        
         # Renombrando los archivos
        try:
            for i in range(len(old_names)):         

                if i + start > end:
                    print("Se ha alcanzado el número final para la numeración.")
                    exit()

                ext = os.path.splitext(old_names[i])[1]
                new_name = f"{name} #{i+start}{ext}"
                new_path = os.path.join(rute, new_name)

                if os.path.exists(new_path):
                    print(f"El archivo '{new_name}' ya existe. No se puede renombrar '{old_names[i]}'.")
                    pass
                
                else:
                    os.rename(os.path.join(rute, old_names[i]), new_path)
                
                
        except Exception as e:
            print(f"Error al renombrar los archivos: {e}")
        
except Exception as e:
    print("La ruta no existe")
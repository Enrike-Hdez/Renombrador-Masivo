__version__ = "0.1.2"

import os
import ctypes
import functools
from pathlib import Path

# Pedir al usuario la ruta y el nombre para los documentos
rute = Path(input("Ingrese la ruta donde se encuentran los archivos: "))
name = input("Ingrese el nombre que desea para los archivos: ")

try:
    if rute.exists():

            # Listas para almacenar los nombres viejos y nuevos
            new_names = []
            old_names = [f for f in os.listdir(rute) if os.path.isfile(os.path.join(rute, f))]

            # Función para transformar la función de comparación de StrCmpLogicalW
            # en una función que python pueda usar para ordenar de forma natural
            # porque al parecer no hay otra forma de hacer esto sin meterte en los
            # metadatos de los archivos COMO SI FUERA YO A HACKEAR UN PUTO COMIC PARA RENOMBRARLO
            natSort = functools.cmp_to_key(ctypes.windll.shlwapi.StrCmpLogicalW)

            # Ordenando los nombres viejos de forma natural gracias a la conversón
            old_names.sort(key=natSort)          

            # Generando los nombres nuevos
            for i in range(len(old_names)):
                new_names.append(f"{name} #{i+1}{os.path.splitext(old_names[i])[1]}")

            # Renombrando los archivos
            try:
                for i in range(len(old_names)):
                    os.rename(os.path.join(rute, old_names[i]), os.path.join(rute, new_names[i]))
                
            except Exception as e:
                print(f"Error al renombrar los archivos: {e}")
        
except Exception as e:
    print("La ruta no existe")
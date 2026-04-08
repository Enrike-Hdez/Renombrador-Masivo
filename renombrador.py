import os
import ctypes
import functools
from pathlib import Path

__version__ = "0.3.1"

# Obtener la ruta y el nombre para los documentos del usuario
def get_user_input():
    try:
        rute = Path(input("Ingrese la ruta donde se encuentran los archivos: "))
        name = input("Ingrese el nombre que desea para los archivos: ")

        return rute, name

    except Exception as e:
        print(f"Error al ingresar la ruta: {e}")
        exit()

# Obtener los nombres de los archivos en la ruta dada filtando sólo los archivos
def get_archives(rute):
    try:
        if rute.exists():
            old_names = [f for f in os.listdir(rute) if os.path.isfile(os.path.join(rute, f))]

            return old_names
        
    except Exception as e:
        print(f"Error al acceder a la ruta: {e}")
        exit()

# Verificar que el rango de numeración sea correcto
def check_range(start, end, old_names):
    if start > end or start < 0 or end < 0 or end - start >= len(old_names):
        print("El número de inicio debe ser menor o igual al número final y debe coincidir con la cantidad de archivos.")
        exit()

# Obtener el rango de numeración para los archivos
def get_range(old_names):
    try:
        selection = input("Pulse 1 para seleccionar todos los archivos o pulse 2 para seleccionar un rango específico: ")

        if selection == "1":
            start = 1
            end = len(old_names)
            check_range(start, end, old_names)

            return start, end

        elif selection == "2":
            start = int(input("Ingrese el número de inicio para la numeración: "))
            end = int(input("Ingrese el número final para la numeración: "))
            check_range(start, end, old_names)

            return start, end
        
        else:
            print("Selección no válida. Por favor, ingrese 1 o 2.")
            exit()
            
    except ValueError as e:
        print("Debe ingresar un número natural.")
        exit()
        
# Verificación para el usuario
def verify():
    verify = input("¿Desea continuar con el proceso de renombrado? (s/n): ")

    if verify.lower() != 's':
        print("Proceso de renombrado cancelado por el usuario.")
        exit()

# Función para transformar la función de comparación de StrCmpLogicalW
# en una función que python pueda usar para ordenar de forma natural
# porque al parecer no hay otra forma de hacer esto sin meterte en los
# metadatos de los archivos COMO SI FUERA YO A HACKEAR UN PUTO COMIC PARA RENOMBRARLO
def sort_natural(old_names):
    natSort = functools.cmp_to_key(ctypes.windll.shlwapi.StrCmpLogicalW)

    # Ordenando los nombres viejos de forma natural gracias a la conversón
    old_names_sorted = sorted(old_names, key=natSort)

    return old_names_sorted

# Renombrando los archivos
def rename_archives(rute, name, old_names_sorted, start, end):
    
    try:
        for i in range(len(old_names_sorted)):         

            if (i + start) > end:
                print("Se ha alcanzado el número final para la numeración.")
                exit()

            ext = os.path.splitext(old_names_sorted[i])[1]
            new_name = f"{name} #{i+start}{ext}"
            new_path = os.path.join(rute, new_name)

            if os.path.exists(new_path):
                print(f"El archivo '{new_name}' ya existe. No se puede renombrar.")
                pass
                    
            else:
                os.rename(os.path.join(rute, old_names_sorted[i]), new_path)
                    
    except Exception as e:
        print(f"Error al renombrar los archivos: {e}")
        
# main
def main():
    rute, name = get_user_input()
    old_names = get_archives(rute)
    start, end = get_range(old_names)
    verify()
    old_names_sorted = sort_natural(old_names)
    rename_archives(rute, name, old_names_sorted, start, end)

if __name__ == "__main__":
    main()
import os
import ctypes
import functools
import shutil
from datetime import datetime
from pathlib import Path

__version__ = "0.4.2"

# Obtener la ruta y el nombre para los documentos del usuario
def get_user_input():
    while True:
        try:
            rute = Path(input("Ingrese la ruta donde se encuentran los archivos: "))
            name = input("Ingrese el nombre que desea para los archivos: ")

            if rute.exists():
                return rute, name
            
            print("Ha ocurrido un error al ingresar la ruta")

        except Exception as e:
            print(f"Error desconocido: {e}")



# Obtener los nombres de los archivos en la ruta dada filtando sólo los archivos
def get_archives(rute):
    try:
        old_names = [f for f in os.listdir(rute) if os.path.isfile(os.path.join(rute, f))]

        return old_names
        
    except Exception as e:
        print(f"Error al obtener los archivos: {e}")
        return[]



# Verificar que el rango de numeración sea correcto
def check_range(start, end, old_names):
        if start > end or start < 0 or end < 0 or end - start >= len(old_names):
            print("El número de inicio debe ser menor o igual al número final y debe coincidir con la cantidad de archivos.")

            return False

        return True



# Obtener el rango de numeración para los archivos
def get_range(old_names):
    while True:
        try:
            selection = input("Pulse 1 para seleccionar todos los archivos o pulse 2 para seleccionar un rango específico: ")

            if selection == "1":
                start = 1
                end = len(old_names)

                if check_range(start, end, old_names):
                    return start, end

            elif selection == "2":
                while True:
                    try:
                        start = int(input("Ingrese el número de inicio para la numeración: "))
                        end = int(input("Ingrese el número final para la numeración: "))

                        if check_range(start, end, old_names):
                            return start, end
                    
                    except Exception as e:
                        print(f"Fallo al rellenar el campo: {e}")
                        continue
                
            else:
                print("Selección no válida. Por favor, ingrese 1 ó 2.")
                continue

        except ValueError as e:
            print(f"Error desconocido: {e}")
            continue



# Verificación para el usuario
def verify(rute, name):
    while True:
        print(f"Usted va a cambiar los nombres de la ruta {rute} a {name}.")
    
        verify = input("¿Está seguro que desea continuar con el proceso de renombrado? (Y/N): ")
    
        if verify.lower() == 'y':
            return True
            
        elif verify.lower() == 'n':
            print("Ha decidido no continuar")

            return False
        
        else: 
            print("Campo inválido, debe ingresar (Y/N).")



# Crea una copia de seguridad a los archivos que se van a copiar
def backup(rute, old_names):
    while True:
        try:
            decision = input("¿Desea crear una copia de seguridad de los archivos antes de renombrarlos? (Y/N): ").lower()

            if decision.lower() == "y":
                try:
                    # Tema de las fechas
                    now = datetime.now()
                    formated_now = now.strftime("backup %d-%m-%Y %H-%M")
                    backup_rute = os.path.join(rute,formated_now)

                    # Cógigo principal del backup
                    os.makedirs(backup_rute, exist_ok=True)

                    for file in old_names:
                        final_rute = os.path.join(rute, old_names[file])
                        
                        shutil.copy2(final_rute, backup_rute)

                    return

                except FileNotFoundError:
                    print("Error: El archivo de origen no fue encontrado.")
                
                except PermissionError:
                    print("Error: Permiso denegado.")

                except Exception as e:
                    print(f"Ocurrió un error inesperado: {e}")

            elif decision.lower() == "n":
                print("Ha decidido no crear una copia de seguridad.")
                return

            else:
                print("Campo inválido, debe ingresar (Y/N).")
                continue
        
        except Exception as e:
            print(f"Error desconocido: {e}") 



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
                return

            ext = os.path.splitext(old_names_sorted[i])[1]
            new_name = f"{name} #{i+start}{ext}"
            new_path = os.path.join(rute, new_name)

            if os.path.exists(new_path):
                print(f"El archivo '{new_name}' ya existe. No se puede renombrar.")
                continue
                    
            else:
                os.rename(os.path.join(rute, old_names_sorted[i]), new_path)
                    
    except Exception as e:
        print(f"Error al renombrar los archivos: {e}")





def main():
    while True:
        rute, name = get_user_input()
        old_names = get_archives(rute)
        start, end = get_range(old_names)

        if verify(rute, name):
            break
    
    backup(rute, old_names)
    old_names_sorted = sort_natural(old_names)
    rename_archives(rute, name, old_names_sorted, start, end)

if __name__ == "__main__":
    main()
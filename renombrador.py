import os
import ctypes
import functools
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from datetime import datetime
from pathlib import Path

__version__ = "5.0.0"

# Zona de funciones
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



# Crea una copia de seguridad a los archivos que se van a copiar
def backup(rute, old_names):
    while True:
        try:
            # Tema de las fechas
            now = datetime.now()
            formated_now = now.strftime("backup %d-%m-%Y %H-%M")
            backup_rute = os.path.join(rute,formated_now)

            # Cógigo principal del backup
            os.makedirs(backup_rute, exist_ok=True)

            for i in range(len(old_names)):
                final_rute = os.path.join(rute, old_names[i])
                
                shutil.copy2(final_rute, backup_rute)

            return

        except FileNotFoundError:
            print("Error: El archivo de origen no fue encontrado.")
        
        except PermissionError:
            print("Error: Permiso denegado.")

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")




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
def rename_archives(rute, name, old_names_sorted, start, end, delimiter):
    try:
        temp = []
        final_names = []
        
        # Creando nombres temporales para evitar conflictos de nombres al renombrar los archivos
        for i in range(len(old_names_sorted)):       

            if (i + start) > end:
                break  
            
            tem_name = datetime.now().strftime("temp %H-%M-%S superman batman robin spiderman")
            ext = os.path.splitext(old_names_sorted[i])[1]
            new_name = f"{tem_name}{delimiter}{i+start}{ext}"
            new_path = os.path.join(rute, new_name)

            temp.append(new_path)
            os.rename(os.path.join(rute, old_names_sorted[i]), new_path)

        # Renombrando los archivos con los nombres finales
        for i in range(len(old_names_sorted)):     
            if (i + start) > end:
                break    

            ext = os.path.splitext(old_names_sorted[i])[1]
            new_name = f"{name}{delimiter}{i+start}{ext}"
            new_path = os.path.join(rute, new_name)

            os.rename(os.path.join(rute, temp[i]), new_path)

            final_names.append(new_name)
            print(old_names_sorted[i] + " -> " + final_names[i])
            
        return final_names
                    
    except Exception as e:
        print(f"Error al renombrar los archivos: {e}")





# Zona del GUI
# Parte principal
def create_gui():
    # Configiración de la ventana principal
    root = tk.Tk()
    root.title("Renombrador Masivo")
    root.resizable(False, False)

    # Obteniendo el tamaño de la pantalla del usuario
    width_pc = root.winfo_screenwidth()
    height_pc = root.winfo_screenheight()
    width = 450
    height = 500

    # Calcula la posición para centrar la ventana
    position_x = (width_pc // 2) - (width // 2)
    position_y = (height_pc // 2) - (height // 2) -30 # Truquito de YT para centrar la ventana en Windows

    root.geometry(f"{width}x{height}+{position_x}+{position_y}")    

    # Funciones para los botones
    def clear_records():
        record_text.delete("1.0", tk.END)

    def write_name():
        name = name_entry.get()
        record_text.insert(tk.END, f"Nombre ingresado: {name}\n")

    # Funciones para establecer limites de caracteres en las cajas de texto
    def limit_entry(entry, limit):
        def on_write(*args):
            value = entry.get()
            if len(value) > limit:
                entry.set(value[:limit])
        entry.trace("w", on_write)        

    # Función principal del delimitador
    def get_delimiter():
        delimiter = delimiter_combo.get()

        if delimiter == "#":
            return "#"
        elif delimiter == "ESPACIO":
            return " "
        elif delimiter == "ESPACIO + .":
            return " ."
        elif delimiter == "Otro":
            return delimiter_combo.get()
        else:
            return delimiter

    # Función que activa el modo de texto libre al seleccionar "Otro"
    def other_options(event=None):
        if delimiter_combo.get() == "Otro":
            delimiter_combo.set("#")
            delimiter_combo.config(state="normal")
            delimiter_combo.focus()
        else:
            delimiter_combo.config(state="readonly")
            


    # Función start
    def start():
        rute = path_entry.get().strip()
        name = name_entry.get().strip()
        start_value = first_n_range_entry.get().strip()
        end_value = second_n_range_entry.get().strip()
        delimiter = get_delimiter()

        try:
            start_num = int(start_value)
            end_num = int(end_value)
        except ValueError:
            print("Error: Inicio y final deben ser números enteros.")
            return

        old_names = get_archives(rute)
        if not old_names:
            print("Error: No se encontraron archivos en la ruta.")
            return

        if not check_range(start_num, end_num, old_names):
            return

        if backup_var.get() == 1:
            backup(rute, old_names)

        old_names_sorted = sort_natural(old_names)
        rename_archives(rute, name, old_names_sorted, start_num, end_num, delimiter)


    # Cajas o contenedores 
    principal_frame = tk.Frame(root, bg="#e8e8e8")
    preferences_frame = tk.Frame(root, bg="#e8e8e8")
    backup_frame = tk.Frame(root, bg="#e8e8e8")
    bottom_frame = tk.Frame(root, bg="#e8e8e8")


    # Etiqueas 
    name_and_rute_label = tk.Label(principal_frame,
                                    text="Ruta-Nombre",
                                    font=("Segoe UI", 16),
                                    bg="#e8e8e8")
                        
    path_label = tk.Label(principal_frame,
                          text="Ruta",
                          font=("Segoe UI", 12),
                          bg="#e8e8e8")

    name_label = tk.Label(principal_frame,
                          text="Nombre",
                          font=("Segoe UI", 12),
                          bg="#e8e8e8")

    preferences_label = tk.Label(preferences_frame,
                           text="Preferencias",
                           font=("Segoe UI", 16),
                           bg="#e8e8e8")

    first_n_range_label = tk.Label(preferences_frame,
                                  text="Inicio:",
                                  font=("Segoe UI", 12),
                                  bg="#e8e8e8")

    second_n_range_label = tk.Label(preferences_frame,
                                  text="Final:",
                                  font=("Segoe UI", 12),
                                  bg="#e8e8e8")
    

    range_label = tk.Label(preferences_frame,
                            text="Seleccione el rango (ALL para todo)",
                            font=("Segoe UI", 12),
                            bg="#e8e8e8")

    delimiter_label = tk.Label(preferences_frame,
                               text="Delimitador",
                               font=("Segoe UI", 12),
                               bg="#e8e8e8")

    backup_label = tk.Label(backup_frame,
                            text="Copia de seguridad",
                            font=("Segoe UI", 16),
                            bg="#e8e8e8")

    selecction_backup_label = tk.Label(backup_frame,
                            text="Marque la casilla si desea crear una copia de seguridad",
                            font=("Segoe UI", 12),
                            bg="#e8e8e8")

    bottom_label = tk.Label(bottom_frame,
                            text="Ejecución",
                            font=("Segoe UI", 16),
                            bg="#e8e8e8")

    version_label = tk.Label(bottom_frame,
                             text=f"{__version__}",
                             font=("Segoe UI", 10),
                             fg="gray")
        
    
    # Botones
    start_button = tk.Button(bottom_frame,
                            text="Iniciar",
                            font=("Segoe UI", 12),
                            relief="solid",
                            bd=1,
                            command=start)

    examine_button = tk.Button(text="Examinar",
                            font=("Segoe UI", 12),
                            relief="flat",
                            bd=1,
                            fg="#1a1a1a",
                            bg="#cccccc",
                            command=lambda: path_entry.insert(0, filedialog.askdirectory()))
    
    show_more_button = tk.Button(text="Mostrar más",
                                font=("Segoe UI", 12),
                                relief="solid",
                                bd=1,
                                state="disabled")
    
    hidden_button = tk.Button(text="Ocultar",
                              font=("Segoe UI", 12),
                              relief="solid",
                              bd=1)
    
    clear_button = tk.Button(text="Eliminar",
                            font=("Segoe UI", 12),
                            relief="solid",
                            bd=1,
                            command=clear_records)
    

    # Cajas de texto
    path_entry = tk.Entry(principal_frame,
                        width=50,
                        font=("Segoe UI", 11),
                        relief="flat",
                        fg="#4d4d4d",
                        bg="#fafafa",
                        bd=1)              

    name_entry = tk.Entry(principal_frame,
                        width=50,
                        font=("Segoe UI", 11),
                        relief="flat",
                        fg="#4d4d4d",
                        bg="#fafafa",
                        bd=1)
    
    first_n_range_entry = tk.Entry(preferences_frame,
                            width=5,
                            font=("Arial", 11),
                            relief="flat",
                            fg="#4d4d4d",
                            bg="#fafafa",
                            bd=1)
    
    second_n_range_entry = tk.Entry(preferences_frame,
                            width=5,
                            font=("Arial", 11),
                            relief="flat",
                            fg="#4d4d4d",
                            bg="#fafafa",
                            bd=1)

    record_text = tk.Text(root,
                        width=60,
                        height=5,
                        font=("Arial", 10),
                        relief="flat",
                        bd=1)


    # Combobox
    delimiter_combo = ttk.Combobox(preferences_frame, 
                                  values=["#", "-", "_", "ESPACIO", "ESPACIO + .", ".", "Otro"],
                                  state="readonly")

    delimiter_combo.set("#")

    delimiter_combo.bind("<<ComboboxSelected>>", other_options)


    # Checkbutton
    backup_var = tk.IntVar()

    backup_check = tk.Checkbutton(backup_frame,
                                  font=("Segoe UI", 12),
                                  bg="#e8e8e8",
                                  relief="flat",
                                  bd=1,
                                  variable=backup_var)

    
    


    # Mostrando las cajas o contenedores en la ventana principal
    principal_frame.grid(row=0, column=0, sticky="nsew")
    preferences_frame.grid(row=1, column=0, sticky="nsew")
    backup_frame.grid(row=2, column=0, sticky="nsew")
    bottom_frame.grid(row=3, column=0, sticky="nsew")

    # Mostrando los elementos
    name_and_rute_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=3)

    path_label.place(x=15, y=40)
    path_entry.place(x=16, y=65, width=350, height=25)
    examine_button.place(x=370, y=65, width=70, height=25)

    name_label.place(x=15, y=95)
    name_entry.place(x=16, y=120, width=350, height=25)


    preferences_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=3)
    
    range_label.place(x=15, y=40)

    first_n_range_label.place(x=16, y=70, width=50, height=25)
    first_n_range_entry.place(x=122, y=70, width=35, height=25)

    second_n_range_label.place(x=250, y=70, width=35, height=25)
    second_n_range_entry.place(x=350, y=70, width=35, height=25)

    delimiter_label.place(x=15, y=100)

    delimiter_combo.place(x=122, y=100, width=70, height=25)

    backup_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=3)

    selecction_backup_label.grid(row=1, column=0, sticky="w", padx=10, pady=3)
    backup_check.grid(row=1, column=1, sticky="w", padx=1, pady=3)

    bottom_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=3)
    start_button.place(relx=0.5, rely=1.0, x=0, y=-20, anchor="s", width=100, height=30)
    version_label.place(relx=1.0, rely=1.0, x=-10, y=-5, anchor="se")





    # Especificaciones del comporamiento de las cajas o contenedores
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=3)
    root.rowconfigure(1, weight=3)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=2)


    # Bucle principal
    root.mainloop()    

def main():
    create_gui()

if __name__ == "__main__":
    main()

#invalid_caracters = set('<>:"/\\|?*')
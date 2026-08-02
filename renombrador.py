import os
import ctypes
import functools
import shutil
import tkinter as tk
from tkinter.messagebox import showerror, askyesno, showwarning
from tkinter import filedialog
from tkinter import ttk
from datetime import datetime

__version__ = "1.0.1"

# Zona de funciones
# Función que compureba que el nombre ingresado no contiene carácteres inválidos
def invalid_character(text):
    characters = ['<','>',':','"','/',"\\",'|','?','*']

    if text is None:
        return False

    if any(char in characters for char in text):
        showwarning(title="Campo inválido",
                    message=f"No puede tener ese carácter, asegurarse que no se encuentre en la siguiente lista: {characters}")
        return True

    return False



# Obtener los nombres de los archivos en la ruta dada filtando sólo los archivos
def get_archives(rute):
    try:
        old_names = [f for f in os.listdir(rute) if os.path.isfile(os.path.join(rute, f))]

        return old_names
        
    except Exception as e: 
        showerror(title="Eroor",
                  message=f"Error al obtener los archivos: {e}")
        return[]


    
# Obteniendo el rango 
def get_range(start_value, end_value, old_names):
    if not start_value and not end_value:
        start_value = 1
        end_value = len(old_names)

    elif start_value and not end_value:
            end_value = len(old_names) + int(start_value) - 1

    elif not start_value and end_value:
            start_value = 1

    try:
        return int(start_value), int(end_value)

    except ValueError:
                showwarning(title="Campo inválido",
                            message="Error: Inicio y final deben ser números enteros.")
                return None, None



# Verificar que el rango de numeración sea correcto
def check_range(start, end, old_names):
        if start > end or start < 0 or end < 0 or end - start >= len(old_names):
            showwarning(title="Campo inválido",
                        message="El número de inicio debe ser menor o igual al número final y debe coincidir con la cantidad de archivos.")

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
            showwarning(title="Campo inválido",
                        message="Error: El archivo de origen no fue encontrado.")
        
        except PermissionError:
            showerror(title="Error",
                      message="Error: Permiso denegado.")

        except Exception as e:
            showerror(title="Error",
                      message=f"Ocurrió un error inesperado: {e}")



# Función para transformar la función de comparación de StrCmpLogicalW
# en una función que python pueda usar para ordenar de forma natural
# porque al parecer no hay otra forma de hacer esto sin meterte en los
# metadatos de los archivos COMO SI FUERA YO A HACKEAR UN PUTO COMIC PARA RENOMBRARLO
def sort_natural(old_names):
    natSort = functools.cmp_to_key(ctypes.windll.shlwapi.StrCmpLogicalW)

    # Ordenando los nombres viejos de forma natural gracias a la conversón
    old_names_sorted = sorted(old_names, key=natSort)

    return old_names_sorted


def check_existing_targets(rute, name, old_names_sorted, start, end, delimiter):
    for i in range(len(old_names_sorted)):
        current_num = i + start

        if current_num > end:
            break

        old_name = old_names_sorted[i]
        ext = os.path.splitext(old_name)[1]
        target_name = f"{name}{delimiter}{current_num}{ext}"
        target_path = os.path.join(rute, target_name)

        if os.path.exists(target_path) and target_name != old_name:
            return target_name

    return None


# Renombrando los archivos
def rename_archives(rute, name, old_names_sorted, start, end, delimiter):
    try:
        temp = []
        final_names = []
        records = []
        
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
            records.append((old_names_sorted[i], final_names[i]))
            
        return records
                    
    except Exception as e:
        showerror(title="Error",
            message=f"Error al renombrar los archivos: {e}")





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
    # Función principal del delimitador
    def get_delimiter():
        delimiter = delimiter_combo.get()

        if delimiter == "#":
            return " #"
        elif delimiter == "-":
            return " -"
        elif delimiter == "_":
            return " _"
        elif delimiter == "ESPACIO":
            return " "
        elif delimiter == "ESPACIO + .":
            return " ."
        elif delimiter == ".":
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



    # Función de acceso al registro
    def register_or_close(total):
        return askyesno(title="Renombrador Masivo",
                 message=f"Se han renombrado correctamente {total} archivos.\n¿Desea abrir el registro?")



    # Función que crea una ventana secundaria y mostrar el registro en ella
    def show_register(records, old_names_sorted, name, start_num, end_num, delimiter):
        log_window = tk.Toplevel()
        log_window.title("Registro")
        log_window.geometry("600x400")

        log_frame = tk.Frame(log_window)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        log_text = tk.Text(log_frame, wrap="word", state="normal")
        log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        log_text.configure(yscrollcommand=scrollbar.set)

        display_records = []

        if records:
            display_records = records
        else:
            for i in range(len(old_names_sorted)):
                current_num = i + start_num

                if current_num > end_num:
                    break

                old_name = old_names_sorted[i]
                ext = os.path.splitext(old_name)[1]
                new_name = f"{name}{delimiter}{current_num}{ext}"
                display_records.append((old_name, new_name))

        if display_records:
            for old_name, new_name in display_records:
                log_text.insert(tk.END, f"{old_name} -> {new_name}\n")
        else:
            log_text.insert(tk.END, "No se generaron registros.")

        log_text.config(state="disabled")



    # Función start
    def start():
        rute = path_entry.get().strip()
        name = name_entry.get().strip()
        start_value = first_n_range_entry.get().strip()
        end_value = second_n_range_entry.get().strip()
        delimiter = get_delimiter()

        if invalid_character(name):
            return
        
        if invalid_character(delimiter):
            return

        old_names = get_archives(rute)
        
        if not old_names:
            showwarning(title="Campo inválido",
                        message="Error: Asegúrese que la ruta sea correcta.")
        
            return

        start_num, end_num = get_range(start_value, end_value, old_names)

        if not check_range(start_num, end_num, old_names):
            return

        if backup_var.get() == 1:
            backup(rute, old_names)

        old_names_sorted = sort_natural(old_names)
        conflict_name = check_existing_targets(rute, name, old_names_sorted, start_num, end_num, delimiter)

        if conflict_name:
            showwarning(title="Campo inválido",
                        message=f"No se puede renombrar porque ya existe el archivo: {conflict_name}")
            return

        records = rename_archives(rute, name, old_names_sorted, start_num, end_num, delimiter)
        want_register = register_or_close((end_num - start_num) + 1)

        if want_register:
            show_register(records, old_names_sorted, name, start_num, end_num, delimiter)
        


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
                           text="Seleccione el rango (Dejar vacío implica selccionar todo)",
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
# Renombrador Masivo (Windows) — v0.3.1

¡Bienvenido! Este proyecto `Renombrador Masivo` es un script en Python diseñado para renombrar varios archivos en una carpeta con un nombre estándar y numeración secuencial, preservando las extensiones.

## 📝 Contexto

Este script nació para normalizar colecciones de archivos (por ejemplo cómics, fotos o documentos) con nombres inconsistentes. En vez de editar uno por uno, renombra automáticamente en bloque con numeración ordenada.

## 🔧 Qué hace

- Pide la ruta de la carpeta donde están los archivos.
- Pide el nombre base para los archivos.
- Verifica que la ruta exista.
- Permite seleccionar todos los archivos o un rango específico de numeración.
- Filtra solo los archivos (ignora carpetas) en la ruta especificada.
- Ordena los archivos en orden natural (1, 2, 10 en vez de 1, 10, 2) usando `StrCmpLogicalW` de Windows.
- Renombra cada archivo a: `NombreBase #<número><ext>` (preservando la extensión original del archivo).
- Si el nuevo nombre ya existe, omite ese archivo y continúa con los demás.
- Pregunta al usuario si desea continuar antes de ejecutar el renombrado.

## 🖥️ Requisitos

- Windows (usa `ctypes.windll.shlwapi.StrCmpLogicalW` para orden natural)
- Python 3

## ▶️ Uso

1. Coloca `renombrador.py` en cualquier ubicación.
2. Abre una terminal y ejecuta:

```bash
python renombrador.py
```

3. Responde a las preguntas:
   - `Ingrese la ruta donde se encuentran los archivos:` (ejemplo: `C:\MisComics`)
   - `Ingrese el nombre que desea para los archivos:` (ejemplo: `Mi Archivo`)
   - `Pulse 1 para seleccionar todos los archivos o pulse 2 para seleccionar un rango específico:`
     - Si eliges `1`, se numeran todos los archivos empezando en `1`.
     - Si eliges `2`, se te pedirá el número de inicio y el número final para la numeración.
   - `¿Desea continuar con el proceso de renombrado? (s/n):` para confirmar la ejecución.

4. El script renombrará los archivos existentes en la carpeta indicada con nombre y numeración secuencial.

## 🧠 Consideraciones

- Se valida que el inicio sea menor o igual al final y que ambos sean enteros no negativos.
- Si el rango de numeración excede la cantidad de archivos, el script detiene el proceso antes de renombrar.
- Si la ruta no existe, el script muestra un mensaje y finaliza.
- Si el nuevo nombre de archivo ya existe, se omite ese archivo y continúa con el siguiente.
- Si ocurre un error en `os.rename`, mostrará la excepción y no abortará en esa iteración.

## 💡 Mejora sugerida

- Añadir copia de seguridad de los archivos antes de renombrar.
- Añadir confirmación de usuario antes de ejecutar cambios definitivos.

---
# Renombrador Masivo (Windows) — v0.2.0

¡Bienvenido! Este proyecto `Renombrador Masivo` es un script en Python diseñado para renombrar varios archivos en una carpeta con un nombre estándar y numeración secuencial, preservando extensiones.

## 📝 Contexto

Este script nació para normalizar colecciones de archivos (por ejemplo cómics, fotos o documentos) con nombres inconsistente. En vez de editar uno por uno, renombra automáticamente en bloque con numeración ordenada.

## 🔧 Qué hace

- Pide la ruta de la carpeta donde están los archivos.
- Pide el nombre base para los archivos.
- Pide el número de inicio y el número final de la numeración.
- Ordena los archivos en orden natural (1, 2, 10 en vez de 1, 10, 2) usando `StrCmpLogicalW` de Windows.
- Renombra cada archivo a: `NombreBase #<número><ext>` (preservando la extensión original del archivo).
- Detiene el proceso al llegar al número final y muestra un mensaje claro.

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
   - `Ingrese el número de inicio para la numeración:`
   - `Ingrese el número final para la numeración:`

4. El script renombrará los archivos existentes en la carpeta indicada con nombre y numeración secuencial.

## 🧠 Consideraciones

- Se valida que el inicio sea menor o igual al final y ambos sean enteros no negativos.
- Si la ruta no existe, el script muestra un mensaje y finaliza.
- Si ocurre un error en `os.rename`, mostrará la excepción y no abortará en esa iteración.

## 💡 Mejora sugerida

- Añadir copia de seguridad de los archivos antes de renombrar.
- Añadir confirmación de usuario antes de ejecutar cambios definitivos.

---
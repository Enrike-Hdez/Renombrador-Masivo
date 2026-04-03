# Renombrador Masivo (Windows) — v0.1.1

¡Bienvenido! Este proyecto `Renombrador Masivo` es un script en Python diseñado para renombrar varios archivos en una carpeta con un nombre estándar y numeración secuencial.

## 📝 Contexto

Pos resulta que estaba revisando mi biblioteca 100% legal y cuando lo descargué tenían formatos que no me gustaban, o directamente errores ortográficos. De por sí como ya todo viene más o menos ordenado puedo tener un nombre mejor para un programa que estoy desarrollando a futuro, mientras me hace la vida más fácil y evita el toque Xd.

## 🔧 Qué hace

- Pide la ruta de la carpeta donde están los archivos con archivos (ejemplo comics).
- Pide el nombre base para los archivos.
- Ordena los archivos en orden natural (1, 2, 10 en vez de 1, 10, 2).
- Renombra cada archivo en la carpeta a: `NombreBase #1.cbr`, `NombreBase #2.cbr`, etc.

## 🖥️ Requisitos

- Windows (usa `ctypes.windll.shlwapi.StrCmpLogicalW` para orden natural, la otra opción que encontré fue... bueno, mirad los comentarios)
- Python 3

## ▶️ Uso

1. Coloca `renombrador.py` en cualquier ubicación.
2. Abre una terminal y ejecuta:

```bash
python renombrador.py
```

3. Responde a las preguntas:
   - `Ingrese la ruta donde se encuentran los comics:` (ejemplo: `C:\MisComics`)
   - `Ingrese el nombre que desea para los comics:` (ejemplo: `Mi Cómic`)

4. El script renombrará todos los archivos en la carpeta indicada.

## 🧠 Consideraciones

- Si hay errores en `os.rename`, mostrará el error y seguirá (o termina con excepción según el caso).

## 💡 Mejora sugerida

- Dejar copias de seguridad antes de renombrar.
- Filtrar solo archivos con extensiones de cómic: `.cbr`, `.cbz`, `.pdf`.
- Añadir confirmación para evitar cambios accidentales.

---

¡Listo! Ya puedes empezar a usarlo y adaptar a tu gusto.
# Renombrador Masivo (Windows) — v1.0.1

¡Bienvenido! Este proyecto ofrece una herramienta en Python para renombrar varios archivos de una carpeta con un nombre base y numeración secuencial, manteniendo sus extensiones.

## 📝 Contexto

Este proyecto está pensado para normalizar colecciones de archivos como cómics, fotos o documentos cuando sus nombres no siguen un patrón uniforme. En lugar de renombrarlos uno por uno, lo hace de forma automática y ordenada.

## 🔧 Qué hace

- Abre una interfaz gráfica con Tkinter.
- Permite elegir la carpeta que contiene los archivos mediante el botón Examinar.
- Solicita un nombre base para los archivos.
- Permite definir un rango de numeración con los campos Inicio y Final.
- Admite distintos delimitadores entre el nombre y el número, como `#`, `-`, `_`, espacio o un valor personalizado.
- Ordena los archivos de forma natural en Windows usando `StrCmpLogicalW`.
- Crea una copia de seguridad opcional dentro de la misma carpeta antes de renombrar.
- Valida caracteres no permitidos en el nombre base y en el delimitador.
- Renombra los archivos en dos pasos para evitar conflictos de nombre:
  1. `original -> temporal`
  2. `temporal -> final`
- Genera nombres con el formato `NombreBase<delimitador><número><extensión>`.
- Muestra un registro final con los cambios realizados si así se desea.

## 🖥️ Requisitos

- Windows
- Python 3.x (solo si vas a ejecutar el script desde código)
- Tkinter incluido con la instalación estándar de Python

## ▶️ Uso

### Opción 1: Ejecutable

1. Ejecuta el archivo `renombrador.exe` en cualquier equipo con Windows.
2. En la ventana:
   - Completa la ruta de la carpeta o usa el botón Examinar.
   - Escribe el nombre base que quieres usar.
   - Define el rango de numeración en Inicio y Final.
   - Elige un delimitador si lo deseas.
   - Marca la opción de copia de seguridad si quieres crear un respaldo.
   - Haz clic en Iniciar.

### Opción 2: Desde Python

1. Coloca el archivo `renombrador.py` en la ubicación que prefieras.
2. Abre una terminal y ejecuta:

```bash
python renombrador.py
```

3. Sigue los mismos pasos de la interfaz.

## 🧠 Consideraciones

- El rango debe cumplir que el valor inicial sea menor o igual al final y que no exceda la cantidad de archivos.
- Si el rango es menor que el total de archivos, solo se renombrarán los archivos incluidos en ese intervalo.
- La copia de seguridad se crea en una carpeta con el formato `backup DD-MM-YYYY HH-MM` dentro de la carpeta original.
- El renombrado usa nombres temporales intermedios para evitar colisiones entre archivos.
- Si un nombre final ya existe, la herramienta muestra una advertencia para evitar sobrescribir archivos.
- Si la ruta elegida no contiene archivos válidos, la aplicación mostrará un aviso en lugar de intentar seguir.

---

Mejoras en algún futuro improvable
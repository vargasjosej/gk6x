# 🚀 Cómo Ejecutar GK6X GUI en Fedora Kinoite

## ✅ Estado Actual

- ✅ Contenedor `gk6x-gui` creado
- ✅ Python 3 y Tkinter instalados en el contenedor
- ✅ Mono instalado en el contenedor
- ⚠️ Hay errores en tu `.bashrc` relacionados con brew (no afectan la GUI)

## 🖥️ EJECUTAR LA GUI AHORA

Abre tu terminal y ejecuta **UNO** de estos comandos:

### Opción 1: Comando Simple (Recomendado)

```bash
toolbox run -c gk6x-gui python3 /var/home/joss/Proyectos/gk6x/gk6x_gui.py
```

### Opción 2: Desde el directorio del proyecto

```bash
cd ~/Proyectos/gk6x
toolbox run -c gk6x-gui python3 gk6x_gui.py
```

### Opción 3: Entrando al contenedor primero

```bash
toolbox enter gk6x-gui
cd ~/Proyectos/gk6x
python3 gk6x_gui.py
```

## 📝 Crear Alias (Opcional pero Recomendado)

Para ejecutar la GUI más fácilmente en el futuro, agrega esto a tu `~/.bashrc`:

```bash
alias gk6x='toolbox run -c gk6x-gui python3 /var/home/joss/Proyectos/gk6x/gk6x_gui.py'
```

Luego solo necesitas escribir:
```bash
gk6x
```

## 🔧 Si Tienes Problemas

### Error: "No module named tkinter"
El contenedor ya tiene tkinter instalado. Si ves este error, asegúrate de estar ejecutando dentro del contenedor.

### Error: DISPLAY
Si no se abre la ventana, verifica tu variable DISPLAY:
```bash
echo $DISPLAY
# Debería mostrar algo como :0 o :1
```

Si está vacía:
```bash
export DISPLAY=:0
toolbox run -c gk6x-gui python3 /var/home/joss/Proyectos/gk6x/gk6x_gui.py
```

### Error: brew no encontrado
Ignora estos errores - son de tu configuración de bash pero no afectan la GUI.

## 🎨 Lo que Verás

Cuando ejecutes el comando, se abrirá una ventana con:

```
╔══════════════════════════════════════════╗
║    GK6X Keyboard Configurator            ║
╠══════════════════════════════════════════╣
║                                          ║
║  Device Status: [Checking...]            ║
║                                          ║
║  ┌────────────────────────────────────┐  ║
║  │  Quick Actions  │ Config Editor │  │  ║
║  │  Console │ Web GUI               │  │  ║
║  └────────────────────────────────────┘  ║
║                                          ║
║  [📝 Apply Configuration]                ║
║  [🔄 Reset to Default]                   ║
║  [📋 List Keys]                          ║
║  [🔍 Identify Keys]                      ║
║                                          ║
╚══════════════════════════════════════════╝
```

## 📦 Crear Script de Lanzamiento

Creé un script simple para ti:

```bash
#!/bin/bash
toolbox run -c gk6x-gui python3 /var/home/joss/Proyectos/gk6x/gk6x_gui.py
```

Guárdalo como `~/gk6x-launch.sh` y hazlo ejecutable:
```bash
chmod +x ~/gk6x-launch.sh
./gk6x-launch.sh
```

## 🐛 Debugging

Si quieres ver mensajes de error detallados:

```bash
toolbox run -c gk6x-gui python3 /var/home/joss/Proyectos/gk6x/gk6x_gui.py 2>&1 | tee gk6x.log
```

Esto guardará todo el output en `gk6x.log`.

## 📚 Más Información

- Ver `README.md` para documentación completa
- Ver `QUICKSTART.md` para ejemplos de uso
- El contenedor `gk6x-gui` tiene acceso a tu carpeta home automáticamente

## ✨ Resumen Rápido

```bash
# Ejecutar la GUI
toolbox run -c gk6x-gui python3 ~/Proyectos/gk6x/gk6x_gui.py

# O entrar al contenedor y ejecutar
toolbox enter gk6x-gui
python3 ~/Proyectos/gk6x/gk6x_gui.py
```

¡Eso es todo! 🎉

# 🚀 Guía de Inicio Rápido - GK6X

Esta guía te ayudará a comenzar a usar GK6X en menos de 5 minutos.

## ⚡ Inicio Ultra-Rápido (1 minuto)

```bash
# 1. Descargar y ejecutar
wget https://github.com/vargasjosej/gk6x/releases/latest/download/GK6X-x86_64.AppImage
chmod +x GK6X-x86_64.AppImage
./GK6X-x86_64.AppImage

# 2. Conecta tu teclado GK6X
# 3. ¡Listo! La app se abrirá y detectará tu teclado
```

## 📋 Requisitos Mínimos

- ✅ Linux (cualquier distribución)
- ✅ Python 3 (generalmente pre-instalado)
- ✅ Mono runtime: `sudo dnf install mono-core` (Fedora) o `sudo apt install mono-runtime` (Ubuntu)
- ✅ Teclado GK6X conectado por USB

## 🎯 Primeros Pasos

### 1. Ejecutar por Primera Vez

```bash
# Hacer ejecutable
chmod +x GK6X-x86_64.AppImage

# Ejecutar (puede necesitar sudo la primera vez)
./GK6X-x86_64.AppImage
# O con sudo si no tienes permisos USB:
sudo ./GK6X-x86_64.AppImage
```

### 2. Verificar Detección del Teclado

La aplicación debería mostrar:
```
Connected to device 'GK64S RGB' model:655491200 fw:v1.16
```

Si no detecta el teclado:
```bash
# Verificar que está conectado
lsusb | grep 1ea7

# Si aparece pero no se detecta, ejecutar con sudo
sudo ./GK6X-x86_64.AppImage
```

### 3. Usar las Acciones Rápidas

La pestaña "Quick Actions" tiene todo lo básico:

#### 📝 Aplicar Configuración
1. Crea un archivo de configuración (ver ejemplos abajo)
2. Guárdalo en la carpeta UserData con el nombre de tu modelo
3. Click en "Apply Configuration (Map)"
4. ¡Listo!

#### 🔄 Resetear a Default
- Click en "Reset to Default (Unmap)"
- Confirma
- Tu teclado vuelve a la configuración de fábrica

#### 📋 Ver Todas las Teclas
- Click en "List Keys (Dump Keys)"
- La consola mostrará todas las teclas disponibles
- Usa estos nombres en tu configuración

## 📝 Configuración Básica

### Ejemplo 1: Mapeo Simple

Archivo: `UserData/655491200.txt` (usa el ID de tu teclado)

```
# Intercambiar Caps Lock y Esc
CapsLock=Esc
Esc=CapsLock

# Tecla Windows actúa como Ctrl
LWin=LControl
```

### Ejemplo 2: Macros Útiles

```
# F1 = Copiar (Ctrl+C)
F1={LControl,C}

# F2 = Pegar (Ctrl+V)
F2={LControl,V}

# F3 = Abrir terminal (Ctrl+Alt+T)
F3={LControl,LAlt,T}

# F4 = Guardar (Ctrl+S)
F4={LControl,S}
```

### Ejemplo 3: Capas (Layers)

```
# Capa base normal
A=A
S=S
D=D
F=F

# Layer 1 (activada con Fn)
[Layer1]
A=Up      # A se convierte en Flecha Arriba
S=Down    # S se convierte en Flecha Abajo  
D=Left    # D se convierte en Flecha Izquierda
F=Right   # F se convierte en Flecha Derecha

# Layer 2 
[Layer2]
1=F1
2=F2
3=F3
4=F4
```

## 🔐 Configurar Permisos USB (Recomendado)

Para no tener que usar `sudo` cada vez:

```bash
# Crear archivo de reglas
sudo nano /etc/udev/rules.d/99-gk6x.rules

# Pegar estas líneas:
SUBSYSTEM=="input", GROUP="input", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE:="666", GROUP="plugdev"
KERNEL=="hidraw*", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE="0666", GROUP="plugdev"

# Guardar (Ctrl+O, Enter, Ctrl+X)

# Agregar tu usuario al grupo
sudo usermod -a -G plugdev $USER

# Recargar reglas
sudo udevadm control --reload-rules
sudo udevadm trigger

# Cerrar sesión y volver a entrar
```

## 🛠️ Instalación Opcional

Para instalar GK6X en el sistema (disponible desde el menú):

```bash
# Usando el script de instalación
./install.sh

# Selecciona opción 3 o 4 para instalación completa
# Luego ejecuta desde cualquier lugar:
gk6x
```

## 🔧 Tareas Comunes

### Cambiar Caps Lock por Ctrl

```
CapsLock=LControl
```

### Crear Atajos de Productividad

```
# Copiar/Pegar/Cortar en F1-F3
F1={LControl,C}
F2={LControl,V}
F3={LControl,X}

# Deshacer/Rehacer
F5={LControl,Z}
F6={LControl,Y}

# Guardar
F7={LControl,S}
```

### Teclas de Navegación (Vim-style)

```
[Layer1]
H=Left
J=Down
K=Up
L=Right
```

### Teclas Multimedia

```
F9=VolumeMute
F10=VolumeDown
F11=VolumeUp
F12=MediaPlayPause
```

## 🐛 Solución de Problemas Rápida

### No detecta el teclado
```bash
# 1. Verificar conexión
lsusb | grep 1ea7

# 2. Ejecutar con sudo
sudo ./GK6X-x86_64.AppImage

# 3. Ver permisos
ls -l /dev/hidraw*
```

### Error: "mono: command not found"
```bash
# Fedora/RHEL
sudo dnf install mono-core

# Ubuntu/Debian  
sudo apt install mono-runtime

# Arch
sudo pacman -S mono
```

### La configuración no se aplica
```bash
# 1. Verificar nombre de archivo (debe coincidir con ID del modelo)
# 2. Revisar sintaxis del archivo
# 3. Ver output en la consola (pestaña Console)
# 4. Intentar Unmap primero, luego Map
```

### GUI no abre
```bash
# Verificar Python
python3 --version

# Verificar Tkinter
python3 -m tkinter

# Si falta Tkinter:
sudo dnf install python3-tkinter  # Fedora
sudo apt install python3-tk       # Ubuntu
```

## 📚 Más Información

- **README completo**: [README.md](README.md)
- **Guía de compilación**: [BUILDING.md](BUILDING.md)
- **Documentación detallada**: [README_APPIMAGE.md](README_APPIMAGE.md)
- **Proyecto original**: [GK6X GitHub](https://github.com/pixeltris/GK6X)

## 💡 Tips Pro

1. **Backup de configuración**: Guarda copias de tus configs en Git
2. **Experimenta con capas**: Las capas son súper poderosas
3. **Macros complejos**: Puedes encadenar muchas teclas `{Key1,Key2,Key3,...}`
4. **Web GUI**: Si prefieres visual, usa la pestaña "Web GUI"
5. **Consola**: Siempre revisa la consola para ver qué pasó

## 🎓 Ejemplos Avanzados

### Programador Layout
```
# Símbolos frecuentes más accesibles
[Layer1]
J=LBracket    # [
K=RBracket    # ]
U=LBrace      # {
I=RBrace      # }
M=Minus       # -
Comma=Equal   # =
```

### Gaming Layer
```
[Layer2]
# WASD para flechas
W=Up
A=Left
S=Down
D=Right

# Q/E para PgUp/PgDn
Q=PageUp
E=PageDown

# Espacio para Enter
Space=Enter
```

---

**¿Necesitas más ayuda?** Abre un issue en [GitHub](https://github.com/vargasjosej/gk6x/issues)

¡Disfruta tu teclado personalizado! 🎹✨

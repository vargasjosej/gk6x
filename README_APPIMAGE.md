# GK6X AppImage - Configurador de Teclados GK6X para Linux

![GK6X Logo](gk6x.png)

## 📋 Descripción

Aplicación GUI moderna para configurar teclados mecánicos GK6X (GK61, GK64, GK84, etc.) en Linux.

Esta aplicación empaquetada como AppImage te permite:
- ✅ Mapear teclas personalizadas
- ✅ Crear macros complejos
- ✅ Configurar iluminación RGB
- ✅ Gestionar múltiples capas (layers)
- ✅ Interfaz gráfica intuitiva
- ✅ Acceso a la GUI web original
- ✅ Editor de configuración integrado

## 🚀 Características

- **Interfaz Moderna**: GUI oscura y amigable hecha con Python/Tkinter
- **Multiplataforma**: Basado en el proyecto GK6X original con soporte completo para Linux
- **Portátil**: AppImage auto-contenido, no requiere instalación
- **Editor Integrado**: Edita archivos de configuración directamente en la app
- **Consola en Tiempo Real**: Monitorea todas las operaciones
- **Acceso Web GUI**: Interfaz web visual incluida

## 📦 Requisitos del Sistema

### Mínimos:
- Linux (kernel 2.6+)
- Arquitectura x86_64
- ~150MB de espacio en disco
- USB 2.0+

### Software (generalmente pre-instalado):
- Python 3.6+
- Mono Runtime (para la lógica de backend)
- Acceso a dispositivos USB/HID

## 🔧 Instalación

### Método 1: Usar el AppImage Pre-compilado

1. Descarga el AppImage:
```bash
wget https://github.com/vargasjosej/gk6x/releases/download/v1.0/GK6X-x86_64.AppImage
chmod +x GK6X-x86_64.AppImage
```

2. Ejecuta:
```bash
./GK6X-x86_64.AppImage
```

### Método 2: Compilar desde el Código Fuente

1. Clona este repositorio:
```bash
git clone https://github.com/vargasjosej/gk6x.git
cd gk6x
```

2. Instala las dependencias:
```bash
sudo dnf install python3 mono-complete wget imagemagick
# O en Ubuntu/Debian:
# sudo apt install python3 mono-complete wget imagemagick
```

3. Ejecuta el script de compilación:
```bash
./build_appimage.sh
```

4. El AppImage se generará como `GK6X-x86_64.AppImage`

## 🔐 Permisos USB

Para acceder al teclado sin `sudo`, configura reglas udev:

1. Crea el archivo `/etc/udev/rules.d/99-gk6x.rules`:
```bash
sudo nano /etc/udev/rules.d/99-gk6x.rules
```

2. Agrega estas líneas:
```
SUBSYSTEM=="input", GROUP="input", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE:="666", GROUP="plugdev"
KERNEL=="hidraw*", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE="0666", GROUP="plugdev"
```

3. Agrega tu usuario al grupo `plugdev`:
```bash
sudo usermod -a -G plugdev $USER
```

4. Recarga las reglas udev:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

5. Reinicia o vuelve a conectar el teclado

## 📖 Uso

### Inicio Rápido

1. Conecta tu teclado GK6X
2. Ejecuta el AppImage
3. El dispositivo debería detectarse automáticamente
4. Usa las "Acciones Rápidas" para:
   - **Aplicar Configuración**: Mapea tu configuración personalizada
   - **Resetear**: Vuelve a la configuración de fábrica
   - **Listar Teclas**: Muestra todas las teclas disponibles
   - **Identificar Teclas**: Herramienta para encontrar nombres de teclas

### Editor de Configuración

1. Ve a la pestaña "Config Editor"
2. Haz clic en "Sample" para cargar un ejemplo
3. Edita la configuración según tus necesidades:

```
# Mapeo básico de teclas
A=B                    # La tecla A ahora escribe B

# Macros
F1={LControl,C}        # F1 ejecuta Ctrl+C
F2={LControl,LAlt,T}   # F2 ejecuta Ctrl+Alt+T

# Capas (Layers)
[Layer1]
A=C
B=D

[Layer2]
A=E
B=F
```

4. Guarda tu configuración
5. Aplica con "Map" en Acciones Rápidas

### Web GUI

1. Ve a la pestaña "Web GUI"
2. Haz clic en "Start Web GUI"
3. Tu navegador se abrirá automáticamente en http://localhost:6464
4. Configura visualmente tu teclado

## 🎯 Teclados Compatibles

- GK61
- GK64
- GK64S
- GK68XS
- GK84
- SK61
- Y otros teclados con chip GK6X

## 🐛 Resolución de Problemas

### El dispositivo no se detecta

1. Verifica que el teclado esté conectado:
```bash
lsusb | grep 1ea7
```

2. Comprueba los permisos:
```bash
ls -l /dev/hidraw*
```

3. Intenta ejecutar con sudo:
```bash
sudo ./GK6X-x86_64.AppImage
```

### Mono no está instalado

```bash
# Fedora/RHEL:
sudo dnf install mono-complete

# Ubuntu/Debian:
sudo apt install mono-complete

# Arch:
sudo pacman -S mono
```

### Error al compilar GK6X.exe

El script de compilación intenta compilar automáticamente. Si falla:

```bash
cd source_code
xbuild /p:Configuration=Release GK6X.sln
# O intenta:
msbuild /p:Configuration=Release GK6X.sln
```

## 📚 Documentación Adicional

- [Documentación oficial GK6X](https://github.com/pixeltris/GK6X)
- [Ejemplos de configuración](source_code/Build/UserData/)
- [Parámetros de línea de comandos](source_code/README-CommandlineParameters.md)

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

El proyecto GK6X original está licenciado bajo MIT por pixeltris.

## 🙏 Agradecimientos

- [pixeltris/GK6X](https://github.com/pixeltris/GK6X) - Proyecto original
- [wgwoods/gk64-python](https://github.com/wgwoods/gk64-python) - Trabajo de ingeniería inversa
- Comunidad de AppImage
- Todos los contribuidores

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/vargasjosej/gk6x/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/vargasjosej/gk6x/discussions)

## 🔄 Changelog

### v1.0 (2025-11-05)
- ✨ Lanzamiento inicial
- 🎨 GUI moderna con Tkinter
- 📦 Empaquetado AppImage
- 🔧 Editor de configuración integrado
- 🌐 Soporte para Web GUI
- 📝 Consola de monitoreo en tiempo real
- 🚀 Detección automática de dispositivos

---

**Hecho con ❤️ para la comunidad de teclados mecánicos**

# 🔧 Instalación de Tkinter en Fedora Kinoite

Tu sistema es **Fedora Kinoite 43** (inmutable), por lo que la instalación de paquetes es diferente.

## 📋 Problema Detectado

```
ModuleNotFoundError: No module named 'tkinter'
```

Python 3.14 está instalado, pero falta el módulo Tkinter necesario para la GUI.

## ✅ Soluciones

### Opción 1: Instalar Tkinter con rpm-ostree (Recomendado)

```bash
# Instalar python3-tkinter en el sistema
rpm-ostree install python3-tkinter

# Reiniciar para aplicar cambios
systemctl reboot
```

Después del reinicio:
```bash
cd /var/home/joss/Proyectos/gk6x
python3 gk6x_gui.py
```

### Opción 2: Usar Toolbox/Distrobox (Sin reinicio)

Crear un contenedor con todas las dependencias:

```bash
# Crear toolbox
toolbox create gk6x-dev

# Entrar al toolbox
toolbox enter gk6x-dev

# Instalar dependencias dentro del toolbox
sudo dnf install python3-tkinter mono-complete

# Ejecutar la GUI desde el toolbox
cd /var/home/joss/Proyectos/gk6x
python3 gk6x_gui.py
```

### Opción 3: Usar Flatpak con Python

```bash
# Instalar Python runtime de Flatpak
flatpak install flathub org.freedesktop.Platform//23.08

# Ejecutar Python con Tkinter desde Flatpak
flatpak run --command=python3 --filesystem=host org.freedesktop.Platform//23.08 /var/home/joss/Proyectos/gk6x/gk6x_gui.py
```

### Opción 4: Crear un contenedor Docker

```bash
# Crear Dockerfile
cat > Dockerfile << 'EOF'
FROM fedora:43
RUN dnf install -y python3 python3-tkinter mono-complete
WORKDIR /app
COPY . /app
CMD ["python3", "gk6x_gui.py"]
EOF

# Build y ejecutar
podman build -t gk6x-gui .
podman run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix gk6x-gui
```

## 🚀 Solución Rápida (Recomendada)

La manera más simple para Fedora Kinoite es usar **Toolbox**:

```bash
# Un solo comando para crear y entrar
toolbox create -y gk6x && toolbox enter gk6x

# Dentro del toolbox
sudo dnf install -y python3-tkinter mono-complete
cd /var/home/joss/Proyectos/gk6x
python3 gk6x_gui.py
```

## 📝 Verificación

Después de instalar, verifica:

```bash
python3 -m tkinter
# Debería abrir una ventana pequeña de prueba
```

## 🎯 Estado Actual del Proyecto

✅ Código de la GUI completado
✅ AppImage generado  
✅ Documentación completa
⚠️ Tkinter necesita instalación en tu sistema
✅ El AppImage debería funcionar (incluye dependencias)

## 💡 Nota sobre AppImage

El AppImage **debería funcionar** incluso sin Tkinter del sistema porque incluye sus propias dependencias. Prueba:

```bash
cd /var/home/joss/Proyectos/gk6x
./GK6X-x86_64.AppImage
```

Si el AppImage tampoco funciona en Kinoite, usa la opción de Toolbox arriba.

## 🔗 Referencias

- [Fedora Silverblue/Kinoite Docs](https://docs.fedoraproject.org/en-US/fedora-silverblue/)
- [Toolbox Documentation](https://containertoolbx.org/)
- [rpm-ostree Documentation](https://coreos.github.io/rpm-ostree/)

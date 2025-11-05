# Guía de Compilación - GK6X AppImage

Esta guía detalla el proceso de compilación del AppImage de GK6X paso a paso.

## Requisitos Previos

### Sistema Operativo
- Linux (probado en Fedora 43, pero debería funcionar en cualquier distribución)
- Arquitectura x86_64

### Herramientas Requeridas

```bash
# Fedora/RHEL/CentOS:
sudo dnf install -y \
    python3 \
    mono-complete \
    wget \
    git \
    imagemagick \
    xbuild \
    msbuild

# Ubuntu/Debian:
sudo apt install -y \
    python3 \
    mono-complete \
    wget \
    git \
    imagemagick \
    mono-xbuild

# Arch Linux:
sudo pacman -S \
    python3 \
    mono \
    wget \
    git \
    imagemagick
```

## Proceso de Compilación

### 1. Preparar el Entorno

```bash
# Clonar el repositorio
git clone https://github.com/vargasjosej/gk6x.git
cd gk6x

# Verificar que todos los archivos están presentes
ls -la
```

Deberías ver:
- `gk6x_gui.py` - La aplicación GUI en Python
- `build_appimage.sh` - Script de compilación
- `AppRun` - Script de ejecución del AppImage
- `gk6x.desktop` - Archivo desktop para el sistema
- `source_code/` - Código fuente de GK6X

### 2. Compilar el Backend de GK6X

El backend está escrito en C# y usa Mono:

```bash
cd source_code

# Método 1: Usando xbuild (recomendado para Mono antiguo)
xbuild /p:Configuration=Release GK6X.sln

# Método 2: Usando msbuild (para Mono moderno)
msbuild /p:Configuration=Release GK6X.sln

# Método 3: Si los anteriores fallan
xbuild /p:TargetFrameworkVersion=v4.5 /p:TargetFrameworkProfile="" GK6X.sln

cd ..
```

Verifica que se creó `source_code/Build/GK6X.exe`:
```bash
ls -l source_code/Build/GK6X.exe
```

### 3. Ejecutar el Script de Compilación

```bash
# Hacer ejecutable (si no lo es ya)
chmod +x build_appimage.sh

# Ejecutar la compilación
./build_appimage.sh
```

El script hará lo siguiente:
1. ✅ Verificar dependencias
2. ✅ Limpiar compilaciones anteriores
3. ✅ Crear estructura AppDir
4. ✅ Copiar archivos Python
5. ✅ Copiar ejecutables C#/Mono
6. ✅ Copiar librerías compartidas
7. ✅ Crear icono (si ImageMagick está disponible)
8. ✅ Descargar appimagetool
9. ✅ Empaquetar todo en AppImage

### 4. Resultado

Si todo va bien, verás:
```
=== Build Complete ===
AppImage created: GK6X-x86_64.AppImage
```

## Estructura del AppImage

```
GK6X.AppDir/
├── AppRun                              # Script de ejecución principal
├── gk6x.desktop                        # Desktop entry
├── gk6x.png                           # Icono
└── usr/
    ├── bin/
    │   ├── gk6x_gui                   # GUI Python
    │   ├── gk6x                       # Wrapper CLI
    │   └── python3                    # Python runtime
    ├── lib/
    │   ├── mono/                      # Runtime Mono
    │   │   ├── 4.5/
    │   │   └── gac/
    │   └── *.so                       # Librerías compartidas
    ├── etc/
    │   └── mono/                      # Configuración Mono
    └── share/
        ├── gk6x/                      # Código fuente GK6X
        │   └── Build/
        │       ├── GK6X.exe
        │       ├── UserData/
        │       └── Data/
        ├── applications/
        └── icons/
```

## Solución de Problemas

### Error: "mono: command not found"

```bash
# Instalar Mono
sudo dnf install mono-complete  # Fedora
sudo apt install mono-complete  # Ubuntu
```

### Error: "xbuild: command not found"

```bash
# Fedora
sudo dnf install mono-devel

# Ubuntu
sudo apt install mono-xbuild
```

### Error al compilar GK6X.sln

Algunos mensajes de warning son normales. Si falla completamente:

```bash
# Verificar versión de Mono
mono --version

# Intentar con diferentes targets
xbuild /p:TargetFrameworkVersion=v4.5 GK6X.sln
xbuild /p:TargetFrameworkVersion=v4.0 GK6X.sln
```

### Error: "appimagetool: not found"

El script descarga automáticamente appimagetool. Si falla:

```bash
# Descargar manualmente
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Renombrar si es necesario
mv appimagetool-x86_64.AppImage appimagetool-$(uname -m).AppImage
```

### El AppImage no ejecuta

```bash
# Verificar permisos
chmod +x GK6X-x86_64.AppImage

# Probar con verbose
./GK6X-x86_64.AppImage --appimage-debug

# Extraer contenido para debug
./GK6X-x86_64.AppImage --appimage-extract
cd squashfs-root
./AppRun
```

### Faltan librerías Mono

```bash
# Verificar qué librerías Mono están instaladas
ls /usr/lib64/mono/
ls /usr/lib/mono/

# Instalar paquetes adicionales si es necesario
sudo dnf install mono-core mono-devel libgdiplus
```

## Compilación Personalizada

### Cambiar el Icono

1. Crea o descarga un icono PNG de 256x256:
```bash
# Ejemplo con ImageMagick
convert -size 256x256 xc:transparent \
    -fill "#00ff88" \
    -draw "roundrectangle 20,20 236,236 20,20" \
    -fill white -pointsize 80 -gravity center \
    -annotate +0+0 "GK6X" \
    gk6x.png
```

2. Coloca `gk6x.png` en el directorio raíz antes de compilar

### Modificar la GUI

Edita `gk6x_gui.py` y recompila:

```bash
# Editar
nano gk6x_gui.py

# Recompilar
./build_appimage.sh
```

### Incluir Configuraciones Personalizadas

Agrega tus configuraciones en `source_code/Build/UserData/` antes de compilar:

```bash
cp mi_config.txt source_code/Build/UserData/
./build_appimage.sh
```

## Optimización del Tamaño

El AppImage puede ser grande (~150-200 MB). Para reducirlo:

### 1. Usar UPX para comprimir binarios

```bash
sudo dnf install upx
cd GK6X.AppDir/usr/lib
upx --best *.so 2>/dev/null || true
```

### 2. Eliminar archivos innecesarios de Mono

```bash
cd GK6X.AppDir/usr/lib/mono
# Eliminar locales no necesarios
rm -rf gac/I18N.*
# Eliminar assemblies de desarrollo
rm -rf gac/Microsoft.Build.*
```

### 3. Recompilar el AppImage

```bash
ARCH=x86_64 ./appimagetool-x86_64.AppImage GK6X.AppDir GK6X-x86_64.AppImage
```

## Testing

### Prueba Básica

```bash
# Ejecutar el AppImage
./GK6X-x86_64.AppImage

# Debería abrir la GUI
```

### Prueba con Dispositivo

1. Conecta un teclado GK6X
2. Verifica detección:
```bash
lsusb | grep 1ea7
```
3. Ejecuta el AppImage (posiblemente con sudo)
4. La GUI debería mostrar "Device connected"

### Prueba de Funcionalidades

- [ ] GUI se abre correctamente
- [ ] Dispositivo se detecta
- [ ] Dump Keys funciona
- [ ] Find Keys funciona
- [ ] Cargar/Guardar configuración funciona
- [ ] Map/Unmap ejecuta sin errores
- [ ] Web GUI inicia (puerto 6464)
- [ ] Consola muestra output correctamente

## CI/CD (Opcional)

Para automatizar las compilaciones con GitHub Actions:

```yaml
name: Build AppImage

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y mono-complete python3 wget imagemagick
    
    - name: Build GK6X
      run: |
        cd source_code
        xbuild /p:Configuration=Release GK6X.sln
        cd ..
    
    - name: Build AppImage
      run: ./build_appimage.sh
    
    - name: Upload AppImage
      uses: actions/upload-artifact@v2
      with:
        name: GK6X-AppImage
        path: GK6X-*.AppImage
```

## Mantenimiento

### Actualizar GK6X Source

```bash
cd source_code
git pull origin master
cd ..
./build_appimage.sh
```

### Actualizar Python GUI

```bash
# Editar gk6x_gui.py
nano gk6x_gui.py

# Probar sin compilar
python3 gk6x_gui.py

# Cuando funcione, recompilar AppImage
./build_appimage.sh
```

## Recursos Adicionales

- [Documentación AppImage](https://docs.appimage.org/)
- [Mono Documentation](https://www.mono-project.com/docs/)
- [GK6X Original](https://github.com/pixeltris/GK6X)

---

**¿Problemas?** Abre un issue en: https://github.com/vargasjosej/gk6x/issues

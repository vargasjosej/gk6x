# 🚀 Guía de Publicación - GK6X Linux GUI

Esta guía te ayudará a publicar el proyecto en GitHub y distribuir el AppImage.

## 📋 Pre-requisitos

- [x] Código commiteado en Git
- [x] AppImage compilado y probado
- [x] Documentación completa
- [ ] Teclado GK6X para testing final (recomendado)

## 🔄 Pasos para Publicar

### 1. Push al Repositorio Remoto

```bash
cd /var/home/joss/Proyectos/gk6x

# Verificar estado
git status
git log --oneline -3

# Push a GitHub
git push origin main
```

### 2. Crear un Release en GitHub

#### Opción A: Usando GitHub CLI (gh)

```bash
# Crear release v1.0
gh release create v1.0 \
  --title "GK6X Linux GUI v1.0" \
  --notes-file RELEASE_NOTES.md \
  GK6X-x86_64.AppImage

# O crear release interactivo
gh release create v1.0 --generate-notes
```

#### Opción B: Usando la Web de GitHub

1. Ve a tu repositorio: https://github.com/vargasjosej/gk6x
2. Click en "Releases" (barra derecha)
3. Click en "Create a new release"
4. Configurar:
   - **Tag version**: `v1.0`
   - **Release title**: `GK6X Linux GUI v1.0`
   - **Description**: Ver RELEASE_NOTES.md abajo
   - **Attach files**: Sube `GK6X-x86_64.AppImage`
5. Click "Publish release"

### 3. Release Notes Template

Copia esto para las release notes:

```markdown
# GK6X Linux GUI v1.0 🎉

Primera versión estable de GK6X Linux GUI - Aplicación moderna con AppImage para configurar teclados mecánicos GK6X.

## 🎯 Highlights

- ✨ Interfaz gráfica moderna con Python/Tkinter
- 📦 AppImage portable (48 MB)
- 🔧 Configuración completa de teclas, macros y capas
- 📝 Editor de configuración integrado
- 🖥️ Console de monitoreo en tiempo real
- 🌐 Soporte para Web GUI original
- 📚 Documentación completa

## 📥 Descarga

**[⬇️ GK6X-x86_64.AppImage](https://github.com/vargasjosej/gk6x/releases/download/v1.0/GK6X-x86_64.AppImage)** (48 MB)

```bash
# Descargar y ejecutar
wget https://github.com/vargasjosej/gk6x/releases/download/v1.0/GK6X-x86_64.AppImage
chmod +x GK6X-x86_64.AppImage
./GK6X-x86_64.AppImage
```

## 🎯 Teclados Compatibles

- GK61 / SK61
- GK64 / GK64S
- GK68XS
- GK84
- Otros con chip GK6X

## 📖 Documentación

- [README](https://github.com/vargasjosej/gk6x#readme)
- [Quick Start Guide](https://github.com/vargasjosej/gk6x/blob/main/QUICKSTART.md)
- [Building Guide](https://github.com/vargasjosej/gk6x/blob/main/BUILDING.md)
- [AppImage Guide](https://github.com/vargasjosej/gk6x/blob/main/README_APPIMAGE.md)

## ⚙️ Requisitos

- Linux (cualquier distribución)
- Python 3.6+
- Mono runtime: `sudo dnf install mono-core` (Fedora) o `sudo apt install mono-runtime` (Ubuntu)

## 🐛 Issues Conocidos

- Requiere permisos USB (ejecutar con sudo o configurar udev rules)
- Web GUI tiene limitaciones (usar config editor para funcionalidad completa)

## 🙏 Agradecimientos

Basado en el excelente proyecto [GK6X](https://github.com/pixeltris/GK6X) por [@pixeltris](https://github.com/pixeltris)

## 📝 Changelog

### Added
- Interfaz gráfica moderna con 4 pestañas
- Editor de configuración integrado
- Console de output en tiempo real
- Sistema de build automatizado con AppImage
- Script de instalación interactivo
- Documentación completa (4 guías)
- Soporte para permisos USB con udev rules
- Icono y desktop entry

### Technical
- Python 3.14 + Tkinter
- Mono runtime para backend C#
- AppImage packaging
- Auto-descarga de binarios pre-compilados
```

## 4. Actualizar el README Principal

Después de crear el release, actualiza el README con el link de descarga real:

```bash
# Editar README.md
nano README.md

# Cambiar esta línea:
# **[⬇️ Descargar GK6X-x86_64.AppImage](GK6X-x86_64.AppImage)** (48 MB)

# Por:
# **[⬇️ Descargar GK6X-x86_64.AppImage](https://github.com/vargasjosej/gk6x/releases/download/v1.0/GK6X-x86_64.AppImage)** (48 MB)

# Commit y push
git add README.md
git commit -m "Update download link to v1.0 release"
git push origin main
```

## 5. Promoción (Opcional)

### Comunidades donde compartir:

1. **Reddit**
   - r/MechanicalKeyboards
   - r/linux
   - r/linuxhardware

   ```
   Título: [Project] GK6X Linux GUI - Modern AppImage app for GK6X keyboard configuration
   ```

2. **GitHub**
   - Considera agregar a AppImageHub
   - Abre issue en pixeltris/GK6X mencionando tu fork

3. **Discord/Foros**
   - Comunidades de teclados mecánicos
   - Foros de Linux

### Template de Anuncio:

```markdown
# 🎹 GK6X Linux GUI v1.0 Released!

I've created a modern GUI app with AppImage for configuring GK6X keyboards on Linux!

## Features:
✅ Modern dark UI with Python/Tkinter
✅ Portable AppImage (no installation needed)
✅ Config editor + real-time console
✅ Full keyboard configuration support
✅ udev rules setup included

## Download:
https://github.com/vargasjosej/gk6x/releases/tag/v1.0

Based on the excellent GK6X project by @pixeltris

#mechanicalkeyboards #linux #opensource #gk6x
```

## 📊 Verificaciones Post-Release

Después de publicar, verifica:

- [ ] El release aparece en la página de releases
- [ ] El AppImage se puede descargar
- [ ] El link de descarga en el README funciona
- [ ] Las badges de GitHub aparecen correctamente
- [ ] La documentación se renderiza correctamente

## 🔄 Actualizaciones Futuras

Para versiones futuras (v1.1, v1.2, etc.):

```bash
# 1. Hacer cambios
git add .
git commit -m "Fix: descripción del cambio"

# 2. Actualizar versión en archivos
# - gk6x_gui.py (línea de versión si existe)
# - README.md (número de versión)

# 3. Compilar nuevo AppImage
./build_appimage.sh

# 4. Crear nuevo release
git tag v1.1
git push origin v1.1
gh release create v1.1 --notes "Changelog de v1.1" GK6X-x86_64.AppImage
```

## 📝 Checklist de Release

Usa esto antes de cada release:

- [ ] Código funciona correctamente
- [ ] AppImage compilado y probado
- [ ] Versión actualizada en todos los archivos
- [ ] CHANGELOG actualizado
- [ ] Documentación actualizada
- [ ] Commit y push realizados
- [ ] Tag creado
- [ ] Release publicado en GitHub
- [ ] AppImage adjunto al release
- [ ] README actualizado con link de descarga
- [ ] Release notes completas
- [ ] Anuncio en comunidades (opcional)

## 🆘 Solución de Problemas

### Error al crear release

```bash
# Verificar que gh esté autenticado
gh auth status

# Re-autenticar si es necesario
gh auth login
```

### No se puede subir el AppImage (muy grande)

GitHub permite archivos hasta 2GB. Si el AppImage es muy grande:

1. Optimiza el tamaño (ver BUILDING.md)
2. Usa GitHub Large File Storage (LFS)
3. Aloja en otro servicio (SourceForge, etc.)

### Tag ya existe

```bash
# Eliminar tag local
git tag -d v1.0

# Eliminar tag remoto
git push origin :refs/tags/v1.0

# Crear nuevo tag
git tag v1.0
git push origin v1.0
```

## 📞 Soporte

Si tienes problemas publicando:
- Revisa la [documentación de GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- Abre un issue en el proyecto
- Contacta a través de GitHub

---

**¡Buena suerte con el release!** 🚀

Una vez publicado, no olvides actualizar este archivo (RELEASE.md) marcando los pasos completados.

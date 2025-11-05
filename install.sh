#!/bin/bash
# Instalador opcional para GK6X AppImage
# Este script instala el AppImage en el sistema y configura los permisos USB

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   GK6X Linux Installer                 ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}No ejecutes este script como root (sin sudo)${NC}"
    exit 1
fi

# Find AppImage
APPIMAGE=$(find . -name "GK6X-*.AppImage" -type f | head -n 1)

if [ -z "$APPIMAGE" ]; then
    echo -e "${RED}Error: No se encontró el AppImage en el directorio actual${NC}"
    echo "Asegúrate de estar en el directorio del proyecto o descarga el AppImage primero"
    exit 1
fi

echo -e "${GREEN}✓ AppImage encontrado: $APPIMAGE${NC}"
echo ""

# Ask what to install
echo "¿Qué deseas instalar?"
echo "1) Solo el AppImage en ~/.local/bin"
echo "2) AppImage + Reglas udev (permisos USB)"
echo "3) AppImage + Reglas udev + Icono de escritorio"
echo "4) Instalación completa (todo lo anterior + mono-runtime)"
echo ""
read -p "Selecciona una opción [1-4]: " choice

case $choice in
    1|2|3|4)
        echo ""
        ;;
    *)
        echo -e "${RED}Opción inválida${NC}"
        exit 1
        ;;
esac

# Install AppImage
echo -e "${YELLOW}[1/4] Instalando AppImage...${NC}"
mkdir -p ~/.local/bin
cp "$APPIMAGE" ~/.local/bin/gk6x.AppImage
chmod +x ~/.local/bin/gk6x.AppImage
echo -e "${GREEN}✓ AppImage instalado en ~/.local/bin/gk6x.AppImage${NC}"

# Create symlink
ln -sf ~/.local/bin/gk6x.AppImage ~/.local/bin/gk6x 2>/dev/null || true
echo -e "${GREEN}✓ Enlace simbólico creado: ~/.local/bin/gk6x${NC}"

# Add to PATH if needed
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo -e "${YELLOW}⚠ ~/.local/bin no está en tu PATH${NC}"
    echo "Agrega esta línea a tu ~/.bashrc o ~/.zshrc:"
    echo -e "${BLUE}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
    echo ""
fi

if [ "$choice" -ge 2 ]; then
    # Install udev rules
    echo ""
    echo -e "${YELLOW}[2/4] Configurando reglas udev...${NC}"
    
    UDEV_RULES="/etc/udev/rules.d/99-gk6x.rules"
    
    if [ -f "$UDEV_RULES" ]; then
        echo -e "${YELLOW}Las reglas udev ya existen. ¿Sobrescribir? [s/N]${NC}"
        read -p "> " overwrite
        if [[ "$overwrite" =~ ^[Ss]$ ]]; then
            sudo tee "$UDEV_RULES" > /dev/null << 'EOF'
# GK6X Keyboard USB permissions
SUBSYSTEM=="input", GROUP="input", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE:="666", GROUP="plugdev"
KERNEL=="hidraw*", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE="0666", GROUP="plugdev"
EOF
            echo -e "${GREEN}✓ Reglas udev actualizadas${NC}"
        else
            echo -e "${YELLOW}⊘ Reglas udev no modificadas${NC}"
        fi
    else
        sudo tee "$UDEV_RULES" > /dev/null << 'EOF'
# GK6X Keyboard USB permissions
SUBSYSTEM=="input", GROUP="input", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE:="666", GROUP="plugdev"
KERNEL=="hidraw*", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE="0666", GROUP="plugdev"
EOF
        echo -e "${GREEN}✓ Reglas udev creadas${NC}"
    fi
    
    # Add user to plugdev group
    if groups | grep -q plugdev; then
        echo -e "${GREEN}✓ Ya estás en el grupo plugdev${NC}"
    else
        sudo usermod -a -G plugdev $USER
        echo -e "${GREEN}✓ Agregado al grupo plugdev${NC}"
        echo -e "${YELLOW}⚠ Necesitas cerrar sesión y volver a entrar para que los cambios surtan efecto${NC}"
    fi
    
    # Reload udev rules
    sudo udevadm control --reload-rules
    sudo udevadm trigger
    echo -e "${GREEN}✓ Reglas udev recargadas${NC}"
fi

if [ "$choice" -ge 3 ]; then
    # Install desktop entry
    echo ""
    echo -e "${YELLOW}[3/4] Instalando icono de escritorio...${NC}"
    
    mkdir -p ~/.local/share/applications
    mkdir -p ~/.local/share/icons/hicolor/256x256/apps
    
    # Copy icon if exists
    if [ -f "gk6x.png" ]; then
        cp gk6x.png ~/.local/share/icons/hicolor/256x256/apps/
        echo -e "${GREEN}✓ Icono copiado${NC}"
    else
        echo -e "${YELLOW}⚠ Icono no encontrado (gk6x.png)${NC}"
    fi
    
    # Create desktop entry
    cat > ~/.local/share/applications/gk6x.desktop << EOF
[Desktop Entry]
Name=GK6X Configurator
Comment=Configure GK6X Keyboards (GK61, GK64, GK84)
Exec=$HOME/.local/bin/gk6x.AppImage
Icon=gk6x
Type=Application
Categories=Utility;Settings;HardwareSettings;
Terminal=false
StartupNotify=true
Keywords=keyboard;gk6x;gk61;gk64;gk84;configuration;macro;lighting;
EOF
    
    # Update desktop database
    update-desktop-database ~/.local/share/applications 2>/dev/null || true
    
    echo -e "${GREEN}✓ Entrada de escritorio creada${NC}"
    echo -e "${GREEN}✓ Ahora puedes encontrar GK6X en tu menú de aplicaciones${NC}"
fi

if [ "$choice" -eq 4 ]; then
    # Install mono-runtime
    echo ""
    echo -e "${YELLOW}[4/4] Instalando mono-runtime...${NC}"
    
    if command -v mono &> /dev/null; then
        echo -e "${GREEN}✓ mono-runtime ya está instalado${NC}"
        mono --version | head -1
    else
        echo "Detectando distribución..."
        
        if [ -f /etc/fedora-release ]; then
            echo "Fedora/RHEL detectado"
            sudo dnf install -y mono-core mono-devel
        elif [ -f /etc/debian_version ]; then
            echo "Debian/Ubuntu detectado"
            sudo apt update
            sudo apt install -y mono-runtime mono-devel
        elif [ -f /etc/arch-release ]; then
            echo "Arch Linux detectado"
            sudo pacman -S --noconfirm mono
        else
            echo -e "${YELLOW}⚠ Distribución no reconocida. Instala mono-runtime manualmente${NC}"
        fi
        
        if command -v mono &> /dev/null; then
            echo -e "${GREEN}✓ mono-runtime instalado correctamente${NC}"
        else
            echo -e "${RED}✗ Error al instalar mono-runtime${NC}"
        fi
    fi
fi

# Final message
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Instalación Completada! ✓           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Para ejecutar GK6X:"
echo -e "  ${BLUE}gk6x${NC}                      (desde terminal)"
echo -e "  ${BLUE}~/.local/bin/gk6x.AppImage${NC}  (ruta completa)"

if [ "$choice" -ge 3 ]; then
    echo -e "  ${BLUE}Menú de aplicaciones${NC}       (busca 'GK6X')"
fi

echo ""
echo "Documentación:"
echo -e "  ${BLUE}https://github.com/vargasjosej/gk6x${NC}"
echo ""

if [ "$choice" -ge 2 ]; then
    echo -e "${YELLOW}⚠ IMPORTANTE: Si acabas de ser agregado al grupo 'plugdev',${NC}"
    echo -e "${YELLOW}   necesitas cerrar sesión y volver a entrar para usar el teclado sin sudo${NC}"
    echo ""
fi

echo -e "¿Deseas ejecutar GK6X ahora? [s/N]"
read -p "> " run_now

if [[ "$run_now" =~ ^[Ss]$ ]]; then
    echo -e "${BLUE}Iniciando GK6X...${NC}"
    ~/.local/bin/gk6x.AppImage &
fi

echo ""
echo -e "${GREEN}¡Gracias por usar GK6X!${NC}"

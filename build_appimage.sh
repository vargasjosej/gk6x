#!/bin/bash
# Build script for GK6X AppImage

set -e

echo "=== Building GK6X AppImage ==="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="GK6X"
APP_DIR="GK6X.AppDir"
ARCH=$(uname -m)

# Check dependencies
echo -e "${YELLOW}Checking dependencies...${NC}"

check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        echo "Install with: sudo dnf install $2"
        exit 1
    fi
}

check_command python3 python3
check_command wget wget

# Check for mono (optional - we'll download prebuilt if not available)
if ! command -v mono &> /dev/null; then
    echo -e "${YELLOW}Warning: mono is not installed${NC}"
    echo "The AppImage will download prebuilt GK6X binaries."
    echo "To build from source, install: sudo dnf install mono-complete"
    MONO_AVAILABLE=false
else
    echo -e "${GREEN}Mono found: $(mono --version | head -1)${NC}"
    MONO_AVAILABLE=true
fi

# Clean previous build
echo -e "${YELLOW}Cleaning previous build...${NC}"
rm -rf "$APP_DIR" GK6X-*.AppImage

# Create AppDir structure
echo -e "${YELLOW}Creating AppDir structure...${NC}"
mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/lib"
mkdir -p "$APP_DIR/usr/share/applications"
mkdir -p "$APP_DIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APP_DIR/usr/lib/mono"
mkdir -p "$APP_DIR/usr/etc/mono"

# Copy Python GUI
echo -e "${YELLOW}Copying Python GUI...${NC}"
cp gk6x_gui.py "$APP_DIR/usr/bin/gk6x_gui"
chmod +x "$APP_DIR/usr/bin/gk6x_gui"

# Copy GK6X source and build
echo -e "${YELLOW}Preparing GK6X C# application...${NC}"

# Check if we need to download prebuilt
if [ ! -d "source_code/Build" ] || [ ! -f "source_code/Build/GK6X.exe" ]; then
    echo -e "${YELLOW}Build directory not found. Downloading prebuilt release...${NC}"
    
    # Create Build directory
    mkdir -p source_code/Build
    cd source_code/Build
    
    # Download latest release
    echo "Downloading GK6X prebuilt binaries..."
    wget -q --show-progress "https://github.com/pixeltris/GK6X/releases/download/GK6X-v1.21/GK6X-v1.21-GUI.zip" -O gk6x.zip
    
    if [ $? -eq 0 ]; then
        echo "Extracting..."
        # Use -o to overwrite and -qq for extra quiet (ignore warnings about filenames)
        unzip -o -qq gk6x.zip 2>&1 | grep -v "mismatching" || true
        rm gk6x.zip
        
        # Move files from extracted directory to Build if needed
        if [ -d "GK6X-v1.21-GUI" ]; then
            mv GK6X-v1.21-GUI/* . 2>/dev/null || true
            rmdir GK6X-v1.21-GUI 2>/dev/null || true
        fi
        
        echo -e "${GREEN}Downloaded and extracted successfully${NC}"
    else
        echo -e "${RED}Failed to download. Trying to build from source...${NC}"
        cd ..
        if command -v xbuild &> /dev/null; then
            xbuild /p:Configuration=Release GK6X.sln || echo "Build may have warnings, continuing..."
        elif command -v msbuild &> /dev/null; then
            msbuild /p:Configuration=Release GK6X.sln || echo "Build may have warnings, continuing..."
        else
            echo -e "${RED}Error: Cannot build - neither xbuild nor msbuild found${NC}"
            echo "Please install mono-complete: sudo dnf install mono-complete"
            exit 1
        fi
    fi
    cd ../..
else
    echo "Build directory found, using existing build"
fi

# Copy GK6X build
echo -e "${YELLOW}Copying GK6X files...${NC}"
cp -r source_code "$APP_DIR/usr/share/gk6x"

# Create a wrapper script
cat > "$APP_DIR/usr/bin/gk6x" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export MONO_PATH="${HERE}/../lib/mono"
export MONO_CONFIG="${HERE}/../etc/mono/config"
exec mono "${HERE}/../share/gk6x/Build/GK6X.exe" "$@"
EOF
chmod +x "$APP_DIR/usr/bin/gk6x"

# Copy Python and dependencies
echo -e "${YELLOW}Copying Python runtime...${NC}"
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
cp $(which python3) "$APP_DIR/usr/bin/" || echo "Python3 binary copy skipped"

# Copy mono runtime essentials
echo -e "${YELLOW}Copying Mono runtime...${NC}"

if [ "$MONO_AVAILABLE" = true ]; then
    echo "Copying mono from system..."
    if [ -d "/usr/lib64/mono" ]; then
        cp -r /usr/lib64/mono/4.5 "$APP_DIR/usr/lib/mono/" 2>/dev/null || true
        cp -r /usr/lib64/mono/gac "$APP_DIR/usr/lib/mono/" 2>/dev/null || true
    elif [ -d "/usr/lib/mono" ]; then
        cp -r /usr/lib/mono/4.5 "$APP_DIR/usr/lib/mono/" 2>/dev/null || true
        cp -r /usr/lib/mono/gac "$APP_DIR/usr/lib/mono/" 2>/dev/null || true
    fi

    if [ -d "/etc/mono" ]; then
        cp -r /etc/mono/* "$APP_DIR/usr/etc/mono/" 2>/dev/null || true
    fi

    # Copy shared libraries needed by mono
    echo -e "${YELLOW}Copying required libraries...${NC}"
    mkdir -p "$APP_DIR/usr/lib"

    copy_libs() {
        for lib in libmono-native libMonoPosixHelper libmonosgen-2.0 libgdiplus; do
            find /usr/lib64 /usr/lib -name "${lib}*.so*" -exec cp {} "$APP_DIR/usr/lib/" \; 2>/dev/null || true
        done
    }
    copy_libs
else
    echo -e "${YELLOW}Mono not available - AppImage will require mono-runtime to be installed on target system${NC}"
    echo "Creating stub mono directories..."
    mkdir -p "$APP_DIR/usr/lib/mono/4.5"
    mkdir -p "$APP_DIR/usr/etc/mono"
fi

# Create desktop file
echo -e "${YELLOW}Creating desktop file...${NC}"
cp gk6x.desktop "$APP_DIR/usr/share/applications/"
cp gk6x.desktop "$APP_DIR/"

# Create/download icon
echo -e "${YELLOW}Creating icon...${NC}"
if [ -f "gk6x.png" ]; then
    cp gk6x.png "$APP_DIR/usr/share/icons/hicolor/256x256/apps/gk6x.png"
    cp gk6x.png "$APP_DIR/gk6x.png"
else
    # Create a simple icon with ImageMagick or use a placeholder
    if command -v convert &> /dev/null; then
        convert -size 256x256 xc:transparent -fill "#00ff88" -draw "roundrectangle 20,20 236,236 20,20" \
                -fill white -pointsize 80 -gravity center -annotate +0+0 "GK6X" \
                "$APP_DIR/gk6x.png"
        cp "$APP_DIR/gk6x.png" "$APP_DIR/usr/share/icons/hicolor/256x256/apps/"
    else
        echo "Warning: No icon created. Install ImageMagick to auto-generate one."
        touch "$APP_DIR/gk6x.png"
    fi
fi

# Copy AppRun
echo -e "${YELLOW}Copying AppRun...${NC}"
cp AppRun "$APP_DIR/"
chmod +x "$APP_DIR/AppRun"

# Download appimagetool if not present
echo -e "${YELLOW}Downloading appimagetool...${NC}"
if [ ! -f "appimagetool-${ARCH}.AppImage" ]; then
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-${ARCH}.AppImage"
    chmod +x "appimagetool-${ARCH}.AppImage"
fi

# Create AppImage
echo -e "${YELLOW}Creating AppImage...${NC}"
ARCH=$ARCH ./appimagetool-${ARCH}.AppImage "$APP_DIR" "GK6X-${ARCH}.AppImage"

# Make it executable
chmod +x "GK6X-${ARCH}.AppImage"

echo -e "${GREEN}=== Build Complete ===${NC}"
echo -e "${GREEN}AppImage created: GK6X-${ARCH}.AppImage${NC}"
echo ""
echo "To run: ./GK6X-${ARCH}.AppImage"
echo ""
echo "Note: You may need to run with sudo or set up udev rules for USB access:"
echo "  sudo ./GK6X-${ARCH}.AppImage"
echo ""
echo "Or create /etc/udev/rules.d/99-gk6x.rules with:"
echo '  SUBSYSTEM=="input", GROUP="input", MODE="0666"'
echo '  SUBSYSTEM=="usb", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE:="666", GROUP="plugdev"'
echo '  KERNEL=="hidraw*", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE="0666", GROUP="plugdev"'

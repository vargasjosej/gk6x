#!/bin/bash
# Script para ejecutar GK6X GUI en Fedora Kinoite usando Toolbox

set -e

CONTAINER_NAME="gk6x-gui"
PROJECT_DIR="/var/home/joss/Proyectos/gk6x"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     GK6X GUI - Launcher para Fedora Kinoite               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar si el contenedor existe
if ! toolbox list | grep -q "$CONTAINER_NAME"; then
    echo "📦 Creando contenedor toolbox '$CONTAINER_NAME'..."
    toolbox create -y "$CONTAINER_NAME"
    echo "✅ Contenedor creado"
    echo ""
    
    echo "📥 Instalando dependencias en el contenedor..."
    toolbox run -c "$CONTAINER_NAME" sudo dnf install -y python3-tkinter mono-core 2>&1 | tail -5
    echo "✅ Dependencias instaladas"
    echo ""
else
    echo "✅ Contenedor '$CONTAINER_NAME' ya existe"
    echo ""
fi

echo "🚀 Iniciando GK6X GUI..."
echo ""

# Exportar DISPLAY para GUI
export DISPLAY="${DISPLAY:-:0}"

# Ejecutar la GUI en el contenedor
toolbox run -c "$CONTAINER_NAME" bash -c "
    export DISPLAY=$DISPLAY
    cd $PROJECT_DIR
    python3 gk6x_gui.py
"

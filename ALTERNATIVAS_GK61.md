# 🔧 Alternativas para GK61 (RY Micro 3532:c0c1)

## ⚠️ Problema Identificado

Tu teclado **Geeky GK61** usa un chip **RY Micro (3532:c0c1)** diferente al GK6X original (1ea7), por lo que el software GK6X no puede comunicarse con él.

---

## 🔍 Investigación y Alternativas

### 1. Software Oficial del Fabricante

#### Buscar Software Oficial:
- **Nombre del teclado**: Geeky GK61
- **Fabricante**: RY Micro
- **Búsqueda recomendada**:
  - Página donde compraste el teclado
  - Manual incluido con el teclado
  - "Geeky GK61 software download"
  - "RY Micro keyboard software"

#### Posibles nombres del software:
- Geeky Driver
- RY Keyboard Software
- GK61 Configuration Tool

---

### 2. QMK Firmware (Recomendado si es compatible)

**QMK** es un firmware open source muy popular para teclados mecánicos.

#### Verificar Compatibilidad:

```bash
# Visitar sitios:
# https://qmk.fm/
# https://config.qmk.fm/

# Buscar en GitHub:
# https://github.com/qmk/qmk_firmware/tree/master/keyboards
```

#### ¿Cómo saber si tu GK61 es compatible?
- Busca "GK61 QMK" en internet
- Revisa si hay un fork/branch específico
- Algunos GK61 vienen con QMK pre-flasheado

#### Si es compatible con QMK:

**Ventajas**:
- ✅ Control total del teclado
- ✅ Soporte nativo en Linux
- ✅ Configuración con VIA (GUI)
- ✅ Macros ilimitados
- ✅ Capas infinitas

**Pasos para usar QMK**:
1. Instalar QMK toolbox
2. Crear keymap personalizado
3. Compilar firmware
4. Flashear al teclado

---

### 3. VIA Configurator

**VIA** es una GUI que funciona con teclados QMK compatibles.

```bash
# Descargar VIA:
# https://www.caniusevia.com/

# Si tu GK61 es compatible con VIA:
# - Interfaz visual drag & drop
# - No necesitas compilar nada
# - Cambios en tiempo real
```

---

### 4. Software en Windows (con Wine/VM)

Si encuentras el software oficial solo para Windows:

#### Opción A: Wine
```bash
# Instalar Wine
sudo dnf install wine winetricks

# Ejecutar el software de Windows
wine GK61-Setup.exe
```

#### Opción B: Máquina Virtual
```bash
# Usar GNOME Boxes o VirtualBox
# Instalar Windows en VM
# Usar el software oficial allí
# Las configs se guardan en la memoria del teclado
```

---

### 5. Ingeniería Inversa (Avanzado)

Si eres aventurero y quieres crear tu propio driver:

#### Herramientas necesarias:
```bash
# Wireshark para capturar USB
sudo dnf install wireshark

# Python para prototipar
sudo dnf install python3-usb python3-hidapi

# Proyecto de referencia:
# https://github.com/wgwoods/gk64-python
```

#### Proceso:
1. Capturar tráfico USB con el software oficial en Windows
2. Analizar los paquetes HID
3. Replicar el protocolo en Linux
4. Crear un script/programa Python

---

### 6. Alternativa: Karabiner/xmodmap

Para remapeo básico de teclas sin software del teclado:

#### xmodmap (Linux básico):
```bash
# Crear archivo ~/.Xmodmap
xmodmap -pke > ~/.Xmodmap

# Editar para cambiar teclas
# Ejemplo: intercambiar Caps Lock y Escape
nano ~/.Xmodmap
# Buscar y modificar keycodes
```

#### keyd (Moderno, recomendado):
```bash
# Instalar keyd
git clone https://github.com/rvaiya/keyd
cd keyd
make && sudo make install

# Crear config en /etc/keyd/default.conf
sudo nano /etc/keyd/default.conf
```

**Ejemplo de config keyd**:
```ini
[ids]
*

[main]
capslock = esc
esc = capslock

# Macros
f1 = C-c
f2 = C-v

# Layers
[meta]
w = up
a = left
s = down
d = right
```

#### Ventajas de keyd:
- ✅ Funciona a nivel de kernel
- ✅ No necesita X11/Wayland
- ✅ Muy configurable
- ✅ No depende del teclado

#### Desventajas:
- ❌ No controla LEDs
- ❌ No modifica el firmware del teclado
- ❌ Solo funciona en tu PC

---

## 🎯 Plan de Acción Recomendado

### Paso 1: Verificar Documentación del Teclado
```bash
# Buscar en tu sistema
find ~ -type f -iname "*gk61*" -o -iname "*geeky*" 2>/dev/null

# Ver si vino con un CD/USB con software
```

### Paso 2: Probar keyd (Solución Inmediata)
```bash
# Instalar keyd
git clone https://github.com/rvaiya/keyd
cd keyd
make && sudo make install
sudo systemctl enable keyd
sudo systemctl start keyd

# Configurar
sudo nano /etc/keyd/default.conf
# (ver ejemplo arriba)

# Recargar
sudo keyd reload
```

### Paso 3: Investigar QMK/VIA
- Buscar "GK61 RY Micro QMK" en foros
- Revisar Reddit: r/MechanicalKeyboards
- Preguntar en Discord de QMK

### Paso 4: Último Recurso - Windows VM
- Instalar Windows en VirtualBox
- Usar software oficial
- Guardar config en memoria del teclado

---

## 📋 Información para Buscar Ayuda

Cuando busques ayuda en foros, proporciona:

```
Teclado: Geeky GK61 Gaming Keyboard
Vendor ID: 3532:c0c1
Fabricante: RY Micro
Sistema: Fedora Kinoite 43
Output de lsusb:
Bus 003 Device 006: ID 3532:c0c1 RY Micro Geeky GK61 Gaming Keyboard
```

---

## 🔗 Enlaces Útiles

### Foros y Comunidades:
- **r/MechanicalKeyboards** - Reddit
- **geekhack.org** - Foro especializado
- **Discord de QMK** - https://discord.gg/qmk
- **deskthority.net** - Wiki y foros

### Software Open Source:
- **QMK Firmware**: https://github.com/qmk/qmk_firmware
- **VIA**: https://www.caniusevia.com/
- **keyd**: https://github.com/rvaiya/keyd
- **kmonad**: https://github.com/kmonad/kmonad

### Proyectos Similares:
- **OpenRGB**: https://gitlab.com/CalcProgrammer1/OpenRGB (para LEDs)
- **ckb-next**: https://github.com/ckb-next/ckb-next (Corsair, pero puede tener insights)

---

## 💡 Solución Temporal: keyd

Mientras investigas la solución definitiva, **keyd** es tu mejor opción:

### Instalación rápida:
```bash
# Clonar e instalar
git clone https://github.com/rvaiya/keyd ~/keyd
cd ~/keyd
make
sudo make install

# Habilitar servicio
sudo systemctl enable keyd --now

# Configurar
sudo tee /etc/keyd/default.conf << 'EOF'
[ids]
*

[main]
# Intercambiar Caps Lock y Escape
capslock = esc
esc = capslock

# Macros útiles
f1 = C-c
f2 = C-v
f3 = C-x
f5 = C-z
f7 = C-s

[meta]
# Alt como modificador
# Cuando presionas Alt + WASD = Flechas
w = up
a = left
s = down
d = right
EOF

# Recargar
sudo keyd reload
```

**Prueba inmediata**:
- Presiona Caps Lock → Debería actuar como Esc
- Presiona F1 → Debería copiar (Ctrl+C)
- Presiona Alt+W → Debería ser Flecha Arriba

---

## 🎯 Próximos Pasos

1. **Ahora mismo**: Instala keyd para tener remapeo funcional
2. **Esta semana**: Busca software oficial del fabricante
3. **Investiga**: Mira si tu GK61 específico soporta QMK
4. **Comunidad**: Pregunta en r/MechanicalKeyboards con tu modelo exacto

---

## 📝 Mantente Informado

Guarda esta información:
- Modelo exacto de tu teclado
- Vendor ID: 3532:c0c1
- Cualquier software que encuentres

Si encuentras una solución, considera:
- Documentarla en GitHub
- Compartirla en foros
- ¡Ayudar a otros con el mismo teclado!

---

**¡No te rindas! Muchos teclados tienen soluciones alternativas. keyd te dará funcionalidad inmediata mientras investigas opciones más completas.**

# 🧪 Guía de Pruebas - GK6X GUI

## Pre-requisitos

1. **Teclado GK6X conectado** por USB
2. **GUI abierta**: `~/run-gk6x.sh`
3. **Mono instalado** en el contenedor (ya está)

---

## 🔍 Prueba 1: Detectar el Teclado

### Pasos:

1. Conecta tu teclado GK6X por USB
2. En la GUI, mira la parte superior: **"Device Status:"**
3. Click en el botón **"🔄 Refresh"**
4. O ve a: **Tools → Check Device**

### Resultado Esperado:

✅ Debería mostrar algo como:
```
Device Status: 'GK64S RGB' model:655491200 fw:v1.16
```

❌ Si muestra "No device detected":
- Verifica con: `lsusb | grep 1ea7`
- Puede necesitar permisos USB (ver abajo)

---

## 🔍 Prueba 2: Listar Todas las Teclas

### Pasos:

1. Ve a la pestaña **"Quick Actions"**
2. Click en **"📋 List Keys (Dump Keys)"**
3. Ve a la pestaña **"Console"**

### Resultado Esperado:

✅ Verás una lista de todas las teclas:
```
Row 0: Esc, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, Minus, Equal, Backspace
Row 1: Tab, Q, W, E, R, T, Y, U, I, O, P, LBracket, RBracket, Backslash
...
```

---

## 🔍 Prueba 3: Crear Configuración Simple

### Pasos:

1. Ve a la pestaña **"Config Editor"**
2. Click en **"📝 New"** para limpiar
3. Escribe una configuración simple:

```
# Intercambiar Caps Lock y Escape
CapsLock=Esc
Esc=CapsLock
```

4. Click en **"💾 Save"**
5. Guarda como: `test_config.txt` en la carpeta `UserData`

### Resultado Esperado:

✅ El archivo se guarda correctamente
✅ Muestra el nombre en "Current: test_config.txt"

---

## 🔍 Prueba 4: Aplicar Configuración

### Pasos:

1. Con el archivo guardado en UserData
2. Ve a **"Quick Actions"**
3. Click en **"📝 Apply Configuration (Map)"**
4. Confirma en el diálogo
5. Observa la **Console**

### Resultado Esperado:

✅ En Console verás:
```
Running: mono .../GK6X.exe /map
Connected to device...
Command completed successfully
```

✅ **Prueba física**: 
- Presiona **Caps Lock** → debería actuar como **Esc**
- Presiona **Esc** → debería actuar como **Caps Lock**

---

## 🔍 Prueba 5: Reset a Default

### Pasos:

1. Ve a **"Quick Actions"**
2. Click en **"🔄 Reset to Default (Unmap)"**
3. Confirma
4. Observa Console

### Resultado Esperado:

✅ Teclado vuelve a configuración de fábrica
✅ Caps Lock y Esc funcionan normal

---

## 🔍 Prueba 6: Editor de Configuración

### Pasos:

1. Ve a **"Config Editor"**
2. Click en **"📄 Sample"**
3. Explora el archivo de ejemplo
4. Prueba **Load** y **Save**

### Resultado Esperado:

✅ Se carga Sample.txt con ejemplos
✅ Puedes editar y guardar cambios

---

## 🔍 Prueba 7: Web GUI (Opcional)

### Pasos:

1. Ve a la pestaña **"Web GUI"**
2. Click en **"🌐 Start Web GUI"**
3. Espera que se abra el navegador

### Resultado Esperado:

✅ Navegador abre en http://localhost:6464
✅ Interfaz web visual del GK6X
✅ Status muestra "Running on http://localhost:6464"

---

## 🔍 Prueba 8: Macros

### Pasos:

1. En **Config Editor**, crea:

```
# Macro para Copiar (Ctrl+C)
F1={LControl,C}

# Macro para Pegar (Ctrl+V)
F2={LControl,V}

# Macro para abrir terminal (Ctrl+Alt+T)
F3={LControl,LAlt,T}
```

2. Guarda y aplica con **Map**
3. Prueba presionando F1, F2, F3

### Resultado Esperado:

✅ F1 copia texto seleccionado
✅ F2 pega
✅ F3 abre terminal

---

## 🔍 Prueba 9: Capas (Layers)

### Pasos:

1. En **Config Editor**:

```
# Capa base normal
A=A
S=S

# Layer 1 (con Fn presionado)
[Layer1]
A=Up
S=Down
D=Left
F=Right
```

2. Aplica con **Map**
3. Mantén **Fn** y presiona A, S, D, F

### Resultado Esperado:

✅ Sin Fn: A, S funcionan normal
✅ Con Fn: A=↑, S=↓, D=←, F=→

---

## 🔧 Solución de Problemas

### ❌ "No device detected"

**Causa**: Falta permisos USB

**Solución 1** - Temporal:
```bash
sudo toolbox run -c gk6x-gui python3 ~/Proyectos/gk6x/gk6x_gui_fixed.py
```

**Solución 2** - Permanente (configurar udev):
```bash
# Crear reglas udev
sudo nano /etc/udev/rules.d/99-gk6x.rules

# Agregar:
SUBSYSTEM=="input", GROUP="input", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE:="666", GROUP="plugdev"
KERNEL=="hidraw*", ATTRS{idVendor}=="1ea7", ATTRS{idProduct}=="0907", MODE="0666", GROUP="plugdev"

# Recargar:
sudo udevadm control --reload-rules
sudo udevadm trigger
```

**Solución 3** - Verificar conexión:
```bash
lsusb | grep 1ea7
ls -l /dev/hidraw*
```

---

### ❌ "mono: command not found"

**Causa**: Mono no está en el contenedor

**Solución**:
```bash
toolbox enter gk6x-gui
sudo dnf install mono-core mono-devel
exit
```

---

### ❌ Config no se aplica

**Verificar**:
1. El archivo está guardado en `source_code/Build/UserData/`
2. El nombre del archivo coincide con tu modelo (ej: `655491200.txt`)
3. La sintaxis es correcta (sin errores de tipeo)
4. Revisa la Console para ver errores

---

## 📝 Configuración Recomendada para Probar

```
# Archivo: UserData/[TU_MODELO].txt
# Configuración de prueba completa

# ===== MAPEO BÁSICO =====
# Intercambiar Caps Lock y Escape
CapsLock=Esc
Esc=CapsLock

# ===== MACROS ÚTILES =====
# Copiar, Pegar, Cortar
F1={LControl,C}
F2={LControl,V}
F3={LControl,X}

# Deshacer, Rehacer
F5={LControl,Z}
F6={LControl,Y}

# Guardar
F7={LControl,S}

# ===== LAYER 1 (con Fn) =====
[Layer1]
# WASD como flechas
W=Up
A=Left
S=Down
D=Right

# HJKL estilo Vim
H=Left
J=Down
K=Up
L=Right

# ===== LAYER 2 =====
[Layer2]
# Teclas de función
1=F1
2=F2
3=F3
4=F4
5=F5
```

---

## ✅ Checklist de Pruebas

- [ ] Teclado detectado correctamente
- [ ] Dump Keys muestra todas las teclas
- [ ] Puede crear y guardar configuración
- [ ] Map aplica configuración exitosamente
- [ ] Unmap resetea a default
- [ ] Macros funcionan (F1=Ctrl+C, etc)
- [ ] Capas funcionan (Fn + teclas)
- [ ] Web GUI se abre (opcional)
- [ ] Editor Load/Save funciona
- [ ] Console muestra output correctamente

---

## 🎯 Próximos Pasos Después de Probar

1. **Si todo funciona**: 
   - Crea tu configuración personalizada
   - Guárdala con backup
   - Experimenta con más macros

2. **Si algo falla**:
   - Revisa la Console para errores
   - Verifica permisos USB
   - Consulta esta guía de troubleshooting

3. **Compartir**:
   - Publica tu experiencia
   - Comparte tus configs en GitHub
   - Ayuda a otros usuarios

---

**¡Buena suerte con las pruebas!** 🚀

Si encuentras algún problema, revisa la Console en la GUI para más detalles.

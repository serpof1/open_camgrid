# 🎥 Open CamGrid

Visor de cámaras DVR/IP simple y liviano desarrollado en Python.

Permite visualizar múltiples cámaras en grilla configurable utilizando RTSP, ideal para redes locales (LAN).

---

## 🚀 Características

* ✔ Visualización en grillas: 1x1, 2x2, 2x4, 4x4
* ✔ Configuración inicial con interfaz gráfica (Tkinter)
* ✔ Soporte RTSP (DVR/NVR/IP cameras)
* ✔ Modo blanco y negro (opcional)
* ✔ Nombres personalizados por cámara
* ✔ Guardado de configuración en archivo JSON
* ✔ Visualización en tiempo real con OpenCV

---

## 🖥️ Capturas

*(Agregar imágenes cuando estés en la red local)*

---

## ⚙️ Requisitos

* Python 3.10 o superior
* OpenCV
* Numpy
* Tkinter (incluido en la mayoría de instalaciones)

---

## 📦 Instalación

Clonar el repositorio:

```bash
git clone https://github.com/serpof1/open_camgrid.git
cd open_camgrid
```

Instalar dependencias:

```bash
pip install opencv-python numpy
```

---

## ▶️ Uso

Ejecutar:

```bash
python src/main.py
```

---

## ⚙️ Configuración

Al iniciar el programa se puede:

* Ingresar usuario, contraseña e IP del DVR
* Seleccionar tipo de grilla
* Activar modo blanco y negro
* Definir nombres de cámaras

Los datos se guardan en:

```
config/config.json
```

---

## 🌐 Notas

* Funciona en redes locales (LAN)
* Para acceso remoto se requiere configuración de puertos/VPN

---

## 🛠️ Futuras mejoras

* Grabación de video
* Detección de movimiento
* Soporte ONVIF
* Interfaz mejorada
* Integración con cámaras móviles

---

## 📄 Licencia

MIT License

---

## 🤝 Contribuciones

Proyecto abierto para la comunidad.
Cualquier mejora es bienvenida.

---


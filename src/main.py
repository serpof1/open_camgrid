# =========================================================
# IMPORTS
# =========================================================
import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import ttk
import json
import os

# =========================================================
# CONFIG DEFAULT + ARCHIVO
# =========================================================
CONFIG_FILE = "config/config.json"

config = {
    "user": "admin",
    "password": "tea20251",
    "ip": "192.168.1.108",
    "grid": "2x2",
    "byn": False,
    "names": ["Cam1", "Cam2", "Cam3", "Cam4"]
}

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config.update(json.load(f))

# =========================================================
# GRID CONFIG
# =========================================================
GRID_MAP = {
    "1x1": (1, 1),
    "2x2": (2, 2),
    "2x4": (2, 4),
    "4x4": (4, 4)
}

SUBTYPE = 1
WIDTH = 320
HEIGHT = 240

# =========================================================
# RTSP
# =========================================================
def rtsp_url(ch):
    return f"rtsp://{config['user']}:{config['password']}@{config['ip']}:554/cam/realmonitor?channel={ch:02d}&subtype={SUBTYPE}"

# =========================================================
# VIDEO
# =========================================================
frames = {}
fullscreen = None

def capture_thread(ch):
    url = rtsp_url(ch)
    cap = cv2.VideoCapture(url)
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cap = cv2.VideoCapture(url)
            continue
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        if config["byn"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        frames[ch] = frame

def build_grid(channels, rows, cols):
    imgs = []
    for ch in channels:
        img = frames.get(ch, np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8))
        if ch-1 < len(config["names"]):
            cv2.putText(img, config["names"][ch-1], (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        imgs.append(img)
    grid_rows = []
    idx = 0
    for r in range(rows):
        row_imgs = []
        for c in range(cols):
            if idx < len(imgs):
                row_imgs.append(imgs[idx])
            else:
                row_imgs.append(np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8))
            idx += 1
        grid_rows.append(np.hstack(row_imgs))
    return np.vstack(grid_rows)

# =========================================================
# VIEWER
# =========================================================
def viewer():
    rows, cols = GRID_MAP[config["grid"]]
    total = rows * cols
    channels = list(range(1, total + 1))

    for ch in channels:
        frames[ch] = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        t = threading.Thread(target=capture_thread, args=(ch,), daemon=True)
        t.start()

    cv2.namedWindow("CamGrid")

    while True:
        frame = build_grid(channels, rows, cols)
        cv2.imshow("CamGrid", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break

    cv2.destroyAllWindows()

# =========================================================
# CONFIG WINDOW
# =========================================================
def config_window(parent=None):
    def save_config():
        update_config()
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    def start():
        update_config()
        if parent:
            parent.destroy()
        root.quit()
        root.destroy()

    def update_config():
        config["user"] = entry_user.get()
        config["password"] = entry_pass.get()
        config["ip"] = entry_ip.get()
        config["grid"] = combo_grid.get()
        config["byn"] = var_byn.get()
        for i in range(len(name_entries)):
            config["names"][i] = name_entries[i].get()

    root = tk.Tk()
    root.title("Configuración DVR")
    root.geometry("400x600")
    root.configure(bg="#222222")

    tk.Label(root, text="Usuario", fg="white", bg="#222222").pack()
    entry_user = tk.Entry(root)
    entry_user.insert(0, config["user"])
    entry_user.pack()

    tk.Label(root, text="Password", fg="white", bg="#222222").pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.insert(0, config["password"])
    entry_pass.pack()

    tk.Label(root, text="IP", fg="white", bg="#222222").pack()
    entry_ip = tk.Entry(root)
    entry_ip.insert(0, config["ip"])
    entry_ip.pack()

    tk.Label(root, text="Grilla", fg="white", bg="#222222").pack(pady=5)
    combo_grid = ttk.Combobox(root, values=list(GRID_MAP.keys()))
    combo_grid.set(config["grid"])
    combo_grid.pack()

    var_byn = tk.BooleanVar(value=config["byn"])
    tk.Checkbutton(root, text="Blanco y Negro", variable=var_byn, bg="#222222", fg="white").pack()

    tk.Label(root, text="Nombres cámaras", fg="white", bg="#222222").pack(pady=5)
    rows, cols = GRID_MAP[config["grid"]]
    total = rows * cols
    while len(config["names"]) < total:
        config["names"].append(f"Cam{len(config['names'])+1}")

    name_entries = []
    for i in range(total):
        e = tk.Entry(root)
        e.insert(0, config["names"][i])
        e.pack()
        name_entries.append(e)

    tk.Button(root, text="Guardar", command=save_config).pack(pady=5)
    tk.Button(root, text="Iniciar", command=start).pack(pady=5)
    tk.Button(root, text="Salir", command=root.destroy).pack(pady=5)

    root.mainloop()

# =========================================================
# MENU INICIAL
# =========================================================
def main_menu():
    def open_config():
        root.destroy()
        config_window()
        main_menu()  # volver al menú luego de guardar

    def open_viewer():
        root.destroy()
        viewer()

    root = tk.Tk()
    root.title("Open CamGrid")
    root.geometry("400x300")
    root.configure(bg="#111111")

    tk.Label(root, text="Open CamGrid", fg="white", bg="#111111", font=("Arial", 16)).pack(pady=10)

    # mostrar configuración actual
    tk.Label(root, text=f"Usuario: {config['user']}", fg="white", bg="#111111").pack()
    tk.Label(root, text=f"IP: {config['ip']}", fg="white", bg="#111111").pack()
    tk.Label(root, text=f"Grilla: {config['grid']}", fg="white", bg="#111111").pack()
    tk.Label(root, text=f"Modo BYN: {'Sí' if config['byn'] else 'No'}", fg="white", bg="#111111").pack(pady=5)

    tk.Button(root, text="Ingresar", command=open_viewer).pack(pady=10)
    tk.Button(root, text="Configurar", command=open_config).pack(pady=10)
    tk.Button(root, text="Salir", command=root.destroy).pack(pady=10)

    root.mainloop()

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    main_menu()

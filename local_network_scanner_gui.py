import socket
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from tkinter import ttk
import threading

# ===== VARIABEL GLOBAL UNTUK SAVE AS =====
hasil_port_global = []
ip_global = ""
waktu_global = ""

# ===== FUNGSI SCAN PORT =====
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((ip, port))
        sock.close()
        return "TERBUKA" if result == 0 else "TERTUTUP"
    except:
        return "ERROR"

# ===== FUNGSI SCAN =====
def start_scan():
    threading.Thread(target=scan_process, daemon=True).start()

def scan_process():
    global hasil_port_global, ip_global, waktu_global

    ip = entry_ip.get()
    ports_input = entry_ports.get()

    if not ip or not ports_input:
        messagebox.showwarning("Peringatan", "IP dan Port tidak boleh kosong!")
        return

    progress.start(10)
    text_result.delete("1.0", tk.END)

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hasil_port = []

    ports = ports_input.split(",")

    for port in ports:
        try:
            port = int(port.strip())
            status = scan_port(ip, port)

            warna = "open" if status == "TERBUKA" else "closed"
            text_result.insert(tk.END, f"Port {port} → {status}\n", warna)

            hasil_port.append(f"Port {port} → {status}")
        except ValueError:
            text_result.insert(tk.END, f"Port tidak valid: {port}\n")

    progress.stop()

    hasil_port_global = hasil_port
    ip_global = ip
    waktu_global = waktu

    # ===== SIMPAN KE GLOBAL (UNTUK SAVE AS) =====
    hasil_port_global = hasil_port
    ip_global = ip
    waktu_global = waktu

    # ===== AUTO SAVE KE FILE LOG =====
    with open("hasil_scan.txt", "a", encoding="utf-8") as file:
        file.write("================================\n")
        file.write(f"Waktu : {waktu}\n")
        file.write(f"IP    : {ip}\n")
        for h in hasil_port:
            file.write(h + "\n")
        file.write("\n")

# ===== SAVE AS (HANYA HASIL TERAKHIR) =====
def save_as():
    if not hasil_port_global:
        messagebox.showwarning("Peringatan", "Belum ada hasil scan!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt")],
        title="Simpan Hasil Scan"
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("================================\n")
            file.write(f"Waktu : {waktu_global}\n")
            file.write(f"IP    : {ip_global}\n")
            for h in hasil_port_global:
                file.write(h + "\n")
            file.write("================================\n")

        messagebox.showinfo("Sukses", "Hasil scan berhasil disimpan!")

# ===== CLEAR =====
def clear_hasil():
    entry_ip.delete(0, tk.END)
    entry_ports.delete(0, tk.END)
    text_result.delete("1.0", tk.END)
    hasil_port_global.clear()

def get_ip_otomatis():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # connect dummy
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

mode_gelap = True

def toggle_mode():
    global mode_gelap

    if mode_gelap:
        # LIGHT MODE
        window.configure(bg="#f5f5f5")

        title_label.config(bg="#f5f5f5", fg="#222")
        frame_input.config(bg="#f5f5f5")
        frame_btn.config(bg="#f5f5f5")

        label_ip.config(bg="#f5f5f5", fg="#222")
        label_port.config(bg="#f5f5f5", fg="#222")
        hasil_label.config(bg="#f5f5f5", fg="#222")

        text_result.config(bg="white", fg="black", insertbackground="black")

        mode_button.config(text="Dark Mode", bg="#ccc", fg="black")

        mode_gelap = False

    else:
        # DARK MODE
        window.configure(bg="#1e1e2f")

        title_label.config(bg="#1e1e2f", fg="white")
        frame_input.config(bg="#1e1e2f")
        frame_btn.config(bg="#1e1e2f")

        label_ip.config(bg="#1e1e2f", fg="white")
        label_port.config(bg="#1e1e2f", fg="white")
        hasil_label.config(bg="#1e1e2f", fg="white")

        # hasil scan tetap putih biar kontras
        text_result.config(bg="white", fg="black", insertbackground="black")

        mode_button.config(text="Light Mode", bg="#555", fg="white")

        mode_gelap = True


# ================= GUI =================
window = tk.Tk()
window.title("Local Network Scanner")
window.geometry("520x520")
window.resizable(False, False)
window.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("default")

style.configure("Blue.Horizontal.TProgressbar",
                troughcolor="#d9d9d9",
                background="#2196F3",
                thickness=12)

# ICON
logo = tk.PhotoImage(file="LogoLNS.png")
window.iconphoto(True, logo)

font_label = ("Segoe UI", 10)
font_entry = ("Segoe UI", 10)
font_button = ("Segoe UI", 10, "bold")

# ===== TITLE =====
title_label = tk.Label(window,
         text="LOCAL NETWORK SCANNER",
         font=("Segoe UI", 16, "bold"),
         fg="white",
         bg="#1e1e2f")
title_label.pack(pady=15)

# ===== INPUT FRAME =====
frame_input = tk.Frame(window, bg="#1e1e2f")
frame_input.pack(pady=10)

label_ip = tk.Label(frame_input,
                    text="IP Address",
                    font=font_label,
                    fg="white",
                    bg="#1e1e2f")
label_ip.grid(row=0, column=0, sticky="w", pady=5)

entry_ip = tk.Entry(frame_input, width=32, font=font_entry)
entry_ip.grid(row=1, column=0, pady=5)
entry_ip.insert(0, get_ip_otomatis())

label_port = tk.Label(frame_input,
                      text="Port (pisahkan dengan koma)",
                      font=font_label,
                      fg="white",
                      bg="#1e1e2f")
label_port.grid(row=2, column=0, sticky="w", pady=5)

entry_ports = tk.Entry(frame_input, width=32, font=font_entry)
entry_ports.grid(row=3, column=0, pady=5)

# ===== BUTTON FRAME =====
frame_btn = tk.Frame(window, bg="#1e1e2f")
frame_btn.pack(pady=15)

tk.Button(frame_btn, text="Scan",
          width=12, bg="#4CAF50", fg="white",
          font=font_button, command=start_scan).grid(row=0, column=0, padx=6)

tk.Button(frame_btn, text="Save As",
          width=12, bg="#2196F3", fg="white",
          font=font_button, command=save_as).grid(row=0, column=1, padx=6)

tk.Button(frame_btn, text="Clear",
          width=12, bg="#f44336", fg="white",
          font=font_button, command=clear_hasil).grid(row=0, column=2, padx=6)

# ===== DARK/LIGHT TOGGLE =====
mode_button = tk.Button(window,
                        text="Light Mode",
                        font=("Segoe UI", 9),
                        bg="#555",
                        fg="white",
                        command=toggle_mode)
mode_button.pack(pady=5)

# ===== PROGRESS BAR =====
progress = ttk.Progressbar(window,
                           style="Blue.Horizontal.TProgressbar",
                           mode="indeterminate",
                           length=420)
progress.pack(pady=5)

# ===== RESULT AREA =====
hasil_label = tk.Label(window,
                       text="Hasil Scan",
                       font=font_label,
                       fg="white",
                       bg="#1e1e2f")
hasil_label.pack(pady=5)

text_result = tk.Text(window,
                      height=13,
                      width=60,
                      bg="white",
                      fg="black",
                      insertbackground="black")
text_result.pack(pady=5)

text_result.tag_config("open", foreground="#00c853")
text_result.tag_config("closed", foreground="#d50000")

window.mainloop()
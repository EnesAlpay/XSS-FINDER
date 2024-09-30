import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox

def load_payloads(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Hata", f"Dosya bulunamadı: {file_path}")
        return []

def test_xss():
    url = entry_url.get()
    param_name = entry_param.get()
    payloads = load_payloads('payloads.txt')  # Payload dosyasını yükle

    results_text.delete(1.0, tk.END)  # Önceki sonuçları temizle
    found_xss = False  # XSS açığı bulunup bulunmadığını kontrol etmek için

    for payload in payloads:
        try:
            response = requests.get(url, params={param_name: payload})
            if payload in response.text:
                results_text.insert(tk.END, f"[!] XSS açığı bulundu: {payload}\n")
                found_xss = True
                break  # İlk açık bulunduğunda döngüden çık
        except Exception as e:
            messagebox.showerror("Hata", f"İstek gönderilirken hata oluştu: {e}")

    if not found_xss:
        results_text.insert(tk.END, "[+] XSS açığı bulunamadı\n")

# Tkinter arayüzü oluşturma
root = tk.Tk()
root.title("XSS Tespit Aracı")

# Koyu tema renkleri
bg_color = "#2e2e2e"
fg_color = "#ffffff"
entry_bg_color = "#3e3e3e"
btn_bg_color = "#4e4e4e"

# Arka plan rengini ayarlama
root.configure(bg=bg_color)

# URL Girişi
tk.Label(root, text="Hedef URL:", bg=bg_color, fg=fg_color).pack()
entry_url = tk.Entry(root, width=50, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
entry_url.pack(pady=5)

# Parametre Adı Girişi
tk.Label(root, text="Parametre Adı:", bg=bg_color, fg=fg_color).pack()
entry_param = tk.Entry(root, width=50, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
entry_param.pack(pady=5)

# Test Butonu
btn_test = tk.Button(root, text="Test Et", command=test_xss, bg=btn_bg_color, fg=fg_color)
btn_test.pack(pady=10)

# Sonuçları Gösterme Alanı
results_text = scrolledtext.ScrolledText(root, width=60, height=20, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
results_text.pack(pady=10)

# Arayüzü başlat
root.mainloop()


import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox

def load_payloads(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {file_path}")
        return []

def test_xss():
    url = entry_url.get()
    param_name = entry_param.get()
    payloads = load_payloads('payloads.txt')  # Load payload file

    results_text.delete(1.0, tk.END)  # Clear previous results
    found_xss = False  # Check if XSS vulnerability is found

    for payload in payloads:
        try:
            response = requests.get(url, params={param_name: payload})
            if payload in response.text:
                results_text.insert(tk.END, f"[!] XSS vulnerability found: {payload}\n")
                found_xss = True
                break  # Exit loop after first vulnerability found
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while sending the request: {e}")

    if not found_xss:
        results_text.insert(tk.END, "[+] No XSS vulnerability found\n")

# Create Tkinter interface
root = tk.Tk()
root.title("XSS Detection Tool")

# Dark theme colors
bg_color = "#2e2e2e"
fg_color = "#ffffff"
entry_bg_color = "#3e3e3e"
btn_bg_color = "#4e4e4e"

# Set background color
root.configure(bg=bg_color)

# URL Entry
tk.Label(root, text="Target URL:", bg=bg_color, fg=fg_color).pack()
entry_url = tk.Entry(root, width=50, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
entry_url.pack(pady=5)

# Parameter Name Entry
tk.Label(root, text="Parameter Name:", bg=bg_color, fg=fg_color).pack()
entry_param = tk.Entry(root, width=50, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
entry_param.pack(pady=5)

# Test Button
btn_test = tk.Button(root, text="Test", command=test_xss, bg=btn_bg_color, fg=fg_color)
btn_test.pack(pady=10)

# Results Display Area
results_text = scrolledtext.ScrolledText(root, width=60, height=20, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
results_text.pack(pady=10)

# Start the interface
root.mainloop()

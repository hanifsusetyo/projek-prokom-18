import json
from tabulate import tabulate
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

file = 'database_makanan_coba.json'
user_file = 'registered_users.json'

def register():
    username = entry_username.get()
    password = entry_password.get()

    if username != "" and password != "":
        user_data = {'username': username, 'password': password}
        with open(user_file, 'a') as file_obj:
            json.dump(user_data, file_obj)
            file_obj.write('\n')

        messagebox.showinfo("Info", "Registrasi berhasil! Silakan login dengan akun yang telah didaftarkan.")
    else:
        messagebox.showerror("Error", "Username dan password tidak boleh kosong.")

def login():
    username = entry_username.get()
    password = entry_password.get()

    with open(user_file, 'r') as file_obj:
        users = [json.loads(line) for line in file_obj]

    if any(user['username'] == username and user['password'] == password for user in users):
        messagebox.showinfo("Info", "Login berhasil!")
        root.deiconify()
        login_window.withdraw()
    else:
        messagebox.showerror("Error", "Username atau Password salah, klik registrasi jika belum memiliki akun")

def get_masakan_by_harga():
    global file
    global hasil_pencarian
    budget = int(entry_budget.get())
    kategori = entry_kategori.get().lower()

    with open(file, 'r') as file_obj:
        data = json.load(file_obj)

    hasil_pencarian = []

    for makanan in data:
        if makanan['Kategori'] == kategori:
            total_harga = sum(makanan['Harga'])
            if total_harga <= budget:
                makanan['Total Harga'] = total_harga
                hasil_pencarian.append(makanan)

    table_data = print_masakan(hasil_pencarian)
    if table_data:
        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Daftar masakan:\n\n")
        result_text.insert(tk.END, table_data)
        result_text.config(state='disabled')
    else:
        messagebox.showinfo("Info", "Tidak ada masakan yang sesuai dengan kriteria.")

def print_masakan(masakan):
    if len(masakan) > 0:
        table = []
        for i, makanan in enumerate(masakan, start=1):
            table.append([i, makanan['Nama'], makanan['Total Harga']])
        headers = ["No.", "Nama", "Total Harga"]
        table_data = tabulate(table, headers=headers)

        return table_data
    else:
        return None

def print_resep():
    masakan = hasil_pencarian 
    
    if masakan:
        pilihan = int(entry_pilihan.get())
        if 1 <= pilihan <= len(masakan):
            masakan_pilihan = masakan[pilihan - 1]
            resep = masakan_pilihan['Resep']

            bahan = resep['Bahan']
            instruksi = resep['Instruksi']

            result_text.config(state='normal')
            result_text.insert(tk.END, f"\n\nResep {masakan_pilihan['Nama']}:\n")
            result_text.insert(tk.END, "Bahan:\n")
            result_text.insert(tk.END, bahan)
            result_text.insert(tk.END, "\n\nInstruksi:\n")
            result_text.insert(tk.END, instruksi)
            result_text.config(state='disabled')
        else:
            messagebox.showerror("Error", "Masakan tidak valid.")
    else:
        messagebox.showinfo("Info", "Tidak ada masakan yang sesuai dengan kriteria.")
        
def search_again():
    entry_budget.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)
    entry_pilihan.delete(0, tk.END)
    result_text.config(state='normal')
    result_text.delete("1.0", tk.END)
    result_text.config(state='disabled')

root = tk.Tk()
root.title("Program Resep Masakan")
root.geometry("600x500")

style = ttk.Style()
style.theme_use("clam")

login_window = tk.Toplevel(root)
login_window.title("Login")
login_window.geometry("300x150")

frame_login = ttk.Frame(login_window)
frame_login.pack(pady=20)

label_username = ttk.Label(frame_login, text="Username:")
label_username.grid(row=0, column=0, sticky=tk.W)
entry_username = ttk.Entry(frame_login)
entry_username.grid(row=0, column=1)

label_password = ttk.Label(frame_login, text="Password:")
label_password.grid(row=1, column=0, sticky=tk.W)
entry_password = ttk.Entry(frame_login, show="*")
entry_password.grid(row=1, column=1)

button_login = ttk.Button(login_window, text="Login", command=login)
button_login.pack()

button_register = ttk.Button(login_window, text="Register", command=register)
button_register.pack()

root.withdraw()

frame_search = ttk.Frame(root)
frame_search.pack(pady=20)

label_budget = ttk.Label(frame_search, text="Masukkan budget Anda:")
label_budget.grid(row=0, column=0, sticky=tk.W)
entry_budget = ttk.Entry(frame_search)
entry_budget.grid(row=0, column=1)

label_kategori = ttk.Label(frame_search, text="Masukkan kategori (appetizer/main course/dessert/diet food):")
label_kategori.grid(row=1, column=0, sticky=tk.W)
entry_kategori = ttk.Entry(frame_search)
entry_kategori.grid(row=1, column=1)

button_search = ttk.Button(root, text="Cari", command=get_masakan_by_harga)
button_search.pack()

frame_resep = ttk.Frame(root)
frame_resep.pack(pady=20)

label_pilihan = ttk.Label(frame_resep, text="Pilih nomor masakan untuk melihat resep:")
label_pilihan.grid(row=0, column=0, sticky=tk.W)
entry_pilihan = ttk.Entry(frame_resep)
entry_pilihan.grid(row=0, column=1)

button_print_resep = ttk.Button(frame_resep, text="Print Resep", command=print_resep)
button_print_resep.grid(row=1, column=0, pady=10)

button_search_again = ttk.Button(frame_resep, text="Cari Lagi", command=search_again)
button_search_again.grid(row=1, column=1, pady=10)

result_text = tk.Text(root, height=15, width=50)
result_text.pack()
result_text.config(state='disabled')

root.mainloop()

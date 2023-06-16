import json
from tabulate import tabulate
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

file = 'database_makanan_revisi.json'
user_file = 'registered_users.json'

def register():
    username = entry_username.get()
    password = entry_password.get()

    if username != "" and password != "":
        user_data = {'username': username, 'password': password}

        with open(user_file, 'r') as file_obj:
            for line in file_obj:
                data = json.loads(line)
                if data['username'] == username:
                    messagebox.showinfo("Info", "Anda sudah terdaftar! Silakan login.")
                    return

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
    if budget > 50000:
        messagebox.showinfo("Info", "Batas Budget Adalah 50.000")
    if budget < 5000:
        messagebox.showinfo("Info", "Maaf Uang Anda Tidak Cukup")
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

def print_resep(hasil_pencarian):
    masakan = hasil_pencarian

    if masakan:
        pilihan = int(entry_pilihan.get())
        if 1 <= pilihan <= len(masakan):
            masakan_pilihan = masakan[pilihan - 1]
            resep = masakan_pilihan['Resep']
            
            resep_tab = tk.Toplevel(root)
            resep_tab.title("Resep " + masakan_pilihan['Nama'])
            resep_tab.geometry("1280x720")

            background_image_resep = Image.open("makanan.jpg")
            background_image_resep = background_image_resep.resize((1280, 720), Image.ANTIALIAS)
            background_photo_resep = ImageTk.PhotoImage(background_image_resep)

            resep_text = tk.Text(resep_tab, height=60, width=80)
            resep_text.pack()

            resep_text.insert(tk.END, f"\n\nResep {masakan_pilihan['Nama']}:\n")
            resep_text.insert(tk.END, "Bahan:\n")
            
            bahan_table = [[i + 1, bahan, harga] for i, (bahan, harga) in enumerate(zip(resep['Bahan'], masakan_pilihan['Harga']))]
            bahan_headers = ["No.", "Bahan", "Harga"]
            bahan_table_data = tabulate(bahan_table, headers=bahan_headers)
            
            resep_text.insert(tk.END, bahan_table_data)
            resep_text.insert(tk.END, "\n\nInstruksi:\n")
            
            instruksi_table = [[langkah] for langkah in resep['Instruksi']]
            instruksi_table_data = tabulate(instruksi_table)
            
            resep_text.insert(tk.END, instruksi_table_data)
            resep_text.config(state='disabled')
        else:
            messagebox.showerror("Error", "Masukkan Angka Yang Sesuai.")
    else:
        messagebox.showinfo("Info", "Tidak ada masakan yang sesuai dengan kriteria.")

def search_again():
    entry_budget.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)
    entry_pilihan.delete(0, tk.END)
    result_text.config(state='normal')
    result_text.delete("1.0", tk.END)
    result_text.config(state='disabled')

def log_out():
    login_window.deiconify()
    root.withdraw()
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_budget.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)
    entry_pilihan.delete(0, tk.END)
    result_text.config(state='normal')
    result_text.delete("1.0", tk.END)
    result_text.config(state='disabled')

root = tk.Tk()
root.title("Program Masak on Budget")
root.geometry("1280x720")

style = ttk.Style()
style.theme_use("clam")
style.configure("Biru.TButton", background="blue", foreground="white")
style.configure("Merah.TButton", background="red", foreground="white")
style.configure("Custom.TLabel", background="white", foreground="black")
style.configure("Green.TButton", background="green", foreground="white")

background_image = Image.open("makanan.jpg")
background_image = background_image.resize((1280, 720), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

login_window = tk.Toplevel(root)
login_window.title("Login")
login_window.geometry("1280x720")

background_image_login = Image.open("makanan.jpg")
background_photo_login = ImageTk.PhotoImage(background_image_login)
background_label_login = tk.Label(login_window, image=background_photo_login)
background_label_login.place(x=0, y=0, relwidth=1, relheight=1)

frame_login = ttk.Frame(login_window)
frame_login.pack(pady=20)

label_title = ttk.Label(login_window, text="Program Masak On Budget",font=("Segoe UI Black", 28))
label_title.place(x=410,y=150)

label_username = ttk.Label(login_window, text="Username:", font=("Times New Roman", 14))
label_username.place(x=485,y=450)
entry_username = ttk.Entry(login_window, font=("Times New Roman", 14))
entry_username.place(x=570,y=450)

label_password = ttk.Label(login_window, text="Password:", font=("Times New Roman", 14))
label_password.place(x=485, y=480)
entry_password = ttk.Entry(login_window,font=("Times New Roman", 14), show="*")
entry_password.place(x=570,y=480)

button_login = ttk.Button(login_window, text="Login", style="Biru.TButton", command=login)
button_login.place(x=600,y=550)

button_register = ttk.Button(login_window, text="Register", style="Merah.TButton", command=register)
button_register.place(x=600,y=600)
root.withdraw()

frame_search = ttk.Frame(root)
frame_search.pack(pady=40)

label_budget = ttk.Label(frame_search, text="Masukkan budget Anda: (ex. 15000)", style="Custom.TLabel")
label_budget.grid(row=0, column=0, sticky=tk.W)
entry_budget = ttk.Entry(frame_search)
entry_budget.grid(row=0, column=1)

label_kategori = ttk.Label(frame_search, text="Masukkan kategori (appetizer/main course/dessert/diet food):", style="Custom.TLabel")
label_kategori.grid(row=1, column=0, sticky=tk.W)
entry_kategori = ttk.Entry(frame_search)
entry_kategori.grid(row=1, column=1)

button_cari = ttk.Button(root, text="Cari", style="Biru.TButton", command=get_masakan_by_harga)
button_cari.pack()

frame_resep = ttk.Frame(root)
frame_resep.pack(pady=40)

label_pilihan = ttk.Label(frame_resep, text="Pilih nomor masakan untuk melihat resep:", style="Custom.TLabel")
label_pilihan.grid(row=0, column=0, sticky=tk.W)
entry_pilihan = ttk.Entry(frame_resep)
entry_pilihan.grid(row=0, column=1)

button_print_resep = ttk.Button(frame_resep, text="Print Resep", style="Biru.TButton", command=lambda: print_resep(hasil_pencarian))
button_print_resep.grid(row=1, column=0, pady=10)

button_search_again = ttk.Button(frame_resep, text="Cari Lagi", style="Green.TButton", command=search_again)
button_search_again.grid(row=1, column=1, pady=10)

button_logout = ttk.Button(root, text="Log Out", style="Merah.TButton", command=log_out)
button_logout.pack()

result_text = tk.Text(root, height=20, width=60)
result_text.pack()
result_text.config(state='disabled')

root.mainloop()

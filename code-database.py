import json

# Fungsi untuk menyimpan data ke dalam file JSON
def save_to_json(data):
    with open('database_makanan.json', 'w') as file:
        json.dump(data, file, indent=4)

# Fungsi untuk memasukkan data makanan, resep, dan harga ke dalam database
def insert_data(data, nama, deskripsi, kategori, bahan, instruksi, harga):
    # Membuat dictionary untuk menyimpan data baru
    new_data = {
        "Nama": nama,
        "Deskripsi": deskripsi,
        "Kategori": kategori,
        "Resep": {
            "Bahan": bahan,
            "Instruksi": instruksi
        },
        "Harga": harga
    }

    # Menambahkan data baru ke dalam list data
    data.append(new_data)

# Contoh input list makanan
database_makanan = []

# Memasukkan data makanan pertama
insert_data(database_makanan, "Salad Buah", "Campuran buah segar dengan saus yogurt", "appetizer", ["Apel", "Jeruk", "Anggur", "Pisang", "Saus yogurt"], "1. Potong buah-buahan. 2. Campurkan dengan saus yogurt.", 15000)

# Memasukkan data makanan kedua
insert_data(database_makanan, "Pancake", "Pancake lezat dengan sirup maple", "dessert", ["Tepung", "Susu", "Telur", "Gula", "Sirup maple"], "1. Campurkan bahan-bahan. 2. Goreng pancake hingga matang.", 20000)

# Memasukkan data makanan ketiga
insert_data(database_makanan, "Nasi Goreng", "Nasi yang digoreng dengan bumbu", "main course", ["Nasi", "Telur", "Bawang", "Kecap"], "1. Goreng nasi. 2. Masukkan telur dan bumbu-bumbu lain.", 25000)

# Memasukkan data makanan keempat
insert_data(database_makanan, "Salad Sayuran", "Campurkan berbagai sayuran segar", "diet food", ["Daun selada", "Tomat", "Timun", "Paprika", "Dressing rendah kalori"], "1. Cuci sayuran. 2. Iris dan campurkan dengan dressing rendah kalori.", 18000)

# Menyimpan database makanan ke dalam file JSON
save_to_json(database_makanan)

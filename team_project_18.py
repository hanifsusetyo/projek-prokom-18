import json

def get_masakan_by_harga(file, kategori, harga_min, harga_max):
    with open(file, 'r') as file:
        data = json.load(file)

    hasil_pencarian = []

    for makanan in data:
        if makanan['Kategori'] == kategori and harga_min <= makanan['Harga'] <= harga_max:
            hasil_pencarian.append(makanan)

    return hasil_pencarian

def print_masakan(masakan):
    if len(masakan) > 0:
        print(f"Daftar masakan:")
        for i, makanan in enumerate(masakan, start=1):
            print(f"{i}. {makanan['Nama']} - Harga: {makanan['Harga']}")
        print()
    else:
        print("Tidak ada masakan yang sesuai dengan kriteria.")

def print_resep(masakan, pilihan):
    masakan_pilihan = masakan[pilihan-1]
    print(f"Resep {masakan_pilihan['Nama']}:")
    print(masakan_pilihan['Resep'])

#proses
file = 'database_makanan.json'


while True:
    range_harga = input("Masukkan range harga (5000-15000, 15000-25000, 25000-35000, 35000-50000): ")
    kategori = input("Masukkan kategori (appetizer/main course/dessert/diet food): ")
    if range_harga == '5000-15000':
        harga_min, harga_max = 5000, 15000
    elif range_harga == '15000-25000':
        harga_min, harga_max = 15000, 25000
    elif range_harga == '25000-35000':
        harga_min, harga_max = 25000, 35000
    elif range_harga == '35000-50000':
        harga_min, harga_max = 35000, 50000
    else:
        print("Range harga tidak valid.")
    masakan = get_masakan_by_harga(file, kategori, harga_min, harga_max)
    print_masakan(masakan)
    if len(masakan) > 0:
        pilihan = int(input("Pilih nomor masakan untuk melihat resep: "))
    if 1 <= pilihan <= len(masakan):
        print_resep(masakan, pilihan)
    else:
        print("Masakan tidak valid.")
    ulang = input("Apakah Anda ingin mencari resep lagi? (ya/tidak): ")
    if ulang.lower() != 'ya':
        break
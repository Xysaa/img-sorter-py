# 🖼️ Image Sorter App (GUI)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
Aplikasi desktop berbasis Python + Tkinter untuk **menyortir gambar** dari satu folder sumber ke beberapa folder tujuan secara manual dan cepat.

---

![Image](https://github.com/user-attachments/assets/db3f6d0b-5e38-41f0-bfbd-bbc165009d01)

---

## ✨ Fitur

- Pilih folder sumber yang berisi gambar acak.
- Tambahkan beberapa folder tujuan.
- Tampilkan gambar satu per satu.
- Pindahkan gambar ke folder yang diinginkan hanya dengan satu klik tombol.
- Skip/lewati gambar jika belum ingin dipindah.
- Mendukung berbagai format: `.jpg`, `.png`, `.jpeg`, `.gif`, `.bmp`, dll.

---

## 🚀 Cara Menjalankan

### 1. Clone repositori

```bash
git clone https://github.com/Xysaa/img-sorter-py.git
cd image-sorter-app
```
### 2. Pastikan Python sudah terinstal
```bash
python --version
```
### 3. Instal dependensi
```bash
pip install Pillow
```
### 4. Jalankan aplikasi
```bash
python main.py
```


## 🛠️ Cara Menggunakan
- Saat aplikasi dibuka, akan muncul jendela setup.
- Pilih folder sumber yang berisi gambar belum tersortir.
- Tambahkan nama-nama folder tujuan (akan otomatis dibuat).
- Klik OK, dan aplikasi akan menampilkan gambar satu per satu.
- Klik tombol sesuai nama folder tujuan untuk memindahkan gambar.
- Gunakan tombol Lewati jika ingin melewati gambar tersebut.
  

## 🖼️ Tampilan Awal
![Image](https://github.com/user-attachments/assets/db3f6d0b-5e38-41f0-bfbd-bbc165009d01)
## 💡 Tips
- Jika file dengan nama sama sudah ada di folder tujuan, file baru akan diganti nama otomatis (misalnya: gambar_1.jpg, gambar_2.jpg, dst).
- Gambar yang sudah dipindahkan akan hilang dari daftar dan tidak muncul lagi.
## 📦 Dependensi
- tkinter (default di Python)
- Pillow (untuk membaca dan menampilkan gambar)
## 📄 Lisensi
- Proyek ini open-source dan bebas digunakan untuk keperluan pribadi atau komersial.

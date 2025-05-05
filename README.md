# 📈 Yahoo Finance Historical Data Downloader (YSI)

![Platform](https://img.shields.io/badge/Platform-Localhost-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square)
---

## 🧭 Pendahuluan

**YSI** (Yahoo Finance Historical Data Downloader) adalah alat bantu untuk mengunduh data historis saham dari Yahoo Finance secara lengkap dan bersih. Proyek ini dibuat karena kebutuhan akan data historis saham yang mudah diakses tanpa harus berlangganan atau menggunakan API tambahan.

Dengan UI yang telah disesuaikan berbasis Streamlit, pengguna hanya perlu menempelkan URL historis dari Yahoo Finance, dan aplikasi akan secara otomatis mengambil, membersihkan, dan menyajikan data siap unduh dalam format CSV maupun Excel.

🔍 **Kenapa dibuat?**
- Yahoo Finance adalah salah satu sumber penyedia data terbesar namun memiliki keterbatasan akses data jika tidak berlangganan.
- Banyak pengguna membutuhkan data bersih tanpa elemen seperti dividen dan stock split serta kolom yang rapih.
- Proyek ini mempermudah pemrosesan data saham untuk keperluan analisis teknikal, machine learning, atau laporan keuangan.

Live Preview : https://yahoofinance.up.railway.app/

---
### ✨ User Interface Preview

Berikut adalah cuplikan tampilan antarmuka dari program **Yahoo Finance Historical Data Downloader (YSI)**:

- Pengguna dapat memasukkan URL data historis dari Yahoo Finance, misalnya:  
  `https://finance.yahoo.com/quote/TSLA/history/`
- Program akan otomatis mengenali kode saham dan menampilkan notifikasi keberhasilan.
- Setelah data berhasil diambil, pengguna dapat melihat **preview data historis** (5 baris pertama), termasuk kolom seperti:  
  `Tanggal`, `Open`, `High`, `Low`, `Close`, `Adj Close`, dan `Volume`.
- Total jumlah baris data juga ditampilkan.
- Pengguna kemudian dapat mengunduh data tersebut dalam format **CSV** atau **Excel** yang sudah dibersihkan secara langsung dengan satu klik.
- Terdapat catatan penting dan informasi pengembang di bagian bawah aplikasi.
- Tampilan ini dirancang agar **intuitif, ringan, dan mudah digunakan** bahkan oleh pengguna non-teknis.

<p align="center">
  <img src="https://res.cloudinary.com/dlf3r1kut/image/upload/v1745999999/Preview_YSI_qre7du.png" alt="Contoh Penggunaan YSI" />
</p>

---
## 🛠️ Library & Teknologi yang Digunakan

| Komponen          | Teknologi                         | Fungsi                                 |
|-------------------|-----------------------------------|----------------------------------------|
| Bahasa Pemrograman| Python 3.11+                      | Bahasa utama                           |
| Data Fetching     | [yfinance](https://pypi.org/project/yfinance/) | Mengambil data dari Yahoo Finance      |
| Data Processing   | [pandas](https://pypi.org/project/pandas/)     | Manipulasi dan pembersihan data        |
| Ekspor Excel      | [xlsxwriter](https://pypi.org/project/XlsxWriter/) | Ekspor data ke format Excel            |
| Antarmuka Web     | [Streamlit](https://pypi.org/project/streamlit/) | Antarmuka pengguna berbasis web        |

---

## 🧪 Langkah Instalasi & Penggunaan Program di LocalHost 

Ikuti langkah-langkah berikut untuk menjalankan proyek ini secara lokal:

### 1. Clone Repository

```bash
git clone https://github.com/aldevvv/yahoofinance.git
cd yahoofinance
```

### 2. Buat Virtual Environment (opsional tapi disarankan)

```bash
python -m venv venv
source venv/bin/activate  # Linux / MacOS
venv\Scripts\activate     # Windows
```

### 3. Instal Semua Dependensi Yang Dibutuhkan

```bash
pip install -r requirements.txt
```

### 4. Jalankan Program di LocalHost

```bash
python -m streamlit run ysi.py
```

Aplikasi akan otomatis terbuka di browser pada `http://localhost:8501`

---

## 📎 Contoh URL Saham yang Valid

Masukkan URL seperti ini:

```
https://finance.yahoo.com/quote/TSLA/history/
```

---

## ⚠️ Catatan Penting

- **Rate Limit**: Yahoo Finance memberlakukan pembatasan akses (rate limit). Jika Anda terlalu sering menarik data, sistem akan otomatis memblokir sementara. Aplikasi ini akan menampilkan **waktu tunggu (countdown)** sebelum dapat mencoba lagi.
- **Data Bersih**: Aplikasi ini memfilter data yang tidak relevan seperti baris dividen dan stock split, serta merapikan kolom yang tidak perlu.
- **Tidak memerlukan API Key**: Anda tidak perlu mendaftar atau membuat akun untuk menggunakannya.

---

## 🤝 Kontribusi

Saya sangat terbuka untuk siapapun yang ingin berkontribusi.

Jika Anda menemukan bug, kekurangan, atau ingin menambahkan fitur baru:
- Silakan buat [Issue](https://github.com/aldevvv/yahoofinance/issues)
- Atau langsung kirim [Pull Request](https://github.com/aldevvv/yahoofinance/pulls)

---

## 📄 Lisensi

Proyek ini 100% gratis untuk digunakan siapapun.

---

## 👨‍💻 Developer

Dikembangkan dengan ❤️ oleh [AlDev - Muhammad Alif](https://www.instagram.com/mhdalif.id/)

Silakan follow & hubungi saya jika ada saran, feedback, atau ingin kerja sama.

---

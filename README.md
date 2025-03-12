📊 Dashboard Analisis Data: Bike Sharing Dataset

📌 Pendahuluan

Dashboard ini dibuat menggunakan Streamlit untuk menganalisis data peminjaman sepeda berdasarkan berbagai faktor seperti waktu, musim, dan suhu.

🛠️ Instalasi

Pastikan Anda telah menginstal Python di komputer Anda. Ikuti langkah-langkah berikut untuk menjalankan dashboard ini:

1️⃣ Unduh Repository

kaggle https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset

2️⃣ Buat Virtual Environment (Opsional)

python -m venv venv
source venv/bin/activate  # Untuk macOS/Linux
venv\Scripts\activate  # Untuk Windows

3️⃣ Instal Dependensi

pip install -r requirements.txt

🚀 Menjalankan Dashboard

Pastikan Anda memiliki file dataset day.xlsx dan hour.xlsx di dalam folder proyek.

Jalankan perintah berikut untuk membuka dashboard:

streamlit run app.py

Dashboard akan berjalan di http://localhost:8501 dan bisa dibuka di browser.

🗂️ Struktur Proyek

submission
├───dashboard
| ├───dashboard.py
| ├───day.xlsx
| └───hour.xlsx
├───data
| ├───day.xlsx
| └───hour.xlsx
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt

📊 Fitur dalam Dashboard

RFM Analysis – Menganalisis recency, frequency, dan monetary data peminjaman sepeda.

Clustering (Binning) – Mengelompokkan jumlah peminjaman sepeda berdasarkan kategori penggunaan.

Analisis Pola Peminjaman Sepeda

Berdasarkan waktu (jam dalam sehari)

Berdasarkan musim (Spring, Summer, Fall, Winter)

Perbandingan antara hari kerja dan akhir pekan

Pengaruh suhu terhadap jumlah peminjaman sepeda

📌 Catatan

Pastikan dataset tersedia dalam format yang sesuai.

Jika menemukan bug atau ingin berkontribusi, silakan buat pull request atau laporkan masalah melalui Github.

🎯 Selamat menganalisis! 🚴‍♂️


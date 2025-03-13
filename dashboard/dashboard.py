pip install openpyxl

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("Analisis Data: Bike Sharing Dataset")
st.markdown("Muhammad Agal Lulanika | MC001D5Y1224")

@st.cache_data
def load_data(path: str):
    data = pd.read_excel(path)
    return data

# Membaca kedua file Excel
df_day = load_data("/mount/src/project-analisis-dbs/data/day.xlsx")
df_hour = load_data("/mount/src/project-analisis-dbs/data/hour.xlsx")

# Menambahkan Analisis RFM
st.header("RFM Analysis")

st.write(df_hour.head())
st.write(df_day.head())

df_day['dteday'] = pd.to_datetime(df_day['dteday'])

last_date = df_day['dteday'].max()
df_day['Recency'] = (last_date - df_day['dteday']).dt.days
df_day['Frequency'] = 1
df_day['Monetary'] = df_day['cnt']

rfm_df = df_day.groupby('dteday').agg({'Recency': 'min', 'Frequency': 'sum', 'Monetary': 'sum'}).reset_index()

st.subheader("Tabel RFM Analysis")
st.write(rfm_df.head())

st.subheader("Hasil RFM Analysis")
st.markdown("- Hasil tabel menunjukkan lima entri pertama dari analisis RFM. Kolom dteday merepresentasikan tanggal transaksi, Recency menunjukkan jarak dalam hari sejak transaksi terakhir (menurun setiap harinya), Frequency selalu bernilai 1 karena data dikelompokkan per hari, dan Monetary menunjukkan jumlah total peminjaman dalam satu hari.") 
st.markdown("- Sebagai contoh, pada 1 Januari 2011, nilai Recency adalah 730 hari sejak transaksi terakhir, Frequency adalah 1, dan Monetary sebesar 985. Pada hari berikutnya, Recency berkurang menjadi 729, sementara Frequency tetap 1 dan Monetary turun menjadi 801.")
st.markdown("- Data ini dapat digunakan untuk menganalisis pola peminjaman berdasarkan waktu dan mengidentifikasi tren penggunaan layanan peminjaman.")

# Clustering (Binning)
st.header("Clustering (Binning)")

bins = [0, 1000, 3000, 5000, df_day['cnt'].max()]
labels = ['Low Usage', 'Medium Usage', 'High Usage', 'Very High Usage']
df_day['Usage Cluster'] = pd.cut(df_day['cnt'], bins=bins, labels=labels, include_lowest=True)

# Konversi value_counts() menjadi DataFrame agar tampil lebih rapi
cluster_counts = df_day['Usage Cluster'].value_counts().reset_index()
cluster_counts.columns = ['Usage Cluster', 'Count']

st.write("Distribusi Cluster Penggunaan:")
st.dataframe(cluster_counts)  # Menggunakan st.dataframe untuk tampilan yang lebih rapi

st.subheader("Hasil Clustering (Binning)")
st.markdown("Saya mengelompokkan hari berdasarkan jumlah peminjaman sepeda:") 
st.markdown("- Very High Usage: >5000 peminjaman (286 hari)")
st.markdown("- High Usage: 3000–5000 peminjaman (273 hari)")
st.markdown("- Medium Usage: 1000–3000 peminjaman (153 hari)")
st.markdown("- Low Usage: <1000 peminjaman (19 hari)")
st.markdown("Kita bisa melihat bahwa sebagian besar hari memiliki jumlah peminjaman yang tinggi, dan hanya sedikit hari dengan penggunaan rendah.")

# Menampilkan informasi dataset
def display_info(df, name):
    st.header(f"Informasi Dataset {name}")
    info_df = pd.DataFrame({
        "Kolom": df.columns,
        "Tipe Data": df.dtypes.values,
        "Jumlah Missing Value": df.isnull().sum().values,
        "Jumlah Unik": df.nunique().values
    })
    st.write(info_df)

st.markdown("---")
display_info(df_hour, "Hourly")
st.markdown("---")
display_info(df_day, "Daily")

# Menampilkan Statistik Deskriptif
st.header("Informasi Statistik Dataset Hourly")
st.write(df_hour.describe())

st.header("Informasi Statistik Dataset Daily")
st.write(df_day.describe())

st.subheader("1. Menampilkan Informasi Dataset dalam Bentuk Tabel")
st.markdown("- Fungsi display_info(df, name) dibuat untuk menampilkan informasi dataset dalam bentuk tabel, termasuk nama kolom, tipe data, jumlah nilai yang hilang (missing values), dan jumlah nilai unik. Hal ini mempermudah analisis awal dataset dibandingkan hanya menggunakan df.info(), karena memberikan tampilan yang lebih rapi dan mudah dibaca.")

st.subheader("2. Ringkasan Statistik Dataset")
st.markdown("- hour_df.describe() dan day_df.describe() digunakan untuk menampilkan statistik ringkasan dataset, seperti rata-rata (mean), standar deviasi (std), nilai minimum (min), kuartil, dan nilai maksimum (max). Ini membantu dalam memahami distribusi data dan mendeteksi kemungkinan outlier atau nilai ekstrem.")

st.subheader("3. Menampilkan Jumlah Missing Values dalam Bentuk Tabel")
st.markdown("- Fungsi display_missing_values(df, dataset_name) digunakan untuk menampilkan jumlah missing values pada setiap kolom dalam format tabel menggunakan pustaka tabulate. Format ini lebih rapi dibandingkan hanya menggunakan df.isnull().sum(), sehingga lebih mudah untuk mengidentifikasi apakah ada kolom yang memiliki nilai kosong yang perlu ditangani sebelum analisis lebih lanjut.")

st.subheader("4. Cleaning Data")
st.markdown("- Berdasarkan hasil pengecekan, tidak ditemukan missing values maupun data duplikat dalam dataset hourly maupun daily. Selain itu, tipe data pada setiap kolom sudah sesuai dengan nilai yang diharapkan. Oleh karena itu, tidak diperlukan proses pembersihan data lebih lanjut.")


# Grafik Pola Peminjaman Sepeda Berdasarkan Jam
st.header("A. Pola Peminjaman Sepeda Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df_hour, x="hr", y="cnt", estimator=np.mean, errorbar=None, color="b", ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Jumlah Peminjaman Sepeda")
ax.set_title("Pola Peminjaman Sepeda Berdasarkan Jam")
ax.set_xticks(range(0, 24))
st.pyplot(fig)

st.subheader("Pola Peminjaman Sepeda Berdasarkan Jam")
st.markdown("Peminjaman sepeda cenderung meningkat tajam pada sekitar pukul 7-8 pagi dan sekitar pukul 17-18 sore. Pola ini menunjukkan adanya dua puncak yang kemungkinan besar berkaitan dengan jam berangkat dan pulang kerja atau sekolah. Pada tengah malam hingga dini hari, jumlah peminjaman sepeda sangat rendah, yang sesuai dengan pola aktivitas manusia.")

# Grafik Pengaruh Musim terhadap Peminjaman Sepeda
st.header("B. Pengaruh Musim terhadap Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_day, x="season", y="cnt", estimator=np.mean, errorbar=None, hue="season", palette="Blues", legend=False, ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Jumlah Peminjaman Sepeda")
ax.set_title("Pengaruh Musim terhadap Peminjaman Sepeda")
ax.set_xticks(ticks=[0, 1, 2, 3])
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
st.pyplot(fig)

st.subheader("Pengaruh Musim terhadap Peminjaman Sepeda")
st.markdown("Musim gugur (Fall) memiliki rata-rata peminjaman sepeda tertinggi dibandingkan musim lainnya. Musim dingin (Winter) menunjukkan rata-rata peminjaman yang lebih rendah, kemungkinan karena cuaca yang kurang mendukung untuk bersepeda. Musim semi (Spring) dan musim panas (Summer) memiliki pola peminjaman yang relatif seimbang tetapi masih lebih rendah dibandingkan musim gugur.")

# Grafik Pola peminjaman berdasarkan hari kerja dan akhir pekan
st.header("C. Pola peminjaman berdasarkan hari kerja dan akhir pekan")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df_hour, x="hr", y="cnt", hue="workingday", estimator='mean', palette=["red", "blue"], ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Jumlah Peminjaman Sepeda")
ax.set_title("Pola Peminjaman Sepeda: Hari Kerja vs Akhir Pekan")
ax.legend(["Akhir Pekan", "Hari Kerja"])
ax.set_xticks(range(0, 24))
st.pyplot(fig)

st.subheader("Pola Peminjaman Sepeda di Hari Kerja vs Akhir Pekan")
st.markdown("- Grafik diatas menunjukkan pola peminjaman sepeda berdasarkan jam dalam sehari untuk hari kerja (garis biru) dan akhir pekan (garis merah).")
st.markdown("- Pada hari kerja, terdapat dua puncak peminjaman sepeda yang signifikan: pagi sekitar pukul 8 (kemungkinan besar terkait dengan jam berangkat kerja/sekolah) dan sore sekitar pukul 17-18 (jam pulang kerja/sekolah).")
st.markdown("- Pola peminjaman di akhir pekan lebih merata dengan puncak yang lebih landai sekitar pukul 10-15, yang menunjukkan peminjaman lebih banyak dilakukan untuk aktivitas rekreasi daripada transportasi rutin.")

# Grafik Analisis Pengaruh Suhu terhadap Peminjaman Sepeda di Setiap Musim
st.header("D. Analisis Pengaruh Suhu terhadap Peminjaman Sepeda di Setiap Musim")

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_day, x="temp", y="cnt", hue="season", palette="coolwarm", ax=ax)
ax.set_xlabel("Suhu Normalisasi (0-1)")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
ax.set_title("Pengaruh Suhu terhadap Peminjaman Sepeda di Setiap Musim")
ax.legend(["Spring", "Summer", "Fall", "Winter"])
st.pyplot(fig)

st.subheader("Pengaruh Suhu terhadap Peminjaman Sepeda di Setiap Musim")
st.markdown("- Grafik scatter plot diatas menunjukkan hubungan antara suhu normalisasi (0-1) dan jumlah peminjaman sepeda di setiap musim.")
st.markdown("- Tren menunjukkan bahwa semakin tinggi suhu (dalam rentang normalisasi), semakin banyak jumlah peminjaman sepeda, terutama pada musim panas dan musim gugur.")
st.markdown("- Pada suhu yang lebih rendah (musim semi dan musim dingin), jumlah peminjaman sepeda cenderung lebih sedikit, menunjukkan bahwa kondisi cuaca yang lebih hangat lebih mendukung penggunaan sepeda.")

st.subheader("Conclusion")
st.markdown("- Pola harian peminjaman sepeda menunjukkan bahwa sepeda lebih sering digunakan sebagai moda transportasi utama pada hari kerja, dengan lonjakan peminjaman di jam berangkat dan pulang kerja/sekolah.")
st.markdown("- Musim memiliki pengaruh besar terhadap jumlah peminjaman sepeda, dengan tingkat tertinggi terjadi pada musim gugur dan panas, sementara musim semi dan dingin menunjukkan peminjaman yang lebih rendah.")

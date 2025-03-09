# Public-E-Commerce

# E-Commerce Analysis Dashboard

## Deskripsi Proyek
Proyek ini merupakan analisis data e-commerce public yang mencakup proses mulai dari pengumpulan data, pembersihan, eksplorasi, hingga visualisasi. Hasil analisis mencakup:
- **Top 10 Kategori Produk:** Visualisasi kategori produk dengan pendapatan tertinggi atau jumlah produk terbanyak.
- **RFM Analysis:** Analisis perilaku pelanggan berdasarkan Recency, Frequency, dan Monetary.
- **Geospatial Analysis:** Peta interaktif yang menampilkan sebaran lokasi berdasarkan data geolocation.

## Cara Menjalankan Dashboard
Pastikan Anda telah menginstal semua dependensi dengan perintah:
pip install -r requirements.txt

Untuk menjalankan dashboard, gunakan perintah:
streamlit run dashboard/dashboard.py

## Struktur Folder
- **data/**: Berisi dataset yang digunakan dalam analisis.
- **dashboard/**: Berisi file `dashboard.py` dan file output CSV (jika ada).
- **notebook.ipynb**: Notebook Jupyter dengan proses analisis data lengkap.
- **requirements.txt**: Daftar library yang digunakan.
- **url.txt**: Tautan dashboard jika sudah di-deploy (opsional).

## Insight Utama
- **Top 10 Kategori:** Menunjukkan kategori produk unggulan yang memberikan kontribusi signifikan terhadap pendapatan.
- **RFM Analysis:** Mengidentifikasi pelanggan terbaik berdasarkan waktu transaksi terakhir, frekuensi pembelian, dan total pengeluaran.
- **Geospatial Analysis:** Memetakan sebaran lokasi untuk mendeteksi tren dan konsentrasi transaksi berdasarkan lokasi.

© 2025, E-Commerce Analysis Dashboard

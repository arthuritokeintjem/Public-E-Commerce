# Public-E-Commerce

# E-Commerce Analysis Dashboard

## Deskripsi Proyek
Proyek ini merupakan analisis data e-commerce public yang mencakup proses mulai dari pengumpulan data, pembersihan, eksplorasi, hingga visualisasi. Proyek ini bertujuan untuk memberikan insight mendalam terkait perilaku pelanggan, preferensi pembayaran, performa penjualan produk, efisiensi pengiriman, tingkat kepuasan pelanggan, serta distribusi geografis. Analisis yang dilakukan mencakup:
- Customer Segmentation: Visualisasi Top 10 state dengan jumlah pelanggan terbanyak untuk mengidentifikasi wilayah pasar potensial.
- Payment Preferences: Distribusi metode pembayaran yang digunakan, yang menunjukkan preferensi pelanggan terhadap pembayaran non-tunai dan digital.
- Top-Selling Products: Visualisasi Top 10 kategori produk terlaris berdasarkan jumlah item terjual untuk mendukung strategi inventaris dan promosi.
- Delivery Performance: Analisis distribusi waktu pengiriman dan delay time untuk mengukur efisiensi logistik dan akurasi estimasi pengiriman.
- Customer Satisfaction: Distribusi rating ulasan pelanggan yang memberikan gambaran tentang kualitas layanan dan produk.
- Geospatial Analysis: Peta interaktif yang menampilkan sebaran lokasi pelanggan dan penjual, mengungkap area dengan aktivitas transaksi yang intens.

## Cara Menjalankan Dashboard
Pastikan Anda telah menginstal semua dependensi dengan perintah:
pip install -r requirements.txt

Untuk menjalankan dashboard, gunakan perintah:
streamlit run dashboard/dashboard.py

## Struktur Folder
- **data/**: Berisi dataset yang digunakan dalam analisis.
- **dashboard/**: Berisi file `dashboard.py` dan file output CSV.
- **analisis_data.ipynb**: Notebook Jupyter dengan proses analisis data lengkap.
- **requirements.txt**: Daftar library yang digunakan.
- **url.txt**: Tautan dashboard jika sudah di-deploy.

## Insight Utama
1. **Customer Segmentation**
- Negara bagian seperti "SP" (Sao Paulo) memiliki jumlah pelanggan yang jauh lebih tinggi dibandingkan dengan negara bagian lainnya.
- Perbedaan signifikan antar negara bagian menunjukkan wilayah dengan potensi pasar lebih besar untuk ditargetkan dalam strategi pemasaran.

2. **Payment Preferences**
- Kartu kredit adalah metode pembayaran yang paling sering digunakan, menunjukkan preferensi pelanggan terhadap pembayaran non-tunai.
- Metode lain seperti boleto (invoice pembayaran) juga masih digunakan dalam transaksi.

3. **Top-Selling Products**
- Beberapa kategori produk memiliki jumlah penjualan yang jauh lebih tinggi dibandingkan kategori lainnya.
- Kategori dengan penjualan tinggi menunjukkan permintaan yang kuat, yang dapat menjadi fokus untuk optimasi inventaris dan strategi pemasaran.

4. **Delivery Performance**
- Mayoritas pesanan dikirim dalam waktu yang relatif singkat, namun terdapat beberapa kasus keterlambatan pengiriman yang cukup signifikan.
- Analisis keterlambatan membantu dalam mengevaluasi seberapa akurat estimasi pengiriman dibandingkan dengan waktu aktual.

5. **Customer Satisfaction**
- Sebagian besar pelanggan memberikan rating tinggi untuk produk yang mereka beli, yang menunjukkan tingkat kepuasan pelanggan yang baik.
- Namun, beberapa ulasan negatif mengindikasikan potensi perbaikan dalam layanan atau kualitas produk tertentu.

6. **Geospatial Analysis**
- Peta interaktif menunjukkan konsentrasi transaksi di area tertentu, memberikan insight tentang wilayah dengan aktivitas perdagangan yang tinggi.
- Informasi ini berguna dalam pengambilan keputusan bisnis, seperti penentuan gudang atau ekspansi ke wilayah potensial.

© 2025, E-Commerce Analysis Dashboard

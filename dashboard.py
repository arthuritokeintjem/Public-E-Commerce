import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

# ---------------------------
# 1. Fungsi Memuat Data
# ---------------------------
@st.cache_data
def load_data():
    """
    Memuat file CSV hasil cleaning.
    Pastikan file-file berikut ada di folder 'data':
    - order_reviews_imputed.csv
    - orders_clean.csv
    - products_clean.csv
    - geolocation_clean.csv
    """
    order_reviews = pd.read_csv('order_reviews_imputed.csv')
    orders = pd.read_csv('orders_clean.csv')
    products = pd.read_csv('products_clean.csv')
    geolocation = pd.read_csv('geolocation_sample.csv')
    return order_reviews, orders, products, geolocation

@st.cache_data
def load_rfm_data():
    """
    Memuat dataset RFM yang telah dihitung dan disimpan sebagai CSV.
    Pastikan file 'rfm.csv' sudah tersimpan di folder 'data'.
    """
    rfm = pd.read_csv('data/rfm.csv')
    return rfm

# ---------------------------
# 2. Visualisasi: Top 10 Kategori Produk
# ---------------------------
def plot_top_10_categories(orders, products):
    """
    Visualisasi ini menampilkan 10 kategori produk dengan jumlah produk terbanyak.
    (Anda dapat menyesuaikan logika ini untuk menghitung total pendapatan jika data order_items tersedia.)
    """
    # Contoh: hitung jumlah produk per kategori
    cat_count = products.groupby('product_category_name').size().reset_index(name='counts')
    top_10 = cat_count.sort_values('counts', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_10, x='counts', y='product_category_name', palette='Blues_r', ax=ax)
    ax.set_title('Top 10 Kategori Produk (Berdasarkan Jumlah Produk)', fontsize=14)
    ax.set_xlabel('Counts', fontsize=12)
    ax.set_ylabel('Kategori Produk', fontsize=12)
    plt.tight_layout()
    return fig

# ---------------------------
# 3. Visualisasi: RFM Analysis
# ---------------------------
def plot_rfm_charts(rfm):
    """
    Membuat tiga horizontal bar chart untuk menampilkan top 5 pelanggan berdasarkan:
    - Recency (nilai terendah lebih baik)
    - Frequency (nilai tertinggi)
    - Monetary (nilai tertinggi)
    """
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
    colors = ["#72BCD4"] * 5

    # Recency: sort ascending (lebih rendah lebih baik)
    rfm_recency = rfm.sort_values(by='recency', ascending=True).head(5)
    sns.barplot(x="recency", y="customer_id", data=rfm_recency, palette=colors, ax=axes[0])
    axes[0].set_xlabel("Recency (days)", fontsize=12)
    axes[0].set_ylabel("Customer ID", fontsize=12)
    axes[0].set_title("Top 5 Customers by Recency", fontsize=18)
    axes[0].tick_params(axis='y', labelsize=12)

    # Frequency: sort descending (lebih tinggi lebih baik)
    rfm_frequency = rfm.sort_values(by='frequency', ascending=False).head(5)
    sns.barplot(x="frequency", y="customer_id", data=rfm_frequency, palette=colors, ax=axes[1])
    axes[1].set_xlabel("Frequency (No. of Orders)", fontsize=12)
    axes[1].set_ylabel("Customer ID", fontsize=12)
    axes[1].set_title("Top 5 Customers by Frequency", fontsize=18)
    axes[1].tick_params(axis='y', labelsize=12)

    # Monetary: sort descending (lebih tinggi lebih baik)
    rfm_monetary = rfm.sort_values(by='monetary', ascending=False).head(5)
    sns.barplot(x="monetary", y="customer_id", data=rfm_monetary, palette=colors, ax=axes[2])
    axes[2].set_xlabel("Monetary (Total Price)", fontsize=12)
    axes[2].set_ylabel("Customer ID", fontsize=12)
    axes[2].set_title("Top 5 Customers by Monetary", fontsize=18)
    axes[2].tick_params(axis='y', labelsize=12)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

# ---------------------------
# 4. Visualisasi: Geospatial Analysis
# ---------------------------
def plot_geospatial(geolocation):
    """
    Membuat peta interaktif menggunakan Folium.
    Ukuran peta diperbesar dengan width=900 dan height=700.
    """
    # Ambil sampel data agar peta tidak overload
    geo_sample = geolocation.sample(n=min(5000, len(geolocation)), random_state=42)
    m = folium.Map(location=[-20.998353, -46.461098], zoom_start=4)
    for _, row in geo_sample.iterrows():
        lat = row['geolocation_lat']
        lng = row['geolocation_lng']
        folium.CircleMarker(
            location=[lat, lng],
            radius=2,
            fill=True,
            color='blue',
            fill_opacity=0.5
        ).add_to(m)
    st_map = st_folium(m, width=900, height=700)
    return st_map

# ---------------------------
# 5. Streamlit Utama
# ---------------------------
def main():
    st.set_page_config(page_title="E-Commerce Analysis Dashboard", layout="wide")
    st.title("E-Commerce Analysis Dashboard")

    # Muat data
    order_reviews, orders, products, geolocation = load_data()
    rfm_df = load_rfm_data()
    
    # Sidebar menu
    st.sidebar.title("Menu")
    menu_options = ["Home", "Top 10 Categories", "RFM Analysis", "Geospatial Analysis"]
    choice = st.sidebar.selectbox("Pilih Halaman", menu_options)

    if choice == "Home":
        st.subheader("Selamat Datang di Dashboard E-Commerce!")
        st.write("Gunakan menu di sidebar untuk eksplorasi data.")
    
    elif choice == "Top 10 Categories":
        st.subheader("Visualisasi: Top 10 Kategori Produk")
        fig_top10 = plot_top_10_categories(orders, products)
        st.pyplot(fig_top10)
        st.markdown("**Insight:** Visualisasi ini menunjukkan 10 kategori produk dengan jumlah produk terbanyak. Insight ini membantu tim pemasaran untuk mengidentifikasi kategori yang paling potensial untuk peningkatan penjualan atau pengembangan produk.")
    
    elif choice == "RFM Analysis":
        st.subheader("RFM Analysis")
        fig_rfm = plot_rfm_charts(rfm_df)
        st.pyplot(fig_rfm)
        st.markdown("**Insight:** Berdasarkan analisis RFM, terlihat bahwa pelanggan yang baru-baru ini bertransaksi (recency rendah), yang sering bertransaksi (frequency tinggi), dan yang memiliki total pengeluaran tinggi (monetary tinggi) merupakan target utama untuk strategi retensi dan promosi. Visualisasi ini memberikan gambaran tentang pelanggan terbaik berdasarkan tiga parameter tersebut.")
    
    elif choice == "Geospatial Analysis":
        st.subheader("Geospatial Analysis")
        st.write("Peta interaktif di bawah ini menampilkan sebaran lokasi berdasarkan data geolocation. Titik yang lebih padat menunjukkan konsentrasi lokasi transaksi yang tinggi.")
        plot_geospatial(geolocation)
    
    st.write("---")
    st.write("© 2025, E-Commerce Analysis Dashboard")

if __name__ == "__main__":
    main()

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
    Pastikan file-file berikut ada di folder 'data' atau 'dashboard' sesuai dengan path:
      - customers_dataset.csv
      - orders_clean.csv
      - order_payments_dataset.csv
      - order_items_dataset.csv
      - order_reviews_imputed.csv
      - products_clean.csv
      - product_category_name_translation.csv
      - geolocation_sample.csv
    """
    customers = pd.read_csv('data/customers_dataset.csv')
    orders = pd.read_csv('dashboard/orders_clean.csv')
    order_payments = pd.read_csv('data/order_payments_dataset.csv')
    order_items = pd.read_csv('data/order_items_dataset.csv')
    order_reviews = pd.read_csv('dashboard/order_reviews_imputed.csv')
    geolocation = pd.read_csv('dashboard/geolocation_sample.csv')
    products = pd.read_csv('dashboard/products_clean.csv')
    products_category = pd.read_csv('data/product_category_name_translation.csv')
    return customers, orders, order_payments, order_items, order_reviews, geolocation, products, products_category

@st.cache_data

# ---------------------------
# 2. Visualisasi: Customer Segmentation
# ---------------------------
def plot_customer_segmentation(customers):
    """
    Menampilkan Top 10 States with the Most Customers.
    
    **Insight:**
    - Visualisasi bar chart menunjukkan distribusi pelanggan per state, dengan beberapa state (misalnya “SP”) memiliki jumlah pelanggan yang jauh lebih tinggi.
    - Perbedaan signifikan antar state mengindikasikan bahwa wilayah tertentu memiliki potensi pasar yang lebih besar.
    - Data geografis ini bisa dijadikan dasar untuk strategi pemasaran yang ditargetkan sesuai dengan potensi wilayah.
    """
    customer_location = customers['customer_state'].value_counts().reset_index()
    customer_location.columns = ['State', 'Customer Count']
    customer_location = customer_location.sort_values(by='Customer Count', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='State', y='Customer Count', data=customer_location, palette='Blues_r', ax=ax)
    ax.set_title('Top 10 States with the Most Customers', fontsize=15)
    ax.set_xlabel('State', fontsize=12)
    ax.set_ylabel('Customer Count', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    return fig

# ---------------------------
# 3. Visualisasi: Payment Preferences
# ---------------------------
def plot_payment_preferences(customers, orders, order_payments):
    """
    Menampilkan distribusi metode pembayaran yang paling sering digunakan.
    
    **Insight:**
    - Count plot menunjukkan bahwa metode pembayaran tertentu, misalnya kartu kredit, mendominasi transaksi.
    - Distribusi ini mengindikasikan preferensi pelanggan terhadap pembayaran non-tunai dan digital.
    - Informasi ini memberikan dasar untuk evaluasi dan pengoptimalan sistem pembayaran agar sesuai dengan kebiasaan konsumen.
    """
    # Gabungkan dataset untuk mendapatkan kolom 'payment_type'
    payments_orders = pd.merge(order_payments, orders, on='order_id', how='inner')
    payments_orders_customers = pd.merge(payments_orders, customers, on='customer_id', how='inner')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(y='payment_type', data=payments_orders_customers,
                  order=payments_orders_customers['payment_type'].value_counts().index,
                  palette='pastel', ax=ax)
    ax.set_title('Distribution of Payment Methods', fontsize=15)
    plt.tight_layout()
    return fig

# ---------------------------
# 4. Visualisasi: Top-Selling Products
# ---------------------------
def plot_top_selling_products(order_items, products, products_category):
    """
    Menampilkan Top 10 Best Selling Product Categories.
    
    **Insight:**
    - Visualisasi bar chart top 10 kategori produk menunjukkan bahwa beberapa kategori memiliki jumlah item terjual jauh lebih tinggi.
    - Kategori dengan penjualan tinggi mengindikasikan adanya permintaan yang kuat dari pelanggan terhadap produk-produk tertentu.
    - Insight ini sangat berguna untuk pengambilan keputusan terkait inventaris dan strategi promosi.
    """
    products_order_items = pd.merge(products, order_items, on='product_id')
    products_category_order_items = pd.merge(products_category, products_order_items, on='product_category_name')
    top_category = products_category_order_items['product_category_name_english'].value_counts().reset_index()
    top_category.columns = ['Category', 'Item Count']
    top_category = top_category.sort_values(by='Item Count', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Item Count', y='Category', data=top_category, palette='crest', ax=ax)
    ax.set_title('Top 10 Best Selling Product Categories', fontsize=15)
    ax.set_xlabel('Item Count', fontsize=12)
    ax.set_ylabel('Category', fontsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    return fig
    
# ---------------------------
# 5. Visualisasi: Delivery Performance
# ---------------------------
def plot_delivery_performance(orders):
    """
    Menampilkan distribusi waktu pengiriman dan delay time.
    
    **Insight:**
    - Histogram distribusi waktu pengiriman (shipping time) menunjukkan bahwa mayoritas pesanan dikirim dalam rentang waktu yang relatif singkat.
    - Terdapat outlier yang mengindikasikan adanya pesanan dengan keterlambatan signifikan.
    - Analisis delay time membantu mengukur akurasi estimasi pengiriman dibandingkan waktu aktual, memberikan gambaran efisiensi logistik.
    """
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
    
    orders['shipping_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
    orders['delay_time'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days
    
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.histplot(orders['shipping_time'].dropna(), bins=50, kde=True, color='skyblue', ax=ax1)
    ax1.set_title('Distribution of Shipping Time', fontsize=15)
    ax1.set_xlabel('Shipping Time (days)', fontsize=12)
    ax1.set_ylabel('Order Count', fontsize=12)
    plt.tight_layout()
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.histplot(orders['delay_time'].dropna(), bins=50, kde=True, color='salmon', ax=ax2)
    ax2.set_title('Distribution of Delay Time', fontsize=15)
    ax2.set_xlabel('Delay Time (days)', fontsize=12)
    ax2.set_ylabel('Order Count', fontsize=12)
    plt.tight_layout()
    
    return fig1, fig2

# ---------------------------
# 6. Visualisasi: Customer Satisfaction
# ---------------------------
def plot_customer_satisfaction(order_reviews, order_items):
    """
    Menampilkan distribusi review score dari pelanggan.
    
    **Insight:**
    - Count plot distribusi rating menunjukkan mayoritas pelanggan memberikan nilai tinggi, menandakan kepuasan yang baik.
    - Adanya rating yang lebih rendah mengindikasikan area untuk perbaikan layanan atau produk.
    - Analisis ini memberikan gambaran keseluruhan tentang kualitas pengalaman pelanggan.
    """
    reviews_products = pd.merge(order_reviews, order_items, on='order_id', how='inner')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(y='review_score', data=reviews_products, 
                  order=reviews_products['review_score'].value_counts().index, 
                  palette='RdYlGn', ax=ax)
    ax.set_title('Distribution of Customer Review Scores', fontsize=15)
    plt.tight_layout()
    return fig

# ---------------------------
# 7. Visualisasi: Geospatial Analysis
# ---------------------------
def plot_geospatial(geolocation):
    """
    Menampilkan peta interaktif menggunakan Folium.
    Peta diperbesar dengan width=900 dan height=700.
    
    **Insight:**
    - Peta interaktif mengungkapkan sebaran geografis pelanggan dan penjual.
    - Area dengan konsentrasi tinggi menunjukkan wilayah dengan aktivitas transaksi intens, potensial untuk pengembangan infrastruktur atau strategi pemasaran.
    """
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

def plot_orders_over_time(orders):
    """
    Menampilkan tren jumlah pesanan berdasarkan rentang tanggal yang dipilih.
    """
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

    # Sidebar filter untuk memilih rentang tanggal
    min_date = orders['order_purchase_timestamp'].min().date()
    max_date = orders['order_purchase_timestamp'].max().date()
    start_date, end_date = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Filter data berdasarkan tanggal yang dipilih
    filtered_orders = orders[
        (orders['order_purchase_timestamp'].dt.date >= start_date) &
        (orders['order_purchase_timestamp'].dt.date <= end_date)
    ]

    # Hitung jumlah pesanan per tanggal
    orders_per_day = filtered_orders.groupby(filtered_orders['order_purchase_timestamp'].dt.date).size().reset_index(name='order_count')

    # Visualisasi data
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='order_purchase_timestamp', y='order_count', data=orders_per_day, ax=ax, marker='o', color='blue')
    ax.set_title(f'Jumlah Pesanan dari {start_date} sampai {end_date}', fontsize=15)
    ax.set_xlabel('Tanggal', fontsize=12)
    ax.set_ylabel('Jumlah Pesanan', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

def plot_filtered_top_selling_products(order_items, products, products_category):
    """
    Menampilkan jumlah penjualan per kategori produk berdasarkan filter yang dipilih.
    """
    products_order_items = pd.merge(products, order_items, on='product_id')
    products_category_order_items = pd.merge(products_category, products_order_items, on='product_category_name')

    # List semua kategori unik
    all_categories = sorted(products_category_order_items['product_category_name_english'].unique())

    # Sidebar: Dropdown untuk memilih kategori produk
    selected_category = st.sidebar.selectbox("Pilih Kategori Produk", all_categories)

    # Filter data berdasarkan kategori yang dipilih
    filtered_data = products_category_order_items[products_category_order_items['product_category_name_english'] == selected_category]

    # Hitung jumlah item terjual per kategori
    top_category = filtered_data['product_category_name_english'].value_counts().reset_index()
    top_category.columns = ['Category', 'Item Count']
    top_category = top_category.sort_values(by='Item Count', ascending=False).head(10)

    # Membuat visualisasi
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Item Count', y='Category', data=top_category, palette='crest', ax=ax)
    ax.set_title(f'Total Selling Product Categories {"(Filtered)" if selected_category != "Semua Kategori" else ""}', fontsize=15)
    ax.set_xlabel('Item Count', fontsize=12)
    ax.set_ylabel('Category', fontsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# ---------------------------
# 10. Streamlit Utama
# ---------------------------
def main():
    st.set_page_config(page_title="E-Commerce Analysis Dashboard", layout="wide")
    st.title("E-Commerce Analysis Dashboard")
    
    # Memuat data
    customers, orders, order_payments, order_items, order_reviews, geolocation, products, products_category = load_data()
    
    menu = st.sidebar.radio("Select a section:", [
        "Home",
        "Customer Segmentation",
        "Payment Preferences",
        "Top-Selling Products",
        "Delivery Performance",
        "Customer Satisfaction",
        "Geospatial Analysis",
        "Total Selling Products (Category Filter)",
        "Order Trends (Date Filter)"
    ])
    
    if menu == "Home":
        st.subheader("Welcome to the E-Commerce Analysis Dashboard")
        st.write("Use the sidebar to navigate through different sections of the dashboard.")
    
    elif menu == "Customer Segmentation":
        st.subheader("Customer Segmentation: Top 10 States with the Most Customers")
        fig = plot_customer_segmentation(customers)
        st.pyplot(fig)
        st.markdown("""
**Insight:**
- Visualisasi bar chart menunjukkan distribusi pelanggan per state, dengan beberapa state (misalnya “SP”) memiliki jumlah pelanggan yang jauh lebih tinggi dibandingkan state lainnya.
- Perbedaan signifikan antar state mengindikasikan bahwa wilayah tertentu memiliki potensi pasar yang lebih besar.
- Data geografis ini bisa dijadikan dasar untuk strategi pemasaran yang ditargetkan sesuai dengan potensi wilayah.
        """)
    
    elif menu == "Payment Preferences":
        st.subheader("Payment Preferences: Most Frequently Used Payment Methods")
        fig = plot_payment_preferences(customers, orders, order_payments)
        st.pyplot(fig)
        st.markdown("""
**Insight:**
- Count plot dari kolom ‘payment_type’ menunjukkan bahwa metode pembayaran tertentu, misalnya kartu kredit, mendominasi transaksi.
- Distribusi ini mengindikasikan preferensi pelanggan terhadap pembayaran non-tunai dan digital.
- Informasi ini memberikan dasar untuk evaluasi dan pengoptimalan sistem pembayaran agar sesuai dengan kebiasaan konsumen.
        """)
    
    elif menu == "Top-Selling Products":
        st.subheader("Top-Selling Products: Top 10 Best Selling Product Categories")
        fig = plot_top_selling_products(order_items, products, products_category)
        st.pyplot(fig)
        st.markdown("""
**Insight:**
- Visualisasi bar chart top 10 kategori produk menunjukkan bahwa beberapa kategori memiliki jumlah item terjual jauh lebih tinggi dibandingkan yang lain.
- Kategori dengan penjualan tinggi mengindikasikan adanya permintaan yang kuat dari pelanggan terhadap produk-produk tertentu.
- Insight ini sangat berguna untuk pengambilan keputusan terkait inventaris dan strategi promosi agar lebih fokus pada kategori yang paling menguntungkan.
        """)

    elif menu == "Delivery Performance":
        st.subheader("Delivery Performance")
        fig1, fig2 = plot_delivery_performance(orders)
        st.pyplot(fig1)
        st.pyplot(fig2)
        st.markdown("""
**Insight:**
- Histogram distribusi waktu pengiriman (shipping time) menunjukkan bahwa mayoritas pesanan dikirim dalam rentang waktu yang relatif singkat.
- Terdapat outlier yang mengindikasikan adanya pesanan yang mengalami keterlambatan signifikan.
- Analisis delay time membantu mengukur seberapa akurat estimasi pengiriman dibandingkan dengan waktu aktual, memberikan gambaran tentang efisiensi logistik.
        """)
    
    elif menu == "Customer Satisfaction":
        st.subheader("Customer Satisfaction: Distribution of Customer Review Scores")
        fig = plot_customer_satisfaction(order_reviews, order_items)
        st.pyplot(fig)
        st.markdown("""
**Insight:**
- Count plot distribusi rating menunjukkan mayoritas pelanggan memberikan nilai tinggi, yang menandakan tingkat kepuasan yang baik.
- Meskipun begitu, terdapat beberapa nilai rating yang lebih rendah yang perlu ditinjau untuk mengidentifikasi potensi perbaikan dalam layanan atau produk.
- Analisis ini memberikan gambaran keseluruhan tentang kualitas pengalaman pelanggan dan area yang mungkin perlu ditingkatkan.
        """)
    
    elif menu == "Geospatial Analysis":
        st.subheader("Geospatial Analysis")
        st.write("Peta interaktif di bawah ini menampilkan sebaran lokasi berdasarkan data geolocation. Titik yang lebih padat menunjukkan konsentrasi lokasi transaksi yang tinggi.")
        plot_geospatial(geolocation)
        st.markdown("""
**Insight:**
- Peta interaktif mengungkapkan sebaran geografis pelanggan dan penjual.
- Area dengan konsentrasi titik yang tinggi mengindikasikan wilayah dengan aktivitas transaksi yang intens, yang dapat menjadi target pengembangan infrastruktur atau strategi pemasaran.
        """)
    
    elif menu == "Order Trends (Date Filter)":
        st.subheader("Order Trends Over Time")
        plot_orders_over_time(orders)

    elif menu == "Total Selling Products (Category Filter)":
        st.subheader("Total Selling Products with Category Filter")
        plot_filtered_top_selling_products(order_items, products, products_category)

    st.write("---")
    st.write("© 2025, E-Commerce Analysis Dashboard")

if __name__ == "__main__":
    main()

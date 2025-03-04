import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema seaborn
sns.set(style='dark')

# ---- HELPER FUNCTIONS ----
def create_orders_status_df(df):
    """Membuat DataFrame untuk distribusi status order."""
    if df.empty:
        return pd.DataFrame(columns=['order_status', 'count'])  # Mengembalikan DataFrame kosong jika tidak ada data
    orders_status = df['order_status'].value_counts().reset_index()
    orders_status.columns = ['order_status', 'count']
    return orders_status

def create_top_products_df(df):
    """Membuat DataFrame untuk top 10 kategori produk."""
    if df.empty:
        return pd.DataFrame(columns=['product_category_name', 'count'])
    top_products = df['product_category_name'].value_counts().head(10).reset_index()
    top_products.columns = ['product_category_name', 'count']
    return top_products

def create_payment_type_df(df):
    """Membuat DataFrame untuk distribusi metode pembayaran."""
    if df.empty:
        return pd.DataFrame(columns=['payment_type', 'count'])
    payment_type = df['payment_type'].value_counts().reset_index()
    payment_type.columns = ['payment_type', 'count']
    return payment_type

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    orders = pd.read_csv('./Data/orders_dataset.csv')
    payments = pd.read_csv('./Data/order_payments_dataset.csv')
    products = pd.read_csv('./Data/products_dataset.csv')
    sellers = pd.read_csv('./Data/sellers_dataset.csv')
    order_items = pd.read_csv('./Data/order_items_dataset.csv')

    # Konversi ke datetime
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    
    return orders, payments, products, sellers, order_items

# ---- DASHBOARD ----
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Load data
orders, payments, products, sellers, order_items = load_data()

# ---- SIDEBAR ----
st.sidebar.title('E-commerce Dashboard')
st.sidebar.image("foto.jpg", use_column_width=True)

# Profil Developer
st.sidebar.markdown("### Developer")
st.sidebar.write("**Nama:** Muhamad Hamzah")
st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/muhamad-hamzah-b25b85281/)")
st.sidebar.markdown("[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/2206081MuhamadHamzah)")

# ---- FILTER ----
st.sidebar.header("Filter Data")

# Filter Tanggal dengan Try-Except
try:
    min_date = orders['order_purchase_timestamp'].min()
    max_date = orders['order_purchase_timestamp'].max()

    start_date, end_date = st.sidebar.date_input(
        'Pilih Rentang Tanggal',
        [min_date, max_date]
    )

    # Konversi ke datetime jika perlu
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

except:
    start_date, end_date = min_date, max_date  # Default ke min-max jika error

# Filter Berdasarkan Kategori Produk
selected_category = st.sidebar.selectbox(
    'Pilih Kategori Produk',
    options=['All'] + list(products['product_category_name'].dropna().unique())  # Hindari NaN
)

# Filter Berdasarkan Metode Pembayaran
selected_payment = st.sidebar.selectbox(
    'Pilih Metode Pembayaran',
    options=['All'] + list(payments['payment_type'].dropna().unique())
)

# Filter Berdasarkan Cuaca (jika ada dalam dataset)
if 'weather' in orders.columns:
    selected_weather = st.sidebar.selectbox(
        'Pilih Cuaca',
        options=['All'] + list(orders['weather'].dropna().unique())
    )

# ---- FILTER DATA ----
orders_filtered = orders[
    (orders['order_purchase_timestamp'] >= start_date) & 
    (orders['order_purchase_timestamp'] <= end_date)
]

if selected_category != 'All':
    products_filtered = products[products['product_category_name'] == selected_category]
else:
    products_filtered = products

if selected_payment != 'All':
    payments_filtered = payments[payments['payment_type'] == selected_payment]
else:
    payments_filtered = payments

if 'weather' in orders.columns and selected_weather != 'All':
    orders_filtered = orders_filtered[orders_filtered['weather'] == selected_weather]

# ---- DASHBOARD OUTPUT ----
st.title('E-commerce Analysis Dashboard 📊')

st.write(f"Data diperbarui: Menampilkan Pemesanan dari **{start_date.date()}** hingga **{end_date.date()}**")

# ---- METRICS ----
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Orders", f"{len(orders_filtered):,}")
with col2:
    st.metric("Total Products", f"{len(products_filtered):,}")
with col3:
    st.metric("Total Sellers", f"{len(sellers):,}")
with col4:
    st.metric("Total Payments", f"${payments_filtered['payment_value'].sum():,.2f}")

# ---- ORDER STATUS DISTRIBUTION ----
st.header('1. Order Status Distribution')
orders_status_df = create_orders_status_df(orders_filtered)

if orders_status_df.empty:
    st.warning("Tidak ada data untuk Order Status Distribution.")
else:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=orders_status_df, x='order_status', y='count', palette='viridis')
    plt.xticks(rotation=45)
    plt.title('Distribution of Order Status')
    st.pyplot(fig)
    plt.close()

# ---- TOP 10 PRODUCT CATEGORIES ----
st.header('2. Top 10 Product Categories')
top_products_df = create_top_products_df(products_filtered)

if top_products_df.empty:
    st.warning("Tidak ada data untuk kategori produk.")
else:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_products_df, x='count', y='product_category_name', palette='viridis')
    plt.title(f'Top 10 Product Categories (Category: {selected_category})')
    st.pyplot(fig)
    plt.close()

# ---- PAYMENT METHOD DISTRIBUTION ----
st.header('3. Payment Method Distribution')
payment_type_df = create_payment_type_df(payments_filtered)

if payment_type_df.empty:
    st.warning("Tidak ada data untuk metode pembayaran.")
else:
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.pie(payment_type_df['count'], labels=payment_type_df['payment_type'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('viridis', len(payment_type_df)))
    plt.axis('equal')  # Menjaga aspek ratio tetap 1:1
    plt.title('Payment Method Distribution')
    st.pyplot(fig)
    plt.close()

# ---- SELLER DISTRIBUTION ----
st.header('4. Seller Distribution')
sellers_per_state = sellers['seller_state'].value_counts().reset_index()
sellers_per_state.columns = ['seller_state', 'count']

if sellers_per_state.empty:
    st.warning("Tidak ada data untuk distribusi penjual.")
else:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=sellers_per_state, x='seller_state', y='count', palette='magma')
    plt.xticks(rotation=45)
    plt.title('Number of Sellers by State')
    st.pyplot(fig)
    plt.close()

# ---- TRANSACTION TRENDS ----
st.header('5. Transaction Trends Over Time')
orders_filtered['order_date'] = orders_filtered['order_purchase_timestamp'].dt.date
orders_per_day = orders_filtered.groupby('order_date').size().reset_index(name='count')

if orders_per_day.empty:
    st.warning("Tidak ada data untuk tren transaksi.")
else:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=orders_per_day, x='order_date', y='count', marker='o', color='b')
    plt.xlabel('Date')
    plt.ylabel('Number of Orders')
    plt.title('Transactions Over Time')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close()

# ---- FOOTER ----
st.sidebar.markdown("---")
st.sidebar.write("Developed by Muhamad Hamzah")

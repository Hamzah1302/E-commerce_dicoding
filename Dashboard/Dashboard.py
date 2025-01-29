import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema seaborn
sns.set(style='dark')

# Helper Functions
def create_orders_status_df(df):
    orders_status = df['order_status'].value_counts().reset_index()
    orders_status.columns = ['order_status', 'count']
    return orders_status

def create_top_products_df(df):
    top_products = df['product_category_name'].value_counts().head(10).reset_index()
    top_products.columns = ['product_category_name', 'count']
    return top_products

def create_payment_type_df(df):
    payment_type = df['payment_type'].value_counts().reset_index()
    payment_type.columns = ['payment_type', 'count']
    return payment_type

def create_seller_city_df(df):
    seller_city = df['seller_city'].value_counts().head(10).reset_index()
    seller_city.columns = ['seller_city', 'count']
    return seller_city

# Load Data
def load_data():
    orders = pd.read_csv('./Data/orders_dataset.csv')
    payments = pd.read_csv('./Data/order_payments_dataset.csv')
    products = pd.read_csv('./Data/products_dataset.csv')
    sellers = pd.read_csv('./Data/sellers_dataset.csv')
    order_items = pd.read_csv('./Data/order_items_dataset.csv')
    # Pastikan kolom tanggal ada di dataset
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    return orders, payments, products, sellers, order_items

# Dashboard
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Load data
orders, payments, products, sellers, order_items = load_data()

# Sidebar
st.sidebar.title('E-commerce Dashboard')
st.sidebar.image("foto.jpg", use_column_width=True)
# Profil
st.sidebar.markdown("### Developer")
st.sidebar.write("**Nama:** Muhamad Hamzah")
st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/muhamad-hamzah-b25b85281/)")
st.sidebar.markdown("[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/2206081MuhamadHamzah)")

# Main Dashboard
st.title('E-commerce Analysis Dashboard 📊')

# Filter Berdasarkan Tanggal
start_date, end_date = st.sidebar.date_input(
    'Pilih Rentang Tanggal', 
    [orders['order_purchase_timestamp'].min(), orders['order_purchase_timestamp'].max()]
)

# Filter berdasarkan tanggal
orders_filtered = orders[(orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
                          (orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))]

# Filter Berdasarkan Kategori Produk
selected_category = st.sidebar.selectbox(
    'Pilih Kategori Produk', 
    options=['All'] + list(products['product_category_name'].unique())
)

# Filter data produk
if selected_category != 'All':
    products_filtered = products[products['product_category_name'] == selected_category]
else:
    products_filtered = products

# Tampilkan Jumlah Pemesanan Berdasarkan Tanggal
st.write(f"Data Diperbarui: Menampilkan Pemesanan dari {start_date} hingga {end_date}")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Orders", f"{len(orders_filtered):,}")
with col2:
    st.metric("Total Products", f"{len(products_filtered):,}")
with col3:
    st.metric("Total Sellers", f"{len(sellers):,}")
with col4:
    st.metric("Total Payments", f"${payments['payment_value'].sum():,.2f}")

# Order Status Analysis
st.header('1. Order Status Distribution')
orders_status_df = create_orders_status_df(orders_filtered)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=orders_status_df, x='order_status', y='count', palette='viridis')
plt.xticks(rotation=45)
plt.title('Distribution of Order Status')
st.pyplot(fig)
plt.close()

# Product Category Analysis
st.header('2. Top 10 Product Categories')
top_products_df = create_top_products_df(products_filtered)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_products_df, x='count', y='product_category_name', palette='viridis')
plt.title(f'Top 10 Product Categories (Category: {selected_category})')
st.pyplot(fig)
plt.close()

# Payment Analysis
st.header('3. Payment Method Distribution')
payment_type_df = create_payment_type_df(payments)
fig, ax = plt.subplots(figsize=(8, 8))
plt.pie(payment_type_df['count'], labels=payment_type_df['payment_type'], autopct='%1.1f%%')
plt.title('Payment Method Distribution')
st.pyplot(fig)
plt.close()

# Seller Analysis
st.header('4. Top 10 Cities by Number of Sellers')
seller_city_df = create_seller_city_df(sellers)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=seller_city_df, x='count', y='seller_city', palette='viridis')
plt.title('Top 10 Cities by Number of Sellers')
st.pyplot(fig)
plt.close()

# Additional Analysis Section
st.header('5. Additional Insights')
col1, col2 = st.columns(2)

with col1:
    st.subheader('Average Order Value')
    avg_order = payments.groupby('order_id')['payment_value'].sum().mean()
    st.metric("Average Order Value", f"${avg_order:.2f}")

with col2:
    st.subheader('Payment Installments')
    avg_installments = payments['payment_installments'].mean()
    st.metric("Average Installments", f"{avg_installments:.1f}")

# Footer
st.markdown("---")
st.caption("E-commerce Dashboard © 2025")

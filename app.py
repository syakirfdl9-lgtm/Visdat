import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Mengatur tampilan halaman
st.set_page_config(page_title="Dashboard Gizi Balita Jabar", layout="wide")

st.title("Visualisasi Status Gizi Balita Kota Bandung")
st.write("Aplikasi ini mengintegrasikan data master dari Supabase (PostgreSQL) dan data metrik dari SQLite.")

# 1. Koneksi ke Multi-DBMS
sqlite_engine = create_engine('sqlite:///database_sqlite.db')

@st.cache_resource
def init_supabase():
    return create_engine(st.secrets["SUPABASE_URL"])

supabase_engine = init_supabase()

# 2. Tarik Data
df_metrik = pd.read_sql("SELECT * FROM metrik_gizi", sqlite_engine)
df_master = pd.read_sql("SELECT * FROM master_wilayah", supabase_engine)

# 3. Integrasi Data (Merge) & Perbaikan Tipe Data Angka
df_gabungan = pd.merge(df_metrik, df_master, on='bps_kode_kecamatan', how='left')
df_gabungan['jumlah_balita'] = pd.to_numeric(df_gabungan['jumlah_balita'], errors='coerce').fillna(0)

# 4. Slicer / Filter Interaktif di Sidebar (Dropdown)
st.sidebar.header("Filter Data")
opsi_tahun = ["Semua"] + list(sorted(df_gabungan['tahun'].unique()))
opsi_status = ["Semua"] + list(df_gabungan['keterangan'].unique())
opsi_kecamatan = ["Semua"] + list(sorted(df_gabungan['bps_nama_kecamatan'].dropna().unique()))
opsi_puskesmas = ["Semua"] + list(sorted(df_gabungan['upt_puskesmas'].dropna().unique()))

tahun_pilihan = st.sidebar.selectbox("Pilih Tahun:", options=opsi_tahun)
status_pilihan = st.sidebar.selectbox("Pilih Status Gizi:", options=opsi_status)
kecamatan_pilihan = st.sidebar.selectbox("Pilih Kecamatan:", options=opsi_kecamatan)
puskesmas_pilihan = st.sidebar.selectbox("Pilih Puskesmas:", options=opsi_puskesmas)

df_filter = df_gabungan.copy()
if tahun_pilihan != "Semua":
    df_filter = df_filter[df_filter['tahun'] == tahun_pilihan]
if status_pilihan != "Semua":
    df_filter = df_filter[df_filter['keterangan'] == status_pilihan]
if kecamatan_pilihan != "Semua":
    df_filter = df_filter[df_filter['bps_nama_kecamatan'] == kecamatan_pilihan]
if puskesmas_pilihan != "Semua":
    df_filter = df_filter[df_filter['upt_puskesmas'] == puskesmas_pilihan]

# Menampilkan Kembali Tabel (Keterangan di Paling Kanan)
st.subheader("Data Terfilter")
kolom_lain = [col for col in df_filter.columns if col != 'keterangan']
df_display = df_filter[kolom_lain + ['keterangan']]
st.dataframe(df_display, use_container_width=True, height=350)

# 5. Visualisasi Grafik (Plotly Interaktif - Tema Hijau)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Balita Berdasarkan Status Gizi")
    agregasi_status = df_filter.groupby('keterangan')['jumlah_balita'].sum().reset_index()
    agregasi_status = agregasi_status.sort_values(by='jumlah_balita', ascending=False)
    
    fig1 = px.bar(agregasi_status, x='jumlah_balita', y='keterangan', orientation='h',
                  color_discrete_sequence=['mediumseagreen'])
    fig1.update_layout(xaxis_title="Jumlah Balita", yaxis_title="Status Gizi")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Tren Jumlah Balita per Tahun")
    agregasi_tahun = df_filter.groupby('tahun')['jumlah_balita'].sum().reset_index()
    
    fig2 = px.line(agregasi_tahun, x='tahun', y='jumlah_balita', markers=True,
                   color_discrete_sequence=['mediumseagreen'])
    fig2.update_layout(xaxis_title="Tahun", yaxis_title="Total Balita", xaxis=dict(dtick=1))
    st.plotly_chart(fig2, use_container_width=True)
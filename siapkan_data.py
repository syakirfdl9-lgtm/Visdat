import pandas as pd
from sqlalchemy import create_engine

# 1. Ekstrak: Baca file Excel
file_path = 'jumlah_balita_berdasarkan_status_gizi_dengan_indikato.xlsx'
df = pd.read_excel(file_path)

# 2. Transformasi: Pisahkan menjadi dua tabel menggunakan nama kolom asli
# Tabel Master (Untuk Supabase) - Menjadikan Kecamatan sebagai master
df_master = df[['bps_kode_kecamatan', 'bps_nama_kecamatan']].drop_duplicates()

# Tabel Metrik (Untuk SQLite)
df_metrik = df[['bps_kode_kecamatan', 'upt_puskesmas', 'keterangan', 'jumlah_balita', 'satuan', 'tahun']]
print("Data berhasil dipisahkan. Memulai proses unggah ke database...")

# 3. Load 1: Masukkan data Metrik ke SQLite (Lokal)
sqlite_engine = create_engine('sqlite:///database_sqlite.db')
df_metrik.to_sql('metrik_gizi', sqlite_engine, if_exists='replace', index=False)
print("Berhasil menyimpan tabel 'metrik_gizi' ke SQLite!")

# 4. Load 2: Masukkan data Master ke Supabase (PostgreSQL Cloud)
# PENTING: Ganti tulisan di bawah dengan URL koneksi Supabase Anda. 
# Ingat: Ubah karakter '#' pada password (DR#dpe...) menjadi '%23' pada URL.
SUPABASE_URL = "postgresql+psycopg2://postgres.uxmxmyuvinwvyngxsnyt:O35Q9N0ppVO4D1qK@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres?sslmode=require"
supabase_engine = create_engine(SUPABASE_URL)
df_master.to_sql('master_wilayah', supabase_engine, if_exists='replace', index=False)
print("Berhasil menyimpan tabel 'master_wilayah' ke Supabase!")
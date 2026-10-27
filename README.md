# Dashboard Interaktif Status Gizi Balita (Multi-DBMS Data Pipeline)

## Deskripsi Proyek
Proyek ini merupakan implementasi perancangan arsitektur data (*data pipeline*) dan visualisasi informasi interaktif berbasis web. Dibangun menggunakan ekosistem Python, aplikasi ini mengintegrasikan data dari dua Sistem Manajemen Basis Data (DBMS) yang berbeda untuk menyajikan analisis status gizi balita di tingkat kecamatan dan puskesmas secara dinamis.

## Ringkasan Arsitektur (Multi-DBMS)
Proyek ini memisahkan antara data dimensi (master) dan data fakta (metrik) untuk mensimulasikan praktik manajemen basis data yang terstruktur:
1. **DBMS 1: Supabase (PostgreSQL Cloud)** 
   * **Fungsi:** Menyimpan entitas data master wilayah.
   * **Struktur:** Tabel `master_wilayah` yang berisi `bps_kode_kecamatan` (Primary Key) dan `bps_nama_kecamatan`.
   * **Engine:** PostgreSQL yang diakses melalui koneksi jaringan *Connection Pooler* IPv4.
2. **DBMS 2: SQLite (Local Embedded Database)**
   * **Fungsi:** Menyimpan log fakta analitik dan metrik operasional kesehatan.
   * **Struktur:** Tabel `metrik_gizi` yang mencatat detail `upt_puskesmas`, `keterangan` (status gizi), `jumlah_balita`, dan `tahun`. Terhubung ke data master melalui *foreign key* `bps_kode_kecamatan`.

## Alur Integrasi (Data Pipeline)
Integrasi data (*data federation*) dilakukan di tingkat aplikasi (*application level*). 
1. Skrip `siapkan_data.py` mengekstrak data dari *dataset* mentah (Excel), mentransformasikannya, lalu memuatnya (*Load*) ke Supabase dan SQLite secara terpisah.
2. Saat aplikasi web (`app.py`) dimuat, pustaka **SQLAlchemy** menarik tabel dari kedua DBMS tersebut. 
3. **Pandas** bertugas melakukan penggabungan data (`pd.merge`) menggunakan skema *Left Join* pada kunci `bps_kode_kecamatan`. Hasil dari *data pipeline* ini adalah sebuah *dataframe* tunggal yang komprehensif untuk dianalisis.

## Fitur Interaktivitas Visualisasi
Antarmuka dibangun menggunakan framework **Streamlit** dan pustaka **Plotly Express**, meliputi:
* **Slicer / Filter Dinamis:** Pengguna dapat memfilter dataset secara spesifik berdasarkan Tahun, Status Gizi, Kecamatan, dan UPT Puskesmas.
* **Tabel Rincian Responsif:** Menampilkan data tabular yang langsung menyesuaikan dengan parameter filter yang dipilih (kolom *keterangan* diurutkan di bagian paling kanan).
* **Grafik Batang (Bar Chart):** Memvisualisasikan komparasi total balita berdasarkan kategori status gizi untuk melihat sebaran masalah gizi secara horizontal.
* **Grafik Garis (Line Chart):** Menampilkan tren pergerakan jumlah balita yang diukur dari tahun ke tahun.

## Sumber Data & Referensi
* **Sumber Data Asli:** https://opendata.bandung.go.id/dataset/jumlah-balita-berdasarkan-status-gizi-dengan-indikator-tinggi-badan-menurut-umur-tbu-di-puskesmas-kota-bandung
* **Live App (Streamlit):** https://visdat-va23sxseg9fcuuha8u4jxl.streamlit.app/

## Cara Menjalankan Proyek Secara Lokal
1. Instalasi dependensi: `pip install -r requirements.txt`
2. Eksekusi skrip inisialisasi basis data: `python siapkan_data.py`
3. Jalankan server Streamlit: `streamlit run app.py`
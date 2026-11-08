# Dashboard Interaktif Status Gizi Balita (Multi-DBMS Data Pipeline)

**Oleh:** Syakir Fadhillah (NIM: [Isi NIM Anda di sini])  
**Mata Kuliah:** Visualisasi Data dan Informasi (Informatika)

---

## 1. Deskripsi Proyek & Skenario Studi Kasus
Proyek ini merupakan implementasi perancangan arsitektur data (*data pipeline*) dan visualisasi informasi interaktif berbasis web menggunakan ekosistem Python. 

**Skenario Pemisahan Arsitektur:**
Pemilihan arsitektur Multi-DBMS pada kasus pemantauan gizi balita ini didasarkan pada karakteristik data:
* **Data Master Wilayah (Supabase/PostgreSQL):** Data hierarki geografis (Kecamatan) bersifat statis dan digunakan secara lintas sektoral oleh berbagai dinas. Oleh karena itu, data ini disimpan di *cloud* relasional agar menjadi *Single Source of Truth* yang terpusat.
* **Data Metrik Kesehatan (SQLite):** Data jumlah balita, status gizi, dan puskesmas merupakan log operasional tahunan yang terus bertambah secara dinamis. Data ini disimulasikan tersimpan dalam *local embedded database* yang lebih cepat diakses untuk kebutuhan analitik dasbor lokal.

## 2. Ringkasan Arsitektur (Multi-DBMS)
Proyek ini memisahkan antara data dimensi (master) dan data fakta (metrik):
* **DBMS 1: Supabase (PostgreSQL Cloud)** 
  * **Fungsi:** Menyimpan entitas data master wilayah.
  * **Struktur:** Tabel `master_wilayah` yang berisi `bps_kode_kecamatan` (Primary Key) dan `bps_nama_kecamatan`.
* **DBMS 2: SQLite (Local Embedded Database)**
  * **Fungsi:** Menyimpan log fakta analitik dan metrik operasional kesehatan.
  * **Struktur:** Tabel `metrik_gizi` yang mencatat detail `upt_puskesmas`, `keterangan` (status gizi), `jumlah_balita`, dan `tahun`. Terhubung ke data master melalui kunci `bps_kode_kecamatan`.

## 3. Alur Integrasi (Data Pipeline)
Integrasi data (*data federation*) dilakukan di tingkat aplikasi (*application level*). 
1. **Ekstraksi & Inisialisasi:** Skrip *seed* `siapkan_data.py` mengekstrak data dari *dataset* mentah (Excel), mentransformasikannya, lalu memuatnya (*Load*) ke Supabase dan SQLite secara terpisah.
2. **Koneksi:** Saat aplikasi web (`app.py`) dimuat, pustaka **SQLAlchemy** menarik tabel dari kedua DBMS tersebut.
3. **Penggabungan:** Pustaka **Pandas** melakukan penggabungan data (`pd.merge`) menggunakan skema *Left Join* pada atribut `bps_kode_kecamatan`, menghasilkan *dataframe* tunggal untuk dianalisis.

## 4. Fitur Interaktivitas Visualisasi
Antarmuka dibangun menggunakan framework **Streamlit** dan pustaka **Plotly Express**, meliputi:
* **Filter Dinamis (Slicer):** Sidebar interaktif dengan *dropdown* untuk menyaring data berdasarkan Tahun, Status Gizi, Kecamatan, dan UPT Puskesmas.
* **Ringkasan Eksekutif (KPI):** Deretan kartu metrik dinamis di bagian atas dasbor yang menghitung Total Balita, Jumlah Puskesmas Terlibat, dan Rata-rata sesuai filter yang dipilih.
* **Tabel Rincian Responsif:** Menampilkan data tabular hasil penyaringan (kolom *keterangan* diurutkan di bagian paling kanan).
* **Grafik Interaktif:** 
  * *Bar Chart*: Memvisualisasikan komparasi total balita berdasarkan kategori status gizi.
  * *Line Chart*: Menampilkan tren pergerakan jumlah balita dari tahun ke tahun.

## 5. Daftar Tautan & Referensi Utama
* **URL Live Web Application:** https://visdat-va23sxseg9fcuuha8u4jxl.streamlit.app/
* **URL Sumber Data Asli:** [Open Data Kota Bandung - Jumlah Balita Berdasarkan Status Gizi](https://opendata.bandung.go.id/dataset/jumlah-balita-berdasarkan-status-gizi-dengan-indikator-tinggi-badan-menurut-umur-tbu-di-puskesmas-kota-bandung)
* **URL Referensi Kode/Proyek:** [dataprofessor/dashboard-kit](https://github.com/dataprofessor/dashboard-kit) (Dijadikan rujukan untuk pembuatan metrik *Ringkasan Eksekutif* / KPI *Cards*).

## 6. Cara Menjalankan Proyek Secara Lokal
1. Instalasi dependensi: 
   ```bash
   pip install -r requirements.txt
   python siapkan_data.py
   streamlit run app.py

# Analisis Spasial Zona Risiko Banjir

Repositori ini berisi dasbor web interaktif untuk memvisualisasikan dan menganalisis zona risiko banjir. Proyek ini menggunakan data penginderaan jauh dan pemodelan hidrologi untuk mengidentifikasi area yang rentan terhadap banjir.

## Fitur

-   Peta interaktif dengan beberapa lapisan data (Zona Risiko Banjir, DEM, Curah Hujan, Tutupan Lahan).
-   Visualisasi statistik distribusi tingkat risiko banjir.
-   Kemampuan untuk mengekspor tampilan peta saat ini sebagai gambar PNG.
-   Sidebar untuk mengontrol visibilitas lapisan dan mengubah skema warna.

## Sumber Data

-   **DEM (Digital Elevation Model):** SRTM (Shuttle Radar Topography Mission)
-   **Curah Hujan:** CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data) - Data tahun 2022
-   **Tutupan Lahan:** ESA WorldCover 2021

## Prasyarat

-   Python 3.x
-   Git

## Instalasi & Cara Menjalankan

1.  **Clone repositori ini:**
    ```bash
    git clone https://github.com/MuhammadArthur21/Flood-Risk.git
    cd Flood-Risk
    ```

2.  **Masuk ke direktori dashboard:**
    ```bash
    cd dashboard
    ```

3.  **Buat dan aktifkan virtual environment (opsional tapi disarankan):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate  # Windows
    ```

4.  **Install dependensi yang dibutuhkan:**
    Disarankan untuk membuat file `requirements.txt` yang berisi:
    ```
    streamlit
    leafmap
    rasterio
    numpy
    pandas
    altair
    folium
    selenium
    ```
    Kemudian install dengan perintah:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Jalankan aplikasi Streamlit:**
    ```bash
    streamlit run app.py
    ```

6.  Buka browser Anda dan arahkan ke alamat URL yang ditampilkan di terminal (biasanya `http://localhost:8501`).

## Struktur Proyek

-   `dashboard/app.py`: Kode utama untuk aplikasi Streamlit.
-   `dashboard/*.tif`: File data raster yang digunakan dalam analisis.
-   `Data/`: Berisi data-data asli yang digunakan dalam analisis.
-   `README.md`: File ini.

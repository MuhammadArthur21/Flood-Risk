# -*- coding: utf-8 -*-
import streamlit as st
import leafmap.foliumap as leafmap
import rasterio
import numpy as np
import pandas as pd
import altair as alt
import folium
import base64
import tempfile
import os
import time

# === Tambahan untuk export peta ===
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# === KONFIGURASI HALAMAN ===
st.set_page_config(page_title="Flood Risk Dashboard", layout="wide")

st.title("🌊 Spatial Analysis of Flood Risk Zones")
st.markdown("""
**A comprehensive study identifying areas vulnerable to flooding using remote sensing data and hydrological modeling.**  
_Data sources:_ SRTM (DEM), CHIRPS (Rainfall 2022), ESA WorldCover (2021).  
_Developed using QGIS & Python._
""")

# === SIDEBAR ===
st.sidebar.header("🧭 Map Controls")
st.sidebar.write("Aktifkan atau nonaktifkan layer di bawah:")

show_flood = st.sidebar.checkbox("Flood Risk Zones", True)
show_dem = st.sidebar.checkbox("DEM (Elevation)", False)
show_rain = st.sidebar.checkbox("Rainfall 2022", False)
show_land = st.sidebar.checkbox("Land Cover ESA 2021", False)

palette = st.sidebar.selectbox(
    "🎨 Pilih Skema Warna Flood Map:",
    ["YlOrRd", "terrain", "Blues", "viridis", "tab20"],
    index=0
)

# === BUAT PETA ===
m = leafmap.Map(center=[-7.8, 110.3], zoom=9)
m.add_basemap("CartoDB.Positron")

# === TAMBAHKAN LAYER SESUAI PILIHAN ===
try:
    if show_flood:
        m.add_raster("FloodRiskMap.tif", layer_name="Flood Risk Zones", colormap=palette)

    if show_dem:
        m.add_raster("DEM_30m.tif", layer_name="DEM (Elevation)", colormap="terrain")

    if show_rain:
        m.add_raster("Rainfall_2022.tif", layer_name="Rainfall (CHIRPS 2022)", colormap="Blues")

    if show_land:
        m.add_raster("LandCover_ESA2021.tif", layer_name="Land Cover (ESA 2021)", colormap="tab20")

except Exception as e:
    st.error(f"Error saat memuat raster: {e}")

# === LEGENDA CUSTOM HTML ===
legend_html = """
<div style="
    position: fixed;
    bottom: 40px;
    left: 40px;
    width: 180px;
    height: 120px;
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 8px;
    padding: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    z-index:9999;
    font-size: 14px;
">
<b>Flood Risk Classification</b><br>
<div style='margin-top:6px;'>
<span style="background-color:yellow;width:18px;height:18px;display:inline-block;margin-right:6px;border:1px solid #999;"></span>Low
</div>
<div>
<span style="background-color:orange;width:18px;height:18px;display:inline-block;margin-right:6px;border:1px solid #999;"></span>Medium
</div>
<div>
<span style="background-color:red;width:18px;height:18px;display:inline-block;margin-right:6px;border:1px solid #999;"></span>High
</div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# === TAMPILKAN PETA ===
m.to_streamlit(height=650)

# === STATISTIK RISIKO BANJIR ===
st.subheader("📊 Flood Risk Statistics")

try:
    with rasterio.open("FloodRiskMap.tif") as src:
        data = src.read(1)
        unique, counts = np.unique(data, return_counts=True)
        total = counts.sum()
        percent = (counts / total) * 100
        df_stats = pd.DataFrame({
            "Class": unique.astype(str),
            "Pixels": counts,
            "Percent": np.round(percent, 2)
        })

        st.write("Ringkasan Statistik Flood Risk Map")
        st.dataframe(df_stats, use_container_width=True)

        chart = alt.Chart(df_stats).mark_bar(
            size=40,
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x=alt.X('Class:N', title="Flood Risk Class"),
            y=alt.Y('Percent:Q', title='Percentage (%)'),
            color=alt.Color('Class:N', scale=alt.Scale(domain=['1', '2', '3'], range=['yellow', 'orange', 'red'])),
            tooltip=['Class', 'Pixels', 'Percent']
        ).properties(
            width=600,
            height=300,
            title="Distribution of Flood Risk Levels"
        )

        st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.warning(f"⚠️ Statistik tidak dapat dihitung: {e}")

# === FITUR DOWNLOAD HASIL PETA (PAKAI SELENIUM FIX) ===
st.subheader("🖼️ Export Map Snapshot")
st.markdown("Klik tombol di bawah untuk mengekspor tampilan peta (full render, termasuk legend).")

if st.button("Download Map as PNG"):
    try:
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp_html:
            m.save(temp_html.name)
            png_path = temp_html.name.replace(".html", ".png")

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1600,900")

            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f"file:///{temp_html.name}")
            time.sleep(3)  # tunggu JS selesai render peta
            driver.save_screenshot(png_path)
            driver.quit()

            with open(png_path, "rb") as file:
                b64 = base64.b64encode(file.read()).decode()
                href = f'<a href="data:file/png;base64,{b64}" download="FloodRiskMap.png">Klik di sini untuk mengunduh hasil peta (PNG)</a>'
                st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Gagal mengekspor peta: {e}")

st.success("✅ Dashboard interaktif siap digunakan! Gunakan sidebar untuk mengatur layer dan warna peta.")

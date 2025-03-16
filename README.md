# Dashboard Penyewaan Sepeda

## Fitur Dashboard

1. **Menampilkan Data Penyewaan Sepeda**
   - Menampilkan dataset harian dan per jam dalam bentuk tabel interaktif.
2. **Statistik Data**
   - Menampilkan statistik deskriptif dari dataset.
3. **Grafik Penyewaan Sepeda**
   - Grafik tren penyewaan sepeda per hari dan per minggu.
   - Grafik distribusi penyewaan sepeda berdasarkan jam.
   - Grafik penyewaan sepeda berdasarkan kondisi cuaca.
4. **Interaktivitas**
   - Pemilihan tanggal untuk melihat data penyewaan per jam.
   - Filter berdasarkan musim dan kondisi cuaca.

## Data yang Digunakan

Dataset yang digunakan dalam proyek ini adalah **day.csv** dan **hour.csv** yang berisi data penyewaan sepeda berdasarkan berbagai parameter.

## Setup Environment - Shell/Terminal

```sh
mkdir proyek_analisis_data
cd proyek_analisis_data
```

## Instalasi Dependensi


```sh
pip install -r requirements.txt
```

## Struktur Direktori

```
proyek_analisis_data/
│-- Dashboard/
    ├── all_data.csv
    ├── dashboard.py
│-- Data/
│   ├── day.csv
│   ├── hour.csv
│-- Venv
│-- proyek_analisis_data.ipynb
│-- README.md
│-- requirements.txt
│-- url.txt
```

## Menjalankan Dashboard

Untuk run dashboard:

```sh
python -m streamlit run Dashboard/dashboard.py
```
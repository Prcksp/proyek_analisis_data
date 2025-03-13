# Dashboard Penyewaan Sepeda

## Fitur Dashboard
1. **Menampilkan Data Penyewaan Sepeda**
   - Menampilkan dataset harian dan per jam dalam bentuk tabel interaktif.
2. **Statistik Data**
   - Menampilkan statistik deskriptif dari dataset.
3. **Grafik Penyewaan Sepeda**
   - Grafik tren penyewaan sepeda per hari.
   - Grafik tren penyewaan sepeda per jam berdasarkan tanggal yang dipilih.
4. **Interaktivitas**
   - Pemilihan tanggal untuk melihat data penyewaan per jam.

## Data yang Digunakan
Dataset yang digunakan dalam proyek ini adalah **day.csv** dan **hour.csv** yang berisi data penyewaan sepeda berdasarkan berbagai parameter.

## Setup Environment - Shell/Terminal
```sh
mkdir proyek_analisis_data
cd proyek_analisis_data
pip install jupyterlab
pip install streamlit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
streamlit==1.43.1
pandas
matplotlib==3.10.1
numpy==2.2.3
seaborn==0.13.2

```

## Run the code in localhost
```
python -m streamlit run c:/Users/Lenovo/Documents/Test_Python_Dicoding/proyek_analisis_data/Dashboard/dashboard.py
```
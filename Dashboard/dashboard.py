import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

day_df = pd.read_csv("Data/day.csv")
hour_df = pd.read_csv("Data/hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.title("Dashboard Analisis Penyewaan Sepeda")

st.sidebar.header("Filter Data")
st.sidebar.header("Filter Data")
start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal", [day_df['dteday'].min(), day_df['dteday'].max()], min_value=day_df['dteday'].min(), max_value=day_df['dteday'].max())
selected_hour = st.sidebar.slider("Pilih Jam", min_value=int(hour_df["hr"].min()), max_value=int(hour_df["hr"].max()), value=int(hour_df["hr"].min()))

day_filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
hour_filtered_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date)) & (hour_df['hr'] == selected_hour)]

st.subheader("Data Penyewaan Sepeda Harian")
st.dataframe(day_df.head())

st.subheader("Data Penyewaan Sepeda Per Jam")
st.dataframe(hour_df.head())

st.subheader("Statistik Data Harian")
st.write(day_df.describe())

st.subheader("Statistik Data Per Jam")
st.write(hour_df.describe())

st.subheader("Tren Penyewaan Sepeda Harian dalam Rentang Seminggu")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=day_df['dteday'], y=day_df['cnt'], marker='o', linestyle='-', color='b', ax=ax)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Tren Penyewaan Sepeda")
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Distribusi Penyewaan Sepeda Per Jam dalam Rentang Seminggu")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x=hour_df["hr"], y=hour_df["cnt"], palette="coolwarm", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Distribusi Penyewaan Sepeda Per Jam")
st.pyplot(fig)

st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda per Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=hour_df["hr"], y=hour_df["cnt"], hue=hour_df["weathersit"], palette="magma", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
st.pyplot(fig)
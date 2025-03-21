import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

day_df = pd.read_csv("Data/day.csv")
hour_df = pd.read_csv("Data/hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.title("Dashboard Analisis Penyewaan Sepeda")

st.sidebar.header("Filter Data")
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal", 
    [day_df['dteday'].min(), day_df['dteday'].max()], 
    min_value=day_df['dteday'].min(), 
    max_value=day_df['dteday'].max()
)
selected_hour = st.sidebar.slider(
    "Pilih Jam", 
    min_value=int(hour_df["hr"].min()), 
    max_value=int(hour_df["hr"].max()), 
    value=int(hour_df["hr"].min())
)

day_filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
hour_filtered_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date)) & (hour_df['hr'] == selected_hour)]

st.subheader("Data Penyewaan Sepeda Harian")
st.write("Menampilkan data penyewaan sepeda harian yang telah difilter berdasarkan tanggal yang dipilih.")
st.dataframe(day_filtered_df.head())

st.subheader("Data Penyewaan Sepeda Per Jam")
st.write("Menampilkan data penyewaan sepeda per jam yang telah difilter berdasarkan tanggal dan jam yang dipilih.")
st.dataframe(hour_filtered_df.head())

st.subheader("Statistik Data Harian")
st.write(day_filtered_df.describe())

st.subheader("Statistik Data Per Jam")
st.write(hour_filtered_df.describe())

st.subheader("Tren Penyewaan Sepeda Harian")

trend_option = st.radio("Pilih Jenis Tren", ["Harian", "Mingguan"], index=0)
trend_chart_type = st.selectbox("Pilih Tipe Visualisasi", ["Garis", "Area"])

if trend_option == "Mingguan":
    day_filtered_df["week"] = day_filtered_df["dteday"].dt.isocalendar().week
    trend_df = day_filtered_df.groupby("week")["cnt"].mean().reset_index()
    x_label = "Minggu ke-"
else:
    trend_df = day_filtered_df[["dteday", "cnt"]]
    x_label = "Tanggal"

fig, ax = plt.subplots(figsize=(12, 5))

if trend_chart_type == "Garis":
    sns.lineplot(x=trend_df.iloc[:, 0], y=trend_df["cnt"], marker='o', linestyle='-', color='b', ax=ax)
elif trend_chart_type == "Area":
    sns.lineplot(x=trend_df.iloc[:, 0], y=trend_df["cnt"], color='b', ax=ax, linewidth=2)
    ax.fill_between(trend_df.iloc[:, 0], trend_df["cnt"], alpha=0.3, color='b')

ax.set_xlabel(x_label)
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title(f"Tren Penyewaan Sepeda {trend_option}")

max_idx = trend_df["cnt"].idxmax()
ax.annotate(f'Max: {trend_df["cnt"].max():,.0f}', 
            xy=(trend_df.iloc[max_idx, 0], trend_df["cnt"].max()), 
            xytext=(trend_df.iloc[max_idx, 0], trend_df["cnt"].max() + 500),
            arrowprops=dict(facecolor='red', arrowstyle='->'), 
            fontsize=10, color='red')

plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")

season_mapping = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_mapping = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan"
}

day_filtered_df["season_name"] = day_filtered_df["season"].map(season_mapping)
day_filtered_df["weather_desc"] = day_filtered_df["weathersit"].map(weather_mapping)

col1, col2 = st.columns(2)

with col1:
    selected_season = st.selectbox(
        "Pilih Musim:",
        options=["Semua"] + list(season_mapping.values()),  
        index=0  
    )

with col2:
    selected_weather = st.multiselect(
        "Pilih Kondisi Cuaca:",
        options=["Semua"] + list(weather_mapping.values()),  
        default=["Semua"]
    )

filtered_df = day_filtered_df.copy()

if selected_season != "Semua":
    filtered_df = filtered_df[filtered_df["season_name"] == selected_season]

if "Semua" not in selected_weather:
    filtered_df = filtered_df[filtered_df["weather_desc"].isin(selected_weather)]

filtered_df["weekday"] = filtered_df["dteday"].dt.dayofweek
weekday_avg = filtered_df.groupby("weekday")["cnt"].mean()
weekday_avg = weekday_avg.reindex([6, 0, 1, 2, 3, 4, 5])  # Menyesuaikan urutan hari Minggu-Sabtu

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"], y=weekday_avg.values, color="grey", ax=ax)
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
ax.grid(axis='y', linestyle='--', alpha=0.6)
st.pyplot(fig)

st.subheader("Distribusi Penyewaan Sepeda Per Jam")

distribution_type = st.radio("Pilih Jenis Distribusi:", ["Histogram", "KDE", "Boxplot"], index=0)

fig, ax = plt.subplots(figsize=(10, 5))

if distribution_type == "Histogram":
    sns.histplot(hour_df["cnt"], bins=20, kde=True, color="blue", ax=ax)
    ax.set_title("Histogram Penyewaan Sepeda Per Jam")
    ax.set_xlabel("Jumlah Penyewaan")
    ax.set_ylabel("Frekuensi")

elif distribution_type == "KDE":
    sns.kdeplot(hour_df["cnt"], fill=True, color="green", ax=ax)
    ax.set_title("KDE Penyewaan Sepeda Per Jam")
    ax.set_xlabel("Jumlah Penyewaan")
    ax.set_ylabel("Density")

elif distribution_type == "Boxplot":
    sns.boxplot(x=hour_df["hr"], y=hour_df["cnt"], palette="coolwarm", ax=ax)
    ax.set_title("Boxplot Penyewaan Sepeda Per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig)

weather_mapping = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan"
}

hour_df["weather_desc"] = hour_df["weathersit"].map(weather_mapping)

weather_filter = st.selectbox(
    "Pilih Kategori Cuaca",
    options=list(weather_mapping.values()),  
    index=0
)

weather_chart_type = st.radio(
    "Pilih Jenis Visualisasi", 
    ["Barplot", "Boxplot"], 
    index=0
)

filtered_weather_df = hour_df[hour_df["weather_desc"] == weather_filter]

fig, ax = plt.subplots(figsize=(12, 5))

color_mapping = {
    "Cerah": "#1f77b4", 
    "Berawan": "#ff7f0e", 
    "Hujan": "#d62728"  
}

palette_mapping = {
    "Cerah": "Blues",
    "Berawan": "Oranges",
    "Hujan": "Reds"
}

if weather_chart_type == "Barplot":
    hour_avg = filtered_weather_df.groupby('hr')['cnt'].mean()
    sns.barplot(
        x=hour_avg.index, 
        y=hour_avg.values, 
        color=color_mapping.get(weather_filter, "grey"), 
        ax=ax
    )
    ax.set_title(f"Rata-rata Penyewaan Sepeda per Jam pada Cuaca {weather_filter}")

elif weather_chart_type == "Boxplot":
    sns.boxplot(
        x=filtered_weather_df["hr"], 
        y=filtered_weather_df["cnt"], 
        palette=palette_mapping.get(weather_filter, "coolwarm"), 
        ax=ax
    )
    ax.set_title(f"Distribusi Penyewaan Sepeda pada Cuaca {weather_filter}")

ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_xticks(range(24))  
ax.set_xticklabels(range(24))  

st.pyplot(fig)


st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Hari dan Faktor Cuaca")

fig, ax = plt.subplots(figsize=(12, 5))

hour_avg = hour_df.groupby(['weekday', 'weathersit'])['cnt'].mean().reset_index()

barplot = sns.barplot(x='weekday', y='cnt', hue='weathersit', data=hour_avg, palette='coolwarm', ax=ax)

ax.set_xlabel("Hari dalam seminggu (0=Senin, 6=Minggu)")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Hari dan Faktor Cuaca")
ax.grid(axis='y', linestyle='--', alpha=0.6)

handles, labels = barplot.get_legend_handles_labels()
ax.legend(handles=handles, title="Kondisi Cuaca", labels=["Cerah", "Mendung", "Hujan", "Ekstrem"])

st.pyplot(fig)

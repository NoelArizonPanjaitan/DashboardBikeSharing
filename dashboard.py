import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# PAGE CONFIG
st.set_page_config(page_title="Bike Sharing Dashboard", layout="centered")

st.title("🚲 Bike Sharing Dashboard")
st.write("Dashboard interaktif analisis penyewaan sepeda")

# LOAD DATA
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Mapping
season_map = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

weather_map = {
    1: 'Clear',
    2: 'Mist + Cloudy',
    3: 'Light Rain/Snow',
    4: 'Heavy Rain/Snow'
}

day_df['season_name'] = day_df['season'].map(season_map)
hour_df['weather_name'] = hour_df['weathersit'].map(weather_map)

# SIDEBAR FILTER
st.sidebar.header("🔍 Filter Data")

# Filter tanggal
start_date = st.sidebar.date_input(
    "Tanggal Mulai",
    day_df['dteday'].min()
)

end_date = st.sidebar.date_input(
    "Tanggal Akhir",
    day_df['dteday'].max()
)

# Filter musim
selected_season = st.sidebar.selectbox(
    "Pilih Musim",
    ["All"] + list(day_df['season_name'].unique())
)

# Filter cuaca
selected_weather = st.sidebar.selectbox(
    "Pilih Cuaca",
    ["All"] + list(hour_df['weather_name'].unique())
)

# APPLY FILTER
filtered_day = day_df[
    (day_df['dteday'] >= pd.to_datetime(start_date)) &
    (day_df['dteday'] <= pd.to_datetime(end_date))
]

filtered_hour = hour_df[
    (hour_df['dteday'] >= pd.to_datetime(start_date)) &
    (hour_df['dteday'] <= pd.to_datetime(end_date))
]

if selected_season != "All":
    filtered_day = filtered_day[
        filtered_day['season_name'] == selected_season
    ]

if selected_weather != "All":
    filtered_hour = filtered_hour[
        filtered_hour['weather_name'] == selected_weather
    ]

# VISUALIZATION 1 - JAM
st.subheader("🕒 Rata-rata Penyewaan per Jam")

hourly_rent = filtered_hour.groupby('hr')['cnt'].mean()

fig, ax = plt.subplots(figsize=(6,3))
hourly_rent.plot(kind='line', marker='o', ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah")
ax.set_title("Pola Penyewaan per Jam")
ax.grid(True)

st.pyplot(fig)

# VISUALIZATION 2 - CUACA
st.subheader("🌦️ Rata-rata Berdasarkan Cuaca")

weather_avg = filtered_hour.groupby('weather_name')['cnt'].mean()

fig, ax = plt.subplots(figsize=(6,3))
weather_avg.plot(kind='bar', ax=ax)
ax.set_xlabel("Cuaca")
ax.set_ylabel("Jumlah")
ax.set_title("Penyewaan Berdasarkan Cuaca")

st.pyplot(fig)

# VISUALIZATION 3 - MUSIM
st.subheader("🍂 Rata-rata Berdasarkan Musim")

season_avg = filtered_day.groupby('season_name')['cnt'].mean()

fig, ax = plt.subplots(figsize=(6,3))
season_avg.plot(kind='bar', ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah")
ax.set_title("Penyewaan Berdasarkan Musim")

st.pyplot(fig)
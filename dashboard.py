import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bike Sharing Dashboard", layout="centered")

st.title("Bike Sharing Dashboard")
st.write("Dashboard analisis data penyewaan sepeda")

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# mapping season
season_map = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

# mapping weather
weather_map = {
    1: 'Clear',
    2: 'Mist + Cloudy',
    3: 'Light Rain/Snow',
    4: 'Heavy Rain/Snow'
}

day_df['season_name'] = day_df['season'].map(season_map)
hour_df['weather_name'] = hour_df['weathersit'].map(weather_map)

# =====================================
# KPI
# =====================================
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Penyewaan", f"{hour_df['cnt'].sum():,}")

with col2:
    st.metric("Rata-rata per Jam", f"{hour_df['cnt'].mean():.2f}")

with col3:
    peak_hour = hour_df.groupby('hr')['cnt'].mean().idxmax()
    st.metric("Peak Hour", f"{peak_hour}:00")

# =====================================
# CHART 1 - PER JAM
# =====================================
st.subheader("Rata-rata Penyewaan per Jam")

hourly_rent = hour_df.groupby('hr')['cnt'].mean()

fig, ax = plt.subplots(figsize=(5,3))
hourly_rent.plot(kind='line', marker='o', ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Pola Penyewaan per Jam")
ax.grid(True)

st.pyplot(fig)

# =====================================
# CHART 2 - CUACA
# =====================================
st.subheader("Rata-rata Berdasarkan Cuaca")

weather_avg = hour_df.groupby('weather_name')['cnt'].mean()

fig, ax = plt.subplots(figsize=(5,3))
weather_avg.plot(kind='bar', ax=ax)
ax.set_xlabel("Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Penyewaan Berdasarkan Cuaca")
ax.set_xticklabels(weather_avg.index, rotation=45)

st.pyplot(fig)

# =====================================
# CHART 3 - MUSIM
# =====================================
st.subheader("Rata-rata Berdasarkan Musim")

season_avg = day_df.groupby('season_name')['cnt'].mean()

fig, ax = plt.subplots(figsize=(5,3))
season_avg.plot(kind='bar', ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Penyewaan Berdasarkan Musim")

st.pyplot(fig)

# =====================================
# CHART 4 - CORRELATION
# =====================================
st.subheader("Correlation Heatmap")

corr = hour_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()

fig, ax = plt.subplots(figsize=(5,3))
cax = ax.imshow(corr, interpolation='nearest')
fig.colorbar(cax)

ax.set_xticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45)

ax.set_yticks(range(len(corr.columns)))
ax.set_yticklabels(corr.columns)

ax.set_title("Correlation Matrix")

st.pyplot(fig)

# =====================================
# CONCLUSION
# =====================================
st.subheader("Insight Utama")
st.write("""
- Peak demand terjadi pada jam 08.00 dan 17.00–18.00
- Cuaca cerah menghasilkan penyewaan tertinggi
- Musim Fall memiliki rata-rata demand tertinggi
- Suhu merupakan faktor yang paling memengaruhi penyewaan
""")

import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FIREMAP-X",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 FIREMAP-X")
st.subheader(
    "NASA Space Apps Challenge 2026 — "
    "Harmonization of MODIS and VIIRS Hot Spots"
)

DATA_FILE = "FIREMAP_X_DASHBOARD_DATA.csv"

if not os.path.exists(DATA_FILE):
    st.error(
        "Dashboard dataset not found: "
        f"{DATA_FILE}"
    )
    st.stop()

df = pd.read_csv(DATA_FILE)

df["acq_datetime"] = pd.to_datetime(
    df["acq_datetime"],
    errors="coerce"
)

df["calendar_date"] = pd.to_datetime(
    df["calendar_date"],
    errors="coerce"
).dt.date

st.success(
    f"NASA fire observation records loaded: {len(df)}"
)

st.write(
    "The dashboard presents harmonized MODIS and VIIRS "
    "active-fire observations returned by NASA FIRMS."
)



st.write("### 🗺️ MODIS & VIIRS Fire Observations")

map_data = df.copy()

map_data["acquisition_time"] = (
    map_data["acq_datetime"]
    .dt.strftime("%Y-%m-%d %H:%M")
)

st.write("### 🗺️ Historical MODIS & VIIRS Fire Observations")

fig_map = px.scatter_map(
    map_data,
    lat="latitude",
    lon="longitude",
    color="sensor",
    size="frp",
    hover_name="sensor",
    hover_data={
        "latitude": ":.5f",
        "longitude": ":.5f",
        "frp": ":.2f",
        "acquisition_time": True,
        "satellite": True,
        "daynight": True,
        "sensor": False
    },
    zoom=5,
    height=650,
    title="FIREMAP-X — MODIS & VIIRS Fire Observations"
)

fig_map.update_layout(
    map_style="open-street-map",
    margin={"r": 0, "t": 60, "l": 0, "b": 0}
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)


st.write("### 📊 Daily Burning Activity")

daily_activity = (
    df.groupby("calendar_date")
    .size()
    .reset_index(name="observations")
    .sort_values("calendar_date")
)

fig_daily = px.bar(
    daily_activity,
    x="calendar_date",
    y="observations",
    title="FIREMAP-X — Daily Burning Activity",
    labels={
        "calendar_date": "Date",
        "observations": "Fire Observations"
    },
    text="observations"
)

fig_daily.update_traces(
    textposition="outside"
)

fig_daily.update_layout(
    height=500,
    margin={
        "r": 40,
        "t": 70,
        "l": 60,
        "b": 60
    }
)

st.plotly_chart(
    fig_daily,
    use_container_width=True
)


st.write("### 📡 Sensor Observation Summary")

sensor_summary = (
    df.groupby("sensor")
    .size()
    .reset_index(name="observations")
    .sort_values("sensor")
)

fig_sensor = px.bar(
    sensor_summary,
    x="sensor",
    y="observations",
    title="FIREMAP-X — MODIS vs VIIRS Observations",
    labels={
        "sensor": "Sensor",
        "observations": "Fire Observations"
    },
    text="observations"
)

fig_sensor.update_traces(
    textposition="outside"
)

fig_sensor.update_layout(
    height=500,
    margin={
        "r": 40,
        "t": 70,
        "l": 60,
        "b": 60
    }
)

st.plotly_chart(
    fig_sensor,
    use_container_width=True
)

st.write("### 🔥 Burning Activity Calendar")

calendar_data = (
    df.groupby(["calendar_date", "sensor"])
    .size()
    .reset_index(name="observations")
)

calendar_table = (
    calendar_data
    .pivot(
        index="calendar_date",
        columns="sensor",
        values="observations"
    )
    .fillna(0)
    .reset_index()
)

for sensor in ["MODIS", "VIIRS"]:
    if sensor not in calendar_table.columns:
        calendar_table[sensor] = 0

calendar_table["Total Observations"] = (
    calendar_table["MODIS"]
    + calendar_table["VIIRS"]
)

calendar_table = calendar_table[
    [
        "calendar_date",
        "MODIS",
        "VIIRS",
        "Total Observations"
    ]
]

calendar_table = calendar_table.sort_values(
    "calendar_date"
)

st.dataframe(
    calendar_table,
    use_container_width=True,
    hide_index=True
)

st.write("### Dataset Preview")

st.dataframe(
    df,
    use_container_width=True
)

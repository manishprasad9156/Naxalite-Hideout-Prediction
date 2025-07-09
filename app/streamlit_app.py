import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import joblib

# Load model and data
model = joblib.load("../Models/rf_model.pkl")
df = pd.read_csv("../Data/naxal_hideouts_features.csv")

# Configure page
st.set_page_config(page_title="Naxalite Hideout Predictor", layout="wide")
st.title("🛡️ Naxalite Hideout Prediction Tool")

# Section: Known Hideouts Map
st.subheader("📍 Known Hideouts Map")
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=9)
for _, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['git name'],
        icon=folium.Icon(color='red', icon='crosshairs', prefix='fa')
    ).add_to(m)
# Display map using st_folium
st_folium(m, width=700, height=450)

# Section: Predict New Hideout Location
st.subheader("🧠 Predict New Hideout Location")
lat = st.number_input("Latitude", value=float(df['latitude'].mean()))
lon = st.number_input("Longitude", value=float(df['longitude'].mean()))
elev = st.number_input("Elevation (m)", value=300.0)
dist = st.number_input("Distance to Nearest Village (km)", value=5.0)

if st.button("Predict"):
    input_df = pd.DataFrame([[lat, lon, elev, dist]], 
                            columns=['latitude', 'longitude', 'elevation', 'distance_to_village'])
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]
    if prediction == 1:
        st.error(f"🚨 High Risk: Likely hideout detected! Confidence: {prob:.2f}")
    else:
        st.success(f"✅ Safe Zone. Confidence: {1 - prob:.2f}")

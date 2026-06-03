import json
import streamlit as st

with open("tn_min.geojson") as f:
    geojson_data = json.load(f)

# Grab the properties of the very first shape in the file
try:
    first_feature_props = geojson_data["features"][0]["properties"]
    st.write("🔑 Here are the property keys in your GeoJSON:", first_feature_props)
except Exception as e:
    st.write("Error reading GeoJSON properties:", e)
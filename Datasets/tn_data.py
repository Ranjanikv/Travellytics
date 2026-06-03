import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import numpy as np
import json

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Travellytics", layout="wide") 

# 🚨 CSS HACK TO DELETE THE BLANK TOP SPACE 🚨
st.markdown("""
    <style>
        /* This removes the massive white gap at the top of the page */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            margin-top: 0rem !important;
        }
        /* Optional: This hides the main Streamlit running header entirely */
        [data-testid="stHeader"] {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# 🎯 CENTERED MAIN TITLE ONLY
# -----------------------------------------------------------
st.markdown("<h1 style='text-align: center;'>Tamil Nadu Crowd Heatmap</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True) # Adds a small gap before the controls

# -------------------------------
# DB CONNECTION
# -------------------------------
engine = create_engine("mysql+mysqlconnector://root:Security*101@localhost:3306/tourism_db")

@st.cache_data
def get_latest_year():
    try:
        query = text("SELECT MAX(YEAR(month)) as latest_year FROM crowd_data")
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return int(df["latest_year"].iloc[0]) if not df["latest_year"].isna().iloc[0] else 2026
    except Exception as e:
        return 2026

latest_year = get_latest_year()

def load_filtered_data(year, selected_month_name, whole_year_mode):
    try:
        with engine.connect() as conn:
            if whole_year_mode:
                crowd_query = text("""
                    SELECT district_id, district_name, SUM(total) as total 
                    FROM crowd_data 
                    WHERE YEAR(month) = :year
                    GROUP BY district_id, district_name
                """)
                crowd_df = pd.read_sql(crowd_query, conn, params={"year": year})
            else:
                crowd_query = text("""
                    SELECT district_id, district_name, total 
                    FROM crowd_data 
                    WHERE YEAR(month) = :year AND MONTHNAME(month) = :month
                """)
                crowd_df = pd.read_sql(
                    crowd_query, 
                    conn, 
                    params={"year": year, "month": selected_month_name}
                )
            
            exp_query = text("""
                SELECT district_id, sum
                FROM expenditure
            """)
            exp_df = pd.read_sql(exp_query, conn)
                
        if crowd_df.empty:
            return pd.DataFrame()
        
        crowd_df["district_id"] = crowd_df["district_id"].astype(str).str.strip()
        exp_df["district_id"] = exp_df["district_id"].astype(str).str.strip()
        
        final_df = crowd_df.merge(exp_df, on="district_id", how="left")
        final_df["sum"] = final_df["sum"].fillna(0)
        
        return final_df
        
    except Exception as e:
        st.error(f"DB Error while loading matched data: {e}")
        return pd.DataFrame()

# -------------------------------
# LOAD GEOJSON
# -------------------------------
with open("tn_min.geojson") as f:
    geojson_data = json.load(f)

for f in geojson_data.get("features", []):
    district = f.get("properties", {}).get("dtname")
    if district:
        f["properties"]["dtname"] = district.strip().title()

# -----------------------------------------------------------
# 🛠️ UI LAYOUT & FILTERING (SUBHEADING MOVED HERE)
# -----------------------------------------------------------
st.markdown("### District-wise crowd population heatmap")

view_mode = st.radio(
    "Select Visualization Mode",
    ["View Entire Year", "View Month-wise"],
    horizontal=True
)

whole_year_mode = True if view_mode == "View Entire Year" else False
selected_month_name = None

if not whole_year_mode:
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    st.markdown("---") 
    selected_month_name = st.selectbox("Pick a Month to Inspect", month_order)

filtered_df = load_filtered_data(latest_year, selected_month_name, whole_year_mode)

if not filtered_df.empty:
    filtered_df.columns = filtered_df.columns.str.lower().str.strip()
    
    filtered_df["total"] = pd.to_numeric(filtered_df["total"], errors="coerce").fillna(0)
    filtered_df["sum"] = pd.to_numeric(filtered_df["sum"], errors="coerce").fillna(0)
    filtered_df["district_name"] = filtered_df["district_name"].str.strip().str.title()

    NAME_FIX = {
        "Kancheepuram":    "Kanchipuram",
        "Nilgiris":        "The Nilgiris",
        "Sivagangai":      "Sivaganga",
        "Thiruvannamalai": "Tiruvannamalai",
        "Thoothukudi":     "Tuticorin",
        "Tiruvarur":       "Thiruvarur",
        "Virudunagar":     "Virudhunagar",
    }
    filtered_df["district_name"] = filtered_df["district_name"].replace(NAME_FIX)
    
    filtered_df["log_total"] = np.log10(filtered_df["total"] + 1)
    
    filtered_df["raw_health"] = np.log10((filtered_df["total"] * filtered_df["sum"]) + 1)
    
    min_raw = filtered_df["raw_health"].min()
    max_raw = filtered_df["raw_health"].max()
    
    if max_raw != min_raw:
        filtered_df["health_score"] = ((filtered_df["raw_health"] - min_raw) / (max_raw - min_raw)) * 100
    else:
        filtered_df["health_score"] = 100 if max_raw > 0 else 0
    
else:
    st.warning("No data found for the selected combination.")
    st.stop()


# -----------------------------------------------
# 🧱 PART 1: 75% MAP | 25% TOP PERFORMERS
# -----------------------------------------------
col_heatmap, col_health = st.columns([0.75, 0.25], gap="large")

with col_heatmap:
    current_view_title = f"Full Year " if whole_year_mode else f"{selected_month_name} "

    fig = px.choropleth_mapbox(
        filtered_df,
        geojson=geojson_data,
        locations="district_name",           
        featureidkey="properties.dtname",   
        color="log_total",                   
        color_continuous_scale="YlOrRd",    
        mapbox_style="carto-positron",
        zoom=6.3, 
        center={"lat": 11.1271, "lon": 78.6569}, 
        opacity=0.6,
        title=f"Tamil Nadu Heatmap - {current_view_title}",
        hover_data={"log_total": False, "total": True, "district_name": True, "health_score": True}
    )

    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>Visitors: %{customdata[1]:,}<br>Health Score: %{customdata[3]:.1f}/100<extra></extra>"
    )
    
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=700)

    st.plotly_chart(fig, use_container_width=True)

with col_health:
    st.subheader("District Healthscore")
    st.markdown("Top performing districts scored from **0 to 100**.")

    leaderboard = filtered_df.sort_values(by="health_score", ascending=False).head(3)
    
    for i, (idx, row) in enumerate(leaderboard.iterrows()):
        # 🚨 EMOJIS REMOVED, NOW PRINTS "Rank 1: District" etc. 🚨
        st.metric(
            label=f"Rank {i+1}: {row['district_name']}",
            value=f"{round(row['health_score'], 1)} pts"
        )
        st.caption(f"{int(row['total']):,} visitors | ₹{int(row['sum']):,}")
        st.markdown("---")


# -----------------------------------------------
# 📊 PART 2: FULL DATA TABLE (BELOW BOTH)
# -----------------------------------------------
st.markdown("### Complete Health Score Breakdown")
st.markdown("The complete list of districts, sorted from highest to lowest Healthscore.")

display_df = filtered_df[["district_name", "total", "sum", "health_score"]].copy()
display_df = display_df.sort_values(by="health_score", ascending=False).reset_index(drop=True)
display_df.columns = ["District Name", "Total Visitors", "Total Expenditure (Sum)", "Final Health Score"]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=400 
)
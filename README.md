# Travellytics
A Data Science and Tourism Management project that analyzes tourist crowd patterns and expenditure trends across districts in Tamil Nadu.

Travellytics provides an interactive heatmap dashboard that helps identify high-traffic tourist regions, evaluate district performance, and support data-driven tourism planning.

---

## Project Overview

Tourism departments often collect large amounts of visitor and expenditure data, but extracting meaningful insights can be challenging.

This project combines:

- Tourist crowd statistics
- District-wise expenditure data
- Geographic district boundaries

to generate an interactive analytics dashboard that visualizes tourism activity across Tamil Nadu.

The system calculates a custom **Health Score** for each district based on:

- Number of visitors
- Tourist expenditure

and displays the results through an interactive heatmap and leaderboard.

---

## Objectives

- Analyze tourism crowd distribution across Tamil Nadu.
- Compare district performance using tourism metrics.
- Identify high-performing and low-performing districts.
- Provide an intuitive visual dashboard for tourism management.
- Support data-driven decision-making for tourism development.

---

## Technologies Used

### Programming Language

- Python

### Libraries

- Streamlit
- Pandas
- NumPy
- Plotly Express


### Database

- MySQL

### Data Visualization

- Choropleth Heatmaps
- Interactive Tables
- Leaderboards

### Geographic Data

- GeoJSON

## Features

### 1. Tamil Nadu Crowd Heatmap

Visualizes tourist density across districts using a color-coded map.

- Darker regions indicate higher tourist activity.
- Interactive hover information.
- District-wise visitor statistics.

---

### 2. Year-wise Analysis

View tourism performance aggregated for an entire year.

Provides:

- Total visitors
- Total expenditure
- District Health Score

---

### 3. Month-wise Analysis

Analyze tourism trends for individual months.

Useful for:

- Seasonal tourism analysis
- Peak travel period identification
- Monthly crowd monitoring

---

### 4. District Health Score

A custom metric designed to evaluate district tourism performance.

The score considers:

- Tourist Footfall
- Tourist Expenditure

Higher scores indicate stronger tourism performance.

---

### 5. Top Performing Districts

Displays the best-performing districts based on Health Score.

Includes:

- Rank
- Visitor Count
- Expenditure Value

---

### 6. Detailed Analytics Table

Provides a complete district-wise breakdown including:

- District Name
- Total Visitors
- Expenditure
- Health Score

---

## Database Design

### crowd_data

Stores tourism crowd information.

| Column | Description |
|----------|------------|
| district_id | District Identifier |
| district_name | District Name |
| month | Date |
| total | Visitor Count |

---

### expenditure

Stores tourism expenditure information.

| Column | Description |
|----------|------------|
| district_id | District Identifier |
| sum | Total Expenditure |

---

## Health Score Calculation

The dashboard calculates a tourism performance score using visitor and expenditure data.

### Step 1

Raw score:

```python
raw_health = log10((total_visitors * expenditure) + 1)
```

### Step 2

Normalize score between 0 and 100:

```python
health_score =
((raw_health - min_raw) /
(max_raw - min_raw)) * 100
```

This creates a standardized score that allows fair comparison between districts.

---

## 📈 Data Visualization

The project uses a Choropleth Mapbox visualization.

Key features:

- Interactive district highlighting
- Hover-based insights
- Geographic district boundaries
- Dynamic filtering

Color Scale:

- Yellow → Lower tourism activity
- Orange → Medium tourism activity
- Red → Higher tourism activity

## Future Enhancements

- Machine Learning-based tourist prediction
- Real-time tourism monitoring
- Weather integration
- Hotel occupancy analysis
- Tourist recommendation system
- AI-powered tourism insights
- Mobile responsive dashboard

---

## Acknowledgements

Developed for **TNWISE 2026**, a State-Level Hackathon focused on innovative technology solutions for Tamil Nadu.

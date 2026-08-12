import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Life Expectancy",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA FROM GITHUB
# --------------------------------------------------

url = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit/"
    "main/life-expectancy.csv"
)

df = pd.read_csv(url)

# Rename columns
df = df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy"
    }
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🌍 Life Expectancy Around the World")

st.write(
    "Use the year selector to explore life expectancy "
    "across countries around the world."
)

# --------------------------------------------------
# YEAR SELECTOR
# --------------------------------------------------

years = sorted(df["Year"].dropna().unique())

selected_year = st.select_slider(
    "Select Year",
    options=years,
    value=years[-1]
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

year_data = df[
    df["Year"] == selected_year
].copy()

# --------------------------------------------------
# WORLD MAP
# --------------------------------------------------

fig = px.choropleth(
    year_data,
    locations="Code",
    color="Life Expectancy",
    hover_name="Country",
    color_continuous_scale="YlGnBu",
    projection="natural earth",
    title=f"Life Expectancy by Country — {selected_year}",
    labels={
        "Life Expectancy": "Life Expectancy (years)"
    }
)

fig.update_layout(
    margin=dict(
        l=0,
        r=0,
        t=60,
        b=0
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# SELECTED YEAR INFORMATION
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Year",
        selected_year
    )

with col2:
    st.metric(
        "Average Life Expectancy",
        f"{year_data['Life Expectancy'].mean():.1f} years"
    )

with col3:
    st.metric(
        "Countries",
        year_data["Country"].nunique()
    )

# --------------------------------------------------
# DATA SOURCE
# --------------------------------------------------

st.divider()

st.subheader("📚 Data Source")

st.markdown(
    "[Life Expectancy Dataset on GitHub]"
    "(https://github.com/veronikayushchak-coder/"
    "dsc205-streamlit/blob/main/life-expectancy.csv)"
)

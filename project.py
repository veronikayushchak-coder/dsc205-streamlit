import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Life Expectancy Analysis",
    page_icon="🌍",
    layout="wide"
)


# =========================================================
# DATA URLS
# =========================================================

LIFE_URL = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit/"
    "main/life-expectancy.csv"
)

GDP_URL = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit/"
    "main/life-expectancy-vs-gdp-per-capita.csv"
)

HEALTH_URL = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit/"
    "main/life-expectancy-vs-health-expenditure.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    life_df = pd.read_csv(LIFE_URL)
    gdp_df = pd.read_csv(GDP_URL)
    health_df = pd.read_csv(HEALTH_URL)

    return life_df, gdp_df, health_df


df, gdp_df, health_df = load_data()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df = df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy"
    }
)

gdp_df = gdp_df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy"
    }
)

health_df = health_df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy",
        "Health expenditure per capita":
            "Health Expenditure"
    }
)


# =========================================================
# FIND GDP COLUMN
# =========================================================

gdp_column = None

for column in gdp_df.columns:

    if (
        "gdp" in column.lower()
        and "capita" in column.lower()
    ):

        gdp_column = column
        break


# =========================================================
# TITLE
# =========================================================

st.title("🌍 Life Expectancy Analysis")

st.write(
    """
    Explore life expectancy around the world,
    see how it has changed over time, and compare
    countries using different factors.
    """
)


# =========================================================
# SECTION 1 — WORLD MAP
# =========================================================

st.header("🌎 Life Expectancy by Country")

st.write(
    "Select a year to see life expectancy around the world."
)


map_years = sorted(
    df["Year"].dropna().unique()
)

map_year = st.select_slider(
    "Select Year",
    options=map_years,
    value=map_years[-1],
    key="map_year"
)


map_data = df[
    df["Year"] == map_year
].copy()


fig_map = px.choropleth(
    map_data,
    locations="Code",
    color="Life Expectancy",
    hover_name="Country",
    color_continuous_scale="YlGnBu",
    projection="natural earth",
    title=f"Life Expectancy — {map_year}",
    labels={
        "Life Expectancy":
            "Life Expectancy (years)"
    }
)

fig_map.update_layout(
    margin=dict(
        l=0,
        r=0,
        t=60,
        b=0
    )
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)


# =========================================================
# MAP SUMMARY
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Year",
        map_year
    )

with col2:

    average_life = map_data[
        "Life Expectancy"
    ].mean()

    st.metric(
        "Average Life Expectancy",
        f"{average_life:.1f} years"
    )

with col3:

    st.metric(
        "Countries",
        map_data["Country"].nunique()
    )


# =========================================================
# SECTION 2 — LIFE EXPECTANCY OVER TIME
# =========================================================

st.divider()

st.header("📈 Life Expectancy Over Time")

st.write(
    "Select a country to see how its life expectancy "
    "has changed over time."
)


all_countries = sorted(
    df["Country"].dropna().unique()
)

trend_country = st.selectbox(
    "Select Country",
    all_countries,
    key="trend_country"
)


country_trend = df[
    df["Country"] == trend_country
].sort_values("Year")


fig_trend = px.line(
    country_trend,
    x="Year",
    y="Life Expectancy",
    markers=True,
    title=f"Life Expectancy in {trend_country}",
    labels={
        "Year": "Year",
        "Life Expectancy":
            "Life Expectancy (years)"
    }
)

fig_trend.update_layout(
    margin=dict(
        l=0,
        r=0,
        t=60,
        b=0
    )
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# =========================================================
# SECTION 3 — COMPARE COUNTRIES
# =========================================================

st.divider()

st.header("📊 Compare Countries")

st.write(
    """
    Choose what you want to compare first.
    The available years and countries will then
    update based on your selection.
    """
)


# =========================================================
# COMPARISON CHOICE
# =========================================================

comparison_choice = st.radio(
    "What would you like to compare?",
    [
        "Life Expectancy",
        "Health Spending",
        "GDP per Capita"
    ],
    horizontal=True,
    key="comparison_choice"
)


# =========================================================
# SELECT DATASET
# =========================================================

if comparison_choice == "Life Expectancy":

    comparison_df = df.copy()

    value_column = "Life Expectancy"


elif comparison_choice == "Health Spending":

    comparison_df = health_df.copy()

    value_column = "Health Expenditure"


else:

    comparison_df = gdp_df.copy()

    value_column = gdp_column


# =========================================================
# CHECK DATA
# =========================================================

if value_column is None:

    st.error(
        "The selected data column could not be found."
    )

    st.stop()


# =========================================================
# AVAILABLE YEARS
# =========================================================

years_available = sorted(
    comparison_df[
        comparison_df[value_column].notna()
    ]["Year"]
    .dropna()
    .unique()
)


if len(years_available) == 0:

    st.warning(
        f"No years with {comparison_choice.lower()} "
        "data are available."
    )

    st.stop()


# =========================================================
# YEAR SELECTOR
# =========================================================

comparison_year = st.selectbox(
    "Select Year",
    years_available,
    index=len(years_available) - 1,
    key="comparison_year"
)


# =========================================================
# DATA FOR SELECTED YEAR
# =========================================================

available_data = comparison_df[
    comparison_df["Year"] == comparison_year
].copy()


# Remove rows where selected variable is empty
available_data = available_data.dropna(
    subset=[
        "Country",
        value_column
    ]
)


# =========================================================
# AVAILABLE COUNTRIES
# =========================================================

available_countries = sorted(
    available_data["Country"].unique()
)


if len(available_countries) < 3:

    st.warning(
        f"Fewer than 3 countries have "
        f"{comparison_choice.lower()} data "
        f"for {comparison_year}."
    )

    st.stop()


# =========================================================
# SELECT THREE COUNTRIES
# =========================================================

st.subheader("🌎 Select Three Countries")


country_col1, country_col2, country_col3 = st.columns(3)


# ---------------------------------------------------------
# COUNTRY 1
# ---------------------------------------------------------

with country_col1:

    country_1 = st.selectbox(
        "Country 1",
        available_countries,
        index=0,
        key="compare_country_1"
    )


# ---------------------------------------------------------
# COUNTRY 2
# ---------------------------------------------------------

with country_col2:

    country_2_options = [
        country
        for country in available_countries
        if country != country_1
    ]

    country_2 = st.selectbox(
        "Country 2",
        country_2_options,
        index=0,
        key="compare_country_2"
    )


# ---------------------------------------------------------
# COUNTRY 3
# ---------------------------------------------------------

with country_col3:

    country_3_options = [
        country
        for country in available_countries
        if country not in [
            country_1,
            country_2
        ]
    ]

    country_3 = st.selectbox(
        "Country 3",
        country_3_options,
        index=0,
        key="compare_country_3"
    )


# =========================================================
# SELECTED COUNTRIES
# =========================================================

selected_countries = [
    country_1,
    country_2,
    country_3
]


# =========================================================
# CREATE CHART DATA
# =========================================================

chart_data = available_data[
    available_data["Country"].isin(
        selected_countries
    )
][
    [
        "Country",
        value_column
    ]
].copy()


# =========================================================
# COMPARISON CHART
# =========================================================

st.subheader(
    f"{comparison_choice} Comparison"
)


fig_comparison = px.bar(
    chart_data,
    x="Country",
    y=value_column,
    title=(
        f"{comparison_choice} — "
        f"{comparison_year}"
    ),
    labels={
        value_column:
            comparison_choice
    },
    text=value_column
)

fig_comparison.update_traces(
    textposition="outside"
)

fig_comparison.update_layout(
    margin=dict(
        l=0,
        r=0,
        t=60,
        b=0
    )
)

st.plotly_chart(
    fig_comparison,
    use_container_width=True
)


# =========================================================
# DATA TABLE
# =========================================================

st.subheader("Selected Data")


display_data = chart_data.rename(
    columns={
        value_column:
            comparison_choice
    }
)


st.dataframe(
    display_data,
    hide_index=True,
    use_container_width=True
)


# =========================================================
# DATA SOURCES
# =========================================================

st.divider()

st.subheader("📚 Data Sources")

st.markdown(
    "[Life Expectancy Dataset]"
    "(https://github.com/veronikayushchak-coder/"
    "dsc205-streamlit/blob/main/"
    "life-expectancy.csv)"
)

st.markdown(
    "[Life Expectancy vs GDP per Capita Dataset]"
    "(https://github.com/veronikayushchak-coder/"
    "dsc205-streamlit/blob/main/"
    "life-expectancy-vs-gdp-per-capita.csv)"
)

st.markdown(
    "[Life Expectancy vs Health Expenditure Dataset]"
    "(https://github.com/veronikayushchak-coder/"
    "dsc205-streamlit/blob/main/"
    "life-expectancy-vs-health-expenditure.csv)"
)

st.caption(
    "Data source: Our World in Data (OWID)."
)

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

LIFE_URL = "https://raw.githubusercontent.com/veronikayushchak-coder/dsc205-streamlit/main/life-expectancy.csv"

GDP_URL = "https://raw.githubusercontent.com/veronikayushchak-coder/dsc205-streamlit/main/life-expectancy-vs-gdp-per-capita.csv"

HEALTH_URL = "https://raw.githubusercontent.com/veronikayushchak-coder/dsc205-streamlit/main/life-expectancy-vs-health-expenditure.csv"


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
        "Health expenditure per capita": "Health Expenditure"
    }
)


# =========================================================
# FIND GDP COLUMN
# =========================================================

gdp_column = None

for column in gdp_df.columns:

    if "gdp" in column.lower() and "capita" in column.lower():

        gdp_column = column
        break


# =========================================================
# FIND POPULATION COLUMN
# =========================================================

population_column = None

for column in df.columns:

    if "population" in column.lower():

        population_column = column
        break


# =========================================================
# TITLE
# =========================================================

st.title("🌍 Life Expectancy Analysis")

st.write(
    """
    Explore how life expectancy has changed over time
    and compare countries using different factors.
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
        "Life Expectancy": "Life Expectancy (years)"
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
        "Life Expectancy": "Life Expectancy (years)"
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
    Choose a year and a factor, then select three countries
    to compare.
    """
)


# =========================================================
# YEAR
# =========================================================

comparison_years = sorted(
    df["Year"].dropna().unique()
)

comparison_year = st.selectbox(
    "Select Year",
    comparison_years,
    index=len(comparison_years) - 1,
    key="compare_year"
)


# =========================================================
# RADIO BUTTON
# =========================================================

comparison_choice = st.radio(
    "What would you like to compare?",
    [
        "Life Expectancy",
        "Health Spending",
        "GDP per Capita",
        "Population"
    ],
    horizontal=True
)


# =========================================================
# FIND AVAILABLE COUNTRIES
# =========================================================

# ---------------------------------------------------------
# LIFE EXPECTANCY
# ---------------------------------------------------------

life_available = df[
    df["Year"] == comparison_year
].copy()

life_available = life_available.dropna(
    subset=[
        "Country",
        "Life Expectancy"
    ]
)

life_countries = set(
    life_available["Country"]
)


# ---------------------------------------------------------
# HEALTH SPENDING
# ---------------------------------------------------------

health_available = health_df[
    health_df["Year"] == comparison_year
].copy()

health_available = health_available.dropna(
    subset=[
        "Country",
        "Health Expenditure"
    ]
)

health_countries = set(
    health_available["Country"]
)


# ---------------------------------------------------------
# GDP
# ---------------------------------------------------------

if gdp_column is not None:

    gdp_available = gdp_df[
        gdp_df["Year"] == comparison_year
    ].copy()

    gdp_available = gdp_available.dropna(
        subset=[
            "Country",
            gdp_column
        ]
    )

    gdp_countries = set(
        gdp_available["Country"]
    )

else:

    gdp_countries = set()


# ---------------------------------------------------------
# POPULATION
# ---------------------------------------------------------

if population_column is not None:

    population_available = df[
        df["Year"] == comparison_year
    ].copy()

    population_available = population_available.dropna(
        subset=[
            "Country",
            population_column
        ]
    )

    population_countries = set(
        population_available["Country"]
    )

else:

    population_countries = set()


# =========================================================
# CHOOSE COUNTRIES BASED ON SELECTED VARIABLE
# =========================================================

if comparison_choice == "Life Expectancy":

    available_countries = sorted(
        life_countries
    )

elif comparison_choice == "Health Spending":

    available_countries = sorted(
        health_countries
    )

elif comparison_choice == "GDP per Capita":

    available_countries = sorted(
        gdp_countries
    )

else:

    available_countries = sorted(
        population_countries
    )


# =========================================================
# CHECK AVAILABLE COUNTRIES
# =========================================================

if len(available_countries) < 3:

    st.warning(
        f"There are fewer than 3 countries with "
        f"{comparison_choice.lower()} data available "
        f"for {comparison_year}."
    )

    st.stop()


# =========================================================
# SELECT THREE COUNTRIES
# =========================================================

st.subheader("🌎 Select Three Countries")


country_col1, country_col2, country_col3 = st.columns(3)


with country_col1:

    country_1 = st.selectbox(
        "Country 1",
        available_countries,
        index=0,
        key="comparison_country_1"
    )


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
        key="comparison_country_2"
    )


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
        key="comparison_country_3"
    )


selected_countries = [
    country_1,
    country_2,
    country_3
]


# =========================================================
# CREATE COMPARISON DATA
# =========================================================

comparison_data = []


for country in selected_countries:

    row = {
        "Country": country
    }


    # -----------------------------------------------------
    # LIFE EXPECTANCY
    # -----------------------------------------------------

    life_row = df[
        (df["Country"] == country)
        & (df["Year"] == comparison_year)
    ]

    if not life_row.empty:

        row["Life Expectancy"] = life_row[
            "Life Expectancy"
        ].iloc[0]


    # -----------------------------------------------------
    # HEALTH SPENDING
    # -----------------------------------------------------

    health_row = health_df[
        (health_df["Country"] == country)
        & (health_df["Year"] == comparison_year)
    ]

    if not health_row.empty:

        row["Health Spending"] = health_row[
            "Health Expenditure"
        ].iloc[0]


    # -----------------------------------------------------
    # GDP
    # -----------------------------------------------------

    if gdp_column is not None:

        gdp_row = gdp_df[
            (gdp_df["Country"] == country)
            & (gdp_df["Year"] == comparison_year)
        ]

        if not gdp_row.empty:

            row["GDP per Capita"] = gdp_row[
                gdp_column
            ].iloc[0]


    # -----------------------------------------------------
    # POPULATION
    # -----------------------------------------------------

    if population_column is not None:

        population_row = df[
            (df["Country"] == country)
            & (df["Year"] == comparison_year)
        ]

        if not population_row.empty:

            row["Population"] = population_row[
                population_column
            ].iloc[0]


    comparison_data.append(row)


comparison_df = pd.DataFrame(
    comparison_data
)


# =========================================================
# COMPARISON CHART
# =========================================================

if comparison_choice in comparison_df.columns:

    chart_data = comparison_df[
        [
            "Country",
            comparison_choice
        ]
    ].dropna()


    fig_comparison = px.bar(
        chart_data,
        x="Country",
        y=comparison_choice,
        title=(
            f"{comparison_choice} Comparison — "
            f"{comparison_year}"
        ),
        labels={
            comparison_choice: comparison_choice
        },
        text=comparison_choice
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


    # =====================================================
    # DATA TABLE
    # =====================================================

    st.subheader("Selected Data")

    st.dataframe(
        chart_data,
        hide_index=True,
        use_container_width=True
    )


# =========================================================
# DATA SOURCES
# =========================================================

st.divider()

st.subheader("📚 Data Sources")

st.markdown(
    "[Life Expectancy Dataset](https://github.com/veronikayushchak-coder/dsc205-streamlit/blob/main/life-expectancy.csv)"
)

st.markdown(
    "[Life Expectancy vs GDP per Capita Dataset](https://github.com/veronikayushchak-coder/dsc205-streamlit/blob/main/life-expectancy-vs-gdp-per-capita.csv)"
)

st.markdown(
    "[Life Expectancy vs Health Expenditure Dataset](https://github.com/veronikayushchak-coder/dsc205-streamlit/blob/main/life-expectancy-vs-health-expenditure.csv)"
)

st.caption(
    "Data source: Our World in Data (OWID)."
)

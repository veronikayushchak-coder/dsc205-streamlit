import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Life Expectancy",
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

possible_gdp_columns = [
    "GDP per capita",
    "GDP per Capita",
    "GDP per capita, PPP",
    "GDP per capita (int. $)"
]

gdp_column = None

for column in possible_gdp_columns:

    if column in gdp_df.columns:
        gdp_column = column
        break


# =========================================================
# FIND POPULATION COLUMN
# =========================================================

possible_population_columns = [
    "Population",
    "population",
    "Population (historical)",
    "Population - Sex: all - Age: all - Variant: estimates"
]

population_column = None

for column in possible_population_columns:

    if column in df.columns:
        population_column = column
        break


# =========================================================
# TITLE
# =========================================================

st.title("🌍 Life Expectancy Around the World")

st.write(
    """
    Explore how life expectancy has changed across countries
    and examine its relationship with GDP, health spending,
    and population.
    """
)


# =========================================================
# SECTION 1 — WORLD MAP
# =========================================================

st.header("🌎 Life Expectancy by Country")

st.write(
    "Select a year to see life expectancy around the world."
)


# ---------------------------------------------------------
# MAP YEAR SELECTOR
# ---------------------------------------------------------

map_years = sorted(
    df["Year"].dropna().unique()
)

map_year = st.select_slider(
    "Select Year",
    options=map_years,
    value=map_years[-1],
    key="map_year"
)


# ---------------------------------------------------------
# MAP DATA
# ---------------------------------------------------------

map_data = df[
    df["Year"] == map_year
].copy()


# ---------------------------------------------------------
# WORLD MAP
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# MAP METRICS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# COUNTRY SELECTOR
# ---------------------------------------------------------

all_countries = sorted(
    df["Country"].dropna().unique()
)

selected_country_trend = st.selectbox(
    "Select Country",
    all_countries,
    key="trend_country"
)


# ---------------------------------------------------------
# COUNTRY DATA
# ---------------------------------------------------------

country_trend = df[
    df["Country"] == selected_country_trend
].sort_values("Year")


# ---------------------------------------------------------
# LINE CHART
# ---------------------------------------------------------

fig_trend = px.line(
    country_trend,
    x="Year",
    y="Life Expectancy",
    markers=True,
    title=(
        f"Life Expectancy in "
        f"{selected_country_trend}"
    ),
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
# SECTION 3 — COMPARISONS
# =========================================================

st.divider()

st.header(
    "📊 Life Expectancy Compared with Other Factors"
)

st.write(
    """
    Select a year and country to explore life expectancy
    compared with health spending, GDP per capita, and population.
    """
)


# ---------------------------------------------------------
# YEAR SELECTOR
# ---------------------------------------------------------

comparison_years = sorted(
    df["Year"].dropna().unique()
)

comparison_year = st.selectbox(
    "Select Year",
    comparison_years,
    index=len(comparison_years) - 1,
    key="comparison_year"
)


# ---------------------------------------------------------
# COUNTRY LIST BASED ON SELECTED YEAR
# ---------------------------------------------------------

countries_for_year = sorted(
    df[
        df["Year"] == comparison_year
    ]["Country"]
    .dropna()
    .unique()
)


# ---------------------------------------------------------
# COUNTRY SELECTOR
# ---------------------------------------------------------

selected_country = st.selectbox(
    "Select Country",
    countries_for_year,
    key="comparison_country"
)


# =========================================================
# SELECTED COUNTRY LIFE EXPECTANCY
# =========================================================

selected_life = df[
    (df["Country"] == selected_country) &
    (df["Year"] == comparison_year)
]


if not selected_life.empty:

    life_value = selected_life[
        "Life Expectancy"
    ].iloc[0]

    st.metric(
        f"{selected_country} Life Expectancy",
        f"{life_value:.1f} years"
    )


# =========================================================
# 1. HEALTH SPENDING
# =========================================================

st.subheader(
    "🏥 Life Expectancy vs Health Spending"
)


health_selected = health_df[
    (health_df["Country"] == selected_country) &
    (health_df["Year"] == comparison_year)
].copy()


if not health_selected.empty:

    health_selected = health_selected.dropna(
        subset=[
            "Health Expenditure",
            "Life Expectancy"
        ]
    )


if not health_selected.empty:

    fig_health = px.scatter(
        health_selected,
        x="Health Expenditure",
        y="Life Expectancy",
        hover_name="Country",
        title=(
            f"{selected_country}: "
            f"Health Spending vs Life Expectancy"
        ),
        labels={
            "Health Expenditure":
                "Health Spending per Capita",
            "Life Expectancy":
                "Life Expectancy (years)"
        }
    )

    st.plotly_chart(
        fig_health,
        use_container_width=True
    )

else:

    st.info(
        "Health expenditure data is not available "
        "for this country and year."
    )


# =========================================================
# 2. GDP
# =========================================================

st.subheader(
    "💰 Life Expectancy vs GDP per Capita"
)


if gdp_column is not None:

    gdp_selected = gdp_df[
        (gdp_df["Country"] == selected_country) &
        (gdp_df["Year"] == comparison_year)
    ].copy()

    gdp_selected = gdp_selected.dropna(
        subset=[
            gdp_column,
            "Life Expectancy"
        ]
    )


    if not gdp_selected.empty:

        fig_gdp = px.scatter(
            gdp_selected,
            x=gdp_column,
            y="Life Expectancy",
            hover_name="Country",
            title=(
                f"{selected_country}: "
                f"GDP vs Life Expectancy"
            ),
            labels={
                gdp_column:
                    "GDP per Capita",
                "Life Expectancy":
                    "Life Expectancy (years)"
            }
        )

        st.plotly_chart(
            fig_gdp,
            use_container_width=True
        )

    else:

        st.info(
            "GDP data is not available "
            "for this country and year."
        )

else:

    st.warning(
        "GDP per capita column was not found."
    )


# =========================================================
# 3. POPULATION
# =========================================================

st.subheader(
    "👥 Life Expectancy vs Population"
)


if population_column is not None:

    population_selected = df[
        (df["Country"] == selected_country) &
        (df["Year"] == comparison_year)
    ].copy()

    population_selected = population_selected.dropna(
        subset=[
            population_column,
            "Life Expectancy"
        ]
    )


    if not population_selected.empty:

        fig_population = px.scatter(
            population_selected,
            x=population_column,
            y="Life Expectancy",
            hover_name="Country",
            title=(
                f"{selected_country}: "
                f"Population vs Life Expectancy"
            ),
            labels={
                population_column:
                    "Population",
                "Life Expectancy":
                    "Life Expectancy (years)"
            },
            log_x=True
        )

        st.plotly_chart(
            fig_population,
            use_container_width=True
        )

    else:

        st.info(
            "Population data is not available "
            "for this country and year."
        )

else:

    st.info(
        "Population data is not included in "
        "your life-expectancy.csv file."
    )


# =========================================================
# DATA SOURCES
# =========================================================

st.divider()

st.subheader("📚 Data Sources")

st.markdown(
    "[Life Expectancy Dataset]"
    "(https://github.com/veronikayushchak-coder/"
    "dsc205-streamlit/blob/main/life-expectancy.csv)"
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

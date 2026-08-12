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

# --------------------------------------------------
# LIFE EXPECTANCY OVER TIME
# --------------------------------------------------

st.divider()

st.header("📈 Life Expectancy Over Time")

st.write(
    "Select a country to see how its life expectancy "
    "has changed over the years."
)

# Country selector
country_list = sorted(
    df["Country"].dropna().unique()
)

selected_country = st.selectbox(
    "Select a country",
    country_list
)

# Filter for selected country
country_data = df[
    df["Country"] == selected_country
].sort_values("Year")

# Create line chart
fig = px.line(
    country_data,
    x="Year",
    y="Life Expectancy",
    markers=True,
    title=f"Life Expectancy in {selected_country}",
    labels={
        "Year": "Year",
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

# ==================================================
# LIFE EXPECTANCY COMPARED WITH OTHER FACTORS
# ==================================================

st.divider()

st.header("📊 Life Expectancy Compared with Other Factors")

st.write(
    "Choose a year and country to explore the relationship "
    "between life expectancy, health spending, GDP, and population."
)

# --------------------------------------------------
# LOAD GDP DATA
# --------------------------------------------------

gdp_url = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit/"
    "main/life-expectancy-vs-gdp-per-capita.csv"
)

gdp_df = pd.read_csv(gdp_url)

gdp_df = gdp_df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy"
    }
)

# Find GDP column
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


# --------------------------------------------------
# LOAD HEALTH DATA
# --------------------------------------------------

health_url = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit/"
    "main/life-expectancy-vs-health-expenditure.csv"
)

health_df = pd.read_csv(health_url)

health_df = health_df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy",
        "Health expenditure per capita":
            "Health Expenditure"
    }
)


# --------------------------------------------------
# FIND POPULATION COLUMN
# --------------------------------------------------

population_column = None

possible_population_columns = [
    "Population",
    "population",
    "Population (historical)"
]

for column in possible_population_columns:
    if column in df.columns:
        population_column = column
        break


# ==================================================
# FILTERS
# ==================================================

st.subheader("🔎 Select Data")

col1, col2 = st.columns(2)

# --------------------------------------------------
# YEAR SELECTOR
# --------------------------------------------------

with col1:

    available_years = sorted(
        df["Year"].dropna().unique()
    )

    selected_year = st.selectbox(
        "Select Year",
        available_years,
        index=len(available_years) - 1,
        key="comparison_year"
    )


# --------------------------------------------------
# COUNTRY SELECTOR
# --------------------------------------------------

with col2:

    available_countries = sorted(
        df["Country"].dropna().unique()
    )

    selected_country = st.selectbox(
        "Select Country",
        available_countries,
        key="comparison_country"
    )


# ==================================================
# SELECTED COUNTRY LIFE EXPECTANCY
# ==================================================

country_life = df[
    (df["Country"] == selected_country) &
    (df["Year"] == selected_year)
]

if not country_life.empty:

    life_value = country_life[
        "Life Expectancy"
    ].iloc[0]

    st.metric(
        f"{selected_country} Life Expectancy",
        f"{life_value:.1f} years"
    )

else:

    st.warning(
        "Life expectancy data is not available "
        "for this country and year."
    )


# ==================================================
# 1. HEALTH SPENDING
# ==================================================

st.subheader("🏥 Life Expectancy vs Health Spending")

health_selected = health_df[
    (health_df["Country"] == selected_country) &
    (health_df["Year"] == selected_year)
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
                f"{selected_country} — "
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
            "No health expenditure data available."
        )

else:

    st.info(
        "No health expenditure data available "
        "for this country and year."
    )


# ==================================================
# 2. GDP
# ==================================================

st.subheader("💰 Life Expectancy vs GDP per Capita")

if gdp_column is not None:

    gdp_selected = gdp_df[
        (gdp_df["Country"] == selected_country) &
        (gdp_df["Year"] == selected_year)
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
                f"{selected_country} — "
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
            "No GDP data available for "
            "this country and year."
        )

else:

    st.warning(
        "GDP per capita column was not found."
    )


# ==================================================
# 3. POPULATION
# ==================================================

st.subheader("👥 Life Expectancy vs Population")

if population_column is not None:

    population_selected = df[
        (df["Country"] == selected_country) &
        (df["Year"] == selected_year)
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
                f"{selected_country} — "
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
            "No population data available."
        )

else:

    st.warning(
        "Population data is not included in "
        "life-expectancy.csv."
    )

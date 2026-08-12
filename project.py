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
# LIFE EXPECTANCY COMPARISONS
# ==================================================

st.divider()

st.header("📊 Life Expectancy Compared with Other Factors")

st.write(
    "Explore how life expectancy is related to health spending, "
    "GDP per capita, and population."
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
# LOAD HEALTH EXPENDITURE DATA
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
# PREPARE POPULATION DATA
# --------------------------------------------------

population_column = None

possible_population_columns = [
    "Population",
    "population",
    "Population (historical)",
    "Population - Sex: all - Age: all - Variant: estimates"
]

for column in possible_population_columns:
    if column in df.columns:
        population_column = column
        break


# --------------------------------------------------
# YEAR SELECTOR
# --------------------------------------------------

comparison_years = sorted(
    df["Year"].dropna().unique()
)

comparison_year = st.select_slider(
    "Select Year for Comparison",
    options=comparison_years,
    value=comparison_years[-1],
    key="comparison_year"
)


# ==================================================
# 1. LIFE EXPECTANCY VS HEALTH SPENDING
# ==================================================

st.subheader("🏥 Life Expectancy vs Health Spending")

health_year = health_df[
    health_df["Year"] == comparison_year
].copy()

health_year = health_year.dropna(
    subset=[
        "Life Expectancy",
        "Health Expenditure"
    ]
)

fig_health = px.scatter(
    health_year,
    x="Health Expenditure",
    y="Life Expectancy",
    hover_name="Country",
    title=f"Life Expectancy vs Health Spending — {comparison_year}",
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


# ==================================================
# 2. LIFE EXPECTANCY VS GDP
# ==================================================

st.subheader("💰 Life Expectancy vs GDP per Capita")

if gdp_column is not None:

    gdp_year = gdp_df[
        gdp_df["Year"] == comparison_year
    ].copy()

    gdp_year = gdp_year.dropna(
        subset=[
            "Life Expectancy",
            gdp_column
        ]
    )

    fig_gdp = px.scatter(
        gdp_year,
        x=gdp_column,
        y="Life Expectancy",
        hover_name="Country",
        title=f"Life Expectancy vs GDP per Capita — {comparison_year}",
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

    st.warning(
        "GDP per capita column was not found."
    )


# ==================================================
# 3. LIFE EXPECTANCY VS POPULATION
# ==================================================

st.subheader("👥 Life Expectancy vs Population")

if population_column is not None:

    population_year = df[
        df["Year"] == comparison_year
    ].copy()

    population_year = population_year.dropna(
        subset=[
            "Life Expectancy",
            population_column
        ]
    )

    fig_population = px.scatter(
        population_year,
        x=population_column,
        y="Life Expectancy",
        hover_name="Country",
        title=f"Life Expectancy vs Population — {comparison_year}",
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

    st.warning(
        "A population column was not found in "
        "life-expectancy.csv."
    )

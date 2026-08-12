import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Life Expectancy Analysis",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    life_expectancy = pd.read_csv(
        "life-expectancy.csv"
    )

    gdp = pd.read_csv(
        "life-expectancy-vs-gdp-per-capita.csv"
    )

    health = pd.read_csv(
        "life-expectancy-vs-health-expenditure.csv"
    )

    return life_expectancy, gdp, health


life_df, gdp_df, health_df = load_data()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🌍 Life Expectancy Analysis")

st.write(
    "This interactive dashboard explores life expectancy "
    "and its relationship with GDP per capita and health "
    "expenditure across countries and years."
)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a section:",
    [
        "Life Expectancy",
        "Life Expectancy vs GDP",
        "Life Expectancy vs Health Expenditure"
    ]
)


# ==================================================
# PAGE 1 — LIFE EXPECTANCY
# ==================================================

if page == "Life Expectancy":

    st.header("🌍 Life Expectancy")

    st.write(
        "Explore changes in life expectancy across "
        "countries and over time."
    )

    # ----------------------------------------------
    # Clean columns
    # ----------------------------------------------

    life_df = life_df.rename(
        columns={
            "Entity": "Country",
            "Life expectancy": "Life Expectancy"
        }
    )

    # ----------------------------------------------
    # SIDEBAR FILTERS
    # ----------------------------------------------

    st.sidebar.subheader("Filters")

    countries = sorted(
        life_df["Country"].dropna().unique()
    )

    selected_country = st.sidebar.selectbox(
        "Select Country",
        ["All Countries"] + countries
    )

    min_year = int(life_df["Year"].min())
    max_year = int(life_df["Year"].max())

    selected_year = st.sidebar.slider(
        "Select Year",
        min_year,
        max_year,
        max_year
    )

    # ----------------------------------------------
    # FILTER DATA
    # ----------------------------------------------

    filtered_life = life_df[
        life_df["Year"] == selected_year
    ]

    if selected_country != "All Countries":

        filtered_life = filtered_life[
            filtered_life["Country"] == selected_country
        ]

    # ----------------------------------------------
    # METRICS
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Countries",
            filtered_life["Country"].nunique()
        )

    with col2:

        average_life = filtered_life[
            "Life Expectancy"
        ].mean()

        st.metric(
            "Average Life Expectancy",
            f"{average_life:.1f} years"
        )

    with col3:

        highest = filtered_life[
            "Life Expectancy"
        ].max()

        st.metric(
            "Highest Life Expectancy",
            f"{highest:.1f} years"
        )

    st.divider()

    # ----------------------------------------------
    # LIFE EXPECTANCY BY COUNTRY
    # ----------------------------------------------

    st.subheader(
        f"Life Expectancy by Country — {selected_year}"
    )

    if selected_country == "All Countries":

        top_countries = (
            filtered_life
            .sort_values(
                "Life Expectancy",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            top_countries.sort_values(
                "Life Expectancy"
            ),
            x="Life Expectancy",
            y="Country",
            orientation="h",
            title="Top Countries by Life Expectancy",
            labels={
                "Life Expectancy":
                    "Life Expectancy (years)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.metric(
            selected_country,
            f"{filtered_life['Life Expectancy'].iloc[0]:.1f} years"
        )

    # ----------------------------------------------
    # TREND OVER TIME
    # ----------------------------------------------

    st.subheader("📈 Life Expectancy Over Time")

    if selected_country == "All Countries":

        trend = (
            life_df
            .groupby("Year")["Life Expectancy"]
            .mean()
            .reset_index()
        )

        fig = px.line(
            trend,
            x="Year",
            y="Life Expectancy",
            markers=True,
            title="Average Global Life Expectancy",
            labels={
                "Life Expectancy":
                    "Average Life Expectancy (years)"
            }
        )

    else:

        country_trend = life_df[
            life_df["Country"] == selected_country
        ]

        fig = px.line(
            country_trend,
            x="Year",
            y="Life Expectancy",
            markers=True,
            title=f"Life Expectancy in {selected_country}",
            labels={
                "Life Expectancy":
                    "Life Expectancy (years)"
            }
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==================================================
# PAGE 2 — LIFE EXPECTANCY VS GDP
# ==================================================

elif page == "Life Expectancy vs GDP":

    st.header("💰 Life Expectancy vs GDP per Capita")

    st.write(
        "Explore the relationship between GDP per capita "
        "and life expectancy."
    )

    # ----------------------------------------------
    # CLEAN DATA
    # ----------------------------------------------

    gdp_df = gdp_df.rename(
        columns={
            "Entity": "Country",
            "Life expectancy": "Life Expectancy",
            "GDP per capita": "GDP per Capita"
        }
    )

    # ----------------------------------------------
    # FIND GDP COLUMN
    # ----------------------------------------------

    gdp_columns = gdp_df.columns.tolist()

    possible_gdp_columns = [
        "GDP per Capita",
        "GDP per capita",
        "GDP per capita, PPP",
        "GDP per capita (int. $)"
    ]

    gdp_column = None

    for column in possible_gdp_columns:

        if column in gdp_columns:
            gdp_column = column
            break

    if gdp_column is None:

        st.error(
            "GDP column was not found in the CSV file."
        )

        st.write(
            "Columns found:",
            gdp_columns
        )

        st.stop()

    # ----------------------------------------------
    # YEAR FILTER
    # ----------------------------------------------

    min_year = int(gdp_df["Year"].min())
    max_year = int(gdp_df["Year"].max())

    selected_year = st.sidebar.slider(
        "Select Year",
        min_year,
        max_year,
        max_year
    )

    gdp_year = gdp_df[
        gdp_df["Year"] == selected_year
    ].copy()

    # ----------------------------------------------
    # METRICS
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Countries",
            gdp_year["Country"].nunique()
        )

    with col2:

        avg_life = gdp_year[
            "Life Expectancy"
        ].mean()

        st.metric(
            "Average Life Expectancy",
            f"{avg_life:.1f} years"
        )

    with col3:

        avg_gdp = gdp_year[
            gdp_column
        ].mean()

        st.metric(
            "Average GDP per Capita",
            f"${avg_gdp:,.0f}"
        )

    st.divider()

    # ----------------------------------------------
    # SCATTER PLOT
    # ----------------------------------------------

    st.subheader(
        f"GDP per Capita vs Life Expectancy — {selected_year}"
    )

    gdp_year = gdp_year.dropna(
        subset=[
            gdp_column,
            "Life Expectancy"
        ]
    )

    fig = px.scatter(
        gdp_year,
        x=gdp_column,
        y="Life Expectancy",
        hover_name="Country",
        size="Life Expectancy",
        log_x=True,
        title="GDP per Capita and Life Expectancy",
        labels={
            gdp_column:
                "GDP per Capita",
            "Life Expectancy":
                "Life Expectancy (years)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ----------------------------------------------
    # COUNTRY SELECTION
    # ----------------------------------------------

    st.subheader("🔎 Country Comparison")

    selected_countries = st.multiselect(
        "Select countries",
        sorted(gdp_year["Country"].unique())
    )

    if selected_countries:

        comparison = gdp_year[
            gdp_year["Country"].isin(
                selected_countries
            )
        ]

        st.dataframe(
            comparison[
                [
                    "Country",
                    "Year",
                    gdp_column,
                    "Life Expectancy"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# PAGE 3 — LIFE EXPECTANCY VS HEALTH EXPENDITURE
# ==================================================

elif page == "Life Expectancy vs Health Expenditure":

    st.header(
        "🏥 Life Expectancy vs Health Expenditure"
    )

    st.write(
        "Explore whether countries that spend more "
        "on health care tend to have higher life expectancy."
    )

    # ----------------------------------------------
    # CLEAN DATA
    # ----------------------------------------------

    health_df = health_df.rename(
        columns={
            "Entity": "Country",
            "Life expectancy": "Life Expectancy",
            "Health expenditure per capita":
                "Health Expenditure"
        }
    )

    # ----------------------------------------------
    # CHECK HEALTH COLUMN
    # ----------------------------------------------

    if "Health Expenditure" not in health_df.columns:

        st.error(
            "Health expenditure column was not found."
        )

        st.write(
            "Columns found:",
            health_df.columns.tolist()
        )

        st.stop()

    # ----------------------------------------------
    # YEAR FILTER
    # ----------------------------------------------

    min_year = int(health_df["Year"].min())
    max_year = int(health_df["Year"].max())

    selected_year = st.sidebar.slider(
        "Select Year",
        min_year,
        max_year,
        max_year
    )

    health_year = health_df[
        health_df["Year"] == selected_year
    ].copy()

    # ----------------------------------------------
    # METRICS
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Countries",
            health_year["Country"].nunique()
        )

    with col2:

        average_life = health_year[
            "Life Expectancy"
        ].mean()

        st.metric(
            "Average Life Expectancy",
            f"{average_life:.1f} years"
        )

    with col3:

        average_health = health_year[
            "Health Expenditure"
        ].mean()

        st.metric(
            "Average Health Expenditure",
            f"${average_health:,.0f}"
        )

    st.divider()

    # ----------------------------------------------
    # SCATTER PLOT
    # ----------------------------------------------

    st.subheader(
        f"Health Expenditure vs Life Expectancy — {selected_year}"
    )

    health_year = health_year.dropna(
        subset=[
            "Health Expenditure",
            "Life Expectancy"
        ]
    )

    fig = px.scatter(
        health_year,
        x="Health Expenditure",
        y="Life Expectancy",
        hover_name="Country",
        size="Life Expectancy",
        title="Health Expenditure and Life Expectancy",
        labels={
            "Health Expenditure":
                "Health Expenditure Per Capita",
            "Life Expectancy":
                "Life Expectancy (years)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ----------------------------------------------
    # COUNTRY COMPARISON
    # ----------------------------------------------

    st.subheader("🔎 Country Comparison")

    selected_countries = st.multiselect(
        "Select countries",
        sorted(
            health_year["Country"].unique()
        )
    )

    if selected_countries:

        comparison = health_year[
            health_year["Country"].isin(
                selected_countries
            )
        ]

        st.dataframe(
            comparison[
                [
                    "Country",
                    "Year",
                    "Health Expenditure",
                    "Life Expectancy"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Source: Our World in Data (OWID)"
)

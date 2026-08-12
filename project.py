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


life_df, gdp_df, health_df = load_data()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

life_df = life_df.rename(
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
# MAIN TITLE
# =========================================================

st.title("🌍 Life Expectancy Analysis")

st.write(
    """
    This interactive dashboard explores life expectancy
    across countries and examines its relationship with
    GDP per capita and health expenditure.
    """
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a section:",
    [
        "🌍 Life Expectancy",
        "💰 Life Expectancy vs GDP",
        "🏥 Life Expectancy vs Health Expenditure"
    ]
)


# =========================================================
# PAGE 1 — LIFE EXPECTANCY
# =========================================================

if page == "🌍 Life Expectancy":

    st.header("Life Expectancy")

    st.write(
        "Explore life expectancy across countries and over time."
    )

    # -----------------------------------------------------
    # SIDEBAR FILTERS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # FILTER DATA
    # -----------------------------------------------------

    filtered_life = life_df[
        life_df["Year"] == selected_year
    ].copy()

    if selected_country != "All Countries":

        filtered_life = filtered_life[
            filtered_life["Country"] == selected_country
        ]

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

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

        highest_life = filtered_life[
            "Life Expectancy"
        ].max()

        st.metric(
            "Highest Life Expectancy",
            f"{highest_life:.1f} years"
        )

    st.divider()

    # -----------------------------------------------------
    # COUNTRY COMPARISON
    # -----------------------------------------------------

    st.subheader(
        f"Life Expectancy by Country — {selected_year}"
    )

    if selected_country == "All Countries":

        top_countries = (
            filtered_life
            .dropna(subset=["Life Expectancy"])
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
            title="Top 15 Countries by Life Expectancy",
            labels={
                "Life Expectancy":
                    "Life Expectancy (years)",
                "Country":
                    "Country"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        if not filtered_life.empty:

            value = filtered_life[
                "Life Expectancy"
            ].iloc[0]

            st.metric(
                selected_country,
                f"{value:.1f} years"
            )

    # -----------------------------------------------------
    # LIFE EXPECTANCY TREND
    # -----------------------------------------------------

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
            title="Average Life Expectancy Over Time",
            labels={
                "Year": "Year",
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
                "Year": "Year",
                "Life Expectancy":
                    "Life Expectancy (years)"
            }
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PAGE 2 — LIFE EXPECTANCY VS GDP
# =========================================================

elif page == "💰 Life Expectancy vs GDP":

    st.header("Life Expectancy vs GDP per Capita")

    st.write(
        """
        Explore the relationship between GDP per capita
        and life expectancy.
        """
    )

    # -----------------------------------------------------
    # CHECK GDP COLUMN
    # -----------------------------------------------------

    if gdp_column is None:

        st.error(
            "The GDP per capita column could not be found."
        )

        st.write(
            "Columns found in the dataset:"
        )

        st.write(gdp_df.columns.tolist())

        st.stop()

    # -----------------------------------------------------
    # YEAR FILTER
    # -----------------------------------------------------

    st.sidebar.subheader("GDP Filters")

    min_year = int(gdp_df["Year"].min())
    max_year = int(gdp_df["Year"].max())

    selected_year = st.sidebar.slider(
        "Select Year",
        min_year,
        max_year,
        max_year,
        key="gdp_year"
    )

    gdp_year = gdp_df[
        gdp_df["Year"] == selected_year
    ].copy()

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # SCATTER PLOT
    # -----------------------------------------------------

    st.subheader(
        f"GDP per Capita vs Life Expectancy — {selected_year}"
    )

    gdp_plot = gdp_year.dropna(
        subset=[
            gdp_column,
            "Life Expectancy"
        ]
    )

    fig = px.scatter(
        gdp_plot,
        x=gdp_column,
        y="Life Expectancy",
        hover_name="Country",
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

    # -----------------------------------------------------
    # COUNTRY COMPARISON
    # -----------------------------------------------------

    st.subheader("🔎 Country Comparison")

    selected_countries = st.multiselect(
        "Select countries to compare",
        sorted(
            gdp_plot["Country"].unique()
        ),
        key="gdp_countries"
    )

    if selected_countries:

        comparison = gdp_plot[
            gdp_plot["Country"].isin(
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


# =========================================================
# PAGE 3 — LIFE EXPECTANCY VS HEALTH EXPENDITURE
# =========================================================

elif page == "🏥 Life Expectancy vs Health Expenditure":

    st.header(
        "Life Expectancy vs Health Expenditure"
    )

    st.write(
        """
        Explore the relationship between health expenditure
        per capita and life expectancy.
        """
    )

    # -----------------------------------------------------
    # CHECK HEALTH COLUMN
    # -----------------------------------------------------

    if "Health Expenditure" not in health_df.columns:

        st.error(
            "The health expenditure column could not be found."
        )

        st.write(
            "Columns found in the dataset:"
        )

        st.write(
            health_df.columns.tolist()
        )

        st.stop()

    # -----------------------------------------------------
    # YEAR FILTER
    # -----------------------------------------------------

    st.sidebar.subheader("Health Filters")

    min_year = int(health_df["Year"].min())
    max_year = int(health_df["Year"].max())

    selected_year = st.sidebar.slider(
        "Select Year",
        min_year,
        max_year,
        max_year,
        key="health_year"
    )

    health_year = health_df[
        health_df["Year"] == selected_year
    ].copy()

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # SCATTER PLOT
    # -----------------------------------------------------

    st.subheader(
        f"Health Expenditure vs Life Expectancy — {selected_year}"
    )

    health_plot = health_year.dropna(
        subset=[
            "Health Expenditure",
            "Life Expectancy"
        ]
    )

    fig = px.scatter(
        health_plot,
        x="Health Expenditure",
        y="Life Expectancy",
        hover_name="Country",
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

    # -----------------------------------------------------
    # COUNTRY COMPARISON
    # -----------------------------------------------------

    st.subheader("🔎 Country Comparison")

    selected_countries = st.multiselect(
        "Select countries to compare",
        sorted(
            health_plot["Country"].unique()
        ),
        key="health_countries"
    )

    if selected_countries:

        comparison = health_plot[
            health_plot["Country"].isin(
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

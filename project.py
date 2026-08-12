import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="LifeLens",
    page_icon="🌎",
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

    life = pd.read_csv(LIFE_URL)
    gdp = pd.read_csv(GDP_URL)
    health = pd.read_csv(HEALTH_URL)

    return life, gdp, health


df, gdp_df, health_df = load_data()


# =========================================================
# CLEAN DATA
# =========================================================

df = df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy"
    }
)

gdp_df = gdp_df.rename(
    columns={
        "Entity": "Country"
    }
)

health_df = health_df.rename(
    columns={
        "Entity": "Country",
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
# BASIC DATA
# =========================================================

countries = sorted(
    df["Country"].dropna().unique()
)

years = sorted(
    df["Year"].dropna().unique()
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🌎 LifeLens")

st.sidebar.write(
    "Understanding how the world lives."
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🗺️ Explore the World",
        "🔎 Country Explorer",
        "⚖️ Compare Countries",
        "🔬 Relationships"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Data source: Our World in Data"
)


# =========================================================
# HOME PAGE
# =========================================================

if page == "🏠 Home":

    st.title("🌎 LifeLens")

    st.subheader(
        "Understanding how the world lives."
    )

    st.write(
        """
        Explore how life expectancy has changed around
        the world and investigate how it relates to
        economic and healthcare factors.
        """
    )

    st.divider()

    # -----------------------------------------------------
    # QUICK STATISTICS
    # -----------------------------------------------------

    latest_year = int(years[-1])

    latest_data = df[
        df["Year"] == latest_year
    ].dropna(
        subset=["Life Expectancy"]
    )

    average_latest = latest_data[
        "Life Expectancy"
    ].mean()

    highest_latest = latest_data.loc[
        latest_data["Life Expectancy"].idxmax()
    ]

    lowest_latest = latest_data.loc[
        latest_data["Life Expectancy"].idxmin()
    ]


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Countries",
            len(countries)
        )


    with col2:

        st.metric(
            "Latest Year",
            latest_year
        )


    with col3:

        st.metric(
            "Global Average",
            f"{average_latest:.1f} years"
        )


    with col4:

        st.metric(
            "Years of Data",
            f"{int(years[-1] - years[0])}+"
        )


    st.divider()

    # -----------------------------------------------------
    # HIGHEST / LOWEST
    # -----------------------------------------------------

    st.header(
        f"🌍 The World in {latest_year}"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader("🏆 Highest Life Expectancy")

        st.metric(
            highest_latest["Country"],
            f"{highest_latest['Life Expectancy']:.1f} years"
        )


    with col2:

        st.subheader("📉 Lowest Life Expectancy")

        st.metric(
            lowest_latest["Country"],
            f"{lowest_latest['Life Expectancy']:.1f} years"
        )


    st.divider()

    # -----------------------------------------------------
    # TOP COUNTRIES
    # -----------------------------------------------------

    st.header("🏆 Top 10 Countries")

    top10 = latest_data.sort_values(
        "Life Expectancy",
        ascending=False
    ).head(10)

    fig = px.bar(
        top10.sort_values("Life Expectancy"),
        x="Life Expectancy",
        y="Country",
        orientation="h",
        labels={
            "Life Expectancy":
                "Life Expectancy (years)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.info(
        "Use the navigation menu on the left to explore "
        "the world, individual countries, comparisons, "
        "and relationships between variables."
    )


# =========================================================
# EXPLORE THE WORLD
# =========================================================

elif page == "🗺️ Explore the World":

    st.title("🗺️ Explore the World")

    st.write(
        "See how life expectancy differs around the world."
    )

    # -----------------------------------------------------
    # YEAR
    # -----------------------------------------------------

    selected_year = st.select_slider(
        "Select Year",
        options=years,
        value=years[-1]
    )


    map_data = df[
        df["Year"] == selected_year
    ].dropna(
        subset=[
            "Country",
            "Life Expectancy"
        ]
    ).copy()


    # -----------------------------------------------------
    # MAP
    # -----------------------------------------------------

    fig_map = px.choropleth(
        map_data,
        locations="Code",
        color="Life Expectancy",
        hover_name="Country",
        color_continuous_scale="YlGnBu",
        projection="natural earth",
        labels={
            "Life Expectancy":
                "Life Expectancy (years)"
        },
        title=f"Life Expectancy — {selected_year}"
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


    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    highest = map_data.loc[
        map_data["Life Expectancy"].idxmax()
    ]

    lowest = map_data.loc[
        map_data["Life Expectancy"].idxmin()
    ]

    average = map_data[
        "Life Expectancy"
    ].mean()


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Global Average",
            f"{average:.1f} years"
        )


    with c2:

        st.metric(
            "Highest",
            f"{highest['Life Expectancy']:.1f} years"
        )

        st.caption(highest["Country"])


    with c3:

        st.metric(
            "Lowest",
            f"{lowest['Life Expectancy']:.1f} years"
        )

        st.caption(lowest["Country"])


    st.divider()

    # -----------------------------------------------------
    # TOP / BOTTOM
    # -----------------------------------------------------

    ranking_choice = st.radio(
        "Ranking",
        [
            "Highest",
            "Lowest"
        ],
        horizontal=True
    )


    if ranking_choice == "Highest":

        ranking = map_data.sort_values(
            "Life Expectancy",
            ascending=False
        ).head(10)

    else:

        ranking = map_data.sort_values(
            "Life Expectancy",
            ascending=True
        ).head(10)


    fig_rank = px.bar(
        ranking.sort_values(
            "Life Expectancy"
        ),
        x="Life Expectancy",
        y="Country",
        orientation="h",
        labels={
            "Life Expectancy":
                "Life Expectancy (years)"
        }
    )


    st.plotly_chart(
        fig_rank,
        use_container_width=True
    )


# =========================================================
# COUNTRY EXPLORER
# =========================================================

elif page == "🔎 Country Explorer":

    st.title("🔎 Country Explorer")

    st.write(
        "Select a country and explore its life expectancy "
        "history."
    )


    selected_country = st.selectbox(
        "Select Country",
        countries
    )


    country_data = df[
        df["Country"] == selected_country
    ].dropna(
        subset=["Life Expectancy"]
    ).sort_values("Year")


    if not country_data.empty:

        first = country_data[
            "Life Expectancy"
        ].iloc[0]

        latest = country_data[
            "Life Expectancy"
        ].iloc[-1]

        highest = country_data[
            "Life Expectancy"
        ].max()

        lowest = country_data[
            "Life Expectancy"
        ].min()

        change = latest - first


        # -------------------------------------------------
        # STATISTICS
        # -------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)


        with c1:

            st.metric(
                "First Available",
                f"{first:.1f} years"
            )


        with c2:

            st.metric(
                "Latest",
                f"{latest:.1f} years"
            )


        with c3:

            st.metric(
                "Total Change",
                f"{change:+.1f} years"
            )


        with c4:

            st.metric(
                "Highest",
                f"{highest:.1f} years"
            )


        # -------------------------------------------------
        # TIME PERIOD
        # -------------------------------------------------

        st.subheader(
            "📈 Life Expectancy Over Time"
        )


        min_year = int(
            country_data["Year"].min()
        )

        max_year = int(
            country_data["Year"].max()
        )


        year_range = st.slider(
            "Choose time period",
            min_year,
            max_year,
            (min_year, max_year)
        )


        filtered_country = country_data[
            (
                country_data["Year"]
                >= year_range[0]
            )
            &
            (
                country_data["Year"]
                <= year_range[1]
            )
        ]


        fig_country = px.line(
            filtered_country,
            x="Year",
            y="Life Expectancy",
            markers=True,
            labels={
                "Life Expectancy":
                    "Life Expectancy (years)"
            },
            title=(
                f"Life Expectancy — "
                f"{selected_country}"
            )
        )


        st.plotly_chart(
            fig_country,
            use_container_width=True
        )


        # -------------------------------------------------
        # HIGHEST / LOWEST YEARS
        # -------------------------------------------------

        highest_row = country_data.loc[
            country_data["Life Expectancy"].idxmax()
        ]

        lowest_row = country_data.loc[
            country_data["Life Expectancy"].idxmin()
        ]


        c1, c2 = st.columns(2)


        with c1:

            st.info(
                f"🏆 Highest: "
                f"{highest_row['Life Expectancy']:.1f} "
                f"years in "
                f"{int(highest_row['Year'])}."
            )


        with c2:

            st.info(
                f"📉 Lowest: "
                f"{lowest_row['Life Expectancy']:.1f} "
                f"years in "
                f"{int(lowest_row['Year'])}."
            )


# =========================================================
# COMPARE COUNTRIES
# =========================================================

elif page == "⚖️ Compare Countries":

    st.title("⚖️ Compare Countries")

    st.write(
        """
        Select a variable first. The available years and
        countries will automatically update based on the
        selected data.
        """
    )


    # -----------------------------------------------------
    # VARIABLE
    # -----------------------------------------------------

    comparison = st.radio(
        "What would you like to compare?",
        [
            "Life Expectancy",
            "Health Spending",
            "GDP per Capita"
        ],
        horizontal=True
    )


    # -----------------------------------------------------
    # DATASET
    # -----------------------------------------------------

    if comparison == "Life Expectancy":

        comparison_df = df.copy()
        value_column = "Life Expectancy"

    elif comparison == "Health Spending":

        comparison_df = health_df.copy()
        value_column = "Health Expenditure"

    else:

        comparison_df = gdp_df.copy()
        value_column = gdp_column


    if value_column is None:

        st.error(
            "The selected variable could not be found."
        )

        st.stop()


    # -----------------------------------------------------
    # YEARS
    # -----------------------------------------------------

    available_years = sorted(
        comparison_df[
            comparison_df[value_column].notna()
        ]["Year"]
        .dropna()
        .unique()
    )


    selected_year = st.selectbox(
        "Select Year",
        available_years,
        index=len(available_years) - 1
    )


    # -----------------------------------------------------
    # COUNTRIES
    # -----------------------------------------------------

    year_data = comparison_df[
        comparison_df["Year"] == selected_year
    ].dropna(
        subset=[
            "Country",
            value_column
        ]
    )


    available_countries = sorted(
        year_data["Country"].unique()
    )


    if len(available_countries) < 3:

        st.warning(
            "Fewer than three countries have complete "
            "data for this selection."
        )

        st.stop()


    c1, c2, c3 = st.columns(3)


    with c1:

        country1 = st.selectbox(
            "Country 1",
            available_countries,
            index=0
        )


    with c2:

        country2_options = [
            c for c in available_countries
            if c != country1
        ]

        country2 = st.selectbox(
            "Country 2",
            country2_options
        )


    with c3:

        country3_options = [
            c for c in available_countries
            if c not in [
                country1,
                country2
            ]
        ]

        country3 = st.selectbox(
            "Country 3",
            country3_options
        )


    selected = [
        country1,
        country2,
        country3
    ]


    comparison_data = year_data[
        year_data["Country"].isin(selected)
    ]


    # -----------------------------------------------------
    # VISUALIZATION SWITCHER
    # -----------------------------------------------------

    visualization = st.radio(
        "Choose visualization",
        [
            "Bar Chart",
            "Ranking"
        ],
        horizontal=True
    )


    if visualization == "Bar Chart":

        fig = px.bar(
            comparison_data,
            x="Country",
            y=value_column,
            text=value_column,
            labels={
                value_column:
                    comparison
            },
            title=(
                f"{comparison} — {selected_year}"
            )
        )

        fig.update_traces(
            textposition="outside"
        )

    else:

        ranking_data = comparison_data.sort_values(
            value_column,
            ascending=False
        )

        fig = px.bar(
            ranking_data,
            x=value_column,
            y="Country",
            orientation="h",
            text=value_column,
            labels={
                value_column:
                    comparison
            },
            title=(
                f"{comparison} Ranking — "
                f"{selected_year}"
            )
        )

        fig.update_traces(
            textposition="outside"
        )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# RELATIONSHIPS
# =========================================================

elif page == "🔬 Relationships":

    st.title("🔬 Relationships")

    st.write(
        """
        Investigate whether countries with higher GDP or
        greater health spending tend to have higher life
        expectancy.
        """
    )


    # -----------------------------------------------------
    # FACTOR
    # -----------------------------------------------------

    factor = st.radio(
        "Choose a factor",
        [
            "GDP per Capita",
            "Health Spending"
        ],
        horizontal=True
    )


    # =====================================================
    # GDP
    # =====================================================

    if factor == "GDP per Capita":

        if gdp_column is None:

            st.error(
                "GDP column could not be found."
            )

            st.stop()


        relationship_years = sorted(
            gdp_df[
                gdp_df[gdp_column].notna()
            ]["Year"]
            .dropna()
            .unique()
        )


        selected_year = st.selectbox(
            "Select Year",
            relationship_years,
            index=len(relationship_years) - 1
        )


        scatter = gdp_df[
            gdp_df["Year"] == selected_year
        ].copy()


        life_merge = df[
            [
                "Country",
                "Year",
                "Life Expectancy"
            ]
        ]


        scatter = scatter.merge(
            life_merge,
            on=[
                "Country",
                "Year"
            ],
            how="left"
        )


        scatter = scatter.dropna(
            subset=[
                "Country",
                gdp_column,
                "Life Expectancy"
            ]
        )


        x_column = gdp_column
        x_label = "GDP per Capita"


    # =====================================================
    # HEALTH
    # =====================================================

    else:

        relationship_years = sorted(
            health_df[
                health_df["Health Expenditure"].notna()
            ]["Year"]
            .dropna()
            .unique()
        )


        selected_year = st.selectbox(
            "Select Year",
            relationship_years,
            index=len(relationship_years) - 1
        )


        scatter = health_df[
            health_df["Year"] == selected_year
        ].copy()


        life_merge = df[
            [
                "Country",
                "Year",
                "Life Expectancy"
            ]
        ]


        scatter = scatter.merge(
            life_merge,
            on=[
                "Country",
                "Year"
            ],
            how="left"
        )


        scatter = scatter.dropna(
            subset=[
                "Country",
                "Health Expenditure",
                "Life Expectancy"
            ]
        )


        x_column = "Health Expenditure"
        x_label = "Health Spending per Capita"


    # -----------------------------------------------------
    # SCATTERPLOT
    # -----------------------------------------------------

    fig = px.scatter(
        scatter,
        x=x_column,
        y="Life Expectancy",
        hover_name="Country",
        labels={
            x_column: x_label,
            "Life Expectancy":
                "Life Expectancy (years)"
        },
        title=(
            f"Life Expectancy vs "
            f"{x_label} — {selected_year}"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # CORRELATION
    # -----------------------------------------------------

    if len(scatter) >= 2:

        correlation = scatter[
            [
                x_column,
                "Life Expectancy"
            ]
        ].corr().iloc[0, 1]


        st.metric(
            "Correlation",
            f"{correlation:.2f}"
        )


        if correlation >= 0.7:

            st.success(
                "Strong positive relationship."
            )

        elif correlation >= 0.3:

            st.info(
                "Moderate positive relationship."
            )

        elif correlation > -0.3:

            st.info(
                "Weak relationship."
            )

        else:

            st.warning(
                "Negative relationship."
            )


        st.caption(
            "Correlation shows association, not causation."
        )


# =========================================================
# FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.caption(
    "LifeLens | DSC 205"
)

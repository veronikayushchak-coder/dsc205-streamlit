import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Global Life Expectancy",
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

    column_lower = column.lower()

    if "gdp" in column_lower and "capita" in column_lower:

        gdp_column = column
        break


# =========================================================
# FIND REGION COLUMN
# =========================================================

region_column = None

for column in df.columns:

    column_lower = column.lower()

    if "region" in column_lower:

        region_column = column
        break


# =========================================================
# TITLE
# =========================================================

st.title("🌎 Global Life Expectancy")

st.write(
    """
    Explore how life expectancy has changed around the world
    and investigate its relationship with economic and
    health-related factors.
    """
)


# =========================================================
# SECTION 1 — WORLD MAP
# =========================================================

st.header("🌎 Life Expectancy Around the World")

st.write(
    "Select a year to explore life expectancy by country."
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
].dropna(
    subset=["Country", "Life Expectancy"]
).copy()


fig_map = px.choropleth(
    map_data,
    locations="Code",
    color="Life Expectancy",
    hover_name="Country",
    color_continuous_scale="YlGnBu",
    projection="natural earth",
    title=f"Life Expectancy in {map_year}",
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
# MAP STATISTICS
# =========================================================

highest_country = map_data.loc[
    map_data["Life Expectancy"].idxmax()
]

lowest_country = map_data.loc[
    map_data["Life Expectancy"].idxmin()
]

average_life = map_data[
    "Life Expectancy"
].mean()


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Global Average",
        f"{average_life:.1f} years"
    )

with col2:

    st.metric(
        "Highest",
        f"{highest_country['Life Expectancy']:.1f} years"
    )

    st.caption(
        highest_country["Country"]
    )

with col3:

    st.metric(
        "Lowest",
        f"{lowest_country['Life Expectancy']:.1f} years"
    )

    st.caption(
        lowest_country["Country"]
    )

with col4:

    st.metric(
        "Countries",
        map_data["Country"].nunique()
    )


# =========================================================
# TOP 10 COUNTRIES
# =========================================================

st.subheader(
    f"🏆 Countries with the Highest Life Expectancy — {map_year}"
)


top_10 = map_data.sort_values(
    "Life Expectancy",
    ascending=False
).head(10)


fig_top = px.bar(
    top_10.sort_values("Life Expectancy"),
    x="Life Expectancy",
    y="Country",
    orientation="h",
    title="Top 10 Countries",
    labels={
        "Life Expectancy":
            "Life Expectancy (years)"
    }
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)


# =========================================================
# SECTION 2 — LIFE EXPECTANCY OVER TIME
# =========================================================

st.divider()

st.header("📈 Life Expectancy Over Time")

st.write(
    "Select a country to see how its life expectancy "
    "has changed throughout the available years."
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
].sort_values("Year").dropna(
    subset=["Life Expectancy"]
)


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

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# =========================================================
# COUNTRY HISTORY STATISTICS
# =========================================================

if len(country_trend) > 0:

    first_value = country_trend[
        "Life Expectancy"
    ].iloc[0]

    last_value = country_trend[
        "Life Expectancy"
    ].iloc[-1]

    change = last_value - first_value

    if first_value != 0:

        percentage_change = (
            change / first_value
        ) * 100

    else:

        percentage_change = 0


    highest_value = country_trend[
        "Life Expectancy"
    ].max()

    highest_year = country_trend.loc[
        country_trend["Life Expectancy"].idxmax(),
        "Year"
    ]


    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "First Available",
            f"{first_value:.1f} years"
        )

    with c2:

        st.metric(
            "Latest Available",
            f"{last_value:.1f} years"
        )

    with c3:

        st.metric(
            "Total Change",
            f"{change:+.1f} years"
        )

    with c4:

        st.metric(
            "Highest",
            f"{highest_value:.1f} years"
        )

        st.caption(
            f"Year: {int(highest_year)}"
        )


# =========================================================
# SECTION 3 — COMPARE THREE COUNTRIES
# =========================================================

st.divider()

st.header("📊 Compare Countries")

st.write(
    """
    Choose a factor first. The available years and countries
    will automatically update based on your selection.
    """
)


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
# AVAILABLE YEARS
# =========================================================

if value_column is None:

    st.error(
        "The selected variable could not be found."
    )

    st.stop()


years_available = sorted(
    comparison_df[
        comparison_df[value_column].notna()
    ]["Year"]
    .dropna()
    .unique()
)


comparison_year = st.selectbox(
    "Select Year",
    years_available,
    index=len(years_available) - 1,
    key="comparison_year"
)


# =========================================================
# AVAILABLE COUNTRIES
# =========================================================

available_data = comparison_df[
    comparison_df["Year"] == comparison_year
].copy()


available_data = available_data.dropna(
    subset=[
        "Country",
        value_column
    ]
)


available_countries = sorted(
    available_data["Country"].unique()
)


if len(available_countries) < 3:

    st.warning(
        "There are fewer than 3 countries with "
        "complete data for this selection."
    )

    st.stop()


# =========================================================
# SELECT THREE COUNTRIES
# =========================================================

st.subheader("🌎 Select Three Countries")

c1, c2, c3 = st.columns(3)


with c1:

    country_1 = st.selectbox(
        "Country 1",
        available_countries,
        key="comparison_country_1"
    )


with c2:

    country_2_options = [
        x for x in available_countries
        if x != country_1
    ]

    country_2 = st.selectbox(
        "Country 2",
        country_2_options,
        key="comparison_country_2"
    )


with c3:

    country_3_options = [
        x for x in available_countries
        if x not in [
            country_1,
            country_2
        ]
    ]

    country_3 = st.selectbox(
        "Country 3",
        country_3_options,
        key="comparison_country_3"
    )


selected_countries = [
    country_1,
    country_2,
    country_3
]


# =========================================================
# COMPARISON DATA
# =========================================================

comparison_chart_data = available_data[
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
# BAR CHART
# =========================================================

fig_compare = px.bar(
    comparison_chart_data,
    x="Country",
    y=value_column,
    text=value_column,
    title=(
        f"{comparison_choice} — "
        f"{comparison_year}"
    ),
    labels={
        value_column:
            comparison_choice
    }
)

fig_compare.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)


# =========================================================
# SECTION 4 — GDP / HEALTH RELATIONSHIPS
# =========================================================

st.divider()

st.header(
    "🔬 Life Expectancy and Other Factors"
)

st.write(
    """
    Explore whether countries with higher GDP or greater
    health spending tend to have higher life expectancy.
    """
)


relationship_choice = st.radio(
    "Choose a factor:",
    [
        "GDP per Capita",
        "Health Spending"
    ],
    horizontal=True,
    key="relationship_choice"
)


# =========================================================
# GDP RELATIONSHIP
# =========================================================

if relationship_choice == "GDP per Capita":

    if gdp_column is None:

        st.warning(
            "GDP data could not be found."
        )

        st.stop()


    relationship_years = sorted(
        gdp_df[
            gdp_df[gdp_column].notna()
        ]["Year"]
        .dropna()
        .unique()
    )


    relationship_year = st.selectbox(
        "Select Year",
        relationship_years,
        index=len(relationship_years) - 1,
        key="gdp_year"
    )


    scatter_data = gdp_df[
        gdp_df["Year"] == relationship_year
    ].dropna(
        subset=[
            "Country",
            "Life Expectancy",
            gdp_column
        ]
    ).copy()


    x_column = gdp_column

    x_label = "GDP per Capita"


# =========================================================
# HEALTH RELATIONSHIP
# =========================================================

else:

    relationship_years = sorted(
        health_df[
            health_df["Health Expenditure"].notna()
        ]["Year"]
        .dropna()
        .unique()
    )


    relationship_year = st.selectbox(
        "Select Year",
        relationship_years,
        index=len(relationship_years) - 1,
        key="health_year"
    )


    scatter_data = health_df[
        health_df["Year"] == relationship_year
    ].dropna(
        subset=[
            "Country",
            "Life Expectancy",
            "Health Expenditure"
        ]
    ).copy()


    x_column = "Health Expenditure"

    x_label = "Health Spending per Capita"


# =========================================================
# SCATTERPLOT
# =========================================================

fig_scatter = px.scatter(
    scatter_data,
    x=x_column,
    y="Life Expectancy",
    hover_name="Country",
    trendline="ols",
    title=(
        f"Life Expectancy vs "
        f"{x_label} — {relationship_year}"
    ),
    labels={
        x_column: x_label,
        "Life Expectancy":
            "Life Expectancy (years)"
    }
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# =========================================================
# CORRELATION
# =========================================================

correlation = scatter_data[
    [x_column, "Life Expectancy"]
].corr().iloc[0, 1]


st.metric(
    "Correlation",
    f"{correlation:.2f}"
)


if correlation >= 0.7:

    st.info(
        "There is a strong positive relationship between "
        f"{x_label.lower()} and life expectancy in this year."
    )

elif correlation >= 0.3:

    st.info(
        "There is a moderate positive relationship between "
        f"{x_label.lower()} and life expectancy in this year."
    )

elif correlation > -0.3:

    st.info(
        "There is a weak relationship between these variables "
        "in this year."
    )

else:

    st.info(
        "There is a negative relationship between these "
        "variables in this year."
    )


st.caption(
    "Correlation shows association, not causation."
)


# =========================================================
# SECTION 5 — COUNTRY PROFILE
# =========================================================

st.divider()

st.header("🔎 Country Profile")

st.write(
    "Select a country to see a summary of its life expectancy."
)


profile_country = st.selectbox(
    "Select Country",
    all_countries,
    key="profile_country"
)


profile_data = df[
    df["Country"] == profile_country
].dropna(
    subset=["Life Expectancy"]
).sort_values("Year")


if not profile_data.empty:

    profile_first = profile_data[
        "Life Expectancy"
    ].iloc[0]

    profile_latest = profile_data[
        "Life Expectancy"
    ].iloc[-1]

    profile_change = (
        profile_latest -
        profile_first
    )

    profile_highest = profile_data[
        "Life Expectancy"
    ].max()

    profile_lowest = profile_data[
        "Life Expectancy"
    ].min()

    profile_highest_year = profile_data.loc[
        profile_data["Life Expectancy"].idxmax(),
        "Year"
    ]

    profile_lowest_year = profile_data.loc[
        profile_data["Life Expectancy"].idxmin(),
        "Year"
    ]


    p1, p2, p3, p4 = st.columns(4)

    with p1:

        st.metric(
            "First Available",
            f"{profile_first:.1f} years"
        )

    with p2:

        st.metric(
            "Latest Available",
            f"{profile_latest:.1f} years"
        )

    with p3:

        st.metric(
            "Change",
            f"{profile_change:+.1f} years"
        )

    with p4:

        st.metric(
            "Highest",
            f"{profile_highest:.1f} years"
        )


    st.write(
        f"**Highest:** {profile_highest:.1f} years "
        f"({int(profile_highest_year)})"
    )

    st.write(
        f"**Lowest:** {profile_lowest:.1f} years "
        f"({int(profile_lowest_year)})"
    )


    profile_fig = px.line(
        profile_data,
        x="Year",
        y="Life Expectancy",
        markers=True,
        title=(
            f"Life Expectancy History — "
            f"{profile_country}"
        ),
        labels={
            "Life Expectancy":
                "Life Expectancy (years)"
        }
    )

    st.plotly_chart(
        profile_fig,
        use_container_width=True
    )


# =========================================================
# KEY FINDING
# =========================================================

st.divider()

st.header("💡 Key Finding")

if not map_data.empty:

    difference = (
        highest_country["Life Expectancy"]
        -
        lowest_country["Life Expectancy"]
    )

    st.write(
        f"In **{map_year}**, the difference between "
        f"the country with the highest and lowest "
        f"life expectancy was approximately "
        f"**{difference:.1f} years**."
    )

    st.write(
        f"**{highest_country['Country']}** had the highest "
        f"life expectancy at "
        f"**{highest_country['Life Expectancy']:.1f} years**, "
        f"while **{lowest_country['Country']}** had the "
        f"lowest at "
        f"**{lowest_country['Life Expectancy']:.1f} years**."
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

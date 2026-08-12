# =========================================================
# SECTION 3 — COMPARE COUNTRIES
# =========================================================

st.divider()

st.header("📊 Compare Countries")

st.write(
    "Choose a year, select a variable, and compare three countries."
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
# FIND COUNTRIES AVAILABLE FOR SELECTED YEAR
# =========================================================

# Life expectancy
life_available = df[
    df["Year"] == comparison_year
].dropna(
    subset=["Country", "Life Expectancy"]
)

life_countries = set(
    life_available["Country"]
)


# GDP
if gdp_column is not None:

    gdp_available = gdp_df[
        gdp_df["Year"] == comparison_year
    ].copy()

    gdp_available = gdp_available.dropna(
        subset=["Country", gdp_column]
    )

    gdp_countries = set(
        gdp_available["Country"]
    )

else:

    gdp_countries = set()


# Health expenditure
health_available = health_df[
    health_df["Year"] == comparison_year
].copy()

health_available = health_available.dropna(
    subset=["Country", "Health Expenditure"]
)

health_countries = set(
    health_available["Country"]
)


# Population
if population_column is not None:

    population_available = df[
        df["Year"] == comparison_year
    ].dropna(
        subset=["Country", population_column]
    )

    population_countries = set(
        population_available["Country"]
    )

else:

    population_countries = set()


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
# COUNTRIES AVAILABLE BASED ON CHOICE
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
# CHECK DATA
# =========================================================

if len(available_countries) < 3:

    st.warning(
        f"There are fewer than 3 countries with "
        f"{comparison_choice.lower()} data available "
        f"for {comparison_year}."
    )

    st.stop()


# =========================================================
# SELECT 3 COUNTRIES
# =========================================================

st.subheader("🌎 Select Three Countries")

country_col1, country_col2, country_col3 = st.columns(3)


with country_col1:

    country_1 = st.selectbox(
        "Country 1",
        available_countries,
        index=0,
        key="country_1"
    )


with country_col2:

    # Remove Country 1
    country_2_options = [
        country
        for country in available_countries
        if country != country_1
    ]

    country_2 = st.selectbox(
        "Country 2",
        country_2_options,
        index=0,
        key="country_2"
    )


with country_col3:

    # Remove Country 1 and Country 2
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
        key="country_3"
    )


selected_countries = [
    country_1,
    country_2,
    country_3
]


# =========================================================
# PREPARE COMPARISON DATA
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
# DISPLAY SELECTED DATA
# =========================================================

if comparison_choice in comparison_df.columns:

    chart_data = comparison_df[
        [
            "Country",
            comparison_choice
        ]
    ].copy()

    chart_data = chart_data.dropna()


    # =====================================================
    # BAR CHART
    # =====================================================

    fig_comparison = px.bar(
        chart_data,
        x="Country",
        y=comparison_choice,
        title=(
            f"{comparison_choice} Comparison — "
            f"{comparison_year}"
        ),
        labels={
            comparison_choice:
                comparison_choice
        }
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

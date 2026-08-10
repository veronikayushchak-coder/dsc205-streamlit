import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

URL = 'https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/CT-towns-income-census-2020.csv'
df = pd.read_csv(URL)

df['Per capita income'] = df['Per capita income'].str.replace('$', '').str.replace(',', '').astype(int)
df['Median household income'] = df['Median household income'].str.replace('$', '').str.replace(',', '').astype(int)
df['Median family income'] = df['Median family income'].str.replace('$', '').str.replace(',', '').astype(int)

st.title('Connecticut Town Income Census 2020')

st.markdown(
    'This dataset contains census and income information for cities and towns '
    'in Connecticut. Use the controls below to explore income differences '
    'across Connecticut counties and communities.'
)

#1. Select a county
st.subheader('Cities and Towns by County')

county = st.selectbox('Select a county', sorted(df['County'].unique()))
county_df = df[df['County'] == county]

st.dataframe(county_df, width=800, height=200)

#2. Income range slider
st.subheader('Cities and Towns by Median Household Income')

min_income = int(df['Median household income'].min())
max_income = int(df['Median household income'].max())

income_range = st.slider(
    'Select a household income range',
    min_value=min_income,
    max_value=max_income,
    value=(min_income, max_income),
    step=1000
)

income_df = df[
    (df['Median household income'] >= income_range[0]) &
    (df['Median household income'] <= income_range[1])
]

st.dataframe(
    income_df,
    width=800,
    height=200
)


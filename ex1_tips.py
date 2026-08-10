import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

URL = ('https://raw.githubusercontent.com/iantonios/'
       'dsc205/refs/heads/main/tips.csv')

df = pd.read_csv(URL)

st.title('Restaurant Tips')

st.markdown(
    'This dataset contains information about restaurant bills and tips.'
    'It can be used to explore the relationship between the amount of the bill and the tip given.'
)

st.subheader('The data')

st.dataframe(df, width=700, height=250)

st.write(f'{len(df)} meals are recorded in this dataset.')

st.write(df[['total_bill', 'tip']].describe())

st.subheader('Distribution of the total bill')

fig, ax = plt.subplots()

ax.hist(df['total_bill'], bins=20)

ax.set_xlabel('Total bill ($)')
ax.set_ylabel('Number of meals')

st.pyplot(fig, clear_figure=True)

st.subheader('Bill size vs. tip')

fig2, ax2 = plt.subplots()

ax2.scatter(df['total_bill'], df['tip'], s=12)

ax2.set_xlabel('Total bill ($)')
ax2.set_ylabel('Tip ($)')

st.pyplot(fig2, clear_figure=True)

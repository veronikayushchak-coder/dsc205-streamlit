import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Diabetes Patient Data')
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

st.markdown('---')
st.subheader('Glucose levels by diabetes status')

status = st.radio('Select patient group', ('Diabetic', 'Non-diabetic'))

if status == 'Diabetic':
    df = df.loc[df['Outcome'] == 1]
else:
    df = df.loc[df['Outcome'] == 0]

fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel('Glucose')
ax.set_ylabel('Number of patients')
ax.hist(df['Glucose'], bins=15)
st.pyplot(fig)

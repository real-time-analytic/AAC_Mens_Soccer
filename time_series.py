# import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import streamlit as st 
import altair as alt


# allow user to choose team
teams = ['UNCC', 'SMU', 'FIU', 'Memphis', 'USF', 'FAU', 'Temple', 'Tulsa']
team = st.selectbox('Select a soccer team from the 2023 American Athletic Conference:', teams)


# import dataset
data = pd.read_excel('AAC_Data_copy.xlsx',sheet_name=team)


# create offensive dataset
data = data[(data['Offense/Defense'] == 'offense') & (data['Accuracy'] == 'goal')]


# ensure date column is datetime object
data['Date'] = pd.to_datetime(data['Date']) 


# set up variables to choose from
variables = ['Goals','Avg passes']

# create a selectbox
variable = st.selectbox('Select a variable:',variables)

# prep data based on chosen variable
if variable == 'Goals':
    data = data.groupby(['Date','Location of Shot'])['Location of Shot'].count().reset_index(name='Goals')
elif variable == 'Avg passes':
    data = data.groupby(['Date','# of Passes in Play']).mean().reset_index(name='Avg passes')
else:
    pass 

# create checkbox for user to choose specific zone
# zones_choose = [1,2,3,4,5]
# st.checkbox('Choose a zone or zones:',zones_choose)

# create altair chart
chart = alt.Chart(data).mark_line().encode(
    x = 'Date:T',
    y = alt.Y(variable,title=f'{variable}', scale=alt.Scale(zero=True),
    axis=alt.Axis(format='d')),
    color = 'Location of Shot:N'
)

st.altair_chart(chart) 













# # group by date and perform metric
# total_shots_df = data.groupby("Date")["Opponents"].count().reset_index()
# avg_pass_df = data.groupby("Date")["# of Passes in Play"].mean().reset_index()






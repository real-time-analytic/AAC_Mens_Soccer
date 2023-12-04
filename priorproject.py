# import libraries
import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import random

# create title
st.header('**American Athletic Conference**')

# allow user to choose a team on sidebar to assess performance of that team
st.sidebar.header('**User Input Features**')
teams = ['UNCC','SMU','FIU','Memphis','USF','FAU','Temple','Tulsa']
team = st.sidebar.radio('Team:', teams)
st.write('Team:',team) 

# create path and pandas dataframe for choosen team
path = '/Users/triston/Desktop/Code/streamlit_project/AAC_Data.xlsx'
df = pd.read_excel(path,sheet_name=team)

st.write(f'{team} dataset',df)
# create sidebar for opponent
opponent = st.sidebar.selectbox('Select Opponent:',df['Opponents'].unique())
# st.write('Opponent:',opponent)  

# create chosen team and chosen opponent dataframe
data = df[df['Opponents'] == opponent]

# st.write(f'{team} vs {opponent} dataset',data)

# import libraries to create soccer field
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from matplotlib.patches import Rectangle

# title for soccer field
st.write(f'{team} vs {opponent}')



























# create soccer field object
pitch = Pitch(pitch_type='statsbomb',
              pitch_color='grass',line_color='#fffffc',
              goal_type='box')

fig, ax = pitch.draw(figsize=(10,7))

# create loop that displays soccer zones on field only when a team dataset has a shot in that zone
for index, row in data.iterrows():
    zones = []  # Initialize zones for each row

    # Check conditions and add appropriate zone dictionaries to the zones list
    if row['Offense/Defense'] == 'offense' and row['Location of Shot'] == 1: # zone 1 offense
        zones.append({'xy': (114, 30), 'width': 6, 'height': 20, 'color': 'red'})
    elif row['Offense/Defense'] == 'offense' and row['Location of Shot'] == 2: # zone 2 offense
        zones.append({'xy': (108, 30), 'width': 6, 'height': 20, 'color': 'blue'})
    elif row['Offense/Defense'] == 'offense' and row['Location of Shot'] == 3: # zone 3 offense
        zones.append({'xy': (102, 30), 'width': 6, 'height': 20, 'color': 'orange'})
    elif row['Offense/Defense'] == 'offense' and row['Location of Shot'] == 4: # zone 4 offense
        zones.append({'xy': (102, 18), 'width': 18, 'height': 12, 'color': 'magenta'})
        zones.append({'xy': (102, 50), 'width': 18, 'height': 12, 'color': 'magenta'})
    elif row['Offense/Defense'] == 'offense' and row['Location of Shot'] == 5: # zone 5 offense
        zones.append({'xy': (95, 12), 'width': 25, 'height': 6, 'color': 'cyan'})
        zones.append({'xy': (95, 62), 'width': 25, 'height': 6, 'color': 'cyan'})
        zones.append({'xy': (95, 18), 'width': 7, 'height': 44, 'color': 'cyan'})
    elif row['Offense/Defense'] == 'defense' and row['Location of Shot'] == 1: # zone 1 defense
        zones.append({'xy': (0, 30), 'width': 6, 'height': 20, 'color': 'red'}),
    elif row['Offense/Defense'] == 'defense' and row['Location of Shot'] == 2: # zone 2 defense
        zones.append({'xy': (6, 30), 'width': 6, 'height': 20, 'color': 'blue'}),
    elif row['Offense/Defense'] == 'defense' and row['Location of Shot'] == 3: # zone 3 defense
        zones.append({'xy': (12, 30), 'width': 6, 'height': 20, 'color': 'orange'}),
    elif row['Offense/Defense'] == 'defense' and row['Location of Shot'] == 4: # zone 4 deffense
        zones.append({'xy': (0, 18), 'width': 18, 'height': 12, 'color': 'magenta'})
        zones.append({'xy': (0, 50), 'width': 18, 'height': 12, 'color': 'magenta'})
    elif row['Offense/Defense'] == 'defense' and row['Location of Shot'] == 5: # zone 5 defense
        zones.append({'xy': (0, 12), 'width': 25, 'height': 6, 'color': 'cyan'}) 
        zones.append({'xy': (0, 62), 'width': 25, 'height': 6, 'color': 'cyan'})
        zones.append({'xy': (18, 18), 'width': 7, 'height':44, 'color': 'cyan'}) 
    for zone in zones:
        rect = Rectangle(zone['xy'], zone['width'], zone['height'], linewidth=1, edgecolor='none', facecolor=zone['color'], alpha=0.25)
        ax.add_patch(rect)

# Display the plot in Streamlit
st.pyplot(fig)

# match shot statistics variables
o_shots_on_target = len(data[(data['Opponents']==f'{opponent}') & 
                         (data['Offense/Defense'] == 'offense') &
                          (data['Accuracy'] == 'on')])
o_shots_off_target = len(data[(data['Opponents'] == f'{opponent}') &
                          (data['Offense/Defense'] == 'offense') &
                           (data['Accuracy'] == 'off')])
o_goals = len(data[(data['Opponents'] == f'{opponent}') &
               (data['Offense/Defense'] == 'offense') &
               (data['Accuracy'] == 'goal')])

o_shots_total = o_shots_on_target + o_shots_off_target + o_goals

o_accuracy = str(round(((o_shots_on_target + o_goals) / o_shots_total * 100),1)) + '%' 

o_shooting_perc = str(round((o_goals/o_shots_total*100),1)) + '%'

d_shots_on_target = len(data[(data['Opponents']==f'{opponent}') & 
                         (data['Offense/Defense'] == 'defense') &
                          (data['Accuracy'] == 'on')])
d_shots_off_target = len(data[(data['Opponents']==f'{opponent}') & 
                         (data['Offense/Defense'] == 'defense') &
                          (data['Accuracy'] == 'on')])
d_goals = len(data[(data['Opponents']==f'{opponent}') & 
                         (data['Offense/Defense'] == 'defense') &
                          (data['Accuracy'] == 'on')])
d_shots_total = d_shots_on_target + d_shots_off_target + d_goals

d_accuracy = str(round(((d_shots_on_target + d_goals) / d_shots_total * 100),1)) +'%'

d_shooting_perc = str(round((d_goals/d_shots_total * 100),1)) + '%'

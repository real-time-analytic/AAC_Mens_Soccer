# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import math 
from mplsoccer.pitch import Pitch
from matplotlib.patches import Rectangle

# Header title
st.header("**I made a change 2023 American Athletic Conference: Men's Soccer**")

# Allow user to choose team
teams = ['UNCC', 'SMU', 'FIU', 'Memphis', 'USF', 'FAU', 'Temple', 'Tulsa']
team = st.selectbox('Select a soccer team from the 2023 American Athletic Conference', teams, key='team_general')

# Import dataset for chosen team
path = 'AAC_Data_copy.xlsx'
data = pd.read_excel(path, sheet_name=team)

# Create tabs
tab1, tab2, tab3 = st.tabs(["**Offense Analysis**", "**Defense Analysis**","**Match Analysis**"]) 



# Tab 1: Offense Analysis
with tab1:    

    # import dataset for chosen team
    path = 'AAC_Data_copy.xlsx'
    data = pd.read_excel(path,sheet_name=team)


    # create soccer field object
    pitch = Pitch(pitch_type='statsbomb',
              pitch_color='grass',line_color='#fffffc',
              goal_type='box')
    fig, ax = pitch.draw(figsize=(10,7))


    # create df where chosen team is on offense and scores goal
    data = data[(data['Offense/Defense']=='offense') & (data['Accuracy']=='goal')]
    # st.write(data)


    # get a count of the number of goals scored in each zone
    zone1 = 0
    zone2 = 0
    zone3 = 0
    zone4 = 0
    zone5 = 0

    for index, row in data.iterrows():
        location = row['Location of Shot']
        if location == 1:
            zone1 += 1
        elif location == 2:
            zone2 += 1
        elif location == 3:
            zone3 += 1
        elif location == 4:
            zone4 += 1
        elif location == 5:
            zone5 += 1


    # create header for field visualization
    st.subheader(f'Zones where {team} scores most:')


    # normalize goals for each zone (specifically from 0.1 to 1 for alpha)
    max_goals = max(zone1, zone2, zone3, zone4, zone5)
    power_factor = 2

    zone1_norm = (zone1 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    zone2_norm = (zone2 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    zone3_norm = (zone3 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    zone4_norm = (zone4 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    zone5_norm = (zone5 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 


    # initialize alpha for each row
    for index, row in data.iterrows():
        zones = []  
        
        # Mapping normalized values to the alpha parameter
        if row['Location of Shot'] == 1: # zone 1 offense
            alpha = zone1_norm
        elif row['Location of Shot'] == 2: # zone 2 offense
            alpha = zone2_norm
        elif row['Location of Shot'] == 3: # zone 3 offense
            alpha = zone3_norm
        elif row['Location of Shot'] == 4: # zone 4 offense
            alpha = zone4_norm
        elif row['Location of Shot'] == 5: # zone 5 offense
            alpha = zone5_norm
        else:
            continue  # Skip if the location of shot is not recognized

        # Now add the appropriate zones with the determined alpha value
        if row['Location of Shot'] == 1: # zone 1 offense
            zones.append({'xy': (114, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 2: # zone 2 offense
            zones.append({'xy': (108, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 3: # zone 3 offense
            zones.append({'xy': (102, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 4: # zone 4 offense
            zones.append({'xy': (102, 18), 'width': 18, 'height': 12, 'color': 'crimson','alpha':alpha})
            zones.append({'xy': (102, 50), 'width': 18, 'height': 12, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 5: # zone 5 offense
            zones.append({'xy': (95, 12), 'width': 25, 'height': 6, 'color': 'crimson','alpha':alpha})
            zones.append({'xy': (95, 62), 'width': 25, 'height': 6, 'color': 'crimson','alpha':alpha})
            zones.append({'xy': (95, 18), 'width': 7, 'height': 44, 'color': 'crimson','alpha':alpha})


        # Add the rectangles to the plot
        for zone in zones:
            rect = Rectangle(zone['xy'], zone['width'], zone['height'], 
                            linewidth=1, edgecolor='none', facecolor=zone['color'], 
                            alpha=zone['alpha'])
            ax.add_patch(rect)

    # Display the plot in Streamlit
    st.pyplot(fig)


    # create a chart to show goals in zones
    total_goals = zone1 + zone2 + zone3 + zone4 + zone5
    zones_df = pd.DataFrame({
        'Zone': ['zone 1','zone 2','zone 3','zone 4','zone 5'],
        'Value': [zone1,zone2,zone3,zone4,zone5]})
    # st.write(zones_df)


    # create bar chart to show goals scored in each zone
    chart = alt.Chart(zones_df,title='Goals per Zone').mark_bar().encode(
        y = alt.Y('Zone'),
        x = alt.X('Value',axis = alt.Axis(format='d'),title='Count'),
        color = alt.value('crimson')
        ).configure_title(
            anchor='middle'
        )

    st.altair_chart(chart, use_container_width=True) 




with tab2:

    # import dataset for chosen team
    path = 'AAC_Data_copy.xlsx'
    data = pd.read_excel(path,sheet_name=team)


    # create soccer field object
    pitch = Pitch(pitch_type='statsbomb',
                pitch_color='grass',line_color='#fffffc',
                goal_type='box')
    fig, ax = pitch.draw(figsize=(10,7))


    # create df where chosen team is on defense and scores goal
    data = data[(data['Offense/Defense']=='defense') & (data['Accuracy']=='goal')]
    # st.write(data)


    # get a count of the number of goals scored in each zone
    zone1 = 0
    zone2 = 0
    zone3 = 0
    zone4 = 0
    zone5 = 0

    for index, row in data.iterrows():
        location = row['Location of Shot']
        if location == 1:
            zone1 += 1
        elif location == 2:
            zone2 += 1
        elif location == 3:
            zone3 += 1
        elif location == 4:
            zone4 += 1
        elif location == 5:
            zone5 += 1


    # create header for field visualization
    st.subheader(f'Zones where {team} is scored on most:')


    # normalize goals for each zone (specifically from 0.1 to 1 for alpha)
    max_goals = max(zone1, zone2, zone3, zone4, zone5)
    power_factor = 2

    zone1_norm = (zone1 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    zone2_norm = (zone2 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    zone3_norm = (zone3 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    zone4_norm = (zone4 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    zone5_norm = (zone5 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 


    # initialize alpha for each row
    for index, row in data.iterrows():
        zones = []  
        
        # Mapping normalized values to the alpha parameter
        if row['Location of Shot'] == 1: # zone 1 offense
            alpha = zone1_norm
        elif row['Location of Shot'] == 2: # zone 2 offense
            alpha = zone2_norm
        elif row['Location of Shot'] == 3: # zone 3 offense
            alpha = zone3_norm
        elif row['Location of Shot'] == 4: # zone 4 offense
            alpha = zone4_norm
        elif row['Location of Shot'] == 5: # zone 5 offense
            alpha = zone5_norm
        else:
            continue  # Skip if the location of shot is not recognized

        # Now add the appropriate zones with the determined alpha value
        if row['Location of Shot'] == 1: # zone 1 offense
            zones.append({'xy': (0, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 2: # zone 2 offense
            zones.append({'xy': (6, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 3: # zone 3 offense
            zones.append({'xy': (12, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 4: # zone 4 offense
            zones.append({'xy': (0, 18), 'width': 18, 'height': 12, 'color': 'crimson','alpha':alpha})
            zones.append({'xy': (0, 50), 'width': 18, 'height': 12, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 5: # zone 5 offense
            zones.append({'xy': (0, 12), 'width': 25, 'height': 6, 'color': 'crimson','alpha':alpha})
            zones.append({'xy': (0, 62), 'width': 25, 'height': 6, 'color': 'crimson','alpha':alpha})
            zones.append({'xy': (18, 18), 'width': 7, 'height': 44, 'color': 'crimson','alpha':alpha})


        # Add the rectangles to the plot
        for zone in zones:
            rect = Rectangle(zone['xy'], zone['width'], zone['height'], 
                            linewidth=1, edgecolor='none', facecolor=zone['color'], 
                            alpha=zone['alpha'])
            ax.add_patch(rect)

    # Display the plot in Streamlit
    st.pyplot(fig)


    # create a chart to show goals in zones
    total_goals = zone1 + zone2 + zone3 + zone4 + zone5
    zones_df = pd.DataFrame({
        'Zone': ['zone 1','zone 2','zone 3','zone 4','zone 5'],
        'Value': [zone1,zone2,zone3,zone4,zone5]})
    # st.write(zones_df)


    # create bar chart to show goals scored in each zone
    chart = alt.Chart(zones_df,title='Goals per Zone').mark_bar().encode(
        y = alt.Y('Zone'),
        x = alt.X('Value',axis = alt.Axis(format='d'),title='Count'),
        color = alt.value('crimson')
        ).configure_title(
            anchor='middle'
        )

    st.altair_chart(chart, use_container_width=True) 


with tab3:
    # import libraries
    import streamlit as st
    import pandas as pd
    import numpy as np
    import altair as alt
    import matplotlib.pyplot as plt
    import math 
    from mplsoccer.pitch import Pitch
    from matplotlib.patches import Rectangle


    # Import dataset for chosen team
    path = 'AAC_Data_copy.xlsx'
    df = pd.read_excel(path, sheet_name=team)


    # create sidebar for opponent
    opponent = st.selectbox('Select Opponent:',df['Opponents'].unique())


    # create chosen team and chosen opponent dataframe
    data = df[df['Opponents'] == opponent]


    # selected team vs opponent dataframe: 
    # st.write(data[data['Accuracy']=='goal'])


    # offensive dataset where instances only show goals
    o_data = data[(data['Offense/Defense']=='offense') & (data['Accuracy']=='goal')]


    # create soccer field object
    pitch = Pitch(pitch_type='statsbomb',
        pitch_color='grass',line_color='#fffffc',
        goal_type='box')
    fig, ax = pitch.draw(figsize=(10,7))


    # SELECTED TEAM GOALS
    # get a count of the number of goals scored in each zone
    o_zone1 = 0 
    o_zone2 = 0
    o_zone3 = 0
    o_zone4 = 0
    o_zone5 = 0

    for index, row in o_data.iterrows():
        location = row['Location of Shot']
    if location == 1:
        o_zone1 += 1
    elif location == 2:
        o_zone2 += 1
    elif location == 3:
        o_zone3 += 1
    elif location == 4:
        o_zone4 += 1
    elif location == 5:
        o_zone5 += 1


    # create header for field visualization
    st.markdown(f"<h3 style='text-align: center;'><span style='margin-right: 10px;'>{team}</span> vs <span style='margin-left: 10px;'>{opponent}</h3>", unsafe_allow_html=True)



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

    if o_shots_total > 0:
        o_accuracy = str(round(((o_shots_on_target + o_goals) / o_shots_total * 100),1)) + '%' 
        o_shooting_perc = str(round((o_goals/o_shots_total*100),1)) + '%'
    else: 
        o_accuracy = 'N/A'
        o_shooting_perc = 'N/A'


    d_shots_on_target = len(data[(data['Opponents']==f'{opponent}') & 
                        (data['Offense/Defense'] == 'defense') &
                        (data['Accuracy'] == 'on')])
    d_shots_off_target = len(data[(data['Opponents']==f'{opponent}') & 
                        (data['Offense/Defense'] == 'defense') &
                        (data['Accuracy'] == 'off')])
    d_goals = len(data[(data['Opponents']==f'{opponent}') & 
                        (data['Offense/Defense'] == 'defense') &
                        (data['Accuracy'] == 'goal')])
    d_shots_total = d_shots_on_target + d_shots_off_target + d_goals

    if d_shots_total > 0:
        d_accuracy = str(round(((d_shots_on_target + d_goals) / d_shots_total * 100),1)) +'%'
        d_shooting_perc = str(round((d_goals/d_shots_total * 100),1)) + '%'
    else:
        d_accuracy = 'N/A'
        d_shooting_perc = 'N/A'


    # show match score (color=black)
    st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 24px;'>{o_goals} - {d_goals}</p>", unsafe_allow_html=True)

    # match score (color=crimson red)
    #st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 24px; color: crimson;'>{o_goals} - {d_goals}</p>", unsafe_allow_html=True)



    # normalize goals for each zone (specifically from 0.1 to 1 for alpha)
    max_goals = max(o_zone1, o_zone2, o_zone3, o_zone4, o_zone5)
    power_factor = 2

    o_zone1_norm = (o_zone1 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    o_zone2_norm = (o_zone2 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    o_zone3_norm = (o_zone3 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    o_zone4_norm = (o_zone4 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    o_zone5_norm = (o_zone5 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 


    # initialize alpha for each row
    for index, row in o_data.iterrows():
        o_zones = []  

        # Mapping normalized values to the alpha parameter
        if row['Location of Shot'] == 1: # zone 1 offense
            alpha = o_zone1_norm
        elif row['Location of Shot'] == 2: # zone 2 offense
            alpha = o_zone2_norm
        elif row['Location of Shot'] == 3: # zone 3 offense
            alpha = o_zone3_norm
        elif row['Location of Shot'] == 4: # zone 4 offense
            alpha = o_zone4_norm
        elif row['Location of Shot'] == 5: # zone 5 offense
            alpha = o_zone5_norm
        else:
            continue  # skip if the location of shot is not present

        # Now add the appropriate zones with the determined alpha value
        if row['Location of Shot'] == 1: # zone 1 offense
            o_zones.append({'xy': (114, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 2: # zone 2 offense
            o_zones.append({'xy': (108, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 3: # zone 3 offense
            o_zones.append({'xy': (102, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 4: # zone 4 offense
            o_zones.append({'xy': (102, 18), 'width': 18, 'height': 12, 'color': 'crimson','alpha':alpha})
            o_zones.append({'xy': (102, 50), 'width': 18, 'height': 12, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 5: # zone 5 offense
            o_zones.append({'xy': (95, 12), 'width': 25, 'height': 6, 'color': 'crimson','alpha':alpha})
            o_zones.append({'xy': (95, 62), 'width': 25, 'height': 6, 'color': 'crimson','alpha':alpha})
            o_zones.append({'xy': (95, 18), 'width': 7, 'height': 44, 'color': 'crimson','alpha':alpha})


        # Add the rectangles to the plot
        for zone in o_zones:
            rect = Rectangle(zone['xy'], zone['width'], zone['height'], 
                        linewidth=1, edgecolor='none', facecolor=zone['color'], 
                        alpha=zone['alpha'])
        ax.add_patch(rect)



    # SELECTED OPPONENT GOALS
    # defensive dataset where instances only show goals
    d_data = data[(data['Offense/Defense']=='defense') & (data['Accuracy']=='goal')]


    # SELECTED team goals
    # get a count of the number of goals scored in each zone by opponent
    d_zone1 = 0 
    d_zone2 = 0
    d_zone3 = 0
    d_zone4 = 0
    d_zone5 = 0

    for index, row in d_data.iterrows():
        location = row['Location of Shot']
        if location == 1:
            d_zone1 += 1
        elif location == 2:
            d_zone2 += 1
        elif location == 3:
            d_zone3 += 1
        elif location == 4:
            d_zone4 += 1
        elif location == 5:
            d_zone5 += 1


    # normalize goals for each zone (specifically from 0.1 to 1 for alpha)
    max_goals = max(d_zone1, d_zone2,d_zone3, d_zone4, d_zone5)
    power_factor = 2

    d_zone1_norm = (d_zone1 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    d_zone2_norm = (d_zone2 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    d_zone3_norm = (d_zone3 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    d_zone4_norm = (d_zone4 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 
    d_zone5_norm = (d_zone5 / max_goals * 0.7) ** power_factor if max_goals > 0 else 0 


    # initialize alpha for each row
    for index, row in d_data.iterrows():
        d_zones = []  

        # Mapping normalized values to the alpha parameter
        if row['Location of Shot'] == 1: # zone 1 offense
            alpha = d_zone1_norm
        elif row['Location of Shot'] == 2: # zone 2 offense
            alpha = d_zone2_norm
        elif row['Location of Shot'] == 3: # zone 3 offense
            alpha = d_zone3_norm
        elif row['Location of Shot'] == 4: # zone 4 offense
            alpha = d_zone4_norm
        elif row['Location of Shot'] == 5: # zone 5 offense
            alpha = d_zone5_norm
        else:
            continue  # skip if the location of shot is not found

        # Now add the appropriate zones with the determined alpha value
        if row['Location of Shot'] == 1: # zone 1 offense
            d_zones.append({'xy': (0, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 2: # zone 2 offense
            d_zones.append({'xy': (6, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 3: # zone 3 offense
            d_zones.append({'xy': (12, 30), 'width': 6, 'height': 20, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 4: # zone 4 offense
            d_zones.append({'xy': (0, 18), 'width': 18, 'height': 12, 'color': 'crimson','alpha':alpha})
            d_zones.append({'xy': (0, 50), 'width': 18, 'height': 12, 'color': 'crimson','alpha':alpha})
        elif row['Location of Shot'] == 5: # zone 5 offense
            d_zones.append({'xy': (0, 12), 'width': 25, 'height': 6, 'color': 'crimson','alpha':alpha})
            d_zones.append({'xy': (0, 62), 'width': 25, 'height': 6, 'color': 'crimson','alpha':alpha})
            d_zones.append({'xy': (18, 18), 'width': 7, 'height': 44, 'color': 'crimson','alpha':alpha})


        # Add the rectangles to the plot
        for zone in d_zones:
            rect = Rectangle(zone['xy'], zone['width'], zone['height'], 
                        linewidth=1, edgecolor='none', facecolor=zone['color'], 
                        alpha=zone['alpha'])
        ax.add_patch(rect)


    # Display the plot in Streamlit
    st.pyplot(fig)


    # title for match statistics
    st.markdown("<p style='text-align: center; font-size: 16px; font-weight: bold;'>Match Statistics</p>", unsafe_allow_html=True)


    # create dataframe for match statistics
    match_stats = {
    team:[o_goals,o_shots_total,o_accuracy],
    opponent:[d_goals,d_shots_total,d_accuracy]

    }

    # remove default index column from chart
    df_match_stats = pd.DataFrame(match_stats, index=['Goals', 'Total shots', 'Shooting accuracy'])


    # write table to streamlit
    st.table(df_match_stats)





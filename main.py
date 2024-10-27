import streamlit as st
import pandas as pd
import matplotlib as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os 

# App title with logo
st.markdown(
    """
    <style>
    .header {
        display: flex;
        align-items: center;
    }
    .logo {
        width: 150px;  /* Adjust size as needed */
        margin-right: 10px;
        position: absolute;
        top: -35px;  /* Adjust to move further up */
        left: -225px; /* Adjust to move further left */
    }
    </style>
    <div class="header">
        <img src="https://pplx-res.cloudinary.com/image/upload/v1730065622/user_uploads/jevfesveg/Panther-Head.jpg" class="logo">
        <h1 style='text-align: center; margin-bottom: 30px;'>Pitt Softball 2024 Fall Performance Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)


# creat a data frame and replace 'nan'with empty strings
df = pd.read_excel((r'C:\Users\xostech\Downloads\fall_numbers.xlsx'))


st.markdown("<h2 style='text-align: center;'>Team Quadrant Report</h2>", unsafe_allow_html=True)

# calculate mean and standard deviation for bat speed and exit velo
x_mean = df['BAT SPEED'].mean()
y_mean = df['AVG VELO'].mean()
x_std = df['BAT SPEED'].std()
y_std = df['AVG VELO'].std()

# create scatter plot 
fig = px.scatter(df, x ='BAT SPEED', y ="AVG VELO", hover_name='NAME', text='NAME')


# Create scatter plot with increased dot size
fig = px.scatter(df, x='BAT SPEED', y='AVG VELO', hover_name='NAME', text='NAME',
                 size_max=10,  # Increase max size for dots
                 size=[5] * len(df))  # Set a uniform size

# shade quadrants using one standard deviation
fig.add_shape(type="rect", x0=x_mean-x_std, x1=x_mean, y0=y_mean, y1=y_mean+y_std,
              fillcolor="Yellow", opacity=.2, layer="below")
fig.add_shape(type="rect", x0=x_mean, x1=x_mean+x_std, y0=y_mean, y1=y_mean+y_std,
              fillcolor="LightGreen", opacity=.2, layer="below")
fig.add_shape(type="rect", x0=x_mean-x_std, x1=x_mean, y0=y_mean-y_std, y1=y_mean,
              fillcolor="Red", opacity=.2, layer="below")
fig.add_shape(type="rect", x0=x_mean, x1=x_mean+x_std, y0=y_mean-y_std, y1=y_mean,
              fillcolor="LightCoral", opacity=.2, layer="below")


# add quadrant lines based on means
fig.add_hline(y=y_mean, line_dash="dash", line_color="blue")
fig.add_vline(x=x_mean,line_dash="dash", line_color="blue")

# Update layout 
fig.update_layout(
    title={
        'text': "Evit Velocity vs Bat Speed",
        'x': 0.5,
        'xanchor': 'center'
    },

    xaxis_title="Bat Speed",
    yaxis_title="Exit Velocity(AVG Velo)",
    xaxis=dict(range=[df['BAT SPEED'].min() * 0.9, df['BAT SPEED'].max() * 1.1]),

    annotations=[
        dict(x=.15, y=1, xref="paper", yref="paper", text="High Exit Velo, Low Bat Speed",
             showarrow=False),
        dict(x=.95, y=1, xref="paper", yref="paper", text= "High Exit Velo, High Bat Speed",
             showarrow=False),
        dict(x=.15, y=.05, xref="paper", yref="paper", text= "Low Exit Velo, Low Bat Speed",
             showarrow=False),
        dict(x=.95, y=.05, xref="paper", yref="paper", text= "Low Exit Velo, High Bat Speed",
             showarrow=False)
    ]
)

# Center the intersection of the lines
fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="blue")
fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="blue")

# Display the plot 
st.plotly_chart(fig)

# Search bar for player names
player_name = st.text_input("Search for a player to see their quadrant:")

if player_name:
    player_data = df[df['NAME'].str.contains(player_name, case=False)]
    
    if not player_data.empty:
        for _, row in player_data.iterrows():
            bat_speed = row['BAT SPEED']
            avg_velo = row['AVG VELO']
            quadrant = ""

            if bat_speed > x_mean and avg_velo > y_mean:
                quadrant = "High Exit Velo, High Bat Speed"
            elif bat_speed > x_mean and avg_velo <= y_mean:
                quadrant = "Low Exit Velo, High Bat Speed"
            elif bat_speed <= x_mean and avg_velo > y_mean:
                quadrant = "High Exit Velo, Low Bat Speed"
            else:
                quadrant = "Low Exit Velo, Low Bat Speed"

            st.write(f"{row['NAME']} is in the '{quadrant}' quadrant.")
    else:
        st.write("Player not found.")

# Center the data table using columns
st.markdown("<h2 style='text-align: center;'>Hitter Performance Metrics</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
     st.dataframe(df, width=2000, height=600)  # Adjust width and height as needed


# create third subheader
st.markdown("<h2 style='text-align: center;'>Individual Player Profiles</h2>", unsafe_allow_html=True)

# create second dataframe and fill the 'nan' values with empty strings
df2= pd.read_excel((r'C:\Users\xostech\Downloads\Fall IPP DOC.xlsx'))
df2.fillna('', inplace=True)

# directory storing headshots
image_dir = r'C:\Users\Xostech\Desktop'

# create a grid layout
cols = st.columns([1,1,1])

# create a button for each player + player details
for index, row in df2.iterrows():
     player_buttons = f"{row['Jersey Number:']} - {row['First Name:']}_{row['Last Name:']}.jpg"
     image_path = os.path.join(image_dir, player_buttons)


     # determine which column to place the player profiles in 
     col_index = index % len(cols)
     with cols[col_index]:
          if os.path.exists(image_path):
               st.image(image_path)

          if st.button(f"{row['Jersey Number:']} - {row['First Name:']} {row['Last Name:']}"):
               st.write(f"Year: {row['Year:']}")
               st.write(f"Position: {row['Position:']}")
               st.write(f"Hometown: {row['Hometown:']}")

               # Create Performance Metrics Expander
               with st.expander("Perfomance Metrics"):
                     st.write(f"Exit Velo Tee, FT, Live: {row['Exit Velo Tee']}, {row['Exit Velo FT']}, {row['Exit Live Velo']}")
                     st.write(f"Max Push Ups: {row['Pushups']}")
                     st.write(f" Airdyne: {row['Bike Test']}")
                     st.write(f"300 YD Shuttles: {row['300 YD']}")
                     st.write(f"7 Innings Conditioning: {row['7 INNINGS']}")
                     st.write(f"Trap Bar Deadlift: {row['TRAP BAR']}")
                     st.write(f"Front Squat: {row['FRONT SQUAT']}")
                     st.write(f"Trap Bar Jump: {row['TRAP JUMP']}")
                     st.write(f"Pro Agility Shuttle: {row['5.10.5']}")
                     st.write(f"20 YD Shuttle: {row['20 YARD']}")
                     st.write(f"Max Pull Ups: {row['PULLUPS']}")
                     st.write(f"4 Min Plank: {row['PLANK']}")
               
               # create ares of improvement expander
               with st.expander("Areas of Improvement"):
                    st.write(f"Mental Skills: {row['Mental Skills:']}")
                    st.write(f"Techniques/Exercises: {row['Techniques/ Exercises:']}")
                    st.write(f"Defense: {row['Defense:']}")
                    st.write(f"Offense: {row['Offense:']}")
                    st.write(f"S & C: {row['Strength and Conditioning:']}")
                    st.write(f"Tactical Skills: {row['Tactical Skills To Develop:']}")
               
               # create a specific plan 
               with st.expander("Performance Plan"):
                    st.write(f"Hitting Prep A: {row['Hitting Prep A']}")
                    st.write(f"Hitting Prep B: {row['Hitting Prep B']}")
                    st.write(f"Recovery Protocols: {row['Recovery Protocols:']}")
               







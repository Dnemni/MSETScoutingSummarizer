import numpy as np
import pandas as pd
import streamlit as st
import datetime

st.set_page_config(
    page_title="MSET Scouting Data Visualizer",
    page_icon=":chart:",  # You can use any emoji as an icon
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("MSET Scouting Data Visualizer")

# Set theme
theme = {
    "backgroundColor": "#afc9f7",
    "secondaryBackgroundColor": "#8f98ea",
    "textColor": "#000000",
}

st.markdown(
    """
    <style>
        body {
            background-color: %(backgroundColor)s;
        }
        .secondaryBackgroundColor {
            background-color: %(secondaryBackgroundColor)s;
        }
        .markdown-text-container {
            color: %(textColor)s;
        }
    </style>
    """ % theme,
    unsafe_allow_html=True,
)



#Input
st.sidebar.title("Select Team")

class SideBarSetup:
    def bar(self):
        st.sidebar.header("----------")
    
    def tmnumIN(self, a):
        with st.sidebar:
            t = st.text_input("Team Number", "649", key = "teamname " + str(a), placeholder = "649")
        return t


rawData = pd.read_csv("scoutData.csv")
pitData = pd.read_csv("pitData.csv")

# List the desired column order
desired_columns = ['scoutName', 'teamNumber', 'matchNumber', 'allianceColor'] + [col for col in rawData.columns if col not in ['scoutName', 'teamNumber', 'matchNumber', 'allianceColor']]

# Reorder the columns of the DataFrame
appData = rawData[desired_columns]


# Add teams dynamically
teams_info = []
sblist = []
sb0 = SideBarSetup()
tm0 = sb0.tmnumIN(0)
teams_info.append(tm0)
sblist.append(sb0)
x = 1

if 'buttonClick' not in st.session_state:
    st.session_state.buttonClick = 0

#buttonClick = 0
if st.button("Add Team", type="primary", key=f"add_team_{x}"):
    st.session_state.buttonClick += 1

tab1, tab2, tab3 = st.tabs(["App Scouting", "Paper Scouting", "Pit Scouting"])

for i in range (st.session_state.buttonClick):
    globals()["sb" + str(x)] = SideBarSetup()
    globals()["sb" + str(x)].bar()
    globals()["tm" + str(x)] = globals()["sb" + str(x)].tmnumIN(x)
    teams_info.append(globals()["tm" + str(x)])
    sblist.append(globals()["sb" + str(x)])
    x += 1

with tab1:
    st.header("App Scouting")
    # Display charts for each team
    for idx, tm in enumerate(teams_info):
        if tm == 0:
            st.dataframe(appData)
        else:
            st.write("Team " + str(tm) + " Data")
            filtered_data = appData[appData['teamNumber'] == int(tm)]
            st.dataframe(filtered_data)

with tab2:
    st.header("Paper Scouting")
    for idx, tm in enumerate(teams_info):
        st.write("Team " + str(tm) + " Paper")

with tab3:
    st.header("Pit Scouting")
    for idx, tm in enumerate(teams_info):
        if tm == 0:
            st.dataframe(pitData)
        else:
            st.write("Team " + str(tm) + " Pit")
            filtered_data2 = pitData[pitData['Team Number'] == int(tm)]
            st.dataframe(filtered_data2)
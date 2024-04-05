import numpy as np
import pandas as pd
import streamlit as st
import datetime
import re
import PyPDF2

st.set_page_config(
    page_title="MSET Scouting Summarizer",
    page_icon="🖨",  # You can use any emoji as an icon
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("MSET Scouting Summarizer")

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

def extract_team_info(pdf_text, team_name):
    # Define the pattern to search for the team name
    pattern = re.compile(f"{re.escape(team_name)}.*?\\b\\d+\\s+[A-Z]", re.DOTALL)
    
    # Search for the team name in the PDF text
    match = pattern.search(pdf_text)
    if match:
        # Extract the matched text
        team_info = match.group(0)
        return team_info
    else:
        return None

def read_pdf_file(file_path):
    # Open the PDF file in binary mode
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize an empty string to store text from all pages
        pdf_text = ""
        
        # Loop through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
        
    return pdf_text



#Input
st.sidebar.title("Select Team")
st.sidebar.write("Use 0 to see all data")

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
        if int(tm) == 0:
            st.dataframe(appData)
        else:
            st.write("Team " + str(tm) + " Data")
            filtered_data = appData[appData['teamNumber'] == int(tm)]
            st.dataframe(filtered_data)

with tab2:
    st.header("Paper Scouting")
    for idx, tm in enumerate(teams_info):
        st.write("Team " + str(tm) + " Paper")
    
    # Example usage
    file_path = 'paperData.pdf'
    team_name = "100"

    # Read the PDF file
    pdf_text = read_pdf_file(file_path)

    # Extract team information
    team_info = extract_team_info(pdf_text, team_name)

    if team_info:
        print("Team information found:")
        print(team_info)
    else:
        print(f"Team '{team_name}' not found in the document.")

with tab3:
    st.header("Pit Scouting")
    for idx, tm in enumerate(teams_info):
        if int(tm) == 0:
            st.dataframe(pitData)
        else:
            st.write("Team " + str(tm) + " Pit")
            filtered_data2 = pitData[pitData['Team Number'] == int(tm)]
            st.dataframe(filtered_data2)
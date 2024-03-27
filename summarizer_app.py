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


def basicTeamBoxPlot(tmevscr):
    #Charts
    df = pd.DataFrame([(event, score) for event, scores in tmevscr.items() for score in scores], columns=['Event', 'Points Scored'])

    boxplot = alt.Chart(df).mark_boxplot(extent="min-max", size = 50).encode(
        alt.X("Event:N", axis=alt.Axis(labels=True, ticks=True, domain=True, grid=True, domainColor="white", gridColor="white", labelColor="black", tickColor="white", titleColor="black")),
        alt.Y("Points Scored:Q", axis=alt.Axis(labels=True, ticks=True, domain=True, grid=True, domainColor="white", gridColor="white", labelColor="black", tickColor="white", titleColor="black")).scale(zero=False),
        alt.Color("Event:N").legend(None),
        ).properties(
            width=400,
            height=300
        ).configure_title(
            fontSize=16,
            anchor='start'
        )
    # Display the boxplot
    st.altair_chart(boxplot, use_container_width=True)
    
    
def individualTeamScatterPlot(scores_data):
    
    for event, scores in scores_data.items():
        st.write("Event: ", event)
        min_length = min(len(scores[0]), len(scores[1]))
    
        matchnames, alliances = getEventAlliances(tm, tmy, event)
        # Prepare data for scatter plot
        data = pd.DataFrame({
          'Match': range(1, min_length + 1),
          'Actual Score': scores[0][:min_length],
          'Predicted Score': scores[1][:min_length],
          'Match Name': matchnames,
          'Alliance': alliances
        })
        
        # Create scatter plot
        #data = pd.DataFrame({'Match': range(1, len(scores) + 1), 'Points Scored': scores})

        scatter_plot_1 = alt.Chart(data).mark_circle(size=60).encode(
            alt.X("Match:N", axis=alt.Axis(labels=True, ticks=True, domain=True, grid=True, domainColor="white", gridColor="white", labelColor="black", tickColor="white", titleColor="black")),
            alt.Y("Actual Score:Q", axis=alt.Axis(labels=True, ticks=True, domain=True, grid=True, domainColor="white", gridColor="white", labelColor="black", tickColor="white", titleColor="black")).scale(zero=False),
            color = alt.value("blue"),
            tooltip = ['Match', 'Match Name', 'Actual Score', 'Alliance'] 
            #alt.Color("variable:N", legend=alt.Legend(title="Score Type")),
            ).properties(
                width=200,
                height=300
            )#.configure_legend(
             #   orient='right'
            #)
        
        scatter_plot_2 = alt.Chart(data).mark_circle(size=60).encode(
            alt.X("Match:N", axis=alt.Axis(labels=True, ticks=True, domain=True, grid=True, domainColor="white", gridColor="white", labelColor="black", tickColor="white", titleColor="black")),
            alt.Y("Predicted Score:Q", axis=alt.Axis(labels=True, ticks=True, domain=True, grid=True, domainColor="white", gridColor="white", labelColor="black", tickColor="white", titleColor="black")).scale(zero=False),
            color = alt.value("orange"),
            tooltip = ['Match', 'Match Name', 'Predicted Score', 'Alliance'] 
            #alt.Color("variable:N", legend=alt.Legend(title="Score Type")),
            ).properties(
                width=200,
                height=300
            )
            #.configure_legend(
            #    orient='right'
            #)

        # Combine scatter plot and line of best fit
        #line_of_fit = scatter_plot.transform_regression('Match','Points Scored').mark_line()
        
        combined_chart = scatter_plot_2 + scatter_plot_1

        # Display the chart
        st.altair_chart(combined_chart, use_container_width=True)
        #st.altair_chart(scatter_plot_2, use_container_width=True)


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

tab1, tab2, tab3 = st.tabs(["Plots", "Awards"])

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
        st.write("Team " + str(tm) + " Data")

with tab2:
    st.header("Paper Scouting")
    for idx, tm in enumerate(teams_info):
        st.write("Team " + str(tm) + " Paper:")

with tab3:
    st.header("Pit Scouting")
    for idx, tm in enumerate(teams_info):
        st.write("Team " + str(tm) + " Pit:")
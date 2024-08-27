import streamlit as st
import os
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# --- PAGE SETUP ---
suspension_page = st.Page(
    "views/suspension.py",
    title="Suspension App",
    icon=":material/settings:",
    default=True,
)
battery_page = st.Page(
    "views/battery.py",
    title="Battery App",
    icon=":material/settings:",
)
powertrain_page = st.Page(
    "views/powertrain.py",
    title="PowerTrain App",
    icon=":material/settings:",
)
lowvoltage_page = st.Page(
    "views/lowvoltage.py",
    title="Low Voltage App",
    icon=":material/person:",
)
finance_page = st.Page(
    "views/finance.py",
    title="Finance App",
    icon=":material/agriculture:",
)


# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Formula Student Strathmore APP": [lowvoltage_page,battery_page,finance_page,powertrain_page,suspension_page],
    }
)

# --- SHARED ON ALL PAGES ---
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, 'assets', 'logo.png')
image_path_2 = os.path.join(current_dir, 'assets', 'logo.png')
st.logo(image_path)  
#st.image(image_path_2, width=100)# Adjust the width as needed
st.sidebar.markdown("Made with Prescision")

pg.run()
    
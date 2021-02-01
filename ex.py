import streamlit as st
from pages import pag1, pag2, pag3, pag4, pag5

import pandas as pd
import numpy as np
import folium

import streamlit as st
from streamlit_folium import folium_static
import folium




PAGES = {
    "Introduction on the data": pag4,
    "Maps over inspections": pag1,
    "Data over the time": pag3,
    "Top & Flop Restaurants": pag2,
    "Insert your insepection text and make predictions": pag5,
    
}
st.sidebar.title('Menu')
selection = st.sidebar.radio("Click on", list(PAGES.keys()))
page = PAGES[selection]
page.app()
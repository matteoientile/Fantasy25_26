import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output

st.title("📊 Fantacalcio 25/26 - Asta Statistica")

st.markdown("""
È il momento di **svoltare** la tua asta! 

Smettila di scorrere listoni interminabili, consumare decine di video pieni di bias ed opinioni personali: **qui parlano i numeri**

Use the sidebar to explore:
- 🧤 Goalkeepers  
- 🛡️ Defenders  
- ⚽ Midfielders  
- 🎯 Forwards  

Each page contains interactive visualizations with tooltips and a search option to highlight players.
""")

st.sidebar.success("Select a demo above.")





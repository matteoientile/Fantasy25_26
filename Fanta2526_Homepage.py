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
Welcome to the **Fantacalcio Analysis App**!

Use the sidebar to explore:
- 🧤 Goalkeepers  
- 🛡️ Defenders  
- ⚽ Midfielders  
- 🎯 Forwards  

Each page contains interactive visualizations with tooltips and a search option to highlight players.
""")

st.sidebar.success("Select a demo above.")





import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Fantacalcio 25/26 - Tutte le statistiche")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    In questa App troverai tutto il necessario per fare l'asta perfetta
"""
)

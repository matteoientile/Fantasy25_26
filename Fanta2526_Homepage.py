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

Smettila di scorrere listoni interminabili, consumare decine di video pieni di bias ed opinioni personali: **qui parlano i numeri**.

**Non capisci nulla di statistica?** --> Non c'è problema, per ogni grafico avrai di fianco la spiegazione, sulla base della quale potrai prendere le tue scelte in fase d'asta!

Tramite la barra a lato avrai a disposizione le più importanti informazioni su 
- 🧤 Portieri  
- 🛡️ Difensori  
- ⚽ Centrocampisti  
- 🎯 Attaccanti

relative alle 3 precedenti stagioni di Serie A. 

""")

st.sidebar.success("Scegli il Ruolo")





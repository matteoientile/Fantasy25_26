#--------------- PACKAGES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

#---------------- READ FILES + BASIC EDITS
df2022 = pd.read_excel(r"C:\Users\MATTEO IENTILE\Desktop\Fantacalcio 25-26\2022_23_Merged.xlsx")
df2023 = pd.read_excel(r"C:\Users\MATTEO IENTILE\Desktop\Fantacalcio 25-26\2023_24_Merged.xlsx")
df2024 = pd.read_excel(r"C:\Users\MATTEO IENTILE\Desktop\Fantacalcio 25-26\2024_25_Merged.xlsx")
drop_columns = ["Id", "id", "goals", "assists", "yellow_cards", "red_cards", "matched"]
df2022 = df2022.drop(drop_columns, axis=1)
df2023 = df2023.drop(drop_columns, axis=1)
df2024 = df2024.drop(drop_columns, axis=1)

df2022["xBonus"] = (3*df2022["xG"] + 1*df2022["xA"] + 3*df2022["Rp"]) - (2*df2022["Au"]+ 1*df2022["Gs"] + 1*df2022["Esp"] + 0.5*df2022["Amm"] + df2022["R-"])
df2022["actualBonus"] = (3*df2022["Gf"] + 1*df2022["Ass"] + 3*df2022["Rp"]) - (2*df2022["Au"]+ 1*df2022["Gs"] + 1*df2022["Esp"] + 0.5*df2022["Amm"]+ df2022["R-"])
df2022["xG + xA (pts converted)"] = (3*df2022["xG"] + 1*df2022["xA"])
df2022["G + A (pts converted)"] = (3*df2022["Gf"] + 1*df2022["Ass"])

df2023["xBonus"] = (3*df2023["xG"] + 1*df2023["xA"] + 3*df2023["Rp"]) - (2*df2023["Au"]+ 1*df2023["Gs"] + 1*df2023["Esp"] + 0.5*df2023["Amm"] + df2023["R-"])
df2023["actualBonus"] = (3*df2023["Gf"] + 1*df2023["Ass"] + 3*df2023["Rp"]) - (2*df2023["Au"]+ 1*df2023["Gs"] + 1*df2023["Esp"] + 0.5*df2023["Amm"] + df2023["R-"])
df2023["xG + xA (pts converted)"] = (3*df2023["xG"] + 1*df2023["xA"])
df2023["G + A (pts converted)"] = (3*df2023["Gf"] + 1*df2023["Ass"])


df2024["xBonus"] = (3*df2024["xG"] + 1*df2024["xA"] + 3*df2024["Rp"]) - (2*df2024["Au"]+ 1*df2024["Gs"] + 1*df2024["Esp"] + 0.5*df2024["Amm"] + df2024["R-"])
df2024["actualBonus"] = (3*df2024["Gf"] + 1*df2024["Ass"] + 3*df2024["Rp"]) - (2*df2024["Au"]+ 1*df2024["Gs"] + 1*df2024["Esp"] + 0.5*df2024["Amm"] + df2024["R-"])
df2024["xG + xA (pts converted)"] = (3*df2024["xG"] + 1*df2024["xA"])
df2024["G + A (pts converted)"] = (3*df2024["Gf"] + 1*df2024["Ass"])

df2022 = df2022[df2022["Pv"] > 0]
df2023 = df2023[df2023["Pv"] > 0]
df2024 = df2024[df2024["Pv"] > 0]

gk2022 = df2022[df2022["R"] == "P"]
def2022 = df2022[df2022["R"] == "D"]
mid2022 = df2022[df2022["R"] == "C"]
stk2022 = df2022[df2022["R"] == "A"]

gk2023 = df2023[df2023["R"] == "P"]
def2023 = df2023[df2023["R"] == "D"]
mid2023 = df2023[df2023["R"] == "C"]
stk2023 = df2023[df2023["R"] == "A"]

gk2024 = df2024[df2024["R"] == "P"]
def2024 = df2024[df2024["R"] == "D"]
mid2024 = df2024[df2024["R"] == "C"]
stk2024 = df2024[df2024["R"] == "A"]
#------------------------- GOALKEEPERS ANALYSIS
#-------- Box Plots

fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("2022", "2023", "2024"),
    horizontal_spacing=0.15
)

# --- 2022 ---
box2022 = px.box(
    gk2022[gk2022["Pv"]>1], #x="Squadra", 
    y="Mv", points="all",
    hover_data=["Nome", "Pv"]
)
for trace in box2022.data:
    fig.add_trace(trace, row=1, col=1)

# --- 2023 ---
box2023 = px.box(
    gk2023[gk2023["Pv"]>1], #x="Squadra", 
    y="Mv", points="all",
    hover_data=["Nome", "Pv"]
)
for trace in box2023.data:
    fig.add_trace(trace, row=1, col=2)

# --- 2024 ---
box2024 = px.box(
    gk2024[gk2024["Pv"]>1], #x="Squadra", 
    y="Mv", points="all",
    hover_data=["Nome", "Pv"]
)
for trace in box2024.data:
    fig.add_trace(trace, row=1, col=3)

fig.update_layout(
    height=600, width=1200,
    title="Media Voto 2022 to 2024 (GK)",
    showlegend=False
)

fig.show()



























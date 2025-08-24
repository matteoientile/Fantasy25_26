import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

#---------------- STREAMLIT HEADER
st.title("🛡️ Difensori - Analisi Statistica")
st.markdown("""
In questa sezione analizziamo le performance dei difensori nelle ultime 3 stagioni di Serie A.

Utilizzeremo i seguenti simboli:
- Mv = Media Voto
- Fm = Fanta Media
- x
- Pv = Partite a Voto
""")

#---------------- READ FILES
df2022 = pd.read_excel("2022_23_Merged.xlsx")
df2023 = pd.read_excel("2023_24_Merged.xlsx")
df2024 = pd.read_excel("2024_25_Merged.xlsx")

drop_columns = ["Id", "id", "goals", "assists", "yellow_cards", "red_cards", "matched"]
df2022 = df2022.drop(drop_columns, axis=1)
df2023 = df2023.drop(drop_columns, axis=1)
df2024 = df2024.drop(drop_columns, axis=1)

df2022["xBonus"] = (3*df2022["xG"] + 1*df2022["xA"] + 3*df2022["Rp"] + 1*df2022["clean_sheet"]) - (2*df2022["Au"]+ 1*df2022["Gs"] + 1*df2022["Esp"] + 0.5*df2022["Amm"] + df2022["R-"])
df2022["actualBonus"] = (3*df2022["Gf"] + 1*df2022["Ass"] + 3*df2022["Rp"] + 1*df2022["clean_sheet"]) - (2*df2022["Au"]+ 1*df2022["Gs"] + 1*df2022["Esp"] + 0.5*df2022["Amm"]+ df2022["R-"])
df2022["xG + xA (pts converted)"] = (3*df2022["xG"] + 1*df2022["xA"])
df2022["G + A (pts converted)"] = (3*df2022["Gf"] + 1*df2022["Ass"])

df2023["xBonus"] = (3*df2023["xG"] + 1*df2023["xA"] + 3*df2023["Rp"] + 1*df2023["clean_sheet"]) - (2*df2023["Au"]+ 1*df2023["Gs"] + 1*df2023["Esp"] + 0.5*df2023["Amm"] + df2023["R-"])
df2023["actualBonus"] = (3*df2023["Gf"] + 1*df2023["Ass"] + 3*df2023["Rp"] + 1*df2023["clean_sheet"]) - (2*df2023["Au"]+ 1*df2023["Gs"] + 1*df2023["Esp"] + 0.5*df2023["Amm"] + df2023["R-"])
df2023["xG + xA (pts converted)"] = (3*df2023["xG"] + 1*df2023["xA"])
df2023["G + A (pts converted)"] = (3*df2023["Gf"] + 1*df2023["Ass"])

df2024["xBonus"] = (3*df2024["xG"] + 1*df2024["xA"] + 3*df2024["Rp"]+ 1*df2024["clean_sheet"]) - (2*df2024["Au"]+ 1*df2024["Gs"] + 1*df2024["Esp"] + 0.5*df2024["Amm"] + df2024["R-"])
df2024["actualBonus"] = (3*df2024["Gf"] + 1*df2024["Ass"] + 3*df2024["Rp"] + 1*df2024["clean_sheet"]) - (2*df2024["Au"]+ 1*df2024["Gs"] + 1*df2024["Esp"] + 0.5*df2024["Amm"] + df2024["R-"])
df2024["xG + xA (pts converted)"] = (3*df2024["xG"] + 1*df2024["xA"])
df2024["G + A (pts converted)"] = (3*df2024["Gf"] + 1*df2024["Ass"])

#------------------------- PV FILTER
min_pv = st.slider("Numero minimo di partite a voto (Pv)", min_value=1, max_value=int(df2024["Pv"].max()), value=1)

df2022 = df2022[df2022["Pv"] >= min_pv]
df2023 = df2023[df2023["Pv"] >= min_pv]
df2024 = df2024[df2024["Pv"] >= min_pv]

def2022 = df2022[df2022["R"] == "D"]
def2023 = df2023[df2023["R"] == "D"]
def2024 = df2024[df2024["R"] == "D"]

#------------------------- MULTI SEARCH BOX
all_names = pd.concat([def2022["Nome"], def2023["Nome"], def2024["Nome"]]).unique()
search_names = st.multiselect("Seleziona uno o più portieri da evidenziare", options=sorted(all_names), default=[])

# Palette e simboli
colors = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Dark24
symbols = ["circle", "square", "diamond", "star", "cross", "x", "triangle-up", "triangle-down"]

#========================= SECTION 1: BOX PLOTS =========================
st.header("📊 Boxplot Difensori")

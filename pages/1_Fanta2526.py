# pages/Fanta2526_GK.py
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

#---------------- STREAMLIT HEADER
st.title("🧤 Portieri - Analisi Statistica")
st.markdown("""
In questa sezione analizziamo le performance dei portieri nelle ultime 3 stagioni di Serie A.
""")

#---------------- READ FILES
df2022 = pd.read_excel(r"C:\Users\MATTEO IENTILE\Desktop\Fantacalcio 25-26\2022_23_Merged.xlsx")
df2023 = pd.read_excel(r"C:\Users\MATTEO IENTILE\Desktop\Fantacalcio 25-26\2023_24_Merged.xlsx")
df2024 = pd.read_excel(r"C:\Users\MATTEO IENTILE\Desktop\Fantacalcio 25-26\2024_25_Merged.xlsx")

drop_columns = ["Id", "id", "goals", "assists", "yellow_cards", "red_cards", "matched"]
df2022 = df2022.drop(drop_columns, axis=1)
df2023 = df2023.drop(drop_columns, axis=1)
df2024 = df2024.drop(drop_columns, axis=1)

df2022 = df2022[df2022["Pv"] > 0]
df2023 = df2023[df2023["Pv"] > 0]
df2024 = df2024[df2024["Pv"] > 0]

gk2022 = df2022[df2022["R"] == "P"]
gk2023 = df2023[df2023["R"] == "P"]
gk2024 = df2024[df2024["R"] == "P"]

#------------------------- GOALKEEPERS BOX PLOTS
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("2022", "2023", "2024"),
    horizontal_spacing=0.15
)

for gk, col in zip([gk2022, gk2023, gk2024], [1, 2, 3]):
    box = px.box(
        gk[gk["Pv"] > 1],
        y="Mv", points="all",
        hover_data=["Nome", "Pv"]
    )
    for trace in box.data:
        fig.add_trace(trace, row=1, col=col)

fig.update_layout(
    height=600, width=1200,
    title="Media Voto 2022–2024 (Portieri)",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)


















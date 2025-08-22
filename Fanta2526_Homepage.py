import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# Titolo principale
st.title("📊 Fantacalcio 25/26 - Asta Statistica")

# Sidebar per navigare tra le sezioni
sezione = st.sidebar.selectbox(
    "Scegli il Ruolo",
    ["Home", "Portieri", "Difensori", "Centrocampisti", "Attaccanti"]
)

# Contenuto dinamico in base alla selezione
if sezione == "Home":
    st.markdown("""
    È il momento di **svoltare** la tua asta! 

    Smettila di scorrere listoni interminabili, consumare decine di video pieni di bias ed opinioni personali: **qui parlano i numeri**.

    **❓ Non capisci nulla di Statistica?**  
    ➡️ Nessun problema! Ogni grafico avrà una spiegazione chiara, così potrai prendere le tue decisioni in fase d'asta nel modo più rapido possibile.

    ### 🔎 Cosa troverai:

    Medie, FantaMedie, Overperformance, Underperformance e chi più ne ha più ne metta di
    - 🧤 **Portieri**  
    - 🛡️ **Difensori**  
    - ⚽ **Centrocampisti**  
    - 🎯 **Attaccanti**

    Basati sulle **ultime 3 stagioni di Serie A**.

    Per navigare tra i vari ruoli puoi usare la **barra** a lato!
    """)

elif sezione == "Portieri":
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

elif sezione == "Difensori":
    st.header("🛡️ Difensori")
    st.write("Qui troverai tutte le informazioni necessarie sui difensori")

elif sezione == "Centrocampisti":
    st.header("⚽ Centrocampisti")
    st.write("Qui troverai tutte le informazioni necessarie sui centrocampisti")

elif sezione == "Attaccanti":
    st.header("🎯 Attaccanti")
    st.write("Qui troverai tutte le informazioni necessarie sui attaccanti")






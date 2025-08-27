import streamlit as st
import pandas as pd
#---------------- STREAMLIT HEADER
st.set_page_config(page_title="Fantacalcio 25/26 - Listone & Probabili Formazioni", layout="wide") 
st.title("📋 Listone Stagione 25/26 & ⚽ Probabili Formazioni ")
st.markdown("""
Qui troverai 
- il Listone Fantagazzetta per l'asta 25/26
- i Link ai migliori siti per le Probabili Formazioni di Serie A
""")
#========================= SIDEBAR: INDEX =========================
st.sidebar.header("📌 Indice")
st.sidebar.markdown("""
- [📋 Listone Stagione 25/26](#listone-stagione-25-/-26)
- [⚽ Probabili Formazioni](#probabili-formazioni)
""")

# ========================= SEZIONE LISTONE =========================
st.header("📋 Listone Stagione 25/26")

# File excel
df_listone = pd.read_excel("Quotazioni_Fantacalcio_Stagione_2025_26.xlsx")

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    ruolo = st.selectbox("Filtra per ruolo", ["Tutti"] + sorted(df_listone["Ruolo"].unique()))

with col2:
    search_name = st.text_input("Cerca giocatore per nome:")

with col3:
    quot_range = st.slider(
        "Filtra per quotazione",
        int(df_listone["Quotazione"].min()),
        int(df_listone["Quotazione"].max()),
        (int(df_listone["Quotazione"].min()), int(df_listone["Quotazione"].max()))
    )

# Applica filtri
df_filtered = df_listone.copy()

if ruolo != "Tutti":
    df_filtered = df_filtered[df_filtered["Ruolo"] == ruolo]

if search_name:
    df_filtered = df_filtered[df_filtered["Nome"].str.contains(search_name, case=False, na=False)]

df_filtered = df_filtered[
    (df_filtered["Quotazione"] >= quot_range[0]) &
    (df_filtered["Quotazione"] <= quot_range[1])
]

# Mostra tabella
st.dataframe(
    df_filtered.sort_values(by="Quotazione", ascending=False),
    use_container_width=True
)

# Download del filtrato
st.download_button(
    label="⬇️ Scarica listone filtrato",
    data=df_filtered.to_csv(index=False).encode("utf-8"),
    file_name="listone_filtrato.csv",
    mime="text/csv"
)

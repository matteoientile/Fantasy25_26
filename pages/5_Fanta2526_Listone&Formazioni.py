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

#========================= SECTION 1: LISTONE =========================
st.header("📋 Listone Stagione 25/26")

# Carica il file (modifica il path con quello giusto)
df_listone = pd.read_excel("Quotazioni_Fantacalcio_Stagione_2025_26.xlsx")

# Filtri
ruoli = ["Tutti", "P", "D", "C", "A"]  # Portieri, Difensori, Centrocampisti, Attaccanti
ruolo_sel = st.selectbox("Filtra per Ruolo", ruoli)

if ruolo_sel != "Tutti":
    df_listone = df_listone[df_listone["R"] == ruolo_sel]

# Ricerca giocatore
search = st.text_input("🔍 Cerca un giocatore per nome")
if search:
    df_listone = df_listone[df_listone["Nome"].str.contains(search, case=False, na=False)]

# Ordinamento
sort_col = st.selectbox("Ordina per", ["Nome", "Squadra", "Qt.A", "FVM"])
ascending = st.radio("Ordine", ["Crescente", "Decrescente"]) == "Crescente"

df_listone = df_listone.sort_values(by=sort_col, ascending=ascending)

# Mostra tabella
st.dataframe(df_listone.reset_index(drop=True), use_container_width=True)

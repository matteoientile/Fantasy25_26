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
st.header("📋 Listone Stagione 25/26 (con statistiche 24/25)")

# Carica i file
df_listone = pd.read_excel("Quotazioni_Fantacalcio_Stagione_2025_26.xlsx")
df_stats = pd.read_excel("2024_25_Merged.xlsx")

# Seleziona solo le colonne utili dalle stats
cols_stats = [
    "Nome", "Mv", "Fm", "Pv", "Gf", "Ass", "Rc", "Gs", "clean_sheet"
]
df_stats = df_stats[cols_stats]

# Rinomina le colonne per chiarezza
df_stats = df_stats.rename(columns={
    "Mv": "Mv anno precedente",
    "Fm": "Fm anno precedente",
    "Pv": "Pv anno precedente",
    "Gf": "Gf anno precedente",
    "Ass": "Ass anno precedente",
    "Rc": "Rc anno precedente",
    "Gs": "Gs anno precedente",
    "clean_sheet": "clean_sheet anno precedente"
})

# Merge sul nome
df_listone = df_listone.merge(df_stats, on="Nome", how="left")

# Sostituisci NaN con "-" solo nelle colonne statistiche
stat_cols = [c for c in df_stats.columns if c != "Nome"]
df_listone[stat_cols] = df_listone[stat_cols].fillna("-")

# Filtri
ruoli = ["Tutti", "P", "D", "C", "A"]  
ruolo_sel = st.selectbox("Filtra per Ruolo", ruoli)

if ruolo_sel != "Tutti":
    df_listone = df_listone[df_listone["R"] == ruolo_sel]

# Ricerca giocatore
search = st.text_input("🔍 Cerca un giocatore per nome")
if search:
    df_listone = df_listone[df_listone["Nome"].str.contains(search, case=False, na=False)]

# Ordinamento
sort_col = st.selectbox("Ordina per", df_listone.columns)
ascending = st.radio("Ordine", ["Crescente", "Decrescente"]) == "Crescente"
df_listone = df_listone.sort_values(by=sort_col, ascending=ascending)

# Mostra tabella
st.dataframe(df_listone.reset_index(drop=True), use_container_width=True)

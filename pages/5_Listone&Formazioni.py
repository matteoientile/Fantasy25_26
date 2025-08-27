import streamlit as st
import pandas as pd
import numpy as np

#---------------- STREAMLIT HEADER
st.set_page_config(page_title="Fantacalcio 25/26 - Listone & Probabili Formazioni", layout="wide") 
st.title("📋 Listone Stagione 25/26 & ⚽ Formazioni Tipo")
st.markdown("""
Qui troverai 
- il Listone Fantagazzetta per l'asta 25/26
- i Link ai migliori siti per le Probabili Formazioni di Serie A
""")

#========================= SIDEBAR: INDEX =========================
st.sidebar.header("📌 Indice")
st.sidebar.markdown("""
- [📋 Listone Stagione 25/26](#listone-stagione-25-/-26)
- [⚽ Formazioni Tipo Serie A 2025/26](#formazioni-tipo-serie-a-25-/-26)
""")

#========================= SECTION 1: LISTONE =========================
st.header("📋 Listone Stagione 25/26 (con statistiche 24/25)")

# Carica i file
df_listone = pd.read_excel("Quotazioni_Fantacalcio_Stagione_2025_26.xlsx")
df_stats = pd.read_excel("2024_25_Merged.xlsx")

df_listone = df_listone.rename(columns={
    "Qt.A": "Quotazione Fantagazzetta",
    "FVM": "Prezzo Fantagazzetta / 500C."
})

# Aggiunta Over/Under performance
df_listone["Prezzo Fantagazzetta / 500C."] = np.ceil(df_listone["Prezzo Fantagazzetta / 500C."] / 2).astype(int)
df_stats["xG + xA (pts converted)"] = 3*df_stats["xG"] + 1*df_stats["xA"]
df_stats["G + A (pts converted)"] = 3*df_stats["Gf"] + 1*df_stats["Ass"]
df_stats["Over/Under performance %"] = np.where(
    df_stats["xG + xA (pts converted)"] > 0,
    np.round(
        100 * (df_stats["G + A (pts converted)"] - df_stats["xG + xA (pts converted)"]) / df_stats["xG + xA (pts converted)"],
        0
    ),
    np.nan
)
df_stats["Over/Under performance %"] = df_stats["Over/Under performance %"].fillna("-")

# Seleziona solo le colonne utili dalle stats
cols_stats = [
    "Nome", "Mv", "Fm", "Pv", "Gf", "Ass", "Gs", "clean_sheet", "Amm", "Esp", "Rc", "Over/Under performance %"
]
df_stats = df_stats[cols_stats]

# Rinomina le colonne per chiarezza
df_stats = df_stats.rename(columns={
    "Mv": "Media Voto (24/25) ",
    "Fm": "Fanta Media (24/25)",
    "Pv": "Partite a Voto (24/25)",
    "Gf": "Gol Fatti (24/25)",
    "Ass": "Assist (24/25)",
    "Gs": "Gol Subiti (24/25)",
    "clean_sheet": "Clean Sheet (24/25)",
    "Amm" : "Ammonizioni (24/25)",
    "Esp" : "Espulsioni (24/25)",
    "Rc": "Rigori calciati (24/25)",
    "Over/Under performance %" : "Over/Under performance [%] (24/25)"
})

# Merge sul nome
df_listone = df_listone.merge(df_stats, on="Nome", how="left")

# Sostituisci NaN con "-" solo nelle colonne statistiche
stat_cols = [c for c in df_stats.columns if c != "Nome"]
df_listone[stat_cols] = df_listone[stat_cols].fillna("-")

#========================= FILTRI =========================
# Filtra per ruolo
ruoli = ["Tutti", "P", "D", "C", "A"]  
ruolo_sel = st.selectbox("Filtra per Ruolo", ruoli)
if ruolo_sel != "Tutti":
    df_listone = df_listone[df_listone["R"] == ruolo_sel]

# Ricerca giocatore
search = st.text_input("🔍 Cerca un giocatore per nome")
if search:
    df_listone = df_listone[df_listone["Nome"].str.contains(search, case=False, na=False)]

#========================= ORDINAMENTO =========================
sort_col = st.selectbox("Ordina per", df_listone.columns)
ascending = st.radio("Ordine", ["Crescente", "Decrescente"]) == "Crescente"

# Gestione colonne con "-" per lo sort
if sort_col in stat_cols:
    # Crea colonna temporanea numerica per ordinamento
    df_listone["_sort_temp"] = pd.to_numeric(df_listone[sort_col], errors="coerce")
    df_listone = df_listone.sort_values(by="_sort_temp", ascending=ascending)
    df_listone = df_listone.drop(columns="_sort_temp")
else:
    df_listone = df_listone.sort_values(by=sort_col, ascending=ascending)

#========================= MOSTRA TABELLA =========================
st.dataframe(df_listone.reset_index(drop=True), use_container_width=True)

#========================= SECTION 2: FORMAZIONI TIPO =========================
st.header("⚽ Formazioni Tipo Serie A 2025/26")

st.markdown("""
Per consultare le formazioni tipo aggiornate squadra per squadra, visita i seguenti link:

- [Formazioni tipo Serie A 2025/26 – SOS Fanta](https://www.sosfanta.com/asta-fantacalcio/formazioni-tipo-serie-a-2025-2026-oggi-giocherebbero-cosi/)
- [Probabili formazioni Serie A 2025/26 – Fantacalcio.it](https://www.fantacalcio.it/news/calcio-italia/29_07_2025/asta-fantacalcio-le-probabili-formazioni-della-serie-a-enilive-2025-26-480206)
- [Formazioni Titolari Fantacalcio 2025/26 – Fantacalcio.it](https://www.goal.com/it/liste/fantacalcio-formazioni-titolari-serie-a-2025-2026-tutte-le-squadre-tipo/bltd96a64fe7af82a71#csfc709a336b92e528)
""")


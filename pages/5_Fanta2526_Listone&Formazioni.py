st.markdown("### 📋 Listone Stagione 25/26")

# Filtro ruolo
ruolo = st.selectbox("Seleziona ruolo:", ["Tutti", "Portiere", "Difensore", "Centrocampista", "Attaccante"])

# Ricerca nome
search_name = st.text_input("Cerca giocatore:")

df_listone = df_listone.copy()

if ruolo != "Tutti":
    df_listone = df_listone[df_listone["Ruolo"] == ruolo]

if search_name:
    df_listone = df_listone[df_listone["Nome"].str.contains(search_name, case=False, na=False)]

st.dataframe(
    df_listone.sort_values(by="Quotazione", ascending=False),
    use_container_width=True
)

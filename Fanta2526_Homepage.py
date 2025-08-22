import streamlit as st

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
    st.header("🧤 Portieri")
    st.write("Qui saranno visualizzati i grafici e le analisi dei portieri")

elif sezione == "Difensori":
    st.header("🛡️ Difensori")
    st.write("Qui saranno visualizzati i grafici e le analisi dei difensori")

elif sezione == "Centrocampisti":
    st.header("⚽ Centrocampisti")
    st.write("Qui saranno visualizzati i grafici e le analisi dei centrocampisti")

elif sezione == "Attaccanti":
    st.header("🎯 Attaccanti")
    st.write("Qui saranno visualizzati i grafici e le analisi degli attaccanti")






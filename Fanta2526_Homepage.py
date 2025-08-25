import streamlit as st
st.set_page_config(
    page_title="Fantacalcio 25/26",
    layout="wide"   # <--- this makes the app use the full browser width
)

st.title("📊 Fantacalcio 25/26 - Asta Statistica")

st.markdown("""
È il momento di **svoltare** la tua asta! 

Smettila di scorrere listoni interminabili, consumare decine di video pieni di bias ed opinioni personali: **qui parlano i numeri**.

### 🔎 Cosa troverai:
Tutte le statistiche possibili su
- 🧤 **Portieri**  
- 🛡️ **Difensori**  
- 📐 **Centrocampisti**  
- 🎯 **Attaccanti**

delle **ultime 3 stagioni di Serie A**.
""")
**❓ Non capisci nulla di statistica ❓**  
➡️ Nessun problema! Ecco come leggere i grafici:
with st.expander("🍕 Spiegazione semplice (anche se odi la statistica)"):
    st.markdown("""
    ### 🔗 Matrice di Correlazione
    - È una tabella che mostra quanto due statistiche vanno d’accordo.  
    - Vicino a **+1** → crescono insieme (più tiri = più gol).  
    - Vicino a **-1** → quando una cresce, l’altra scende.  
    - Vicino a **0** → non c’è relazione chiara.  

    ---

    ### 📦 Box Plot (medie dei giocatori)
    - Ogni “scatola” riassume come sono distribuite le **medie voto** di tutti i giocatori.  
    - La linea al centro = la media tipica dei giocatori.  
    - La scatola = dove si concentra la maggior parte dei giocatori.  
    - I puntini fuori = giocatori “speciali” (molto meglio o molto peggio della massa).  
    👉 Serve per confrontare rapidamente: ad esempio, se i centrocampisti hanno una scatola più alta dei difensori, in generale prendono voti migliori.  

    ---

    ### 🔄 Scatter Plot + Regressione
    - Ogni puntino = un giocatore.  
    - La posizione dice **come combina due statistiche** (es. tiri vs gol).  
    - La linea indica la tendenza generale: se sale → chi tira di più segna di più.  
    👉 Ti aiuta a capire se una statistica può “predire” un’altra.
    """)








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
Tantissime statistice (Calcistiche e Fantacalcistiche) su
- 🧤 **Portieri**  
- 🛡️ **Difensori**  
- 📐 **Centrocampisti**  
- 🎯 **Attaccanti**

delle **ultime 3 stagioni di Serie A**.

**❓ Non capisci nulla di statistica ❓**  
➡️ Nessun problema! Ecco come leggere i grafici:
""")

with st.expander("🔢 SPIEGAZIONE SEMPLICE (anche se odi la statistica)"):
    st.markdown("""
    ### 🔗 Matrice di Correlazione
    - È una tabella che mostra quanto due statistiche vanno d’accordo.  
    - Vicino a **+1** → crescono insieme (più tiri = più gol).  
    - Vicino a **-1** → quando una cresce, l’altra scende.  
    - Vicino a **0** → non c’è relazione chiara.  

    ---

    ### 📦 Box Plot
    - Ogni “scatola” riassume i valori di alcune statistiche dei giocatori.  
    - La linea al centro = la mediana, cioè il valore che divide i giocatori in due metà: il 50% ha un valore più basso e il 50% più alto
    - La scatola = qui dentro si concentra la maggior parte dei giocatori.  
    - I puntini fuori = giocatori “speciali” in quella statistica (molto meglio o molto peggio della massa).  
    👉 Serve per confrontare rapidamente dei giocatori su una precisa statistica (Media Voto, Fanta Media...).  

    ---

    ### 🎻 Violin Plot (medie dei giocatori)
    - È come un box plot, ma con in più la **forma** della distribuzione.  
    - La parte più larga = dove ci sono più giocatori con quel valore.  
    - La linea al centro = la mediana (il 50% dei giocatori sta sopra, il 50% sotto).  
    - Se il “violino” è molto largo in alto → tanti giocatori con voti alti.  
    - Se è largo in basso → tanti giocatori con voti bassi.  
    👉 Serve per capire **non solo i valori tipici**, ma anche **come sono distribuiti** i giocatori.

    ---
    
    ### 🔄 Scatter Plot + Regressione
    - Ogni puntino = un giocatore.  
    - La posizione dice **come combina due statistiche** (es. tiri vs gol).  
    - La linea indica la tendenza generale: se sale → chi tira di più segna di più.  
    👉 Serve per confrontare coppie di statistiche e capirne la relazione
    """)








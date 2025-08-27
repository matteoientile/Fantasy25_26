import streamlit as st
st.set_page_config(page_title="Fantacalcio 25/26", layout="wide")

st.title("📊 Fantacalcio 25/26 - Asta Statistica")

st.markdown(""" È il momento di **svoltare** la tua asta!

Smettila di scorrere listoni interminabili, consumare decine di video pieni di bias ed opinioni personali: **qui parlano i numeri**.

### 🔎 Cosa troverai:
Tantissime statistice (Calcistiche e Fantacalcistiche) su 
- 🧤 **Portieri** 
- 🛡️ **Difensori** 
- 📐 **Centrocampisti** 
- 🎯 **Attaccanti**

delle **ultime 3 stagioni di Serie A**.

**❓ Non capisci nulla di statistica ❓** ➡️ Nessun problema! Ecco come leggere i grafici: """)


with st.expander("🔢 SPIEGAZIONE SEMPLICE (anche se odi la statistica)"):
    st.markdown("""
    ### 🔗 Matrice di Correlazione
    - È una tabella che mostra quanto due statistiche vanno d’accordo.  
    - Vicino a **+1** → crescono insieme (più tiri = più gol).  
    - Vicino a **-1** → quando una cresce, l’altra scende.  
    - Vicino a **0** → non c’è relazione chiara.  

    ---

    ### 📦 Box Plot
    - Riassume i valori di una statistica tra tutti i giocatori.  
    - La **linea al centro** = la mediana → metà dei giocatori ha un valore più basso, metà più alto.  
    - La **scatola** = dove si concentra la maggior parte dei giocatori.  
    - I **puntini fuori** = giocatori “speciali” (molto meglio o molto peggio degli altri).  
    👉 Utile per confrontare rapidamente giocatori su una precisa statistica (es. Media Voto, Fanta Media).  

    ---

    ### 🎻 Violin Plot 
    - È come un box plot, ma mostra anche la **forma** della distribuzione.  
    - La parte più larga = tanti giocatori hanno quel valore.  
    - La linea al centro = la mediana (50% sotto, 50% sopra).  
    - Se il violino è largo in alto → molti con valori alti. Largo in basso → molti con valori bassi.  
    👉 Utile per scovare i migliori/peggiori giocatori per ogni statistica.  

    ---

    ### 🔄 Scatter Plot + Regressione
    - Ogni puntino = un giocatore.  
    - L’asse X rappresenta una statistica, l’asse Y un’altra.  
    - La linea indica la tendenza generale: se sale → chi ha valori più alti in X tende ad avere valori più alti anche in Y.  
    👉 Utile per confrontare due statistiche e capire se sono collegate.

    ---

    ### 🟣 Clustering + PCA
    - Il clustering raggruppa i giocatori **simili tra loro** in base a più statistiche contemporaneamente.  
    - Ogni colore = un gruppo di giocatori simili.  
    - La **PCA** trasforma tutte le statistiche in due assi sintetici (PCA1 e PCA2) per visualizzare facilmente i gruppi.  
    - Non preoccuparti di cosa siano PCA1 e PCA2: servono solo a **mostrare i giocatori in uno spazio 2D** preservando le somiglianze.  
    👉 Utile per identificare rapidamente giocatori con profili simili, scoprire “talenti nascosti” o confrontare gruppi di giocatori in modo visivo.
    """)

import streamlit as st 
st.set_page_config( page_title="Fantacalcio 25/26", layout="wide") # <--- this makes the app use the full browser width )
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


with st.expander("🔢 SPIEGAZIONE SEMPLICE (anche se odi la statistica)")
   

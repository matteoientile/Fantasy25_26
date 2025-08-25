import streamlit as st

st.set_page_config(page_title="Fantacalcio 25/26", layout="wide")  # rimosso parentesi in più
st.title("📊 Fantacalcio 25/26 - Asta Statistica")

st.markdown("È il momento di **svoltare** la tua asta!")

with st.expander("🔢 SPIEGAZIONE SEMPLICE"):
    st.markdown("""
    ### 🔗 Matrice di Correlazione
    - È una tabella che mostra quanto due statistiche vanno d’accordo.
    """)

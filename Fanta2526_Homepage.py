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
    👉 Utile per capire **quanto è diffuso un certo valore** e non solo i valori tipici.  

    ---

    ### 🔄 Scatter Plot + Regressione
    - Ogni puntino = un giocatore.  
    - L’asse X rappresenta una statistica, l’asse Y un’altra.  
    - La linea indica la tendenza generale: se sale → chi ha valori più alti in X tende ad avere valori più alti anche in Y.  
    👉 Utile per confrontare due statistiche e capire se sono collegate.
    """)

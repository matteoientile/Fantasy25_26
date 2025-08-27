import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np

#---------------- STREAMLIT HEADER
st.set_page_config(page_title="Fantacalcio 25/26 - Attaccanti", layout="wide") 
st.title("🎯 Attaccanti - Analisi Statistica")
st.markdown("""
In questa sezione analizziamo le performance degli attaccanti nelle ultime 3 stagioni di Serie A.

Utilizzeremo i seguenti simboli:
- Mv = Media Voto
- Fm = Fanta Media
- Pv = Partite a Voto
- Gf = Gol Fatti
- Ass = Assist
- xG_per90 = Expected Goals per 90 Minuti
- xA_per90 = Expected Assist per 90 Minuti
- key_passes = Passaggi Chiave
- G + A (pts converted) = Somma dei Bonus (goal = +3, assist = +1)
- Rc = Rigori Calciati
- R+ = Rigori Segnati
- Amm = Ammonizioni
- Esp = Espulsioni
""")

#========================= SIDEBAR: INDICE =========================
st.sidebar.header("📌 Indice")
st.sidebar.markdown("""
- [📊 Boxplot Attaccanti](#boxplot-attaccanti)
- [📈 Correlazioni Coppie di Variabili](#correlazioni-coppie-di-variabili)
- [📊 Confronto Radar dei Giocatori Selezionati per Stagione](#confronto-radar-dei-giocatori-selezionati-per-stagione)
- [🎯 Clustering Attaccanti](#clustering-attaccanti)
- [⚡ Altre metriche](#altre-metriche)
""")


#---------------- READ & PREPARE FILES
drop_columns = ["Id", "id", "goals", "assists", "yellow_cards", "red_cards", "matched"]

@st.cache_data
def load_and_prepare(path):
    df = pd.read_excel(path)
    df = df.drop(columns=drop_columns, errors='ignore')
    # Fill missing columns if needed
    required_cols = ["xG","xA","Rp","clean_sheet","Au","Gs","Esp","Amm","R-","Gf","Ass","shots","Rc","R+","time","games","key_passes","Pv","R","Nome","Squadra"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0
    # Feature engineering
    df["xBonus"] = (3*df["xG"] + df["xA"] + 3*df["Rp"] + df["clean_sheet"]) - (2*df["Au"] + df["Gs"] + df["Esp"] + 0.5*df["Amm"] + df["R-"])
    df["actualBonus"] = (3*df["Gf"] + df["Ass"] + 3*df["Rp"] + df["clean_sheet"]) - (2*df["Au"] + df["Gs"] + df["Esp"] + 0.5*df["Amm"] + df["R-"])
    df["xG + xA (pts converted)"] = 3*df["xG"] + df["xA"]
    df["G + A (pts converted)"] = 3*df["Gf"] + df["Ass"]
    df["% Gol/Tiri"] = np.where(df["shots"]>0, df["Gf"]/df["shots"],0)
    df["Amm a partita"] = np.where(df["Pv"]>0, df["Amm"]/df["Pv"],0)
    df["Minuti a partita"] = np.where(df["games"]>0, df["time"]/df["games"],0)
    df["Tiri a partita"] = np.where(df["games"]>0, df["shots"]/df["games"],0)
    df["key_passes a partita"] = np.where(df["games"]>0, df["key_passes"]/df["games"],0)
    df["% Rigori Segnati"] = np.where(df["Rc"]>0, df["R+"]/df["Rc"],0)
    df["Gf a partita"] = np.where(df["Pv"]>0, df["Gf"]/df["Pv"],0)
    return df

df2022 = load_and_prepare("2022_23_Merged.xlsx")
df2023 = load_and_prepare("2023_24_Merged.xlsx")
df2024 = load_and_prepare("2024_25_Merged.xlsx")

#------------------------- PV FILTER
min_pv = st.slider("Numero minimo di partite a voto (Pv)", min_value=1, max_value=int(df2024["Pv"].max()), value=1)
df2022 = df2022[df2022["Pv"] >= min_pv]
df2023 = df2023[df2023["Pv"] >= min_pv]
df2024 = df2024[df2024["Pv"] >= min_pv]

#------------------------- FILTER ATTACCANTI
stk2022 = df2022[df2022["R"]=="A"]
stk2023 = df2023[df2023["R"]=="A"]
stk2024 = df2024[df2024["R"]=="A"]

stk2022["Efficienza realizzativa (Gol)"] = np.where(stk2022["xG"]>0, stk2022["Gf"]/stk2022["xG"], 0)
stk2022["Efficienza realizzativa (Assist)"] = np.where(stk2022["xA"]>0, stk2022["Ass"]/stk2022["xA"], 0)

stk2023["Efficienza realizzativa (Gol)"] = np.where(stk2023["xG"]>0, stk2023["Gf"]/stk2023["xG"], 0)
stk2023["Efficienza realizzativa (Assist)"] = np.where(stk2023["xA"]>0, stk2023["Ass"]/stk2023["xA"], 0)

stk2024["Efficienza realizzativa (Gol)"] = np.where(stk2024["xG"]>0, stk2024["Gf"]/stk2024["xG"], 0)
stk2024["Efficienza realizzativa (Assist)"] = np.where(stk2024["xA"]>0, stk2024["Ass"]/stk2024["xA"], 0)

#------------------------- MULTI SEARCH BOX
all_names = pd.concat([stk2022["Nome"], stk2023["Nome"], stk2024["Nome"]]).unique()
search_names = st.multiselect("Seleziona uno o più attaccanti da **confrontare**", options=sorted(all_names), default=[])

colors = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Dark24
symbols = ["circle","square","diamond","star","cross","x","triangle-up","triangle-down"]

#========================= SECTION 0: CORRELATION MATRICES =========================
st.header("📊 Matrici di correlazione - Attaccanti")
corrstk = (stk2022.corr(numeric_only=True) + stk2023.corr(numeric_only=True) + stk2024.corr(numeric_only=True))/3
fig = px.imshow(corrstk, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto",
                title="MATRICE DI CORRELAZIONI MEDIA 2022-24 (ATT)")
fig.update_layout(height=800)
st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 1: BOX PLOTS =========================
st.header("📊 Boxplot Attaccanti")
metrics = ["Mv","Fm","Gf","Ass", "Efficienza realizzativa (Gol)", "Efficienza realizzativa (Assist)",
           "xG_per90","xA_per90","key_passes","G + A (pts converted)",
           "Rc","R+","% Rigori Segnati","Minuti a partita","Amm","Amm a partita"]

for metric in metrics:
    st.subheader(f"{metric} - Boxplot 2022-2024")
    fig = make_subplots(rows=1, cols=3, subplot_titles=("2022","2023","2024"), horizontal_spacing=0.15)
    def add_boxplot(fig, df, col):
        if metric not in df.columns or df.empty:
            return
        box = px.violin(df, y=metric, box=True, points="all", hover_data=["Nome","Squadra","Pv"])
        for trace in box.data:
            fig.add_trace(trace, row=1, col=col)
        # Highlight selected players
        for i, name in enumerate(search_names):
            highlight = df[df["Nome"]==name]
            if not highlight.empty:
                fig.add_trace(px.scatter(highlight, y=metric, hover_name="Nome").update_traces(
                    marker=dict(size=15,color=colors[i % len(colors)],symbol=symbols[i % len(symbols)]),
                    name=name, showlegend=True).data[0], row=1, col=col)
    add_boxplot(fig, stk2022, col=1)
    add_boxplot(fig, stk2023, col=2)
    add_boxplot(fig, stk2024, col=3)
    fig.update_layout(height=500, width=1200, title=f"{metric} - Attaccanti 2022-2024", showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 2: REGRESSION =========================
st.header("📈 Correlazioni Coppie di Variabili")
pairs = [("Mv","Fm"),("shots","Gf"),("Tiri a partita","Fm"),("Gf","Ass"),("xG","Gf"),("xA","Ass"),("Tiri a partita","Gf a partita"),("Gf","R+")]
def add_scatter(fig, df, x, y, col):
    if df.empty or x not in df.columns or y not in df.columns:
        return
    scatter = px.scatter(df, x=x, y=y, trendline="ols", hover_name="Nome", hover_data=["Squadra","Pv"])
    for trace in scatter.data:
        fig.add_trace(trace, row=1, col=col)
    for i,name in enumerate(search_names):
        highlight = df[df["Nome"]==name]
        if not highlight.empty:
            fig.add_trace(px.scatter(highlight,x=x,y=y,hover_name="Nome").update_traces(
                marker=dict(size=15,color=colors[i % len(colors)],symbol=symbols[i % len(symbols)]),
                name=name, showlegend=True).data[0], row=1, col=col)

for x,y in pairs:
    fig = make_subplots(rows=1,cols=3,subplot_titles=("2022","2023","2024"),horizontal_spacing=0.1)
    for col, df in zip([1,2,3],[stk2022,stk2023,stk2024]):
        add_scatter(fig, df, x, y, col)
    fig.update_layout(height=500, width=1600, showlegend=True, title=f"{x} vs {y} - Attaccanti 2022-2024")
    for col in [1,2,3]:
        fig.update_xaxes(title_text=x,row=1,col=col)
        fig.update_yaxes(title_text=y,row=1,col=col)
    st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 3: RADAR PLOT =========================
st.header("📊 Confronto Radar dei Giocatori Selezionati")
if search_names:
    radar_metrics = ["Pv","Mv","Fm","Gf","Ass","xG_per90","xA_per90","% Gol/Tiri","Tiri a partita","G + A (pts converted)","Gf a partita"]
    seasons = {"2022-23":stk2022,"2023-24":stk2023,"2024-25":stk2024}
    cols = st.columns(len(seasons))
    for col,(season_name, df_season) in zip(cols,seasons.items()):
        df_selected = df_season[df_season["Nome"].isin(search_names)][["Nome"]+radar_metrics].copy()
        if df_selected.empty:
            col.info(f"Nessun giocatore selezionato in {season_name}.")
            continue
        df_selected = df_selected.groupby("Nome")[radar_metrics].mean().reset_index()
        df_norm = df_selected.copy()
        for metric in radar_metrics:
            max_val = df_norm[metric].max()
            df_norm[metric] = df_norm[metric]/max_val if max_val!=0 else 0
        df_long = df_norm.melt(id_vars="Nome", value_vars=radar_metrics, var_name="Metrica", value_name="Valore")
        fig = px.line_polar(df_long, r="Valore", theta="Metrica", color="Nome", line_close=True, markers=True)
        fig.update_traces(fill='toself')
        fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,1])),showlegend=True,title=season_name)
        col.plotly_chart(fig, use_container_width=True)
else:
    st.info("Seleziona almeno un giocatore per visualizzare il radar plot.")

#========================= SECTION 4: "FASCE" CLUSTERING =========================
st.header("🎯 Clustering Attaccanti")
def KmeansPCA(df, numericalCols, nclusters, ruolo, highlight_names=None):
    df = df.copy() 
    df_filled = df[numericalCols].fillna(0)
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_filled)
    model = KMeans(n_clusters=nclusters, random_state=42)
    df["cluster"] = model.fit_predict(df_scaled).astype(str)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df_scaled)
    df["PCA1"], df["PCA2"] = pca_result[:,0], pca_result[:,1]
    vivid_colors = ["#e6194b","#3cb44b","#ffe119","#4363d8","#f58231","#911eb4","#46f0f0","#f032e6"]
    color_sequence = [vivid_colors[i % len(vivid_colors)] for i in range(nclusters)]
    fig = px.scatter(df, x="PCA1", y="PCA2", color="cluster", hover_data=["Nome","Squadra","Pv","Fm"], title=f"Cluster {ruolo}", color_discrete_sequence=color_sequence)
    if highlight_names:
        for name in highlight_names:
            highlight = df[df["Nome"]==name]
            if not highlight.empty:
                fig.add_trace(px.scatter(highlight,x="PCA1",y="PCA2",hover_name="Nome").update_traces(marker=dict(size=15,color='black',symbol='star'),name=name,showlegend=True).data[0])
    fig.update_traces(marker=dict(size=12,line=dict(width=1,color='DarkSlateGrey')))
    st.plotly_chart(fig, use_container_width=True)

numericalCols_stk = ["Pv", "Mv", "Fm", "Gf", "Ass", "Amm", "Esp", "xG", "xA", "% Gol/Tiri", "shots", "key_passes", "xGBuildup", "xGChain", "Minuti a partita"]
n_clusters = st.slider("Scegli il numero di 'raggruppamenti' (KMeans)", 2, 8, 3)

if st.button("Esegui clustering attaccanti 2024"):
    KmeansPCA(
        stk2024,                    # Last season dataframe
        numericalCols_stk,          # Your selected numeric columns
        n_clusters, 
        ruolo="Attaccanti 2024",
        highlight_names=search_names # Highlight selected players
    )

#========================= SECTION X: OTHER METRICS =========================
st.header("⚡ Altre metriche")

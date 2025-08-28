import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

#---------------- STREAMLIT HEADER
st.set_page_config(page_title="Fantacalcio 25/26 - Difensori", layout="wide") 
st.title("🛡️ Difensori - Analisi Statistica")
st.markdown("""
In questa sezione analizziamo le performance dei difensori nelle ultime 3 stagioni di Serie A.

Utilizzeremo i seguenti simboli:
- Mv = Media Voto
- Fm = Fanta Media
- Pv = Partite a Voto
- Gf = Gol Fatti
- Ass = Assist
- clean_sheet_def = Partite con 0 Gol Subiti 
- xG_per90 = Expected Goals per 90 Minuti
- xA_per90 = Expected Assist per 90 Minuti
- key_passes = Passaggi Chiave
- shots = Tiri
- G + A (pts converted) = Somma dei Bonus (goal = +3, assist = +1)
- Rc = Rigori Calciati
- R+ = Rigori Segnati
- Amm = Ammonizioni
- Esp = Espulsioni
""")

#========================= SIDEBAR: INDICE =========================
st.sidebar.header("📌 Indice")
st.sidebar.markdown("""
- [📊 Boxplot Difensori](#boxplot-difensori)
- [📈 Correlazioni Coppie di Variabili](#correlazioni-coppie-di-variabili)
- [📊 Confronto Radar dei Giocatori Selezionati per Stagione](#confronto-radar-dei-giocatori-selezionati-per-stagione)
- [🛡️ Clustering Difensori](#clustering-difensori)
- [⚡ Altre metriche](#altre-metriche)
""")

#---------------- FEATURE ENGINEERING
def add_metrics(df, season_label=None):
    df = df.copy()
    
    # Bonus
    df["xBonus"] = (3*df["xG"] + 1*df["xA"] + 3*df["Rp"] + 1*df["clean_sheet"]) - \
                   (2*df["Au"] + 1*df["Gs"] + 1*df["Esp"] + 0.5*df["Amm"] + 3*df["R-"])
    
    df["actualBonus"] = (3*df["Gf"] + 1*df["Ass"] + 3*df["Rp"] + 1*df["clean_sheet"]) - \
                        (2*df["Au"] + 1*df["Gs"] + 1*df["Esp"] + 0.5*df["Amm"] + 3*df["R-"])
    
    # Goal & assist
    df["xG + xA (pts converted)"] = 3*df["xG"] + 1*df["xA"]
    df["G + A (pts converted)"] = 3*df["Gf"] + 1*df["Ass"]
    
    # %
    df["% Gol/Tiri"] = df["Gf"] / df["shots"].replace({0: np.nan})
    
    # stats_per90
    df["Amm a partita"] = df["Amm"] / df["Pv"].replace({0: np.nan})
    df["Minuti a partita"] = df["time"] / df["Pv"].replace({0: np.nan})
    
    # Season label
    if season_label:
        df["season"] = season_label

    return df

#---------------- READ & PREPARE FILES
drop_columns = ["Id","id","goals","assists","yellow_cards","red_cards","matched"]

@st.cache_data
def load_and_prepare(path, season_label=None):
    df = pd.read_excel(path)
    df = df.drop(columns=drop_columns, errors='ignore')
    df = add_metrics(df, season_label=season_label)
    return df

df2022 = load_and_prepare("2022_23_Merged.xlsx","2022-23")
df2023 = load_and_prepare("2023_24_Merged.xlsx","2023-24")
df2024 = load_and_prepare("2024_25_Merged.xlsx","2024-25")

#------------------------- PV FILTER
min_pv = st.slider("Numero minimo di partite a voto (Pv)", min_value=1, max_value=int(df2024["Pv"].max()), value=1)

def filter_pv(df, min_pv):
    return df[df["Pv"] >= min_pv]

df2022, df2023, df2024 = filter_pv(df2022, min_pv), filter_pv(df2023, min_pv), filter_pv(df2024, min_pv)

def2022, def2023, def2024 = df2022[df2022["R"]=="D"], df2023[df2023["R"]=="D"], df2024[df2024["R"]=="D"]

# 22/23 clean sheets
cs_2022 = {
    "Atalanta": 8, "Bologna": 8, "Cremonese": 5, "Empoli": 9, "Fiorentina": 6,
    "Inter": 12, "Juventus": 19, "Lazio": 21, "Lecce": 6, "Milan": 12,
    "Monza": 10, "Napoli": 20, "Roma": 14, "Salernitana": 10, "Sampdoria": 4,
    "Sassuolo": 9, "Spezia": 6, "Torino": 11, "Udinese": 10, "Verona": 6
}

# 23/24 clean sheets
cs_2023 = {
    "Atalanta": 14, "Bologna": 17, "Cagliari": 5, "Empoli": 9, "Fiorentina": 8,
    "Frosinone": 6, "Genoa": 8, "Inter": 21, "Juventus": 16, "Lazio": 13,
    "Lecce": 7, "Milan": 12, "Monza": 12, "Napoli": 6, "Roma": 11, "Salernitana": 2,
    "Sassuolo": 3, "Torino": 18, "Udinese": 9, "Verona": 8
}

# 24/25 clean sheets
cs_2024 = {
    "Atalanta": 14, "Bologna": 12, "Cagliari": 8, "Como": 7, "Empoli": 6,
    "Fiorentina": 12, "Genoa": 10, "Inter": 16, "Juventus": 17, "Lazio": 9,
    "Lecce": 9, "Milan": 12, "Monza": 3, "Napoli": 17, "Parma": 7,
    "Roma": 17, "Torino": 10, "Udinese": 9, "Venezia": 6, "Verona": 8
}

# Map to DataFrames
def2022["clean_sheet_def"] = def2022["Squadra"].map(cs_2022)
def2023["clean_sheet_def"] = def2023["Squadra"].map(cs_2023)
def2024["clean_sheet_def"] = def2024["Squadra"].map(cs_2024)


def2022["Efficienza realizzativa (Gol)"] = np.where(def2022["xG"]>0, def2022["Gf"]/def2022["xG"], 0)
def2022["Efficienza realizzativa (Assist)"] = np.where(def2022["xA"]>0, def2022["Ass"]/def2022["xA"], 0)

def2023["Efficienza realizzativa (Gol)"] = np.where(def2023["xG"]>0, def2023["Gf"]/def2023["xG"], 0)
def2023["Efficienza realizzativa (Assist)"] = np.where(def2023["xA"]>0, def2023["Ass"]/def2023["xA"], 0)

def2024["Efficienza realizzativa (Gol)"] = np.where(def2024["xG"]>0, def2024["Gf"]/def2024["xG"], 0)
def2024["Efficienza realizzativa (Assist)"] = np.where(def2024["xA"]>0, def2024["Ass"]/def2024["xA"], 0)

#------------------------- MULTI SEARCH BOX
all_names = pd.concat([def2022["Nome"], def2023["Nome"], def2024["Nome"]]).unique()
search_names = st.multiselect("Seleziona uno o più difensori da **confrontare**", options=sorted(all_names), default=[])

colors = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Dark24
symbols = ["circle","square","diamond","star","cross","x","triangle-up","triangle-down"]

#========================= SECTION 0: CORRELATION MATRICES =========================
st.header("📊 Matrice di correlazione - Difensori")
corrdef = (def2022.corr(numeric_only=True) + def2023.corr(numeric_only=True) + def2024.corr(numeric_only=True)) / 3
fig = px.imshow(corrdef, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto", title="MATRICE DI CORRELAZIONI MEDIA 2022-24 (DEF)")
fig.update_layout(height=800)
st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 1: BOX PLOTS =========================
st.header("📊 Boxplot Difensori")
metrics = ["Mv","Fm","Gf","Ass", "Efficienza realizzativa (Gol)", "Efficienza realizzativa (Assist)","xG_per90","xA_per90", "key_passes","G + A (pts converted)",
           "Rc","R+","Minuti a partita","Amm","Amm a partita"]

def add_boxplot(fig, df, col, metric):
    box = px.violin(df, y=metric, box=True, points="all", hover_data=["Nome","Squadra","Pv"])
    for trace in box.data:
        fig.add_trace(trace, row=1, col=col)
    for i, name in enumerate(search_names):
        highlight = df[df["Nome"]==name]
        if not highlight.empty:
            fig.add_trace(px.scatter(highlight, y=metric, hover_name="Nome").update_traces(marker=dict(size=15,color=colors[i % len(colors)],symbol=symbols[i % len(symbols)]), name=name, showlegend=True).data[0], row=1, col=col)

for metric in metrics:
    st.subheader(f"{metric} - Boxplot 2022-2024")
    fig = make_subplots(rows=1, cols=3, subplot_titles=("2022","2023","2024"), horizontal_spacing=0.15)
    add_boxplot(fig, def2022, 1, metric)
    add_boxplot(fig, def2023, 2, metric)
    add_boxplot(fig, def2024, 3, metric)
    fig.update_layout(height=500,width=1200,title=f"{metric} - Difensori 2022-2024", showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 2: REGRESSION =========================
st.header("📈 Correlazioni Coppie di Variabili")

def add_scatter(fig, df, x, y, col):
    scatter = px.scatter(df, x=x, y=y, trendline="ols", hover_name="Nome", hover_data=["Squadra","Pv"])
    for trace in scatter.data:
        fig.add_trace(trace, row=1, col=col)
    for i, name in enumerate(search_names):
        highlight = df[df["Nome"]==name]
        if not highlight.empty:
            fig.add_trace(px.scatter(highlight, x=x, y=y, hover_name="Nome").update_traces(marker=dict(size=15,color=colors[i % len(colors)],symbol=symbols[i % len(symbols)]), name=name, showlegend=True).data[0], row=1, col=col)

pairs = [("Mv","Fm"),("Pv","Mv"),("clean_sheet_def","Mv"),("Tiri a partita","Fm"),("shots","Gf"),
         ("xG","Gf"),("xA","Ass"),("key_passes","xA"),("Gf","R+")]

for x,y in pairs:
    fig = make_subplots(rows=1,cols=3,subplot_titles=("2022","2023","2024"),horizontal_spacing=0.1)
    for col,df in zip([1,2,3],[def2022,def2023,def2024]):
        add_scatter(fig, df, x, y, col)
    fig.update_layout(height=500,width=1600,showlegend=True,title=f"{x} vs {y} - Difensori 2022-2024")
    fig.update_xaxes(title_text=x,row=1,col=1)
    fig.update_xaxes(title_text=x,row=1,col=2)
    fig.update_xaxes(title_text=x,row=1,col=3)
    fig.update_yaxes(title_text=y,row=1,col=1)
    fig.update_yaxes(title_text=y,row=1,col=2)
    fig.update_yaxes(title_text=y,row=1,col=3)
    st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 3: RADAR PLOT NORMALIZZATO =========================
st.header("📊 Confronto Radar dei Giocatori Selezionati per Stagione")
if search_names:
    radar_metrics = ["Pv","Mv","Fm","Gf","Ass","xG_per90","xA_per90","% Gol/Tiri","key_passes"]
    seasons = {"2022-23":def2022,"2023-24":def2023,"2024-25":def2024}
    cols = st.columns(len(seasons))
    for col,(season_name,df_season) in zip(cols,seasons.items()):
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
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1], tickfont=dict(color="black"))), showlegend=True, title=season_name)
        col.plotly_chart(fig, use_container_width=True)
else:
    st.info("Seleziona almeno un giocatore per visualizzare il radar plot.")

#========================= SECTION 4: "FASCE" CLUSTERING =========================
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

st.header("🛡️ Clustering Difensori")
numericalCols_def = ["Pv","Mv","Fm","Gf","Ass","Amm","Esp","xG","xA","% Gol/Tiri","shots","key_passes","xGBuildup","xGChain","Minuti a partita","clean_sheet_def"]
n_clusters = st.slider("Scegli il numero di 'raggruppamenti' (KMeans)", 2, 6, 3)
if st.button("Esegui clustering difensori 2024"):
    KmeansPCA(def2024, numericalCols_def, n_clusters, ruolo="Difensori 2024", highlight_names=search_names)

#========================= SECTION X: OTHER METRICS =========================
st.header("⚡ Altre metriche")

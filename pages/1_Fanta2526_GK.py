import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

#---------------- STREAMLIT HEADER
st.set_page_config(page_title="Fantacalcio 25/26 - Portieri", layout="wide") 
st.title("🧤 Portieri - Analisi Statistica")
st.markdown("""
In questa sezione analizziamo le performance dei portieri nelle ultime 3 stagioni di Serie A.

Utilizzeremo i seguenti simboli:
- Mv = Media Voto
- Fm = Fanta Media
- Gs = Gol Subiti
- Pv = Partite a Voto
- clean_sheet = Partite a Rete Inviolata
- Amm = Ammonizioni
- Esp = Espulsioni
""")

#---------------- FEATURE ENGINEERING 
def add_metrics(df, weights=None, fill_missing=True, fill_pv_zero=True, season_label=None):
    df = df.copy()
    required_cols = ["xG","xA","Rp","clean_sheet","Au","Gs","Esp","Amm","R-","Gf","Ass","Pv","Qt.I"]
    if fill_missing:
        for c in required_cols:
            if c not in df.columns:
                df[c] = 0
    for c in required_cols:
        df[c] = pd.to_numeric(df.get(c,0), errors='coerce').fillna(0)

    if weights is None:
        weights = {'g':3,'a':1,'rp':3,'cs':1,'au':2,'gs':1,'esp':1,'amm':0.5,'r-':1}

    df["xBonus"] = (weights['g']*df["xG"] + weights['a']*df["xA"] + weights['rp']*df["Rp"] + weights['cs']*df["clean_sheet"]) - (weights['au']*df["Au"] + weights['gs']*df["Gs"] + weights['esp']*df["Esp"] + weights['amm']*df["Amm"] + weights['r-']*df["R-"])
    df["actualBonus"] = (weights['g']*df["Gf"] + weights['a']*df["Ass"] + weights['rp']*df["Rp"] + weights['cs']*df["clean_sheet"]) - (weights['au']*df["Au"] + weights['gs']*df["Gs"] + weights['esp']*df["Esp"] + weights['amm']*df["Amm"] + weights['r-']*df["R-"])
    df["xG + xA (pts converted)"] = weights['g']*df["xG"] + weights['a']*df["xA"]
    df["G + A (pts converted)"] = weights['g']*df["Gf"] + weights['a']*df["Ass"]
    df["Gs a partita"] = df["Gs"] / df["Pv"].replace({0: pd.NA})
    if fill_pv_zero:
        df["Gs a partita"] = df["Gs a partita"].fillna(0)
    
    # --- ROI ---
    df["ROI"] = df["Fm"] / df["Qt.I"].replace({0: pd.NA})
    df["ROI"] = df["ROI"].fillna(0)

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

df2022, df2023, df2024 = (
    load_and_prepare("2022_23_Merged.xlsx", season_label="2022-23"),
    load_and_prepare("2023_24_Merged.xlsx", season_label="2023-24"),
    load_and_prepare("2024_25_Merged.xlsx", season_label="2024-25")
)

#------------------------- PV FILTER
min_pv = st.slider("Numero minimo di partite a voto (Pv)", min_value=1, max_value=int(df2024["Pv"].max()), value=1)

def filter_pv(df, min_pv):
    return df[df["Pv"] >= min_pv]

df2022, df2023, df2024 = filter_pv(df2022, min_pv), filter_pv(df2023, min_pv), filter_pv(df2024, min_pv)

gk2022, gk2023, gk2024 = df2022[df2022["R"]=="P"], df2023[df2023["R"]=="P"], df2024[df2024["R"]=="P"]

#------------------------- MULTI SEARCH BOX
all_names = pd.concat([gk2022["Nome"], gk2023["Nome"], gk2024["Nome"]]).unique()
search_names = st.multiselect("Seleziona uno o più portieri da **confrontare**", options=sorted(all_names), default=[])

colors = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Dark24
symbols = ["circle","square","diamond","star","cross","x","triangle-up","triangle-down"]

#========================= SECTION 0: CORRELATION MATRICES =========================
corrgk = (gk2022.corr(numeric_only=True) + gk2023.corr(numeric_only=True) + gk2024.corr(numeric_only=True)) / 3
st.header("📊 Matrice di correlazione - Portieri")
fig = px.imshow(corrgk, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto", title="MATRICE DI CORRELAZIONI MEDIA 2022-24 (POR)")
fig.update_layout(height=800)
st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 1: BOX PLOTS =========================
st.header("📊 Boxplot Portieri")

def add_boxplot(fig, df, col, metric):
    box = px.violin(df, y=metric, box=True, points="all", hover_data=["Nome","Squadra","Pv"])
    for trace in box.data:
        fig.add_trace(trace, row=1, col=col)
    for i, name in enumerate(search_names):
        highlight = df[df["Nome"]==name]
        if not highlight.empty:
            fig.add_trace(px.scatter(highlight, y=metric, hover_name="Nome").update_traces(marker=dict(size=15,color=colors[i % len(colors)],symbol=symbols[i % len(symbols)]), name=name, showlegend=True).data[0], row=1, col=col)

metrics = ["Mv","Fm","ROI","Gs","Gs a partita","clean_sheet","Amm","Esp"]
for metric in metrics:
    st.subheader(f"{metric} - Boxplot 2022-2024")
    fig = make_subplots(rows=1, cols=3, subplot_titles=("2022","2023","2024"), horizontal_spacing=0.15)
    add_boxplot(fig,gk2022,1,metric)
    add_boxplot(fig,gk2023,2,metric)
    add_boxplot(fig,gk2024,3,metric)
    fig.update_layout(height=500,width=1200,title=f"{metric} - Portieri 2022-2024", showlegend=True)
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

pairs = [("Mv","Fm","📈 Mv vs Fm - Portieri 2022-2024"), ("clean_sheet","Fm","📈 Clean Sheet vs Fm - Portieri 2022-2024"), ("Gs","Fm","📈 Gs vs Fm - Portieri 2022-2024")]

for x,y,title in pairs:
    fig = make_subplots(rows=1,cols=3,subplot_titles=("2022","2023","2024"),horizontal_spacing=0.1)
    for col,df in zip([1,2,3],[gk2022,gk2023,gk2024]):
        add_scatter(fig,df,x,y,col)
    fig.update_layout(height=500,width=1600,showlegend=True,title=title)
    fig.update_xaxes(title_text=x,row=1,col=1)
    fig.update_xaxes(title_text=x,row=1,col=2)
    fig.update_xaxes(title_text=x,row=1,col=3)
    fig.update_yaxes(title_text=y,row=1,col=1)
    fig.update_yaxes(title_text=y,row=1,col=2)
    fig.update_yaxes(title_text=y,row=1,col=3)
    st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 3: RADAR PLOT NORMALIZZATO =========================
st.header("📊 Confronto Radar dei Giocatori Selezion

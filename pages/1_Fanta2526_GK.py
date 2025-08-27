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

#---------------- FUNZIONE PER AGGIUNGERE METRICHE

def add_metrics(df, weights=None, fill_missing=True, fill_pv_zero=True, season_label=None):
    df = df.copy()
    required_cols = ["xG", "xA", "Rp", "clean_sheet", "Au", "Gs", "Esp", "Amm", "R-", "Gf", "Ass", "Pv"]
    if fill_missing:
        for c in required_cols:
            if c not in df.columns:
                df[c] = 0
    for c in required_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        else:
            df[c] = 0
    if weights is None:
        weights = {
            'g': 3, 'a': 1, 'rp': 3, 'cs': 1,
            'au': 2, 'gs': 1, 'esp': 1, 'amm': 0.5, 'r-': 1
        }
    df["xBonus"] = (
        weights['g'] * df["xG"] +
        weights['a'] * df["xA"] +
        weights['rp'] * df["Rp"] +
        weights['cs'] * df["clean_sheet"]
    ) - (
        weights['au'] * df["Au"] +
        weights['gs'] * df["Gs"] +
        weights['esp'] * df["Esp"] +
        weights['amm'] * df["Amm"] +
        weights['r-'] * df["R-"]
    )
    df["actualBonus"] = (
        weights['g'] * df["Gf"] +
        weights['a'] * df["Ass"] +
        weights['rp'] * df["Rp"] +
        weights['cs'] * df["clean_sheet"]
    ) - (
        weights['au'] * df["Au"] +
        weights['gs'] * df["Gs"] +
        weights['esp'] * df["Esp"] +
        weights['amm'] * df["Amm"] +
        weights['r-'] * df["R-"]
    )
    df["xG + xA (pts converted)"] = weights['g'] * df["xG"] + weights['a'] * df["xA"]
    df["G + A (pts converted)"] = weights['g'] * df["Gf"] + weights['a'] * df["Ass"]
    df["Gs a partita"] = df["Gs"] / df["Pv"].replace({0: pd.NA})
    if fill_pv_zero:
        df["Gs a partita"] = df["Gs a partita"].fillna(0)
    if season_label is not None:
        df["season"] = season_label
    return df

#---------------- LETTURA FILES + PREPARAZIONE

drop_columns = ["Id", "id", "goals", "assists", "yellow_cards", "red_cards", "matched"]

@st.cache_data
def load_and_prepare(path, season_label=None):
    df = pd.read_excel(path)
    df = df.drop(columns=drop_columns, errors='ignore')
    df = add_metrics(df, season_label=season_label)
    return df

df2022 = load_and_prepare("2022_23_Merged.xlsx", season_label="2022-23")
df2023 = load_and_prepare("2023_24_Merged.xlsx", season_label="2023-24")
df2024 = load_and_prepare("2024_25_Merged.xlsx", season_label="2024-25")

#------------------------- PV FILTER
min_pv = st.slider("Numero minimo di partite a voto (Pv)", min_value=1, max_value=int(df2024["Pv"].max()), value=1)

df2022 = df2022[df2022["Pv"] >= min_pv]
df2023 = df2023[df2023["Pv"] >= min_pv]
df2024 = df2024[df2024["Pv"] >= min_pv]

gk2022 = df2022[df2022["R"] == "P"]
gk2023 = df2023[df2023["R"] == "P"]
gk2024 = df2024[df2024["R"] == "P"]


#------------------------- MULTI SEARCH BOX
all_names = pd.concat([gk2022["Nome"], gk2023["Nome"], gk2024["Nome"]]).unique()
search_names = st.multiselect("Seleziona uno o più portieri da **confrontare**", options=sorted(all_names), default=[])

# Palette e simboli
colors = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Dark24
symbols = ["circle", "square", "diamond", "star", "cross", "x", "triangle-up", "triangle-down"]

#========================= SECTION 0: CORRELATION MATRICES =========================
corrgk2022 = gk2022.corr(numeric_only=True)
corrgk2023 = gk2023.corr(numeric_only=True)
corrgk2024 = gk2024.corr(numeric_only=True)
corrgk = (corrgk2022 + corrgk2023 + corrgk2024)/3
st.header("📊 Matrice di correlazione - Portieri")
fig = px.imshow(
    corrgk,
    text_auto=".2f",
    color_continuous_scale='RdBu_r',
    aspect="auto",
    title="MATRICE DI CORRELAZIONI MEDIA 2022-24 (POR)"
)

fig.update_layout(
    height=800
)

st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 1: BOX PLOTS =========================
st.header("📊 Boxplot Portieri")

def add_boxplot(fig, df, col, metric):
    # Base boxplot
    box = px.violin(
        df,
        y=metric,
        box=True,
        points="all",
        hover_data=["Nome", "Squadra", "Pv"]
    )
    for trace in box.data:
        fig.add_trace(trace, row=1, col=col)

    # Highlight selected players
    for i, name in enumerate(search_names):
        highlight = df[df["Nome"] == name]
        if not highlight.empty:
            fig.add_trace(
                px.scatter(
                    highlight,
                    y=metric,
                    hover_name="Nome"
                ).update_traces(
                    marker=dict(size=15, color=colors[i % len(colors)], symbol=symbols[i % len(symbols)]),
                    name=name,
                    showlegend=True
                ).data[0],
                row=1, col=col
            )

metrics = ["Mv", "Fm", "Gs", "Gs a partita", "clean_sheet", "Amm", "Esp"]
for metric in metrics:
    st.subheader(f"{metric} - Boxplot 2022-2024")
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("2022", "2023", "2024"),
        horizontal_spacing=0.15
    )

    add_boxplot(fig, gk2022, col=1, metric=metric)
    add_boxplot(fig, gk2023, col=2, metric=metric)
    add_boxplot(fig, gk2024, col=3, metric=metric)

    fig.update_layout(
        height=500, width=1200,
        title=f"{metric} - Portieri 2022-2024",
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 2: REGRESSION =========================
st.header("📈 Correlazioni Coppie di Variabili")

def add_scatter(fig, df, x, y, col):
    scatter = px.scatter(
        df,
        x=x,
        y=y,
        trendline="ols",
        hover_name="Nome",
        hover_data=["Squadra", "Pv"]
    )
    for trace in scatter.data:
        fig.add_trace(trace, row=1, col=col)

    # Highlight selected players
    for i, name in enumerate(search_names):
        highlight = df[df["Nome"] == name]
        if not highlight.empty:
            fig.add_trace(
                px.scatter(
                    highlight,
                    x=x,
                    y=y,
                    hover_name="Nome"
                ).update_traces(
                    marker=dict(size=15, color=colors[i % len(colors)], symbol=symbols[i % len(symbols)]),
                    name=name,
                    showlegend=True
                ).data[0],
                row=1, col=col
            )

# Variabili da confrontare
pairs = [
    ("Mv", "Fm", "📈 Mv vs Fm - Portieri 2022-2024"),
    ("clean_sheet", "Fm", "📈 Clean Sheet vs Fm - Portieri 2022-2024"),
    ("Gs", "Fm", "📈 Gs vs Fm - Portieri 2022-2024")
]

for x, y, title in pairs:
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("2022", "2023", "2024"),
        horizontal_spacing=0.1
    )
    for col, df in zip([1, 2, 3], [gk2022, gk2023, gk2024]):
        add_scatter(fig, df, x, y, col)

    fig.update_layout(
        height=500, width=1600,
        showlegend=True,
        title=title
    )
    fig.update_xaxes(title_text=x, row=1, col=1)
    fig.update_xaxes(title_text=x, row=1, col=2)
    fig.update_xaxes(title_text=x, row=1, col=3)

    fig.update_yaxes(title_text=y, row=1, col=1)
    fig.update_yaxes(title_text=y, row=1, col=2)
    fig.update_yaxes(title_text=y, row=1, col=3)

    st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 3: RADAR PLOT NORMALIZZATO =========================
st.header("📊 Confronto Radar dei Giocatori Selezionati per Stagione")

if search_names:
    radar_metrics = [
        "Pv", "Mv", "Fm", "Gs a partita", "clean_sheet", "Rp"
    ]

    seasons = {
        "2022-23": gk2022,
        "2023-24": gk2023,
        "2024-25": gk2024
    }

    # Creo colonne affiancate per le 3 stagioni
    cols = st.columns(len(seasons))

    for col, (season_name, df_season) in zip(cols, seasons.items()):
        # Filtra solo i giocatori selezionati presenti in questa stagione
        df_selected = df_season[df_season["Nome"].isin(search_names)][["Nome"] + radar_metrics].copy()
        if df_selected.empty:
            col.info(f"Nessun giocatore selezionato in {season_name}.")
            continue

        df_selected = df_selected.groupby("Nome")[radar_metrics].mean().reset_index()

        # Normalizzazione: per ogni metrica il massimo tra i giocatori selezionati diventa 1
        df_norm = df_selected.copy()
        for metric in radar_metrics:
            max_val = df_norm[metric].max()
            if max_val != 0:
                df_norm[metric] = df_norm[metric] / max_val
            else:
                df_norm[metric] = 0

        # Trasforma in formato long (necessario per px.line_polar)
        df_long = df_norm.melt(id_vars="Nome", value_vars=radar_metrics,
                               var_name="Metrica", value_name="Valore")

        # Plot radar
        fig = px.line_polar(
            df_long,
            r="Valore",
            theta="Metrica",
            color="Nome",
            line_close=True,
            markers=True
        )
        fig.update_traces(fill='toself')
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(color="black"))
            ),
            showlegend=True,
            title=season_name
        )

        col.plotly_chart(fig, use_container_width=True)
else:
    st.info("Seleziona almeno un giocatore per visualizzare il radar plot.")


#========================= SECTION 4: "FASCE" CLUSTERING =========================

def KmeansPCA(df, numericalCols, nclusters, ruolo, highlight_names=None):
    df = df.copy() 
    df_filled = df[numericalCols].fillna(0)
    
    # Standardization
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_filled)
    
    # Fit KMeans on scaled data
    model = KMeans(n_clusters=nclusters, random_state=42)
    df["cluster"] = model.fit_predict(df_scaled).astype(str)  # Convert cluster to string
    
    # PCA on scaled data
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df_scaled)
    df["PCA1"] = pca_result[:, 0]
    df["PCA2"] = pca_result[:, 1]
    
    # Define vivid colors for clusters
    vivid_colors = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4", "#46f0f0", "#f032e6"]
    color_sequence = [vivid_colors[i % len(vivid_colors)] for i in range(nclusters)]
    
    # Plotly scatter
    fig = px.scatter(
        df,
        x="PCA1",
        y="PCA2",
        color="cluster",
        hover_data=["Nome", "Squadra", "Pv", "Fm"],
        title=f"Cluster {ruolo}",
        color_discrete_sequence=color_sequence
    )

    # Highlight selected players
    if highlight_names:
        for i, name in enumerate(highlight_names):
            highlight = df[df["Nome"] == name]
            if not highlight.empty:
                fig.add_trace(
                    px.scatter(
                        highlight,
                        x="PCA1",
                        y="PCA2",
                        hover_name="Nome"
                    ).update_traces(
                        marker=dict(size=15, color='black', symbol='star'),
                        name=name,
                        showlegend=True
                    ).data[0]
                )
    
    fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig, use_container_width=True)

st.header("🧤 Clustering Portieri")
numericalCols_gk = ["Pv", "Mv", "Fm", "Gs", "Rp", "clean_sheet"]
# Sidebar options for clustering
n_clusters = st.slider("Scegli il numero di 'raggruppamenti' (KMeans)", 2, 6, 3)

if st.button("Esegui clustering portieri 2024"):
    KmeansPCA(
        gk2024,                    # Last season dataframe
        numericalCols_gk,          # Your selected numeric columns
        n_clusters, 
        ruolo="Portieri 2024",
        highlight_names=search_names # Highlight selected players
    )


#========================= SECTION X: OTHER METRICS =========================
st.header("⚡ Altre metriche")

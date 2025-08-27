import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
#---------------- STREAMLIT HEADER
st.set_page_config(page_title="Fantacalcio 25/26 - Centrocampisti", layout="wide") 
st.title("📐 Centrocampisti - Analisi Statistica")
st.markdown("""
In questa sezione analizziamo le performance dei centrocampisti nelle ultime 3 stagioni di Serie A.

Utilizzeremo i seguenti simboli:
- Mv = Media Voto
- Fm = Fanta Media
- Pv = Partite a Voto
- Gf = Gol Fatti
- Ass = Assist
- xG_per90 = Expected Goals per 90 Minuti
- xA_per90 = Expected Assist per 90 Minuti
- key_passess = Passaggi Chiave
- G + A (pts converted) = Somma dei Bonus (goal = +3, assist = +1)
- Rc = Rigori Calciati
- R+ = Rigori Segnati
- Amm = Ammonizioni
- Esp = Espulsioni
""")

#---------------- READ FILES
df2022 = pd.read_excel("2022_23_Merged.xlsx")
df2023 = pd.read_excel("2023_24_Merged.xlsx")
df2024 = pd.read_excel("2024_25_Merged.xlsx")

drop_columns = ["Id", "id", "goals", "assists", "yellow_cards", "red_cards", "matched"]
df2022 = df2022.drop(drop_columns, axis=1)
df2023 = df2023.drop(drop_columns, axis=1)
df2024 = df2024.drop(drop_columns, axis=1)

df2022["xBonus"] = (3*df2022["xG"] + 1*df2022["xA"] + 3*df2022["Rp"] + 1*df2022["clean_sheet"]) - (2*df2022["Au"]+ 1*df2022["Gs"] + 1*df2022["Esp"] + 0.5*df2022["Amm"] + df2022["R-"])
df2022["actualBonus"] = (3*df2022["Gf"] + 1*df2022["Ass"] + 3*df2022["Rp"] + 1*df2022["clean_sheet"]) - (2*df2022["Au"]+ 1*df2022["Gs"] + 1*df2022["Esp"] + 0.5*df2022["Amm"]+ df2022["R-"])
df2022["xG + xA (pts converted)"] = (3*df2022["xG"] + 1*df2022["xA"])
df2022["G + A (pts converted)"] = (3*df2022["Gf"] + 1*df2022["Ass"])
df2022["% Gol/Tiri"] = df2022["Gf"]/df2022["shots"]
df2022["Amm a partita"] = df2022["Amm"]/df2022["Pv"]
df2022["Minuti a partita"] = df2022["time"]/df2022["games"]
df2022["Tiri a partita"] = df2022["shots"]/df2022["games"]
df2022["key_passes a partita"] = df2022["key_passes"]/df2022["games"]
df2022["% Rigori Segnati"] = df2022["R+"]/df2022["Rc"]
df2022["Gf a partita"] = df2022["Gf"]/df2022["Pv"]


df2023["xBonus"] = (3*df2023["xG"] + 1*df2023["xA"] + 3*df2023["Rp"] + 1*df2023["clean_sheet"]) - (2*df2023["Au"]+ 1*df2023["Gs"] + 1*df2023["Esp"] + 0.5*df2023["Amm"] + df2023["R-"])
df2023["actualBonus"] = (3*df2023["Gf"] + 1*df2023["Ass"] + 3*df2023["Rp"] + 1*df2023["clean_sheet"]) - (2*df2023["Au"]+ 1*df2023["Gs"] + 1*df2023["Esp"] + 0.5*df2023["Amm"] + df2023["R-"])
df2023["xG + xA (pts converted)"] = (3*df2023["xG"] + 1*df2023["xA"])
df2023["G + A (pts converted)"] = (3*df2023["Gf"] + 1*df2023["Ass"])
df2023["% Gol/Tiri"] = df2023["Gf"]/df2023["shots"]
df2023["Amm a partita"] = df2023["Amm"]/df2023["Pv"]
df2023["Minuti a partita"] = df2023["time"]/df2023["games"]
df2023["Tiri a partita"] = df2023["shots"]/df2023["games"]
df2023["key_passes a partita"] = df2023["key_passes"]/df2023["games"]
df2023["% Rigori Segnati"] = df2023["R+"]/df2023["Rc"]
df2023["Gf a partita"] = df2023["Gf"]/df2023["Pv"]

df2024["xBonus"] = (3*df2024["xG"] + 1*df2024["xA"] + 3*df2024["Rp"]+ 1*df2024["clean_sheet"]) - (2*df2024["Au"]+ 1*df2024["Gs"] + 1*df2024["Esp"] + 0.5*df2024["Amm"] + df2024["R-"])
df2024["actualBonus"] = (3*df2024["Gf"] + 1*df2024["Ass"] + 3*df2024["Rp"] + 1*df2024["clean_sheet"]) - (2*df2024["Au"]+ 1*df2024["Gs"] + 1*df2024["Esp"] + 0.5*df2024["Amm"] + df2024["R-"])
df2024["xG + xA (pts converted)"] = (3*df2024["xG"] + 1*df2024["xA"])
df2024["G + A (pts converted)"] = (3*df2024["Gf"] + 1*df2024["Ass"])
df2024["% Gol/Tiri"] = df2024["Gf"]/df2024["shots"]
df2024["Amm a partita"] = df2024["Amm"]/df2024["Pv"]
df2024["Minuti a partita"] = df2024["time"]/df2024["games"]
df2024["Tiri a partita"] = df2024["shots"]/df2024["games"]
df2024["key_passes a partita"] = df2024["key_passes"]/df2024["games"]
df2024["% Rigori Segnati"] = df2024["R+"]/df2024["Rc"]
df2024["Gf a partita"] = df2024["Gf"]/df2024["Pv"]
#------------------------- PV FILTER
min_pv = st.slider("Numero minimo di partite a voto (Pv)", min_value=1, max_value=int(df2024["Pv"].max()), value=1)

df2022 = df2022[df2022["Pv"] >= min_pv]
df2023 = df2023[df2023["Pv"] >= min_pv]
df2024 = df2024[df2024["Pv"] >= min_pv]

mid2022 = df2022[df2022["R"] == "C"]
mid2023 = df2023[df2023["R"] == "C"]
mid2024 = df2024[df2024["R"] == "C"]

#------------------------- MULTI SEARCH BOX
all_names = pd.concat([mid2022["Nome"], mid2023["Nome"], mid2024["Nome"]]).unique()
search_names = st.multiselect("Seleziona uno o più centrocampisti da **confrontare**", options=sorted(all_names), default=[])

# Palette e simboli
colors = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Dark24
symbols = ["circle", "square", "diamond", "star", "cross", "x", "triangle-up", "triangle-down"]

#========================= SECTION 0: CORRELATION MATRICES =========================
corrmid2022 = mid2022.corr(numeric_only=True)
corrmid2023 = mid2023.corr(numeric_only=True)
corrmid2024 = mid2024.corr(numeric_only=True)
corrmid = (corrmid2022 + corrmid2023 + corrmid2024)/3
st.header("📊 Matrici di correlazione - Centrocampisti")
fig = px.imshow(
    corrmid,
    text_auto=".2f",
    color_continuous_scale='RdBu_r',
    aspect="auto",
    title="MATRICE DI CORRELAZIONI MEDIA 2022-24 (CEN)"
)

fig.update_layout(
    height=800
)

st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 1: BOX PLOTS =========================
st.header("📊 Boxplot Centrocampisti")

metrics = ["Mv", "Fm", "Gf", "Ass", "xG_per90", "xA_per90", "key_passes", "Tiri a partita", "G + A (pts converted)",
           "Rc", "R+", "% Rigori Segnati", "Minuti a partita", "Amm", "Esp"]
for metric in metrics:
    st.subheader(f"{metric} - Boxplot 2022-2024")
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("2022", "2023", "2024"),
        horizontal_spacing=0.15
    )

    def add_boxplot(fig, df, col):
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

    add_boxplot(fig, mid2022, col=1)
    add_boxplot(fig, mid2023, col=2)
    add_boxplot(fig, mid2024, col=3)

    fig.update_layout(
        height=500, width=1200,
        title=f"{metric} - Centrocampisti 2022-2024",
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
    ("Mv", "Fm", "📈 Mv vs Fm - Centrocampisti 2022-2024"),
    ("shots", "Gf", "📈 Tiri vs Gf - Centrocampisti 2022-2024"),
    ("Tiri a partita", "Fm", "📈 Tiri a partita vs Fm - Centrocampisti 2022-2024"),
    ("Gf", "Ass", "📈 Gol Fatti vs Assist - Centrocampisti 2022-2024"),
    ("xG", "Gf", "📈 xG vs Gol Fatti - Centrocampisti 2022-2024"),
    ("xA", "Ass", "📈 xA vs Assist - Centrocampisti 2022-2024"),
    ("key_passes", "Ass", "📈 Passaggi Chiave vs Ass - Centrocampisti 2022-2024"),
    ("Tiri a partita", "Gf a partita", "📈 Tiri a partita vs Gf - Centrocampisti 2022-2024"),
    ("Tiri a partita", "Fm", "📈 Tiri a partita vs Fm - Centrocampisti 2022-2024"),
]

for x, y, title in pairs:
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("2022", "2023", "2024"),
        horizontal_spacing=0.1
    )
    for col, df in zip([1, 2, 3], [mid2022, mid2023, mid2024]):
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
        "Pv", "Mv", "Fm", "Gf", "Ass", "xG_per90", "xA_per90",
        "% Gol/Tiri", "key_passes"
    ]

    seasons = {
        "2022-23": mid2022,
        "2023-24": mid2023,
        "2024-25": mid2024
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

st.header("📐 Clustering Centrocampisti")
numericalCols_mid = ["Pv", "Mv", "Fm", "Gf", "Ass", "Amm", "Esp", "xG", "xA", "% Gol/Tiri", "shots", "key_passes", "xGBuildup", "xGChain", "Minuti a partita"]
n_clusters = st.slider("Scegli il numero di 'raggruppamenti' (KMeans)", 2, 6, 3)

if st.button("Esegui clustering centrocampisti 2024"):
    KmeansPCA(
        mid2024,                    # Last season dataframe
        numericalCols_mid,          # Your selected numeric columns
        n_clusters, 
        ruolo="Centrocampisti 2024",
        highlight_names=search_names # Highlight selected players
    )
#========================= SECTION X: OTHER METRICS =========================
st.header("⚡ Altre metriche")

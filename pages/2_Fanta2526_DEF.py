import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

#---------------- STREAMLIT HEADER
st.title("🛡️ Difensori - Analisi Statistica")
st.markdown("""
In questa sezione analizziamo le performance dei difensori nelle ultime 3 stagioni di Serie A.

Utilizzeremo i seguenti simboli:
- Mv = Media Voto
- Fm = Fanta Media
- Pv = Partite a Voto
- key_passess = Passaggi Chiave
- shots = Tiri 
- G + A (pts converted) = Somma dei Bonus (goal = +3, assist = +1)
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
#------------------------- PV FILTER
min_pv = st.slider("Numero minimo di partite a voto (Pv)", min_value=1, max_value=int(df2024["Pv"].max()), value=1)

df2022 = df2022[df2022["Pv"] >= min_pv]
df2023 = df2023[df2023["Pv"] >= min_pv]
df2024 = df2024[df2024["Pv"] >= min_pv]

def2022 = df2022[df2022["R"] == "D"]
def2023 = df2023[df2023["R"] == "D"]
def2024 = df2024[df2024["R"] == "D"]

#------------------------- MULTI SEARCH BOX
all_names = pd.concat([def2022["Nome"], def2023["Nome"], def2024["Nome"]]).unique()
search_names = st.multiselect("Seleziona uno o più portieri da evidenziare", options=sorted(all_names), default=[])

# Palette e simboli
colors = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Dark24
symbols = ["circle", "square", "diamond", "star", "cross", "x", "triangle-up", "triangle-down"]

#========================= SECTION 0: CORRELATION MATRICES =========================
corrdef2022 = def2022.corr(numeric_only=True)
corrdef2023 = def2023.corr(numeric_only=True)
corrdef2024 = def2024.corr(numeric_only=True)
corrdef = (corrdef2022 + corrdef2023 + corrdef2024)/3
st.header("📊 Matrici di correlazione - Difensori")
fig = px.imshow(
    corrdef,
    text_auto=".2f",
    color_continuous_scale='RdBu_r',
    aspect="auto",
    title="MATRICE DI CORRELAZIONI MEDIA 2022-24 (DEF)"
)

fig.update_layout(
    height=800
)

st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 1: BOX PLOTS =========================
st.header("📊 Boxplot Difensori")

metrics = ["Mv", "Fm", "Gf", "Ass", "xG_per90", "xA_per90", "key_passes", "Tiri a partita", "G + A (pts converted)",
           "Rc", "R+", "% Rigori Segnati", "Minuti a partita", "Amm", "Amm a partita"]
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
            points="all",
            box=True,
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

    add_boxplot(fig, def2022, col=1)
    add_boxplot(fig, def2023, col=2)
    add_boxplot(fig, def2024, col=3)

    fig.update_layout(
        height=500, width=1200,
        title=f"{metric} - Difensori 2022-2024",
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
    ("Mv", "Amm", "📈 Mv vs Amm - Difensori 2022-2024"),
    ("Mv", "Fm", "📈 Mv vs Fm - Difensori 2022-2024"),
    ("shots", "Gf", "📈 Tiri vs Gf - Difensori 2022-2024"),
    ("xG + xA (pts converted)", "G + A (pts converted)", "📈 xBonus vs Bonus - Difensori 2022-2024"),
    ("xG", "Gf", "📈 xG vs Gol Fatti - Difensori 2022-2024"),
    ("xA", "Ass", "📈 xA vs Assist - Difensori 2022-2024"),
]

for x, y, title in pairs:
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("2022", "2023", "2024"),
        horizontal_spacing=0.1
    )
    for col, df in zip([1, 2, 3], [def2022, def2023, def2024]):
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

#========================= SECTION 3:  =========================

#========================= SECTION X: OTHER METRICS =========================
st.header("⚡ Altre metriche")





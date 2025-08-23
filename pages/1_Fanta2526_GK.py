import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

#---------------- STREAMLIT HEADER
st.title("🧤 Portieri - Analisi Statistica")
st.markdown("""
In questa sezione analizziamo le performance dei portieri nelle ultime 3 stagioni di Serie A.

Utilizzeremo i seguenti simboli:
- Mv = Media Voto
- Fm = Fanta Media
- Gs = Gol Subiti
- Pv = Partite a Voto
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

df2023["xBonus"] = (3*df2023["xG"] + 1*df2023["xA"] + 3*df2023["Rp"] + 1*df2023["clean_sheet"]) - (2*df2023["Au"]+ 1*df2023["Gs"] + 1*df2023["Esp"] + 0.5*df2023["Amm"] + df2023["R-"])
df2023["actualBonus"] = (3*df2023["Gf"] + 1*df2023["Ass"] + 3*df2023["Rp"] + 1*df2023["clean_sheet"]) - (2*df2023["Au"]+ 1*df2023["Gs"] + 1*df2023["Esp"] + 0.5*df2023["Amm"] + df2023["R-"])
df2023["xG + xA (pts converted)"] = (3*df2023["xG"] + 1*df2023["xA"])
df2023["G + A (pts converted)"] = (3*df2023["Gf"] + 1*df2023["Ass"])


df2024["xBonus"] = (3*df2024["xG"] + 1*df2024["xA"] + 3*df2024["Rp"]+ 1*df2024["clean_sheet"]) - (2*df2024["Au"]+ 1*df2024["Gs"] + 1*df2024["Esp"] + 0.5*df2024["Amm"] + df2024["R-"])
df2024["actualBonus"] = (3*df2024["Gf"] + 1*df2024["Ass"] + 3*df2024["Rp"] + 1*df2024["clean_sheet"]) - (2*df2024["Au"]+ 1*df2024["Gs"] + 1*df2024["Esp"] + 0.5*df2024["Amm"] + df2024["R-"])
df2024["xG + xA (pts converted)"] = (3*df2024["xG"] + 1*df2024["xA"])
df2024["G + A (pts converted)"] = (3*df2024["Gf"] + 1*df2024["Ass"])

#------------------------- PV FILTER
min_pv = st.slider("Numero minimo di partite a voto (Pv)", min_value=1, max_value=int(df2024["Pv"].max()), value=1)

df2022 = df2022[df2022["Pv"] >= min_pv]
df2023 = df2023[df2023["Pv"] >= min_pv]
df2024 = df2024[df2024["Pv"] >= min_pv]

gk2022 = df2022[df2022["R"] == "P"]
gk2023 = df2023[df2023["R"] == "P"]
gk2024 = df2024[df2024["R"] == "P"]

#------------------------- SEARCH BOX
search_name = st.text_input("Cerca un giocatore", "")

#========================= SECTION 1: BOX PLOTS =========================
st.header("📊 Boxplot Portieri")

metrics = ["Mv", "Fm", "Gs", "clean_sheet"]
for metric in metrics:
    st.subheader(f"{metric} - Boxplot 2022-2024")
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("2022", "2023", "2024"),
        horizontal_spacing=0.15
    )

    def add_boxplot(fig, df, col):
        # Base boxplot
        box = px.box(
            df,
            y=metric,
            points="all",
            hover_data=["Nome", "Squadra", "Pv"]
        )
        for trace in box.data:
            fig.add_trace(trace, row=1, col=col)
        
        # Highlight searched player
        if search_name:
            highlight = df[df["Nome"].str.contains(search_name, case=False)]
            if not highlight.empty:
                fig.add_trace(
                    px.scatter(
                        highlight,
                        y=metric,
                        hover_name="Nome"
                    ).update_traces(
                        marker=dict(size=15, color="red", symbol="star")
                    ).data[0],
                    row=1, col=col
                )

    add_boxplot(fig, gk2022, col=1)
    add_boxplot(fig, gk2023, col=2)
    add_boxplot(fig, gk2024, col=3)

    fig.update_layout(
        height=500, width=1200,
        title=f"{metric} - Portieri 2022-2024",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 2: REGRESSION =========================
st.header("📈 Correlazioni Coppie di Variabili")

fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("2022", "2023", "2024"),
    horizontal_spacing=0.1
)

for col, df, year in zip([1, 2, 3], [gk2022, gk2023, gk2024], [2022, 2023, 2024]):
    # Base scatter + trendline
    scatter = px.scatter(
        df,
        x="Mv",
        y="Gs",
        trendline="ols",
        hover_name="Nome",
        hover_data=["Squadra", "Pv"]
    )
    for trace in scatter.data:
        fig.add_trace(trace, row=1, col=col)

    # Highlight searched player
    if search_name:
        highlight = df[df["Nome"].str.contains(search_name, case=False)]
        if not highlight.empty:
            fig.add_trace(
                px.scatter(
                    highlight,
                    x="Mv",
                    y="Gs",
                    hover_name="Nome"
                ).update_traces(
                    marker=dict(size=15, color="red", symbol="star")
                ).data[0],
                row=1, col=col
            )

fig.update_layout(
    height=500, width=1600,
    showlegend=False,
    title="📈 Mv vs Gs - Portieri 2022-2024"
)
# Increase horizontal spacing between subplots
fig.update_xaxes(title_text="Mv", row=1, col=1)
fig.update_xaxes(title_text="Mv", row=1, col=2)
fig.update_xaxes(title_text="Mv", row=1, col=3)

fig.update_yaxes(title_text="Gs", row=1, col=1)
fig.update_yaxes(title_text="Gs", row=1, col=2)
fig.update_yaxes(title_text="Gs", row=1, col=3)
st.plotly_chart(fig, use_container_width=True)

fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("2022", "2023", "2024"),
    horizontal_spacing=0.1
)

for col, df, year in zip([1, 2, 3], [gk2022, gk2023, gk2024], [2022, 2023, 2024]):
    # Base scatter + trendline
    scatter = px.scatter(
        df,
        x="Mv",
        y="Fm",
        trendline="ols",
        hover_name="Nome",
        hover_data=["Squadra", "Pv"]
    )
    for trace in scatter.data:
        fig.add_trace(trace, row=1, col=col)

    # Highlight searched player
    if search_name:
        highlight = df[df["Nome"].str.contains(search_name, case=False)]
        if not highlight.empty:
            fig.add_trace(
                px.scatter(
                    highlight,
                    x="Mv",
                    y="Fm",
                    hover_name="Nome"
                ).update_traces(
                    marker=dict(size=15, color="red", symbol="star")
                ).data[0],
                row=1, col=col
            )

fig.update_layout(
    height=500, width=1600,
    showlegend=False,
    title="📈 Mv vs Fm - Portieri 2022-2024"
)

# Axis titles
fig.update_xaxes(title_text="Mv", row=1, col=1)
fig.update_xaxes(title_text="Mv", row=1, col=2)
fig.update_xaxes(title_text="Mv", row=1, col=3)

fig.update_yaxes(title_text="Fm", row=1, col=1)
fig.update_yaxes(title_text="Fm", row=1, col=2)
fig.update_yaxes(title_text="Fm", row=1, col=3)

st.plotly_chart(fig, use_container_width=True)


fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("2022", "2023", "2024"),
    horizontal_spacing=0.1
)

for col, df, year in zip([1, 2, 3], [gk2022, gk2023, gk2024], [2022, 2023, 2024]):
    # Base scatter + trendline
    scatter = px.scatter(
        df,
        x="clean_sheet",
        y="Mv",
        trendline="ols",
        hover_name="Nome",
        hover_data=["Squadra", "Pv"]
    )
    for trace in scatter.data:
        fig.add_trace(trace, row=1, col=col)

    # Highlight searched player
    if search_name:
        highlight = df[df["Nome"].str.contains(search_name, case=False)]
        if not highlight.empty:
            fig.add_trace(
                px.scatter(
                    highlight,
                    x="clean_sheet",
                    y="Mv",
                    hover_name="Nome"
                ).update_traces(
                    marker=dict(size=15, color="red", symbol="star")
                ).data[0],
                row=1, col=col
            )

fig.update_layout(
    height=500, width=1600,
    showlegend=False,
    title="📈 Clean Sheet vs Mv - Portieri 2022-2024"
)
# Increase horizontal spacing between subplots
fig.update_xaxes(title_text="clean_sheet", row=1, col=1)
fig.update_xaxes(title_text="clean_sheet", row=1, col=2)
fig.update_xaxes(title_text="clean_sheet", row=1, col=3)

fig.update_yaxes(title_text="Mv", row=1, col=1)
fig.update_yaxes(title_text="Mv", row=1, col=2)
fig.update_yaxes(title_text="Mv", row=1, col=3)
st.plotly_chart(fig, use_container_width=True)


fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("2022", "2023", "2024"),
    horizontal_spacing=0.1
)

for col, df, year in zip([1, 2, 3], [gk2022, gk2023, gk2024], [2022, 2023, 2024]):
    # Base scatter + trendline
    scatter = px.scatter(
        df,
        x="clean_sheet",
        y="Fm",
        trendline="ols",
        hover_name="Nome",
        hover_data=["Squadra", "Pv"]
    )
    for trace in scatter.data:
        fig.add_trace(trace, row=1, col=col)

    # Highlight searched player
    if search_name:
        highlight = df[df["Nome"].str.contains(search_name, case=False)]
        if not highlight.empty:
            fig.add_trace(
                px.scatter(
                    highlight,
                    x="clean_sheet",
                    y="Fm",
                    hover_name="Nome"
                ).update_traces(
                    marker=dict(size=15, color="red", symbol="star")
                ).data[0],
                row=1, col=col
            )

fig.update_layout(
    height=500, width=1600,
    showlegend=False,
    title="📈 Clean Sheet vs Fm - Portieri 2022-2024"
)
# Increase horizontal spacing between subplots
fig.update_xaxes(title_text="clean_sheet", row=1, col=1)
fig.update_xaxes(title_text="clean_sheet", row=1, col=2)
fig.update_xaxes(title_text="clean_sheet", row=1, col=3)

fig.update_yaxes(title_text="Fm", row=1, col=1)
fig.update_yaxes(title_text="Fm", row=1, col=2)
fig.update_yaxes(title_text="Fm", row=1, col=3)
st.plotly_chart(fig, use_container_width=True)

#========================= SECTION 3:  =========================


#========================= SECTION X: OTHER METRICS =========================
st.header("⚡ Altre metriche")

for year, df in zip([2022, 2023, 2024], [gk2022, gk2023, gk2024]):
    st.subheader(f"{year} - Distribuzione xBonus")
    fig = px.histogram(
        df,
        x="xBonus",
        nbins=20,
        hover_data=["Nome", "Squadra", "Pv"]
    )
    # Highlight searched player
    if search_name:
        highlight = df[df["Nome"].str.contains(search_name, case=False)]
        if not highlight.empty:
            fig.add_trace(
                px.scatter(
                    highlight,
                    x="xBonus",
                    y=[0]*len(highlight),  # place marker at bottom of histogram
                    hover_name="Nome"
                ).update_traces(
                    marker=dict(size=15, color="red", symbol="star")
                ).data[0]
            )
    st.plotly_chart(fig, use_container_width=True)

















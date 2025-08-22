import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

#---------------- STREAMLIT HEADER
st.title("🧤 Portieri - Analisi Statistica")
st.markdown("""
In questa sezione analizziamo le performance dei portieri nelle ultime 3 stagioni di Serie A.
""")

#---------------- READ FILES
df2022 = pd.read_excel(r"2022_23_Merged.xlsx")
df2023 = pd.read_excel(r"2023_24_Merged.xlsx")
df2024 = pd.read_excel(r"2024_25_Merged.xlsx")

drop_columns = ["Id", "id", "goals", "assists", "yellow_cards", "red_cards", "matched"]
df2022 = df2022.drop(drop_columns, axis=1)
df2023 = df2023.drop(drop_columns, axis=1)
df2024 = df2024.drop(drop_columns, axis=1)

df2022 = df2022[df2022["Pv"] > 1]
df2023 = df2023[df2023["Pv"] > 1]
df2024 = df2024[df2024["Pv"] > 1]

gk2022 = df2022[df2022["R"] == "P"]
gk2023 = df2023[df2023["R"] == "P"]
gk2024 = df2024[df2024["R"] == "P"]

#========================= SECTION 1: BOX PLOTS =========================
st.header("📊 Boxplot dei portieri")

metrics = ["Mv", "Fm", "Gs"]
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


















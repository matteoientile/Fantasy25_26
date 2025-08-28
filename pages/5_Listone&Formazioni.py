import streamlit as st
import pandas as pd
import numpy as np

#---------------- STREAMLIT HEADER
st.set_page_config(page_title="Fantacalcio 25/26 - Listone & Probabili Formazioni", layout="wide") 
st.title("📋 Listone Stagione 25/26 & ⚽ Formazioni Tipo")
st.markdown("""
Qui troverai 
- il Listone Fantagazzetta per l'asta 25/26
- i Link ai migliori siti per le Probabili Formazioni di Serie A

Nel listone, sono riportate una serie di statistiche relative all'anno scorso. A parte le più ovvie, può essere particolarmente utile
- Over/Under performance [%] = se positivo, vuol dire che il giocatore ha prodotto più bonus rispetto a quelli attesi; se negativo, il giocatore ha underperformato
- Nuovo Arrivo = indica se il giocatore ha giocato nella Serie 24/25, oppure è un nuovo arrivo
""")

#========================= SIDEBAR: INDEX =========================
st.sidebar.header("📌 Indice")
st.sidebar.markdown("""
- [📋 Listone Stagione 25/26](#listone-stagione-25-/-26)
- [⚽ Formazioni Tipo Serie A 2025/26](#formazioni-tipo-serie-a-25-/-26)
""")

#========================= SECTION 1: LISTONE =========================
st.header("📋 Listone Stagione 25/26 (con statistiche 24/25)")

# Carica i file
df_listone = pd.read_excel("Quotazioni_Fantacalcio_Stagione_2025_26.xlsx")
df_stats = pd.read_excel("2024_25_Merged.xlsx")

df_listone = df_listone.rename(columns={
    "Qt.A": "Quotazione Fantagazzetta",
    "FVM": "Prezzo Fantagazzetta / 500C."
})

# Aggiunta Over/Under performance
df_listone["Prezzo Fantagazzetta / 500C."] = np.ceil(df_listone["Prezzo Fantagazzetta / 500C."] / 2).astype(int)
df_stats["xG + xA (pts converted)"] = 3*df_stats["xG"] + 1*df_stats["xA"]
df_stats["G + A (pts converted)"] = 3*df_stats["Gf"] + 1*df_stats["Ass"]
df_stats["Over/Under performance %"] = np.where(
    df_stats["xG + xA (pts converted)"] > 0,
    np.round(
        100 * (df_stats["G + A (pts converted)"] - df_stats["xG + xA (pts converted)"]) / df_stats["xG + xA (pts converted)"],
        0
    ),
    np.nan
)
df_stats["Over/Under performance %"] = df_stats["Over/Under performance %"].fillna("-")

#======================= TITOLARITA' ===============================
#======== PORTIERI
titolari_por = {"Carnesecchi" : "Tit",
                "Skorupski" : "Tit", 
                "Caprile" : "Tit",
                "Butez" : "Tit",
                "Audero" : "Tit",
                "De Gea" : "Tit",
                "Leali" : "Tit",
                "Sommer" : "Tit",
                "Di Gregorio" : "Tit",
                "Provedel" : "Ballottaggio Mandas",
                "Mandas" : "Ballottaggio Provedel",
                "Falcone" : "Tit",
                "Maignan" : "Tit",
                "Meret" : "Ballottaggio Milinkovic",
                "Milinkovic-Savic V." : "Ballottaggio Meret",
                "Suzuki" : "Tit",
                "Semper" : "Ballottaggio Scuffet",
                "Scuffet" : "Ballottaggio Semper",
                "Svilar" : "Tit",
                "Turati" : "Tit",
                "Israel" : "Tit",
                "Okoye" : "Ballottaggio Okoye",
                "Sava" : "Ballottaggio Sava",
                "Montipò" : "Tit"}
#======== DIFENSORI
titolari_dif = {"Scalvini" : "Ballottagio Kossounou",
                "Kossounou" : "Ballottaggio Scalvini",
                "Hien" : "Tit",
                "Djimsiti" : "Ballottaggio Kolasinac",
                "Kolasinac" : "Ballottaggio Djimsiti",
                "Bellanova" : "Tit",
                "Zappacosta" : "Ballottaggio Zalewski",
                "Zortea" : "Ballottaggio Holm",
                "Holm" : "Ballottaggio Zortea",
                "Vitik" : "Tit",
                "Lucumì" : "Tit",
                "Miranda J." : "Tit",
                "Zappa" : "Ballottaggio Palestra",
                "Palestra" : "Ballottaggio Zappa",
                "Mina" : "Tit",
                "Luperto" : "Tit",
                "Idrissi R." : "Ballottaggio Opert",
                "Obert" : "Ballottaggio Idrissi",
                "Vojvoda" : "Tit",
                "Ramon" : "Tit",
                "Kempf" : "Ballottaggio Goldaniga",
                "Goldaniga" : "Ballottaggio Kempf",
                "Valle" : "Ballottaggio Moreno Alb.",
                "Moreno Alb." : "Ballottaggio Valle",
                "Terracciano F." : "Tit",
                "Baschirotto" : "Tit",
                "Pezzella Giu." :"Tit",
                "Bianchetti" : "Ballottaggio Barbieri",
                "Barbieri" : "Ballottaggio Bianchetti",
                "Comuzzo" : "Tit",
                "Pongracic" : "Tit",
                "Ranieri L." : "Tit",
                "Dodò" : "Tit",
                "Gosens":"Tit",
                "Norton-Cuffy" : "Ballottaggio Sabelli",
                "Sabelli" : "Ballottaggio Norton-Cuffy",
                "Ostigard" : "Tit",
                "Vasquez" : "Tit",
                "Martin" : "Tit",
                "Pavard" : "Ballottaggio Bisseck",
                "Bisseck" : "Ballottaggio Pavard",
                "Acerbi" : "Ballottaggio De Vrij",
                "De Vrij" : "Ballottaggio Acerbi",
                "Bastoni" : "Tit",
                "Dumfries" : "Tit",
                "Dimarco" : "Tit",
                "Gatti" : "Ballottaggio Kalulu",
                "Bremer" : "Tit",
                "Kalulu" : "Ballottaggio Gatti",
                "Kelly L." : "Titi (?)",
                "Cambiaso" : "Tit",
                "Joao Mario" : "Tit",
                "Marusic" : "Tit",
                "Romagnoli" : "Ballottaggio Provstgaard",
                "Provstgaard" : "Ballottaggio Romagnoli",
                "Gila" : "Tit",
                "Tavares N." : "Tit",
                "Kouassi" : "Ballottaggio Veiga D.",
                "Veiga D." : "Ballottaggio Kouassi",
                "Gaspar K." : "Tit",
                "Siebert" : "Ballottaggio Tiago Gabriel",
                "Tiago Gabriel" : "Ballottaggio Siebert",
                "Gallo" : "Tit",
                "De Winter" : "Ballottaggio Gabbia",
                "Gabbia" : "Ballottaggio De Winter",
                "Tomori" : "Tit",
                "Pavlovic" : "Tit",
                "Estupinan" : "Tit",
                "Jimenez A." : "Ballottaggio Saelemaekers",
                "Di Lorenzo" : "Tit",
                "Rrahmani" : "Ballottaggio Beukema",
                "Beukema" : "Ballottaggio Rrahmani",
                "Buongiorno" : "Tit",
                "Olivera" : "Ballottaggio Gutierrez",
                "Gutierrez" : "Ballottaggio Olivera",
                "Circati" : "Tit",
                "Troilo" : "Tit",
                "Valenti" : "Ballottaggio Ndiaye",
                "Delprato" : "Tit",
                "Valeri" : "Tit",
                "Calabresi" : "Tit",
                "Caracciolo" : "Ballottaggio Denoon",
                "Denoon" : "Ballottaggio Caracciolo",
                "Lusardi" : "Ballottaggio Canestrelli",
                "Canestrelli" : "Ballottaggio Lusardi",
                "Angori" : "Tit",
                "Cuadrado" : "Tit (?)",
                "Hermoso" : "Ballottaggio Ghilardi",
                "Ghilardi" : "Ballottaggio Hermoso",
                "N'dicka" : "Tit",
                "Mancini" : "Tit",
                "Wesley" : "Tit",
                "Angelino" : "Tit",
                "Idzes" : "Tit",
                "Walukiewicz" : "Tit",
                "Candè" : "Ballottaggio Muharemovic",
                "Muharemovic" : "Ballottaggio Candè",
                "Doig" : "Tit",
                "Lazaro" : "Ballottaggio Pedersen",
                "Pedersen" : "Ballottaggio Lazaro",
                "Coco" : "Ballottaggio Maripan",
                "Maripan" : "Ballottaggio Coco",
                "Ismajli" : "Ballottaggio Masina",
                "Masina" : "Ballottaggio Ismajili",
                "Biraghi" : "Tit",
                "Palma" : "Ballottaggio Goglichidze",
                "Goglichidze" : "Ballottaggio Palma",
                "Kristensen" : "Ballottaggio Bertola",
                "Bertola":"Ballottaggio Kristensen", 
                "Solet" : "Tit",
                "Ehizibue" : "Tit",
                "Zemura" : "Tit",
                "Unai Nunez": "Ballottaggio Bella-Kotchap",
                "Bella-Kotchap" : "Ballottaggio Unai Nunez",
                "Nelsson" : "Tit",
                "Ebosse":"Ballottaggio Bradaric", 
                "Bradaric":"Ballottaggio Ebosse",
                "Belghali":"Tit",
                "Frese":"Tit"}         

#======== CENTROCAMPISTI                
titolari_cen = {"Ederson D.S." : "Tit",
                "De Roon" : "Tit",
                "Zalewski" : "Ballottaggio Zappacosta",
                "Samardzic" : "Ballottaggio De Ketelaere",
                "Maldini" : "Ballottaggio Sulemana",
                "Sulemana" : "Ballottaggio Maldini",
                "Freuler" : "Tit",
                "Ferguson" : "Tit",
                "Orsolini" : "Tit",
                "Odgaard" : "Ballottaggio Bernardeschi",
                "Bernardeschi" : "Ballottaggio Odgaard",
                "Rowe" : "Ballottaggio Cambiaghi",
                "Cambiaghi" : "Ballottaggio Rowe",
                "Adopo" : "Tit",
                "Prati" : "Tit",
                "Folorunsho" : "Tit",
                "Gaetano" : "Ballottaggio Kilicsoy",
                "Da Cunha" : "Ballottaggio Baturina",
                "Baturina" : "Ballottaggio Da Cunha",
                "Perrone" : "Ballottaggio Caqueret",
                "Caqueret" : "Ballottaggio Perrone",
                "Paz N." : "Tit",
                "Zerbin" : "Tit",
                "Collocolo" : "Ballottaggio Bondo",
                "Bondo" : "Ballottaggio Collocolo",
                "Grassi" : "Ballottaggio Payero",
                "Payero" : "Ballottaggio Grassi",
                "Vandeputte" : "Tit",
                "Sohm" : "Tit",
                "Fagioli" : "Ballottaggio Mandragora",
                "Mandragora":"Ballottaggio Fagioli",
                "Gudmundsson A." : "Tit",
                "Masini" : "Tit",
                "Frendrup" : "Tit",
                "Carboni V." : "Tit",
                "Stanciu" : "Ballottaggio Malinovskyi",
                "Malinovskyi" : "Ballottaggio Stanciu",
                "Gronbaek" : "Tit",
                "Barella" : "Tit",
                "Calhanoglu" : "Tit",
                "Sucic P." : "Tit",
                "Locatelli" : "Ballottaggio Koopmeiners",
                "Koopmeiners" : "Ballottaggio Locatelli",
                "Thuram K." : "Tit",
                "Conceicao" : "Tit",
                "Guendouzi" : "Tit",
                "Rovella" : "Tit",
                "Vecino" : "Ballottaggio Dele-Bashiru",
                "Dele-Bashiru" : "Ballottaggio Vecino",
                "Zaccagni" : "Tit",
                "Coulibaly L." : "Tit",
                "Isaksen" : "Ballottaggio Cancellieri/Pedro",
                "Pierret" : "Ballottaggio Ramadani",
                "Ramadani" : "Ballottaggio Pierret",
                "Sala" : "Ballottaggio Helgason",
                "Helgason" : "Ballottaggio Sala",
                "Pierotti" : "Tit",
                "Sottil" : "Ballottaggio Tete Morente/Banda",
                "Tete Morente" : "Ballottaggio Sottil/Banda",
                "Jashari" : "Tit",
                "Saelemaekers" : "Ballottaggio Jimenez A.",
                "Modric" : "Tit",
                "Pulisic" : "Tit",
                "Loftus-Cheek" : "Ballottaggio Ricci",
                "Ricci" : "Ballottaggio Loftus-Cheek",
                "Zambo Anguissa" : "Tit",
                "McTominay" : "Tit",
                "De Bruyne" : "Tit",
                "Politano" : "Ballottaggio Lang/Neres",
                "Neres":"Ballottaggio Politano/Lang",
                "Lobotka" : "Tit",
                "Sorensen O." : "Ballottaggio Ordonez C.",
                "Ordonez C." : "Ballottaggio Sorensen O.",
                "Bernabè" : "Tit",
                "Oristanio" : "Tit",
                "Keita M." : "Tit",
                "Tourè I." : "Tit",
                "Marin M." : "Ballottaggio Piccinini",
                "Piccinini G." : "Ballottaggio Marin M.",
                "Aebischer" : "Tit",
                "Tramoni M." : "Tit",
                "Konè M." : "Tit",
                "El Aynaoui" : "Tit",
                "Bailey" : "Ballottaggio Dybala",
                "Thorstvedt" : "Tit",
                "Matic" : "Ballottaggio Vranckx",
                "Vranckx" : "Ballottaggio Matic",
                "Boloca" : "Ballottaggio Koné",
                "Konè I." : "Ballottaggio Boloca",
                "Anjorin" : "Tit",
                "Asllani" : "Tit",
                "Casadei" : "Tit",
                "Vlasic" : "Ballottaggio Ngonge",
                "Lovric" : "Ballottaggio Miller L.",
                "Miller L." : "Ballottaggio Lovric",
                "Karlstrom" : "Tit",
                "Atta" : "Tit",
                "Ekkelenkamp" : "Ballottaggio Bravo",
                "Harroui" : "Ballottaggio (iniziale, infortunio) Niasse",
                "Niasse" : "Ballottaggio Harroui",
                "Serdar" : "Tit",
                "Bernede" : "Tit"}

#======== ATTACCANTI  
titolari_att = {"De Ketelaere" : "Ballottaggio Samardzic",
                "Krstovic" : "Ballottaggio Scamacca",
                "Scamacca" : "Ballottaggio Krstovic",
                "Cambiaghi" : "Ballottaggio Rowe",
                "Castro S." : "Ballottaggio Immobile",
                "Immobile" : "Ballottaggio Castro S.",
                "Esposito Se." : "Tit",
                "Kilicsoy" : "Ballottaggio Gaetano",
                "Luvumbo" : "Tit",
                "Addai" : "Ballottaggio Khun",
                "Kuhn" : "Ballottaggio Addai",
                "Diao" : "Ballottaggio Rodriguez Je.",
                "Rodriguez Je." : "Ballottaggio Diao",
                "Morata" : "Ballottaggio Douvikas",
                "Douvikas" : "Ballottaggio Morata",
                "Sanabria" : "Tit",
                "Bonazzoli" : "Ballottaggio Vazquez",
                "Vazquez":"Ballottaggio Bonazzoli",
                "Kean" : "Tit",
                "Dzeko" : "Ballottaggio Piccoli",
                "Piccoli" : "Ballottaggio Dzeko",
                "Colombo" : "Ballottaggio Vitinha O.",
                "Vitinha O." : "Ballottaggio Colombo",
                "Thuram" : "Tit",
                "Martinez L." : "Tit",
                "Yildiz" : "Tit",
                "David" : "Tit (occhio Kolo)",
                "Castellanos" : "Ballottaggio Dia",
                "Dia" : "Ballottaggio Castellanos",
                "Cancellieri" : "Ballottaggio Isaksen",
                "Pedro" : "Ballottaggio Cancellieri/Isaksen",
                "Banda" : "Ballottaggio Morente/Sottil",
                "Stulic" : "Ballottaggio Camarda",
                "Camarda" : "Ballottaggio Stulic",
                "Gimenez" : "(???)",
                "Leao" : "Tit",
                "Lang" : "Ballottaggio Politano/Neres",
                "Lucca" : "Ballottaggio Lukaku",
                "Lukaku" : "Ballottaggio Lucca",
                "Pellegrino M." : "Tit",
                "Nzola" : "Tit",
                "Ferguson E." : "Ballottaggio Dovbyk/X",
                "Dovbyk" : "Ballottaggio Ferguson/X",
                "Dybala" : "Ballottaggio Bailey",
                "Soulè" : "Tit",
                "Berardi" : "Tit",
                "Pinamonti" : "Tit",
                "Laurientè" : "Tit",
                "Ngonge" : "Ballottaggio Vlasic",
                "Simeone" : "Tit",
                "Zapata D." : "Ballottaggio Adams C.",
                "Adams C." : "Ballottaggio Zapata D.",
                "Bravo" : "Ballottaggio Ekkelenkamp",
                "Buksa" : "Ballottaggio Davis K.",
                "Davis K." : "Ballottaggio Buksa",
                "Giovane" : "Tit",
                "Sarr A." : "Ballottaggio Orban",
                "Orban G." : "Ballottaggio Sarr A."}
#======== MERGE TITOLARI
titolari_all = {}
titolari_all.update(titolari_por)
titolari_all.update(titolari_dif)
titolari_all.update(titolari_cen)
titolari_all.update(titolari_att)

#======== CALCI PIAZZATI
piazzati = {"Krstovic":"R1-2",
            "Scamacca ":"R1-2",
            "De Ketelaere":"R1-2",
            "Samardzic":"P",
            "Zalewski":"P",
            "Immobile":"R1",
            "Orsolini":"R2, P",
            "Bernardeschi":"R3, P",
            "Miranda J.":"P",
            "Mina":"R1-2",
            "Esposito Se.":"R1-2, P",
            "Gaetano":"R3-4, P",
            "Kilicsoy":"R3-4",
            "Prati":"P",
            "Paz N.":"R1, P",
            "Douvikas":"R3",
            "Morata":"R2",
            "Da Cunha":"P",
            "Baturina":"P",
            "Vazquez":"R1, P",
            "Bonazzoli":"R2-3",
            "Sanabria":"R2-3",
            "Vandeputte":"P",
            "Pezzella Giu.":"P",
            "Kean":"R1-2",
            "Gudmundsson A.":"R1-2, P",
            "Fagioli":"P",
            "Mandragora":"R3, P",
            "Malinovskyi":"R1-2, P",
            "Colombo":"R1-2",
            "Stanciu":"R1-2, P",
            "Martin":"P",
            "Calhanoglu":"R1",
            "Zielinski":"R2",
            "Calhanoglu":"P",
            "Dimarco":"P",
            "Locatelli":"R1",
            "David":"R2",
            "Koopmeiners":"R3, P",
            "Yildiz":"P",
            "Conceicao":"P",
            "Zaccagni":"R1, P",
            "Castellanos":"R2",
            "Pedro":"R3",
            "Rovella":"P",
            "Stulic":"R1-2",
            "Camarda":"R1-2",
            "Tete Morente":"R3, P",
            "Gallo":"P",
            "Pulisic":"R1, P",
            "Modric":"R2-3, P",
            "Gimenez":"R2-3",
            "Lukaku":"R1",
            "Lucca":"R1",
            "De Bruyne":"R2, P",
            "Politano":"P",
            "Hernani":"R1",
            "Pellegrino M.":"R1",
            "Valeri":"R2",
            "Bernabè":"P",
            "Nzola":"R1",
            "Tramoni":"R2, P",
            "Dybala":"R1, P",
            "El Aynaoui":"R2-2",
            "Soulè":"R2-3, P",
            "Dovbyk":"R2-3",
            "Berardi":"R1, P",
            "Pianmonti":"R2",
            "Zapata":"R1",
            "Vlasic":"R2, P",
            "Buksa" : "R1",
            "Davis":"R1-2",
            "Bravo":"R2",
            "Harroui":"R1, P",
            "Sarr":"R2"}

#========== NOTE (Ruolo, Modulo, ...)
note_all = {"Bellanova":"Esterno 3-4-2-1",
            "Samardzic":"Ala 3-4-2-1",
            "Maldini":"Ala 3-4-2-1",
            "Odgaard":"Trq 4-2-3-1",
            "Palestra":"Esterno 3-5-2",
            "Idrissi R.":"Esterno 3-5-2",
            "Obert":"Esterno 3-5-2",
            "Pezzella Giu.":"Esterno 3-5-2",
            "Gosens":"Esterno 3-4-1-2",
            "Dodò":"Esterno 3-4-1-2",
            "Gudmundsson":"Trq 3-4-1-2",
            "Carboni V.":"Esterno 4-2-3-1",
            "Stanciu":"Trq 4-2-3-1",
            "Gronbaek":"Esterno 4-2-3-1",
            "Joao Mario":"Esterno 3-4-2-1",
            "Conceicao":"Esterno 3-4-2-1",
            "Isaksen":"Ala 4-3-3",
            "Pierotti":"Ala 4-3-3",
            "Estupinan":"Esterno 3-5-2",
            "Pulisic":"Attaccante 3-5-2",
            "Oristanio":"Attaccante 3-5-2",
            "Tramoni":"Ala 3-4-2-1",
            "Cuadrado":"Ala 3-4-2-1",
            "Angori":"Esterno 3-4-2-1",
            "Tourè I.":"Esterno 3-4-2-1",
            "Wesley":"Esterno 3-4-2-1",
            "Ehizibue":"Esterno 3-5-2",
            "Frese":"Esterno 3-4-1-2",
            "Belghali":"Esterno 3-4-1-2",
            "Harroui":"Trq 3-4-1-2"}

# Seleziona solo le colonne utili dalle stats
cols_stats = [
    "Nome", "Mv", "Fm", "Pv", "Gf", "Ass", "Gs", "clean_sheet", "Amm", "Esp", "Rc", "Over/Under performance %"
]
df_stats = df_stats[cols_stats]

# Rinomina le colonne per chiarezza
df_stats = df_stats.rename(columns={
    "Mv": "Media Voto (24/25) ",
    "Fm": "Fanta Media (24/25)",
    "Pv": "Partite a Voto (24/25)",
    "Gf": "Gol Fatti (24/25)",
    "Ass": "Assist (24/25)",
    "Gs": "Gol Subiti (24/25)",
    "clean_sheet": "Clean Sheet (24/25)",
    "Amm" : "Ammonizioni (24/25)",
    "Esp" : "Espulsioni (24/25)",
    "Rc": "Rigori calciati (24/25)",
    "Over/Under performance %" : "Over/Under performance [%] (24/25)"
})

# Merge sul nome
df_listone = df_listone.merge(df_stats, on="Nome", how="left")

# Colonna "Nuovo Arrivo" + "Titolarità"
df_listone["Nuovo Arrivo"] = np.where(~df_listone["Nome"].isin(df_stats["Nome"]), "SI", "-")
df_listone["Titolarità"] = df_listone["Nome"].map(titolari_all)
df_listone["Piazzati"] = df_listone["Nome"].map(piazzati)
df_listone["Note"] = df_listone["Nome"].map(note_all)
# Sostituisci NaN con "-" solo nelle colonne statistiche
stat_cols = [c for c in df_stats.columns if c != "Nome"]
df_listone[stat_cols] = df_listone[stat_cols].fillna("-")

#========================= FILTRI =========================
# Filtra per ruolo
ruoli = ["Tutti", "P", "D", "C", "A"]  
ruolo_sel = st.selectbox("Filtra per Ruolo", ruoli)
if ruolo_sel != "Tutti":
    df_listone = df_listone[df_listone["R"] == ruolo_sel]

# Ricerca giocatore
search = st.text_input("🔍 Cerca un giocatore per nome")
if search:
    df_listone = df_listone[df_listone["Nome"].str.contains(search, case=False, na=False)]

#========================= ORDINAMENTO =========================
sort_col = st.selectbox("Ordina per", df_listone.columns)
ascending = st.radio("Ordine", ["Crescente", "Decrescente"]) == "Crescente"

# Gestione colonne con "-" per lo sort
if sort_col in stat_cols:
    # Crea colonna temporanea numerica per ordinamento
    df_listone["_sort_temp"] = pd.to_numeric(df_listone[sort_col], errors="coerce")
    df_listone = df_listone.sort_values(by="_sort_temp", ascending=ascending)
    df_listone = df_listone.drop(columns="_sort_temp")
else:
    df_listone = df_listone.sort_values(by=sort_col, ascending=ascending)

#========================= MOSTRA TABELLA =========================
st.dataframe(df_listone.reset_index(drop=True), use_container_width=True)

#========================= DOWNLOAD IN EXCEL =========================
import io
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_listone.to_excel(writer, index=False, sheet_name="Listone")

st.download_button(
    label="📥 Scarica tabella in Excel",
    data=buffer,
    file_name="listone.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

#========================= SECTION 2: FORMAZIONI TIPO =========================
st.header("⚽ Formazioni Tipo Serie A 2025/26")

st.markdown("""
Per consultare le formazioni tipo aggiornate squadra per squadra, visita i seguenti link:

- [Formazioni tipo Serie A 2025/26 – SOS Fanta](https://www.sosfanta.com/asta-fantacalcio/formazioni-tipo-serie-a-2025-2026-oggi-giocherebbero-cosi/)
- [Probabili formazioni Serie A 2025/26 – Fantacalcio.it](https://www.fantacalcio.it/news/calcio-italia/29_07_2025/asta-fantacalcio-le-probabili-formazioni-della-serie-a-enilive-2025-26-480206)
- [Formazioni Titolari Fantacalcio 2025/26 – Goal.com](https://www.goal.com/it/liste/fantacalcio-formazioni-titolari-serie-a-2025-2026-tutte-le-squadre-tipo/bltd96a64fe7af82a71#csfc709a336b92e528)
""")


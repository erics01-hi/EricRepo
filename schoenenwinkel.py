import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Schoenenverkoop Analyse per Woonplaats en Merk")

# CSV-bestand inlezen
try:
    df = pd.read_csv("exclusieve_schoenen_verkoop_met_locatie.csv")
except FileNotFoundError:
    st.error("CSV-bestand niet gevonden. Zorg dat het bestand 'exclusieve_schoenen_verkoop_met_locatie.csv' in dezelfde map staat.")
    st.stop()

# Toon een preview van de data
st.subheader("Voorbeeld van de data")
st.dataframe(df.head())

# Filter 1: Woonplaats
woonplaatsen = df['woonplaats'].dropna().unique()
gekozen_woonplaats = st.selectbox("Kies een woonplaats", sorted(woonplaatsen))

# Filter data op woonplaats
data_per_woonplaats = df[df['woonplaats'] == gekozen_woonplaats]

# Filter 2: Merk (alleen merken in die woonplaats)
merken = data_per_woonplaats['merk'].dropna().unique()
gekozen_merk = st.selectbox("Kies een merk", sorted(merken))

# Filter definitieve data
gefilterde_data = data_per_woonplaats[data_per_woonplaats['merk'] == gekozen_merk]

# Controle of er data is
if gefilterde_data.empty:
    st.warning("Geen gegevens beschikbaar voor deze combinatie van woonplaats en merk.")
    st.stop()

# Groeperingen (optioneel, want we hebben al gefilterd op merk)
verkoop = gefilterde_data['aantal'].sum()
omzet = gefilterde_data['totaal_bedrag'].sum()

# Visuals naast elkaar
col1, col2 = st.columns(2)

# Visual 1: Aantal verkocht
with col1:
    st.subheader("Aantal verkocht")
    fig1, ax1 = plt.subplots()
    ax1.bar(gekozen_merk, verkoop, color='lightgreen')
    ax1.set_ylabel("Aantal verkocht")
    ax1.set_title(f"{gekozen_merk} in {gekozen_woonplaats}")
    st.pyplot(fig1)

# Visual 2: Totale omzet
with col2:
    st.subheader("Totale omzet (€)")
    fig2, ax2 = plt.subplots()
    ax2.bar(gekozen_merk, omzet, color='salmon')
    ax2.set_ylabel("Totale omzet (€)")
    ax2.set_title(f"{gekozen_merk} in {gekozen_woonplaats}")
    st.pyplot(fig2)

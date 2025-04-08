import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Schoenenverkoop Analyse per Woonplaats")

# CSV-bestand inlezen
try:
    df = pd.read_csv("exclusieve_schoenen_verkoop_met_locatie.csv")
except FileNotFoundError:
    st.error("CSV-bestand niet gevonden. Zorg dat het bestand 'exclusieve_schoenen_verkoop_met_locatie.csv' in dezelfde map staat.")
    st.stop()

# Toon een preview van de data
st.subheader("Voorbeeld van de data")
st.dataframe(df.head())

# Filter op woonplaats
woonplaatsen = df['woonplaats'].dropna().unique()
gekozen_woonplaats = st.selectbox("Kies een woonplaats", sorted(woonplaatsen))

# Data filteren
gefilterde_data = df[df['woonplaats'] == gekozen_woonplaats]

# Groeperingen
verkoop_per_merk = gefilterde_data.groupby('merk')['aantal'].sum().sort_values(ascending=False)
omzet_per_merk = gefilterde_data.groupby('merk')['totaal_bedrag'].sum().sort_values(ascending=False)

# Zet visuals naast elkaar
col1, col2 = st.columns(2)

# Visual 1: Verkoop per merk
with col1:
    st.subheader(f"Aantal verkocht per merk in {gekozen_woonplaats}")
    fig1, ax1 = plt.subplots()
    verkoop_per_merk.plot(kind='bar', ax=ax1, color='lightgreen')
    ax1.set_ylabel("Aantal verkocht")
    ax1.set_xlabel("Merk")
    ax1.set_title("Aantal per merk")
    st.pyplot(fig1)

# Visual 2: Omzet per merk
with col2:
    st.subheader(f"Totaal omzet per merk in {gekozen_woonplaats}")
    fig2, ax2 = plt.subplots()
    omzet_per_merk.plot(kind='bar', ax=ax2, color='salmon')
    ax2.set_ylabel("Totale omzet (€)")
    ax2.set_xlabel("Merk")
    ax2.set_title("Omzet per merk")
    st.pyplot(fig2)

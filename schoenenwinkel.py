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

# Filter 1: Woonplaats (optioneel)
alle_woonplaatsen = ['Alle'] + sorted(df['woonplaats'].dropna().unique().tolist())
gekozen_woonplaats = st.selectbox("Kies een woonplaats (optioneel)", alle_woonplaatsen)

# Filter op woonplaats indien geselecteerd
if gekozen_woonplaats != 'Alle':
    df = df[df['woonplaats'] == gekozen_woonplaats]

# Filter 2: Merk (optioneel)
alle_merken = ['Alle'] + sorted(df['merk'].dropna().unique().tolist())
gekozen_merk = st.selectbox("Kies een merk (optioneel)", alle_merken)

# Filter op merk indien geselecteerd
if gekozen_merk != 'Alle':
    df = df[df['merk'] == gekozen_merk]

# Check of er nog data is
if df.empty:
    st.warning("Geen gegevens beschikbaar voor deze selectie.")
    st.stop()

# Groeperen per merk
verkoop_per_merk = df.groupby('merk')['aantal'].sum().sort_values(ascending=False)
omzet_per_merk = df.groupby('merk')['totaal_bedrag'].sum().sort_values(ascending=False)

# Zet visuals naast elkaar
col1, col2 = st.columns(2)

# Visual 1: Aantal verkocht per merk
with col1:
    st.subheader("Aantal verkocht per merk")
    fig1, ax1 = plt.subplots()
    verkoop_per_merk.plot(kind='bar', ax=ax1, color='lightgreen')
    ax1.set_ylabel("Aantal verkocht")
    ax1.set_xlabel("Merk")
    ax1.set_title("Aantal verkocht")
    st.pyplot(fig1)

# Visual 2: Omzet per merk
with col2:
    st.subheader("Totale omzet per merk (€)")
    fig2, ax2 = plt.subplots()
    omzet_per_merk.plot(kind='bar', ax=ax2, color='salmon')
    ax2.set_ylabel("Totale omzet (€)")
    ax2.set_xlabel("Merk")
    ax2.set_title("Totale omzet")
    st.pyplot(fig2)

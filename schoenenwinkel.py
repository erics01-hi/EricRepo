import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Schoenenverkoop Analyse")

# CSV-bestand inlezen
try:
    df = pd.read_csv("exclusieve_schoenen_verkoop_met_locatie.csv")
except FileNotFoundError:
    st.error("CSV-bestand niet gevonden. Zorg dat het bestand 'exclusieve_schoenen_verkoop_met_locatie.csv' in dezelfde map staat.")
    st.stop()

# Datumkolom naar datetime
df['aankoopdatum'] = pd.to_datetime(df['aankoopdatum'], errors='coerce')

# Optionele filters
alle_woonplaatsen = ['Alle'] + sorted(df['woonplaats'].dropna().unique().tolist())
gekozen_woonplaats = st.selectbox("Kies een woonplaats (optioneel)", alle_woonplaatsen)

if gekozen_woonplaats != 'Alle':
    df = df[df['woonplaats'] == gekozen_woonplaats]

alle_merken = ['Alle'] + sorted(df['merk'].dropna().unique().tolist())
gekozen_merk = st.selectbox("Kies een merk (optioneel)", alle_merken)

if gekozen_merk != 'Alle':
    df = df[df['merk'] == gekozen_merk]

# Check op lege dataset
if df.empty:
    st.warning("Geen gegevens beschikbaar voor deze selectie.")
    st.stop()

# --------- Trendanalyse omzet over tijd ---------
trend_data = df.groupby(df['aankoopdatum'].dt.to_period('M'))['totaal_bedrag'].sum()
trend_data.index = trend_data.index.to_timestamp()

# --------- Donut chart omzet per merk ---------
omzet_per_merk = df.groupby('merk')['totaal_bedrag'].sum()

# Zet visuals naast elkaar
col1, col2 = st.columns(2)

# Visual 1: Trendgrafiek
with col1:
    st.subheader("📈 Omzet over tijd")
    fig1, ax1 = plt.subplots()
    trend_data.plot(ax=ax1, marker='o', color='blue')
    ax1.set_ylabel("Totale omzet (€)")
    ax1.set_xlabel("Maand")
    ax1.set_title("Omzet per maand")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

# Visual 2: Donut chart
with col2:
    st.subheader("🍩 Omzet per merk")
    fig2, ax2 = plt.subplots()
    wedges, texts, autotexts = ax2.pie(
        omzet_per_merk,
        labels=omzet_per_merk.index,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    ax2.set_title("Verdeling omzet per merk")
    st.pyplot(fig2)

# Bestaande visuals: Aantal + omzet per merk
col3, col4 = st.columns(2)

verkoop_per_merk = df.groupby('merk')['aantal'].sum().sort_values(ascending=False)
omzet_per_merk_sorted = omzet_per_merk.sort_values(ascending=False)

with col3:
    st.subheader("📊 Aantal verkocht per merk")
    fig3, ax3 = plt.subplots()
    verkoop_per_merk.plot(kind='bar', ax=ax3, color='lightgreen')
    ax3.set_ylabel("Aantal verkocht")
    ax3.set_title("Aantal verkocht")
    st.pyplot(fig3)

with col4:
    st.subheader("💰 Totale omzet per merk (€)")
    fig4, ax4 = plt.subplots()
    omzet_per_merk_sorted.plot(kind='bar', ax=ax4, color='salmon')
    ax4.set_ylabel("Totale omzet (€)")
    ax4.set_title("Totale omzet")
    st.pyplot(fig4)

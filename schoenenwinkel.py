import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Schoenenverkoop per Merk per Woonplaats")

# CSV-bestand inlezen
try:
    df = pd.read_csv("exclusieve_schoenen_verkoop_met_locatie.csv")
except FileNotFoundError:
    st.error("CSV-bestand niet gevonden. Zorg dat het bestand 'exclusieve_schoenen_verkoop_met_locatie.csv' in dezelfde map staat.")
    st.stop()

# Toon eerste paar rijen
st.subheader("Voorbeeld van de data")
st.dataframe(df.head())

# Filter op woonplaats
woonplaatsen = df['woonplaats'].dropna().unique()
gekozen_woonplaats = st.selectbox("Kies een woonplaats", sorted(woonplaatsen))

# Filter toepassen
gefilterde_data = df[df['woonplaats'] == gekozen_woonplaats]

# Groeperen: aantal schoenen per merk
verkoop_per_merk = gefilterde_data.groupby('merk')['aantal'].sum().sort_values(ascending=False)

# Visualisatie
st.subheader(f"Verkochte schoenen per merk in {gekozen_woonplaats}")
fig, ax = plt.subplots()
verkoop_per_merk.plot(kind='bar', ax=ax, color='skyblue')
ax.set_ylabel("Aantal verkocht")
ax.set_xlabel("Merk")
ax.set_title(f"Verkoop per merk in {gekozen_woonplaats}")
st.pyplot(fig)

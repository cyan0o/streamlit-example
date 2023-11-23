import pandas as pd
import requests
import streamlit as st

# Imposta le allocazioni di asset target
asset_allocations = {
    "azioni": 0.3,
    "obbligazioni_lungo_termine": 0.4,
    "obbligazioni_medio_termine": 0.15,
    "materie_prime": 0.075,
    "oro": 0.075,
}

# Leggi il valore corrente di ciascun asset
asset_values = pd.read_csv("asset_values.csv")

# Imposta la UI
st.title("Portafoglio virtuale di Nancy Pelosi")

# Mostra le allocazioni di asset target
st.write("Allocazioni di asset target:")
for asset, allocation in asset_allocations.items():
    st.write(f"{asset}: {allocation}")

# Mostra il valore corrente del portafoglio
st.write("Valore corrente del portafoglio:")
current_value = 0
for asset, allocation in asset_allocations.items():
    current_value += asset_values[asset].iloc[0] * allocation
st.write(current_value)

# Mostra le operazioni di Nancy Pelosi
st.write("Operazioni di Nancy Pelosi:")
operations = requests.get("https://api.sec.gov/historical/daily-insider/2023/07/20/congress/insider-trades.json").json()
for operation in operations:
    st.write(f"{operation['name']} ha acquistato {operation['amount']} azioni di {operation['ticker']} il {operation['date']}")

# Aggiorna il portafoglio
def update_portfolio():
    for operation in operations:
        asset = operation['ticker']
        amount = operation['amount']
        if operation['type'] == "buy":
            asset_allocations[asset] += amount / current_value
        elif operation['type'] == "sell":
            asset_allocations[asset] -= amount / current_value

# Pulsante per aggiornare il portafoglio
st.button("Aggiorna portafoglio")

# Aggiorna il portafoglio solo se il pulsante viene premuto
if st.button("Aggiorna portafoglio"):
    update_portfolio()

# Mostra le allocazioni di asset aggiornate
st.write("Allocazioni di asset aggiornate:")
for asset, allocation in asset_allocations.items():
    st.write(f"{asset}: {allocation}")

# Mostra il valore corrente del portafoglio aggiornato
st.write("Valore corrente del portafoglio aggiornato:")
current_value = 0
for asset, allocation in asset_allocations.items():
    current_value += asset_values[asset].iloc[0] * allocation
st.write(current_value)

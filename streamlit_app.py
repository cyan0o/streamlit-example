pip install requests
# Define a function to fetch the current price of an asset symbol
def get_asset_price(symbol):
    # Replace with your preferred API or web scraping technique
    url = f"https://www.tradingview.com/symbol/{symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    price_element = soup.find("span", class_="price")
    if price_element is None:
        return None

    price_text = price_element.text.strip()
    price = float(price_text.replace(",", ""))

    return price

# Imposta le allocazioni di asset target
asset_allocations = {
    "azioni": 0.3,
    "obbligazioni_lungo_termine": 0.4,
    "obbligazioni_medio_termine": 0.15,
    "materie_prime": 0.075,
    "oro": 0.075,
}

# Fetch the current price of each asset
asset_prices = {}
for symbol in asset_allocations.keys():
    asset_price = get_asset_price(symbol)
    if asset_price is not None:
        asset_prices[symbol] = asset_price
    else:
        print(f"Failed to fetch price for asset: {symbol}")

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
    if asset in asset_prices:
        current_value += asset_prices[asset] * allocation
    else:
        print(f"Skipping asset: {asset} due to missing price data")
st.write(current_value)

# Mostra le operazioni di Nancy Pelosi
st.write("Operazioni di Nancy Pelosi:")
operations = requests.get("https://api.sec.gov/historical/daily-insider/2023/07/20/congress/insider-trades.json").json()
for operation in operations:
    st.write(f"{operation['name']} ha acquistato {operation['amount']} azioni di {operation['ticker']} il {operation['date']}")

# Aggiorna il portafoglio
def update_portfolio():
    # Update the asset prices using the get_asset_price function
    for symbol in asset_allocations.keys():
        asset_prices[symbol] = get_asset_price(symbol)

    # Aggiorna le allocazioni di asset in base alle nuove operazioni
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
    if asset in asset_prices:
        current_value += asset_prices[asset] * allocation
    else:
        print(f"Skipping asset: {asset} due to missing price data")
st.write(current_value)

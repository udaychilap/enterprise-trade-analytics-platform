from faker import Faker
import pandas as pd
import random
import os
from datetime import datetime, timedelta

fake = Faker()

# ==========================================================
# Configuration
# ==========================================================

NUMBER_OF_TRADES = 5000

DATA_FOLDER = "data"
BRONZE_FOLDER = os.path.join(DATA_FOLDER, "bronze")
REFERENCE_FOLDER = os.path.join(DATA_FOLDER, "reference")

os.makedirs(BRONZE_FOLDER, exist_ok=True)
os.makedirs(REFERENCE_FOLDER, exist_ok=True)

# ==========================================================
# Reference Data
# ==========================================================

securities = [
    ("AAPL", "Technology", "NASDAQ", "USD", "Equity"),
    ("MSFT", "Technology", "NASDAQ", "USD", "Equity"),
    ("NVDA", "Technology", "NASDAQ", "USD", "Equity"),
    ("GOOGL", "Technology", "NASDAQ", "USD", "Equity"),
    ("META", "Technology", "NASDAQ", "USD", "Equity"),
    ("AMZN", "Consumer", "NASDAQ", "USD", "Equity"),
    ("TSLA", "Auto", "NASDAQ", "USD", "Equity"),
    ("JPM", "Financial", "NYSE", "USD", "Equity"),
    ("GS", "Financial", "NYSE", "USD", "Equity"),
    ("BAC", "Financial", "NYSE", "USD", "Equity"),
    ("WFC", "Financial", "NYSE", "USD", "Equity"),
    ("XOM", "Energy", "NYSE", "USD", "Equity"),
    ("CVX", "Energy", "NYSE", "USD", "Equity"),
    ("PFE", "Healthcare", "NYSE", "USD", "Equity"),
    ("JNJ", "Healthcare", "NYSE", "USD", "Equity")
]

portfolios = [
    ("Growth", "Aggressive"),
    ("Income", "Dividend"),
    ("ETF", "Passive"),
    ("Balanced", "Balanced"),
    ("Retirement", "Long Term")
]

brokers = [
    "Goldman Sachs",
    "JPMorgan",
    "Morgan Stanley",
    "Bank of America",
    "Citi",
    "UBS"
]

exchanges = [
    "NYSE",
    "NASDAQ",
    "CBOE"
]

# ==========================================================
# Save Reference Files
# ==========================================================

pd.DataFrame(
    securities,
    columns=[
        "Symbol",
        "Sector",
        "Exchange",
        "Currency",
        "AssetClass"
    ]
).to_csv(
    os.path.join(REFERENCE_FOLDER, "securities.csv"),
    index=False
)

pd.DataFrame(
    portfolios,
    columns=[
        "Portfolio",
        "Strategy"
    ]
).to_csv(
    os.path.join(REFERENCE_FOLDER, "portfolios.csv"),
    index=False
)

pd.DataFrame(
    brokers,
    columns=["Broker"]
).to_csv(
    os.path.join(REFERENCE_FOLDER, "brokers.csv"),
    index=False
)

pd.DataFrame(
    exchanges,
    columns=["Exchange"]
).to_csv(
    os.path.join(REFERENCE_FOLDER, "exchanges.csv"),
    index=False
)

# ==========================================================
# Generate Trades
# ==========================================================

records = []

symbols = [x[0] for x in securities]

for trade_id in range(1, NUMBER_OF_TRADES + 1):

    symbol = random.choice(symbols)

    security = next(s for s in securities if s[0] == symbol)

    trade_date = fake.date_between("-30d", "today")
    settle_date = trade_date + timedelta(days=2)

    quantity = random.choice([100, 200, 500, 1000])

    price = round(random.uniform(25, 500), 2)

    side = random.choice(["BUY", "SELL"])

    commission = round(price * quantity * 0.0005, 2)

    record = {

        "TradeID": trade_id,

        "Portfolio": random.choice(portfolios)[0],

        "Trader": fake.first_name(),

        "Symbol": symbol,

        "Quantity": quantity,

        "Price": price,

        "Side": side,

        "TradeDate": trade_date,

        "SettlementDate": settle_date,

        "Exchange": security[2],

        "Currency": security[3],

        "AssetClass": security[4],

        "Sector": security[1],

        "Broker": random.choice(brokers),

        "Counterparty": fake.company(),

        "Commission": commission

    }

    records.append(record)

# ==========================================================
# Inject Invalid Records
# ==========================================================

# Negative Price
records[10]["Price"] = -50

# Zero Quantity
records[20]["Quantity"] = 0

# Invalid Side
records[30]["Side"] = "TEST"

# Missing Trader
records[40]["Trader"] = None

# Missing Portfolio
records[50]["Portfolio"] = None

# Invalid Symbol
records[60]["Symbol"] = "XXXX"

# Duplicate Trade ID
duplicate = records[100].copy()
duplicate["TradeID"] = records[99]["TradeID"]
records.append(duplicate)

# ==========================================================
# Save Trades
# ==========================================================

df = pd.DataFrame(records)

df.to_csv(
    os.path.join(BRONZE_FOLDER, "trades.csv"),
    index=False
)

print("=" * 60)
print("Enterprise Trade Generator")
print("=" * 60)
print(f"Trades Generated : {len(df)}")
print(f"Security Master  : {len(securities)}")
print(f"Portfolios       : {len(portfolios)}")
print(f"Brokers          : {len(brokers)}")
print(f"Exchanges        : {len(exchanges)}")
print("=" * 60)
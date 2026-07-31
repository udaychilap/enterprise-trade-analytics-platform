from faker import Faker
import csv,random
from pathlib import Path

fake=Faker()
Path("data/bronze").mkdir(parents=True,exist_ok=True)
Path("data/reference").mkdir(parents=True,exist_ok=True)

symbols=[
("AAPL","Tech"),("MSFT","Tech"),("NVDA","Tech"),
("JPM","Financial"),("GS","Financial"),
("AMZN","Consumer"),("TSLA","Auto")
]

with open("data/reference/securities.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["Symbol","Sector"])
    w.writerows(symbols)

with open("data/bronze/trades.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["TradeID","Portfolio","Trader","Symbol","Quantity","Price","Side"])
    for i in range(1,5001):
        s,_=random.choice(symbols)
        w.writerow([
            i,
            random.choice(["Growth","Income","ETF"]),
            fake.first_name(),
            s,
            random.choice([100,200,500]),
            round(random.uniform(50,500),2),
            random.choice(["BUY","SELL"])
        ])
print("Sample data generated.")

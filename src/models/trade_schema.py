from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType,
    DateType
)

trade_schema = StructType([

    StructField("TradeID", IntegerType(), False),

    StructField("Portfolio", StringType(), True),

    StructField("Trader", StringType(), True),

    StructField("Symbol", StringType(), True),

    StructField("Quantity", IntegerType(), True),

    StructField("Price", DoubleType(), True),

    StructField("Side", StringType(), True),

    StructField("TradeDate", DateType(), True),

    StructField("SettlementDate", DateType(), True),

    StructField("Exchange", StringType(), True),

    StructField("Currency", StringType(), True),

    StructField("AssetClass", StringType(), True),

    StructField("Sector", StringType(), True),

    StructField("Broker", StringType(), True),

    StructField("Counterparty", StringType(), True),

    StructField("Commission", DoubleType(), True)

])
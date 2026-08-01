from pyspark.sql.types import *

trade_schema = StructType([
    StructField("TradeID", IntegerType(), False),
    StructField("Portfolio", StringType(), False),
    StructField("Trader", StringType(), False),
    StructField("Symbol", StringType(), False),
    StructField("Quantity", IntegerType(), False),
    StructField("Price", DoubleType(), False),
    StructField("Side", StringType(), False)
])
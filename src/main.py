from common.spark_session import get_spark
from pyspark.sql.functions import col,when,sum as _sum

spark=get_spark()

trades=spark.read.option("header",True).option("inferSchema",True).csv("data/bronze/trades.csv")
sec=spark.read.option("header",True).csv("data/reference/securities.csv")

df=trades.join(sec,"Symbol")
df=df.withColumn("Exposure",
    when(col("Side")=="BUY",col("Quantity")*col("Price"))
    .otherwise(-col("Quantity")*col("Price"))
)

print("Trade Count:",df.count())
df.groupBy("Portfolio").agg(_sum("Exposure").alias("NetExposure")).show()
spark.stop()

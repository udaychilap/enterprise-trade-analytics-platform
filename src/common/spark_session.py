from pyspark.sql import SparkSession

def get_spark():
    return (
        SparkSession.builder
        .master("local[*]")
        .appName("TradeAnalytics")
        .config("spark.sql.shuffle.partitions","8")
        .getOrCreate()
    )

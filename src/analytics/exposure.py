from pyspark.sql.functions import col
from pyspark.sql.functions import when
from pyspark.sql.functions import sum as _sum


class ExposureAnalytics:

    @staticmethod
    def calculate(df):

        return df.withColumn(
            "Exposure",
            when(
                col("Side") == "BUY",
                col("Quantity") * col("Price")
            ).otherwise(
                -col("Quantity") * col("Price")
            )
        )

    @staticmethod
    def portfolio(df):

        return (
            df.groupBy("Portfolio")
            .agg(_sum("Exposure").alias("NetExposure"))
        )
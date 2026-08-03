from pyspark.sql.functions import col, lit


class BusinessValidator:

    @staticmethod
    def validate(df):

        valid = df.filter(
            (col("Quantity") > 0) &
            (col("Price") > 0) &
            (col("Side").isin("BUY", "SELL")) &
            (col("Trader").isNotNull()) &
            (col("Portfolio").isNotNull())
        )

        invalid_price = (
            df.filter(col("Price") <= 0)
              .withColumn("RejectReason", lit("Negative Price"))
        )

        invalid_quantity = (
            df.filter(col("Quantity") <= 0)
              .withColumn("RejectReason", lit("Invalid Quantity"))
        )

        invalid_side = (
            df.filter(~col("Side").isin("BUY", "SELL"))
              .withColumn("RejectReason", lit("Invalid Side"))
        )

        invalid_trader = (
            df.filter(col("Trader").isNull())
              .withColumn("RejectReason", lit("Missing Trader"))
        )

        invalid_portfolio = (
            df.filter(col("Portfolio").isNull())
              .withColumn("RejectReason", lit("Missing Portfolio"))
        )

        invalid = (
            invalid_price
            .unionByName(invalid_quantity)
            .unionByName(invalid_side)
            .unionByName(invalid_trader)
            .unionByName(invalid_portfolio)
        )

        return valid, invalid
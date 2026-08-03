from pyspark.sql.functions import count, col


class DuplicateValidator:

    @staticmethod
    def validate(df):

        # Find duplicate TradeIDs
        duplicate_ids = (
            df.groupBy("TradeID")
              .agg(count("*").alias("cnt"))
              .filter(col("cnt") > 1)
        )

        # Duplicate records
        duplicate_df = df.join(
            duplicate_ids.select("TradeID"),
            "TradeID",
            "inner"
        )

        # Valid records (remove duplicates)
        clean_df = df.join(
            duplicate_ids.select("TradeID"),
            "TradeID",
            "left_anti"
        )

        return clean_df, duplicate_df
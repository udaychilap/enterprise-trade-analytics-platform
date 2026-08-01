from pyspark.sql.functions import count,col

class DuplicateValidator:
    @staticmethod
    def find_duplicates(df):
        return df.groupBy('TradeID').agg(count('*').alias('cnt')).filter(col('cnt')>1)

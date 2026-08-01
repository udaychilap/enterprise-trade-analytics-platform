from pyspark.sql.functions import col

class BusinessValidator:
    @staticmethod
    def validate(df):
        valid=df.filter((col('Quantity')>0)&(col('Price')>0)&(col('Side').isin('BUY','SELL')))
        invalid=df.subtract(valid)
        return valid,invalid

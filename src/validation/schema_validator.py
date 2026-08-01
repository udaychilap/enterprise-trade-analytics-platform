from pyspark.sql.functions import col

class SchemaValidator:
    @staticmethod
    def validate(df):
        valid=df.filter(
            col('TradeID').isNotNull() &
            col('Portfolio').isNotNull() &
            col('Trader').isNotNull() &
            col('Symbol').isNotNull() &
            col('Quantity').isNotNull() &
            col('Price').isNotNull() &
            col('Side').isNotNull()
        )
        invalid=df.subtract(valid)
        return valid,invalid

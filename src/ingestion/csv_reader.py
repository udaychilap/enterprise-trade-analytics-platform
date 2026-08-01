from models.trade_schema import trade_schema


class CSVReader:

    def __init__(self, spark):
        self.spark = spark

    def read_trades(self, path):

        return (
            self.spark.read
            .option("header", True)
            .schema(trade_schema)
            .csv(path)
        )

    def read_reference(self, path):

        return (
            self.spark.read
            .option("header", True)
            .csv(path)
        )
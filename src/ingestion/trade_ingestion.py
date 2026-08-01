from ingestion.csv_reader import CSVReader


class TradeIngestion:

    def __init__(self, spark):

        self.reader = CSVReader(spark)

    def load_trades(self, trade_path):

        return self.reader.read_trades(trade_path)

    def load_security_master(self, security_path):

        return self.reader.read_reference(security_path)
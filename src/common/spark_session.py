from pyspark.sql import SparkSession


class SparkManager:

    @staticmethod
    def get_spark():

        spark = (
            SparkSession.builder
            .master("local[*]")
            .appName("Enterprise Trade Analytics Platform")
            .config("spark.sql.shuffle.partitions", "8")
            .config("spark.driver.memory", "2g")
            .config("spark.executor.memory", "2g")
            .getOrCreate()
        )

        spark.sparkContext.setLogLevel("ERROR")

        return spark
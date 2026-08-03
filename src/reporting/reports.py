from pyspark.sql import DataFrame


class ReportPrinter:

    @staticmethod
    def print_header(title: str):

        print("\n" + "=" * 70)
        print(title)
        print("=" * 70)

    @staticmethod
    def audit(total, schema_failures, business_failures, duplicate_count):

        ReportPrinter.print_header("AUDIT REPORT")

        print(f"Input Trades      : {total}")
        print(f"Schema Failures   : {schema_failures}")
        print(f"Business Failures : {business_failures}")
        print(f"Duplicate Trades  : {duplicate_count}")

    @staticmethod
    def print_portfolio(df: DataFrame):

        ReportPrinter.print_header("PORTFOLIO EXPOSURE")

        df.show(truncate=False)

    @staticmethod
    def print_sector(df: DataFrame):

        ReportPrinter.print_header("SECTOR EXPOSURE")

        df.show(truncate=False)

    @staticmethod
    def print_trader(df: DataFrame):

        ReportPrinter.print_header("TRADER EXPOSURE")

        df.show(truncate=False)

    @staticmethod
    def print_security(df: DataFrame):

        ReportPrinter.print_header("TOP SECURITIES")

        df.show(truncate=False)
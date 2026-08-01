class ReportPrinter:

    @staticmethod
    def audit(total, schema_fail, business_fail, duplicates):

        print("\n" + "=" * 60)
        print("AUDIT REPORT")
        print("=" * 60)

        print(f"Input Trades      : {total}")
        print(f"Schema Failures   : {schema_fail}")
        print(f"Business Failures : {business_fail}")
        print(f"Duplicate Trades  : {duplicates}")

        print("=" * 60)

    @staticmethod
    def print_portfolio(df):

        print("\n" + "=" * 60)
        print("PORTFOLIO EXPOSURE")
        print("=" * 60)

        df.show(truncate=False)
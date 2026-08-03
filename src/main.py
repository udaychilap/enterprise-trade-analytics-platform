from common.spark_session import SparkManager
from common.constants import TRADE_FILE, SECURITY_FILE

from ingestion.trade_ingestion import TradeIngestion

from validation.schema_validator import SchemaValidator
from validation.business_validator import BusinessValidator
from validation.duplicate_validator import DuplicateValidator

from analytics.exposure import ExposureAnalytics
from reporting.reports import ReportPrinter

from analytics.sector import SectorAnalytics

def main():

    # ==========================================================
    # Create Spark Session
    # ==========================================================
    spark = SparkManager.get_spark()

    # ==========================================================
    # Load Data
    # ==========================================================
    ingestion = TradeIngestion(spark)

    trades = ingestion.load_trades(TRADE_FILE)
    securities = ingestion.load_security_master(SECURITY_FILE)

    print("\n" + "=" * 60)
    print("ENTERPRISE TRADE ANALYTICS PLATFORM")
    print("=" * 60)

    total_trades = trades.count()

    print(f"Input Trades : {total_trades}")

    # ==========================================================
    # Schema Validation
    # ==========================================================

    schema_valid, schema_invalid = SchemaValidator.validate(trades)

    schema_failures = schema_invalid.count()

    print(f"Schema Failures : {schema_failures}")

    # ==========================================================
    # Business Validation
    # ==========================================================

    business_valid, business_invalid = BusinessValidator.validate(schema_valid)

    business_failures = business_invalid.count()

    print(f"Business Failures : {business_failures}")

    # Save rejected trades
    (
        business_invalid.write
        .mode("overwrite")
        .option("header", True)
        .csv("data/rejects/rejected_trades")
    )

    # ==========================================================
    # Duplicate Validation
    # ==========================================================

    # duplicates = DuplicateValidator.find_duplicates(business_valid)

    #duplicate_count = duplicates.count()

    # print(f"Duplicate Trades : {duplicate_count}")

    clean_trades, duplicate_trades = DuplicateValidator.validate(
        business_valid
        )

    duplicate_count = duplicate_trades.count()

    print(f"Duplicate Trades : {duplicate_count}")

    duplicate_trades.write \
        .mode("overwrite") \
        .option("header", True) \
        .csv("data/rejects/duplicate_trades")

    print("\nDuplicate Trades")

    duplicate_trades.select(

        "TradeID",

        "Trader",

        "Portfolio",

        "Symbol"

    ).show(truncate=False)

    # ==========================================================
    # Join Security Master
    # ==========================================================

    trade_df = clean_trades.join(
        securities,
        "Symbol",
        "left"
    )

    # ==========================================================
    # Exposure Analytics
    # ==========================================================

    exposure_df = ExposureAnalytics.calculate(trade_df)

    portfolio_df = ExposureAnalytics.portfolio(exposure_df)
    sector_df = SectorAnalytics.exposure(exposure_df)

    # ==========================================================
    # Audit Report
    # ==========================================================

    ReportPrinter.audit(
        total_trades,
        schema_failures,
        business_failures,
        duplicate_count
    )

    print("\nRejected Trades")

    business_invalid.select(
        "TradeID",
        "RejectReason"
    ).show(20, False)

    # ==========================================================
    # Portfolio Exposure
    # ==========================================================

    ReportPrinter.print_portfolio(portfolio_df)

    spark.stop()


if __name__ == "__main__":
    main()
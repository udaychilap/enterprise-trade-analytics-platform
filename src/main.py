from common.spark_session import SparkManager
from common.constants import TRADE_FILE, SECURITY_FILE

from ingestion.trade_ingestion import TradeIngestion

from validation.schema_validator import SchemaValidator
from validation.business_validator import BusinessValidator
from validation.duplicate_validator import DuplicateValidator

from analytics.exposure import ExposureAnalytics
from reporting.reports import ReportPrinter


def main():

    # Create Spark Session
    spark = SparkManager.get_spark()

    # Load Data
    ingestion = TradeIngestion(spark)

    trades = ingestion.load_trades(TRADE_FILE)
    securities = ingestion.load_security_master(SECURITY_FILE)

    ####################################################
    # Input
    ####################################################

    total_trades = trades.count()

    print("\n" + "=" * 60)
    print("ENTERPRISE TRADE ANALYTICS PLATFORM")
    print("=" * 60)

    print(f"Input Trades : {total_trades}")

    ####################################################
    # Schema Validation
    ####################################################

    schema_valid, schema_invalid = SchemaValidator.validate(trades)

    ####################################################
    # Business Validation
    ####################################################

    business_valid, business_invalid = BusinessValidator.validate(schema_valid)

    ####################################################
    # Duplicate Detection
    ####################################################

    duplicates = DuplicateValidator.find_duplicates(business_valid)

    ####################################################
    # Join Security Master
    ####################################################

    trade_df = business_valid.join(securities, "Symbol")

    ####################################################
    # Analytics
    ####################################################

    exposure_df = ExposureAnalytics.calculate(trade_df)

    portfolio_df = ExposureAnalytics.portfolio(exposure_df)

    ####################################################
    # Audit Report
    ####################################################

    ReportPrinter.audit(
        total_trades,
        schema_invalid.count(),
        business_invalid.count(),
        duplicates.count()
    )

    ####################################################
    # Portfolio Report
    ####################################################

    ReportPrinter.print_portfolio(portfolio_df)

    spark.stop()


if __name__ == "__main__":
    main()
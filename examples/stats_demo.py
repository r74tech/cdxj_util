import os
import logging
from cdxj_util.core import CDXJCore
from cdxj_util.stats import CDXJStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_date(timestamp: str) -> str:
    return timestamp[:8]  # YYYYMMDD


def get_hour(timestamp: str) -> str:
    return timestamp[8:10]  # HH


def stats_demo(records):
    stats = CDXJStats(records)
    logger.info("\nCDXJ File Statistics:")
    total_records = stats.total_records()
    unique_urls = stats.unique_urls()
    logger.info(f"Total records: {total_records}")
    logger.info(f"Unique URLs: {unique_urls}")

    logger.info("\nSubdomain distribution:")
    subdomain_dist = stats.subdomain_distribution()
    for subdomain, count in subdomain_dist.items():
        if subdomain == "(root)":
            logger.info(f"  No subdomain: {count} records")
        else:
            logger.info(f"  {subdomain}.example.com: {count} records")

    logger.info("\nMIME type distribution:")
    mime_type_dist = stats.mime_type_distribution()
    for mime_type, count in mime_type_dist.items():
        logger.info(f"  {mime_type}: {count} records")

    logger.info("\nDate distribution:")
    date_dist = stats.distribution_by(get_date)
    for date, count in date_dist.items():
        logger.info(f"  {date}: {count} records")

    logger.info("\nHour distribution:")
    hour_dist = stats.distribution_by(get_hour)
    for hour, count in hour_dist.items():
        logger.info(f"  {hour}:00 - {int(hour)+1}:00: {count} records")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(current_dir, "..", "tests", "cdxj_util", "test.cdxj")

    core = CDXJCore(test_file_path)
    records = core.load_all_records()

    stats_demo(records)


if __name__ == "__main__":
    main()
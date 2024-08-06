import asyncio
import os
import logging
from cdxj_util.async_core import AsyncCDXJCore
from cdxj_util.stats import AsyncCDXJStats
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_date(timestamp: str) -> str:
    return timestamp[:8]  # YYYYMMDD


def get_hour(timestamp: str) -> str:
    return timestamp[8:10]  # HH


async def stats_demo(records):
    stats = AsyncCDXJStats(records)
    logger.info("\nCDXJ File Statistics:")
    total_records = await stats.total_records()
    unique_urls = await stats.unique_urls()
    logger.info(f"Total records: {total_records}")
    logger.info(f"Unique URLs: {unique_urls}")

    logger.info("\nSubdomain distribution:")
    subdomain_dist = await stats.subdomain_distribution()
    for subdomain, count in subdomain_dist.items():
        if subdomain == "(root)":
            logger.info(f"  No subdomain: {count} records")
        else:
            logger.info(f"  {subdomain}.example.com: {count} records")

    logger.info("\nMIME type distribution:")
    mime_type_dist = await stats.mime_type_distribution()
    for mime_type, count in mime_type_dist.items():
        logger.info(f"  {mime_type}: {count} records")

    logger.info("\nDate distribution:")
    date_dist = await stats.distribution_by(get_date)
    for date, count in date_dist.items():
        logger.info(f"  {date}: {count} records")

    logger.info("\nHour distribution:")
    hour_dist = await stats.distribution_by(get_hour)
    for hour, count in hour_dist.items():
        logger.info(f"  {hour}:00 - {int(hour)+1}:00: {count} records")


async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(current_dir, "..", "tests", "cdxj_util", "test.cdxj")

    async_core = AsyncCDXJCore(test_file_path)
    records = await async_core.load_all_records()

    await stats_demo(records)


if __name__ == "__main__":
    asyncio.run(main())
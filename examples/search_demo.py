import os
import logging
from cdxj_util.core import CDXJCore
from cdxj_util.search import CDXJSearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_demo(records):
    search = CDXJSearch(records)
    logger.info("\nSearch functionality demo:")

    url_pattern = "http://example.com/"
    url_results = search.search_by_url(url_pattern, exact_match=True)
    logger.info(
        f"Found {len(url_results)} records exactly matching URL '{url_pattern}':"
    )
    for url, timestamp in url_results[:5]:
        logger.info(f"  {url} - {timestamp}")

    url_pattern = r"http://example\.com/.*"
    url_results = search.search_by_url(url_pattern)
    logger.info(f"\nFound {len(url_results)} records matching pattern '{url_pattern}':")
    for url, timestamp in url_results[:10]:
        logger.info(f"  {url} - {timestamp}")
    if len(url_results) > 10:
        logger.info(f"  ... and {len(url_results) - 10} more")

    start_time = "20170306000000"
    end_time = "20170306235959"
    time_range_results = search.filter_by_timestamp_range(start_time, end_time)
    logger.info(
        f"\nFound {len(time_range_results)} records between {start_time} and {end_time}"
    )
    for url, timestamp in time_range_results[:5]:
        logger.info(f"  {url} - {timestamp}")
    if len(time_range_results) > 5:
        logger.info(f"  ... and {len(time_range_results) - 5} more")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(current_dir, "..", "tests", "cdxj_util", "test.cdxj")

    core = CDXJCore(test_file_path)
    records = core.load_all_records()

    search_demo(records)


if __name__ == "__main__":
    main()
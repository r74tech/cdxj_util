import asyncio
import os
import logging
from cdxj_util.async_core import AsyncCDXJCore
from cdxj_util.search import AsyncCDXJSearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def search_multiple_urls_demo(records):
    search = AsyncCDXJSearch(records)
    logger.info("\nMultiple URL search functionality demo:")

    url_list = [
        "http://example.com/",
        "http://example.com/page1",
        "http://sub.example.com/",
        "http://example.com/non-existent",
    ]

    logger.info(f"Searching for the following URLs: {url_list}")

    result_dict = await search.search_multiple_urls(url_list)

    for url, matches in result_dict.items():
        logger.info(f"\nResults for URL: {url}")
        logger.info(f"Found {len(matches)} matches:")
        for i, match in enumerate(matches, 1):
            logger.info(f"  Match {i}:")
            logger.info(f"    Timestamp: {match['timestamp']}")
            logger.info(f"    URL: {match['metadata'].get('url', 'N/A')}")
            logger.info(f"    MIME Type: {match['metadata'].get('mime', 'N/A')}")
            logger.info(f"    Status: {match['metadata'].get('status', 'N/A')}")

    not_found = set(url_list) - set(result_dict.keys())
    if not_found:
        logger.info("\nThe following URLs were not found:")
        for url in not_found:
            logger.info(f"  {url}")


async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(current_dir, "..", "tests", "cdxj_util", "test.cdxj")

    async_core = AsyncCDXJCore(test_file_path)
    records = await async_core.load_all_records()

    await search_multiple_urls_demo(records)


if __name__ == "__main__":
    asyncio.run(main())
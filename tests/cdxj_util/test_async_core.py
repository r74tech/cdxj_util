import asyncio
import pytest
import os
from cdxj_util.async_core import AsyncCDXJCore
from cdxj_util.exceptions import CDXJLoadError


@pytest.fixture
def test_cdxj_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "test.cdxj")


@pytest.mark.asyncio
async def test_async_load(test_cdxj_file):
    async_core = AsyncCDXJCore(test_cdxj_file)
    records = []
    async for batch in async_core.load(batch_size=10):
        records.extend(batch)

    assert len(records) == 40
    assert records[0].urlkey == "com,example)/"
    assert records[0].timestamp == "20170306040206"
    assert records[0].metadata["url"] == "http://example.com/"
    assert records[0].metadata["mime"] == "text/html"
    assert records[1].timestamp == "20170307040348"
    assert records[1].metadata["mime"] == "warc/revisit"

    assert records[-1].urlkey == "com,example)/"
    assert records[-1].timestamp == "20170306050000"
    assert records[-1].metadata == {
        "url": "http://example.com/",
        "mime": "text/html",
        "status": "200",
        "digest": "sha1:G7HRM7BGOKSKMSXZAHMUQTTV53QOFSMK",
        "length": "1240",
        "offset": "784",
        "filename": "example.warc.gz",
    }


@pytest.mark.asyncio
async def test_async_load_with_different_batch_sizes(test_cdxj_file):
    async_core = AsyncCDXJCore(test_cdxj_file)

    records_5 = []
    async for batch in async_core.load(batch_size=5):
        assert len(batch) <= 5
        records_5.extend(batch)

    records_20 = []
    async for batch in async_core.load(batch_size=20):
        assert len(batch) <= 20
        records_20.extend(batch)

    assert len(records_5) == len(records_20) == 40


@pytest.mark.asyncio
async def test_async_load_file_not_found():
    async_core = AsyncCDXJCore("non_existent_file.cdxj")
    with pytest.raises(CDXJLoadError, match="File not found"):
        async for _ in async_core.load():
            pass


@pytest.mark.asyncio
async def test_async_load_empty_file(tmp_path):
    empty_file = tmp_path / "empty.cdxj"
    empty_file.touch()
    async_core = AsyncCDXJCore(str(empty_file))
    records = []
    async for batch in async_core.load():
        records.extend(batch)

    assert len(records) == 0


@pytest.mark.asyncio
async def test_async_load_invalid_line(tmp_path):
    invalid_file = tmp_path / "invalid_test.cdxj"
    with open(invalid_file, "w") as f:
        f.write('com,example)/ 20170306040206 {"url": "http://example.com/"}\n')
        f.write("invalid line\n")
        f.write('com,example)/ 20170306040348 {"url": "http://example.com/"}\n')

    async_core = AsyncCDXJCore(str(invalid_file))
    records = []
    async for batch in async_core.load():
        records.extend(batch)

    assert len(records) == 2

@pytest.mark.asyncio
async def test_async_load_all_records(test_cdxj_file):
    async_core = AsyncCDXJCore(test_cdxj_file)
    records = await async_core.load_all_records()

    assert len(records) == 40
    assert records[0].urlkey == "com,example)/"
    assert records[0].timestamp == "20170306040206"
    assert records[0].metadata["url"] == "http://example.com/"
    assert records[-1].timestamp == "20170306050000"


@pytest.mark.asyncio
async def test_async_load_large_file(tmp_path):
    large_file = tmp_path / "large.cdxj"
    with open(large_file, "w") as f:
        for i in range(10000):
            f.write(
                f'com,example)/ 2017030604{i:04d} {{"url": "http://example.com/"}}\n'
            )

    async_core = AsyncCDXJCore(str(large_file))
    records = await async_core.load_all_records()

    assert len(records) == 10000
    assert records[0].timestamp == "20170306040000"
    assert records[-1].timestamp == "20170306049999"


if __name__ == "__main__":
    pytest.main([__file__])
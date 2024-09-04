import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pytest import FixtureRequest

from reinfolib.api_client import Client
from reinfolib.api_http_client import ApiHttpClient
from reinfolib.models import TransactionPrice


@pytest.fixture
def api_client() -> Client:
    mock_http_client = MagicMock(ApiHttpClient)
    return Client(http_client=mock_http_client)


@pytest.fixture
def xit001_01():
    file_path = Path(__file__).parent / "fixtures" / "XIT001_01.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def xit001_02():
    file_path = Path(__file__).parent / "fixtures" / "XIT001_02.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize(
    "fixture_name",
    [
        "xit001_01",
        "xit001_02",
    ],
)
def test_get_transaction_price_list(
    fixture_name, api_client: Client, request: FixtureRequest
):
    response_data = request.getfixturevalue(fixture_name)
    api_client._http_client.get_json = MagicMock(return_value=response_data)

    # 実行
    year = 2023
    area = "01"
    quarter = 1
    city = "12345"
    station = "678901"
    price_classification = "01"
    language = "en"
    options = {"headers": {"Content-Type": "application/json"}}

    result = api_client.get_transaction_price_list(
        year=year,
        area=area,
        quarter=quarter,
        city=city,
        station=station,
        price_classification=price_classification,
        language=language,
        options=options,
    )

    # 検証
    expected_result = [TransactionPrice(**item) for item in response_data["data"]]
    assert result == expected_result

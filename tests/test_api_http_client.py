from unittest.mock import MagicMock, patch

import pytest

from reinfolib.api_http_client import ApiHttpClient


@pytest.fixture
def api_client() -> ApiHttpClient:
    return ApiHttpClient(
        base_url="https://api.example.com",
        api_key="API_KEY",
        max_retries=3,
        http_connection_pool_size=10,
    )


@patch("reinfolib.api_http_client.requests.Session.get")
def test_get_json(mock_get: MagicMock, api_client: ApiHttpClient) -> None:
    mock_response: dict[str, str] = {
        "key1": "value1",
        "key2": "value2",
    }
    mock_get.return_value.json.return_value = mock_response

    request_path: str = "some-endpoint"
    url: str = f"https://api.example.com/{request_path}"
    params: dict[str, str] = {"param1": "value1", "param2": "value2"}
    options: dict[str, dict[str, str]] = {
        "headers": {"Content-Type": "application/json"}
    }

    result: dict[str, str] = api_client.get_json(
        request_path, params=params, options=options
    )

    mock_get.assert_called_once_with(
        url,
        params=params,
        headers={
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": "API_KEY",
        },
        timeout=30,
    )

    assert result == mock_response


@patch("reinfolib.api_http_client.requests.Session.get")
def test_get_content(mock_get: MagicMock, api_client: ApiHttpClient) -> None:
    mock_response = b"pbf-content"
    mock_get.return_value.content = mock_response

    request_path = "some-endpoint"
    url = f"https://api.example.com/{request_path}"
    params = {"response_format": "pbf"}
    options = {"headers": {"Accept": "application/x-protobuf"}}

    result = api_client.get_content(request_path, params=params, options=options)

    mock_get.assert_called_once_with(
        url,
        params=params,
        headers={
            "Accept": "application/x-protobuf",
            "Ocp-Apim-Subscription-Key": "API_KEY",
        },
        timeout=30,
    )

    assert result == mock_response

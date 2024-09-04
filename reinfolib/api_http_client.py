from typing import Optional, TypeVar

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_BASE_URL = "https://www.reinfolib.mlit.go.jp"


class ApiHttpClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        max_retries: int = 3,
        http_connection_pool_size: int = 10,
    ):
        self._api_key = api_key
        self._base_url = base_url
        self._max_retries = max_retries
        self._http_connection_pool_size = http_connection_pool_size
        self._session: Optional[requests.Session] = None

    def _make_url(self, request_path: str) -> str:
        return f"{self._base_url}/{request_path}"

    def _request_session(
        self,
        status_forcelist: Optional[list[int]] = None,
        allowed_methods: Optional[list[str]] = None,
    ) -> requests.Session:
        if status_forcelist is None:
            status_forcelist = [429, 500, 502, 503, 504]
        if allowed_methods is None:
            allowed_methods = ["HEAD", "GET", "OPTIONS", "POST"]

        if self._session is None:
            retry_strategy = Retry(
                total=self._max_retries,
                status_forcelist=status_forcelist,
                allowed_methods=allowed_methods,
            )

            adapter = HTTPAdapter(
                pool_connections=self._http_connection_pool_size,
                pool_maxsize=self._http_connection_pool_size,
                max_retries=retry_strategy,
            )
            self._session = requests.Session()
            self._session.mount("https://", adapter)

        return self._session

    def _with_auth_headers(self, headers: dict[str, str]) -> dict[str, str]:
        return {**headers, "Ocp-Apim-Subscription-Key": self._api_key}

    def get_json(
        self,
        request_path: str,
        params: Optional[dict] = None,
        options: Optional[dict] = None,
    ) -> dict:
        url = self._make_url(request_path)
        session = self._request_session()
        headers = (options or {}).get("headers", {})
        headers_with_auth = self._with_auth_headers(headers)
        response = session.get(
            url, params=params, headers=headers_with_auth, timeout=30
        )
        response.raise_for_status()
        return response.json()

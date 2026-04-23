import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from reinfolib.api_client import Client
from reinfolib.api_http_client import ApiHttpClient


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_json_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


@pytest.fixture
def api_client() -> Client:
    mock_http_client = MagicMock(ApiHttpClient)
    return Client(http_client=mock_http_client)


def test_get_urban_planning_zone_gis_list_supports_actual_pbf(api_client: Client) -> None:
    payload = (FIXTURES_DIR / "xkt001_actual.pbf").read_bytes()
    api_client._http_client.get_content = MagicMock(return_value=payload)

    result = api_client.get_urban_planning_zone_gis_list(
        z=11, x=1809, y=806, response_format="pbf"
    )

    api_client._http_client.get_content.assert_called_once_with(
        "/ex-api/external/XKT001",
        {"response_format": "pbf", "z": 11, "x": 1809, "y": 806},
        None,
    )
    assert result == payload


@pytest.mark.parametrize(
    (
        "method_name",
        "fixture_name",
        "kwargs",
        "request_path",
        "expected_params",
        "property_name",
        "expected_value",
    ),
    [
        (
            "get_liquefaction_tendency_gis_list",
            "xkt025_actual.json",
            {"z": 12, "x": 3657, "y": 1504},
            "/ex-api/external/XKT025",
            {"response_format": "geojson", "z": 12, "x": 3657, "y": 1504},
            "mesh_code",
            "6441437843",
        ),
        (
            "get_flood_inundation_assumption_area_gis_list",
            "xkt026_actual.json",
            {"z": 14, "x": 14550, "y": 6451},
            "/ex-api/external/XKT026",
            {"response_format": "geojson", "z": 14, "x": 14550, "y": 6451},
            "A31a_202",
            "神田川",
        ),
        (
            "get_storm_surge_inundation_assumption_area_gis_list",
            "xkt027_actual.json",
            {"z": 13, "x": 7210, "y": 3243},
            "/ex-api/external/XKT027",
            {"response_format": "geojson", "z": 13, "x": 7210, "y": 3243},
            "A49_001",
            "愛知県",
        ),
        (
            "get_tsunami_inundation_assumption_gis_list",
            "xkt028_actual.json",
            {"z": 14, "x": 14421, "y": 6486},
            "/ex-api/external/XKT028",
            {"response_format": "geojson", "z": 14, "x": 14421, "y": 6486},
            "A40_001",
            "愛知県",
        ),
        (
            "get_sediment_disaster_warning_area_gis_list",
            "xkt029_actual.json",
            {"z": 11, "x": 1819, "y": 806},
            "/ex-api/external/XKT029",
            {"response_format": "geojson", "z": 11, "x": 1819, "y": 806},
            "A33_005",
            "須和田3",
        ),
        (
            "get_urban_planning_road_gis_list",
            "xkt030_actual.json",
            {"z": 11, "x": 1819, "y": 806},
            "/ex-api/external/XKT030",
            {"response_format": "geojson", "z": 11, "x": 1819, "y": 806},
            "planning_road_ja",
            "都市計画道路",
        ),
        (
            "get_densely_inhabited_district_gis_list",
            "xkt031_actual.json",
            {"z": 11, "x": 1819, "y": 806, "administrative_area_code": "13101"},
            "/ex-api/external/XKT031",
            {
                "response_format": "geojson",
                "z": 11,
                "x": 1819,
                "y": 806,
                "administrativeAreaCode": "13101",
            },
            "A16_003",
            "千代田区",
        ),
        (
            "get_emergency_evacuation_site_gis_list",
            "xgt001_actual.json",
            {"z": 13, "x": 7272, "y": 3225},
            "/ex-api/external/XGT001",
            {"response_format": "geojson", "z": 13, "x": 7272, "y": 3225},
            "facility_name_ja",
            "井の頭コミュニティ・センター",
        ),
        (
            "get_disaster_history_geo_list",
            "xst001_actual.json",
            {"z": 11, "x": 1819, "y": 806, "disastertype_code": "11"},
            "/ex-api/external/XST001",
            {
                "response_format": "geojson",
                "z": 11,
                "x": 1819,
                "y": 806,
                "disastertype_code": "11",
                },
                "disaster_name_ja",
                "浸水域等",
            ),
    ],
)
def test_new_geo_api_methods_with_actual_fixtures(
    method_name: str,
    fixture_name: str,
    kwargs: dict,
    request_path: str,
    expected_params: dict,
    property_name: str,
    expected_value,
    api_client: Client,
) -> None:
    api_client._http_client.get_json = MagicMock(
        return_value=load_json_fixture(fixture_name)
    )

    method = getattr(api_client, method_name)
    result = method(**kwargs)

    api_client._http_client.get_json.assert_called_once_with(
        request_path, expected_params, None
    )
    assert len(result) == 1
    assert getattr(result[0].properties, property_name) == expected_value


def test_get_transaction_price_list_parses_actual_district_code(api_client: Client) -> None:
    api_client._http_client.get_json = MagicMock(return_value=load_json_fixture("xit001_actual.json"))

    result = api_client.get_transaction_price_list(year=2023, area="13")

    assert result[0].district_code == "131010030"


def test_get_appraisal_report_list_keeps_actual_extended_fields(api_client: Client) -> None:
    api_client._http_client.get_json = MagicMock(return_value=load_json_fixture("xct001_actual.json"))

    result = api_client.get_apraisal_report_list(year=2025, area="13", division="00")

    assert result[0].model_extra["比準価格算定内訳事例a 取引価格"] == "7600"
    assert result[0].model_extra["開発法価格算定内訳 建築工事費"] == "0"


def test_get_transaction_price_geo_list_parses_actual_extended_fields(api_client: Client) -> None:
    api_client._http_client.get_json = MagicMock(return_value=load_json_fixture("xpt001_actual.json"))

    result = api_client.get_transaction_price_geo_list(
        z=13, x=7312, y=3008, from_yyyyn="20223", to_yyyyn="20234"
    )

    props = result[0].properties
    assert props.land_type_name_ja == "中古マンション等"
    assert props.building_use_name_ja == "住宅"
    assert props.remark_name_ja is None


def test_get_land_valuation_geo_list_parses_actual_response_key(api_client: Client) -> None:
    api_client._http_client.get_json = MagicMock(return_value=load_json_fixture("xpt002_actual.json"))

    result = api_client.get_land_valuation_geo_list(z=13, x=7312, y=3008, year=2024)

    assert result[0].properties.proximity_to_transportation_facilitites == 0


def test_get_future_population_mesh_list_keeps_actual_year_specific_fields(api_client: Client) -> None:
    api_client._http_client.get_json = MagicMock(return_value=load_json_fixture("xkt013_actual.json"))

    result = api_client.get_future_population_mesh_list(z=11, x=1819, y=806)

    assert result[0].properties.model_extra["PT00_2025"] == 1577.4734
    assert result[0].properties.model_extra["HITOKU2025"] == ""


def test_get_num_of_station_passenger_list_parses_actual_2023_fields(api_client: Client) -> None:
    api_client._http_client.get_json = MagicMock(return_value=load_json_fixture("xkt015_actual.json"))

    result = api_client.get_num_of_station_passenger_list(z=11, x=1819, y=806)

    props = result[0].properties
    assert props.S12_001g == "003505"
    assert props.S12_054 == "2"
    assert props.S12_057 == 0

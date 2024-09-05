from typing import Optional, Type, TypeVar

import requests
from pydantic import TypeAdapter
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from reinfolib.api_http_client import ApiHttpClient

from .models import (
    AppraisalReport,
    DataAPIResponse,
    DisasterRiskAreaGISData,
    DistrictPlanningGISData,
    ElementarySchoolDistrictGIS,
    EmbankmentGISData,
    FirePreventionAreaGISData,
    FuturePopulationMeshData,
    GeoAPIResponseItem,
    HighUtilizationDistrictGISData,
    JuniorHighSchoolDistrictGISData,
    LandslidePreventionGISData,
    LandValuationGeo,
    LibraryGISData,
    MedicalFacilityGISData,
    Municipality,
    NaturalParkGSIData,
    PreschoolGISData,
    SchoolGISData,
    StationPassengerData,
    SteepSlopeHazardGISData,
    TownHallGISData,
    TransactionPrice,
    TransactionPriceGeo,
    UrbanPlanningLocationNormalizationGIS,
    UrbanPlanningUseDistrictGIS,
    UrbanPlanningZoneGIS,
    WelfareFacilityGISData,
)

T = TypeVar("T")


class Client:
    _base_url = "https://www.reinfolib.mlit.go.jp"
    _http_connection_pool_size = 10
    _max_retries = 3
    _http_client: ApiHttpClient

    @classmethod
    def create(cls, api_key: str):
        return Client(
            ApiHttpClient(
                api_key=api_key,
            )
        )

    def __init__(self, http_client: ApiHttpClient):
        self._http_client = http_client

    def get_transaction_price_list(
        self,
        year: int,
        area: Optional[str] = None,
        quarter: Optional[int] = None,
        city: Optional[str] = None,
        station: Optional[str] = None,
        price_classification: Optional[str] = None,
        language: Optional[str] = None,
        options: Optional[dict] = None,
    ) -> list[TransactionPrice]:
        """
        4. 不動産価格（取引価格・成約価格）情報取得API

        Attributes:
            price_classification (str, optional): 価格情報区分コード。形式は2桁の数字で指定します。
                - '01': 不動産取引価格情報のみ
                - '02': 成約価格情報のみ
                - 未指定: 不動産取引価格情報と成約価格情報の両方

            year (int): 取引時期（年）。形式は4桁の数字で指定します。2005年から指定可能です。
                2005年は第3四半期と第4四半期のみ指定可能です。

            quarter (int, optional): 取引時期（四半期）。形式は1桁の数字で、1～4のいずれかを指定します。
                - 1: 1月～3月
                - 2: 4月～6月
                - 3: 7月～9月
                - 4: 10月～12月

            area (str, optional): 都道府県コード。形式は2桁の数字で指定します。都道府県コードの詳細は「5. 都道府県内市区町村一覧取得API」の＜参考＞を参照。

            city (str, optional): 市区町村コード。形式は5桁の数字で指定します。全国地方公共団体コードの上5桁を指定します。

            station (str, optional): 駅コード。形式は6桁の数字で指定します。国土数値情報の駅データ（鉄道データの下位クラス）のグループコード（N02_005g）を指定します。
                詳細は以下のリンクを参照してください:
                https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_1.html

            language (str, optional): 出力結果の言語を指定します。
                - 'ja': 日本語
                - 'en': 英語
                - 未指定: 日本語
        """

        return self._get_data(
            request_path="/ex-api/external/XIT001",
            params={
                "year": year,
                "area": area,
                "quarter": quarter,
                "city": city,
                "station": station,
                "priceClassification": price_classification,
                "language": language,
            },
            options=options,
            cls=TransactionPrice,
        )

    def get_city_list(
        self, area: str, language: Optional[str] = None, options: Optional[dict] = None
    ) -> list[Municipality]:
        """
        5. 都道府県内市区町村一覧取得API

        Attributes:
            area (str): 都道府県コード。形式は2桁の数字で指定します。
                都道府県コードは2桁の数字で表されます。必須項目です。

            language (str, optional): 出力結果の言語を指定します。
                - 'ja': 日本語
                - 'en': 英語
                - 未指定: デフォルトで日本語が使用されます。
        """
        return self._get_data(
            request_path="/ex-api/external/XIT002",
            params={"area": area, "language": language},
            options=options,
            cls=Municipality,
        )

    def get_apraisal_report_list(
        self,
        year: int,
        area: str,
        division: str,
        options: Optional[dict] = None,
    ) -> list[AppraisalReport]:
        """
        6. 鑑定評価書情報API

        Attributes:
            year (int): 価格時点。形式は4桁の数字で西暦を指定します。必須項目です。

            area (str): 都道府県コード。形式は2桁の数字で指定します。必須項目です。
                都道府県コードの詳細は「5. 都道府県内市区町村一覧取得API」の参考を参照してください。

            division (str): 用途区分。形式は2桁の数字で指定します。必須項目です。
                - '00': 住宅地
                - '03': 宅地見込地
                - '05': 商業地
                - '07': 準工業地
                - '09': 工業地
                - '10': 調整区域内宅地
                - '13': 現況林地
                - '20': 林地（都道府県地価調査）
        """
        return self._get_data(
            request_path="/ex-api/external/XCT001",
            params={
                "year": year,
                "area": area,
                "division": division,
            },
            options=options,
            cls=AppraisalReport,
        )

    def get_transaction_price_geo_list(
        self,
        z: int,
        x: int,
        y: int,
        from_yyyyn: str,
        to_yyyyn: str,
        response_format: str = "geojson",
        price_classification: Optional[str] = None,
        land_type_code: Optional[str] = None,
        options: Optional[dict] = None,
    ) -> list[GeoAPIResponseItem[TransactionPriceGeo]]:
        """
        7. 不動産価格（取引価格・成約価格）情報のポイント (点) API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。必須項目です。

            x (int): タイル座標のX値。XYZ方式におけるタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式におけるタイルのY座標を指定します。必須項目です。

            from_ (str): 取引時期From。形式はYYYYN（数字5桁）で指定し、YYYYは西暦、Nは四半期（1～4）を表します。20053（平成17年第3四半期）以降で指定可能です。必須項目です。

            to (str): 取引時期To。形式はYYYYN（数字5桁）で指定し、YYYYは西暦、Nは四半期（1～4）を表します。20053（平成17年第3四半期）以降で指定可能です。必須項目です。

            price_classification (str, optional): 価格情報区分コード。形式は2桁の数字で指定します。
                - '01': 不動産取引価格情報のみ
                - '02': 成約価格情報のみ
                - 未指定: 不動産取引価格情報と成約価格情報の両方

            land_type_code (str, optional): 種類コード。形式は2桁の数字で指定し、土地の種類を選択します。
                - '01': 宅地（土地）
                - '02': 宅地（土地と建物）
                - '07': 中古マンション等
                - '10': 農地
                - '11': 林地
                - 未指定: すべて
                ※複数指定する場合は、「landTypeCode=01,02,07」のようにカンマ区切りで指定します。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XPT001",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
                "from": from_yyyyn,
                "to": to_yyyyn,
                "priceClassification": price_classification,
                "landTypeCode": land_type_code,
            },
            options=options,
            cls=TransactionPriceGeo,
        )

    def get_land_valuation_geo_list(
        self,
        z: int,
        x: int,
        y: int,
        year: int,
        response_format: str = "geojson",
        price_classification: Optional[str] = None,
        use_category_code: Optional[str] = None,
    ) -> list[GeoAPIResponseItem[LandValuationGeo]]:
        """
        8. 地価公示・地価調査のポイント（点）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。13から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。必須項目です。

            x (int): タイル座標のX値。XYZ方式におけるタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式におけるタイルのY座標を指定します。必須項目です。

            year (int): 対象年。形式は4桁の数字で1970年から最新年（2024年）までのいずれかを指定します。必須項目です。

            price_classification (str, optional): 地価情報区分コード。形式は1桁の数字で指定します。
                - '0': 国土交通省地価公示のみ
                - '1': 都道府県地価調査のみ
                - 未指定: 国土交通省地価公示と都道府県地価調査の両方

            use_category_code (str, optional): 用途区分コード。形式は2桁の数字で指定し、土地の用途を選択します。
                - '00': 住宅地
                - '03': 宅地見込地
                - '05': 商業地
                - '07': 準工業地
                - '09': 工業地
                - '10': 市街地調整区域内の現況宅地
                - '13': 市街地調整区域内の現況林地（国土交通省地価公示のみ）
                - '20': 林地（都道府県地価調査のみ）
                - 未指定: すべて
                ※複数指定する場合は、「useCategoryCode=00,03,05」のようにカンマ区切りで指定します。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XPT002",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
                "year": year,
                "priceClassification": price_classification,
                "useCategoryCode": use_category_code,
            },
            cls=LandValuationGeo,
        )

    def get_urban_planning_zone_gis_list(
        self,
        z: int,
        x: int,
        y: int,
    ) -> list[GeoAPIResponseItem[UrbanPlanningZoneGIS]]:
        """
        9. 都市計画決定GISデータ（都市計画区域/区域区分）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが大きいほどカバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式におけるタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式におけるタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT001",
            params={
                "response_format": "geojson",
                "z": z,
                "x": x,
                "y": y,
            },
            cls=UrbanPlanningZoneGIS,
        )

    def get_urban_planning_use_district_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[UrbanPlanningUseDistrictGIS]]:
        """
        10. 都市計画決定GISデータ（用途地域）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが大きいほどカバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式におけるタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式におけるタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT002",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=UrbanPlanningUseDistrictGIS,
        )

    def get_urban_planning_location_normalization_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[UrbanPlanningLocationNormalizationGIS]]:
        """
        11. 都市計画決定GISデータ（立地適正化計画区域）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが高いほど、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式におけるタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式におけるタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT003",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=UrbanPlanningLocationNormalizationGIS,
        )

    def get_elementary_school_district_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
        administrative_area_code: Optional[str] = None,
    ) -> list[GeoAPIResponseItem[ElementarySchoolDistrictGIS]]:
        """
        12. 国土数値情報（小学校区）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが高いほど、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式におけるタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式におけるタイルのY座標を指定します。必須項目です。

            administrative_area_code (str): 行政区域コード。形式は5桁の数字で指定します。複数のコードを指定する場合は、カンマ区切りで指定します。
                例: '13101,13102'
                詳細については、次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx
        """

        params = {
            "response_format": response_format,
            "z": z,
            "x": x,
            "y": y,
            "administrativeAreaCode": administrative_area_code,
        }
        return self._get_geo_data(
            request_path="/ex-api/external/XKT004",
            params=params,
            cls=ElementarySchoolDistrictGIS,
        )

    def get_junior_high_school_district_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
        administrative_area_code: Optional[str] = None,
    ) -> list[GeoAPIResponseItem[JuniorHighSchoolDistrictGISData]]:
        """
        13. 国土数値情報（中学校区）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが高いほど、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式におけるタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式におけるタイルのY座標を指定します。必須項目です。

            administrative_area_code (str): 行政区域コード。形式は5桁の数字で指定します。複数の行政区域を指定する場合は、カンマ区切りで指定します。
                例: '13101,13102'。詳細については、次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx
        """

        params = {
            "response_format": response_format,
            "z": z,
            "x": x,
            "y": y,
            "administrativeAreaCode": administrative_area_code,
        }
        return self._get_geo_data(
            request_path="/ex-api/external/XKT005",
            params=params,
            cls=JuniorHighSchoolDistrictGISData,
        )

    def get_school_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[SchoolGISData]]:
        """
        14. 国土数値情報（学校）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。13から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが高いほどカバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式におけるタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式におけるタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT006",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=SchoolGISData,
        )

    def get_preschool_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[PreschoolGISData]]:
        """
        15. 国土数値情報（保育園・幼稚園等）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。13から15までの範囲で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが高いほどカバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式におけるタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式におけるタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT007",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=PreschoolGISData,
        )

    def get_medical_facility_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[MedicalFacilityGISData]]:
        """
        16. 国土数値情報（医療機関）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。13から15までの値で指定します。値が大きいほど詳細なズームレベルとなり、カバーする地理的領域が狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT010",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=MedicalFacilityGISData,
        )

    def get_welfare_facility_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
        administrative_area_code: Optional[str] = None,
        welfare_facility_class_code: Optional[str] = None,
        welfare_facility_middle_class_code: Optional[str] = None,
        welfare_facility_minor_class_code: Optional[str] = None,
    ) -> list[GeoAPIResponseItem[WelfareFacilityGISData]]:
        """
        17. 国土数値情報（福祉施設）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。13から15までの値で指定し、値が大きいほど詳細なズームレベルとなり、カバーする地理的領域が狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。

            administrative_area_code (str): 行政区域コード。形式は5桁の数字で指定します。複数の行政区域を指定する場合は、カンマ区切りで指定します。
                例: '13101,13102'。詳細は、次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx

            welfare_facility_class_code (str): 福祉施設大分類コード。形式は2桁の数字で指定します。複数の施設コードを指定する場合は、カンマ区切りで指定します。
                例: '01,02'。詳細は、次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/welfareInstitution_welfareFacilityMajorClassificationCode.html

            welfare_facility_middle_class_code (str): 福祉施設中分類コード。形式は4桁の数字で指定します。複数の施設コードを指定する場合は、カンマ区切りで指定します。
                例: '0101,0201'。詳細は、次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/welfareInstitution_welfareFacilityMiddleClassificationCode.html

            welfare_facility_minor_class_code (str): 福祉施設小分類コード。形式は6桁の数字で指定します。複数の施設コードを指定する場合は、カンマ区切りで指定します。
                例: '020101,020102'。詳細は、次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/welfareInstitution_welfareFacilityMinorClassificationCode.html
        """

        params = {
            "response_format": response_format,
            "z": z,
            "x": x,
            "y": y,
            "administrativeAreaCode": administrative_area_code,
            "welfareFacilityClassCode": welfare_facility_class_code,
            "welfareFacilityMiddleClassCode": welfare_facility_middle_class_code,
            "welfareFacilityMinorClassCode": welfare_facility_minor_class_code,
        }
        return self._get_geo_data(
            request_path="/ex-api/external/XKT011",
            params=params,
            cls=WelfareFacilityGISData,
        )

    def get_future_population_mesh_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[FuturePopulationMeshData]]:
        """
        18. 国土数値情報（将来推計人口500mメッシュ）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほど詳細なズームレベルとなり、カバーする地理的領域が狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT013",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=FuturePopulationMeshData,
        )

    def get_fire_prevention_area_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[FirePreventionAreaGISData]]:
        """
        19. 都市計画決定GISデータ（防火・準防火地域）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほどズームレベルが高くなります。ズームレベルが高いほど、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT014",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=FirePreventionAreaGISData,
        )

    def get_num_of_station_passenger_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[StationPassengerData]]:
        """
        20. 国土数値情報（駅別乗降客数）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定します。ズームレベルが大きいほど、カバーする地理的領域は狭くなりますが、より詳細な情報が提供されます。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づいてタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づいてタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT015",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=StationPassengerData,
        )

    def get_disaster_risk_area_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
        administrative_area_code: Optional[str] = None,
    ) -> list[GeoAPIResponseItem[DisasterRiskAreaGISData]]:
        """
        21. 国土数値情報（災害危険区域）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定します。ズームレベルが大きいほど詳細な地図が表示され、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づいてタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づいてタイルのY座標を指定します。必須項目です。

            administrative_area_code (str): 代表行政コード。形式は5桁の数字で指定します。複数の行政区域を指定する場合は、カンマ区切りで指定します。
                例: '13101,13102'。詳細については、次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx
        """

        params = {
            "response_format": response_format,
            "z": z,
            "x": x,
            "y": y,
            "administrativeAreaCode": administrative_area_code,
        }
        return self._get_geo_data(
            request_path="/ex-api/external/XKT016",
            params=params,
            cls=DisasterRiskAreaGISData,
        )

    def get_library_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
        administrative_area_code: Optional[str] = None,
    ) -> list[GeoAPIResponseItem[LibraryGISData]]:
        """
        22. 国土数値情報（図書館）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。13から15までの値で指定し、値が大きいほどズームレベルが高くなります。ズームレベルが高いほど、カバーする地理的領域が狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。

            administrative_area_code (str): 行政区域コード。形式は5桁の数字で指定します。複数の行政区域を指定する場合は、カンマ区切りで指定します。
                例: '13101,13102'。詳細については、次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx
        """

        params = {
            "response_format": response_format,
            "z": z,
            "x": x,
            "y": y,
            "administrativeAreaCode": administrative_area_code,
        }
        return self._get_geo_data(
            request_path="/ex-api/external/XKT017",
            params=params,
            cls=LibraryGISData,
        )

    def get_town_hall_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
        administrative_area_code: Optional[str] = None,
    ) -> list[GeoAPIResponseItem[TownHallGISData]]:
        """
        23. 国土数値情報（市区町村村役場及び集会施設等）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。13から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが高いほど、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。
        """

        params = {
            "response_format": response_format,
            "z": z,
            "x": x,
            "y": y,
            "administrativeAreaCode": administrative_area_code,
        }
        return self._get_geo_data(
            request_path="/ex-api/external/XKT018",
            params=params,
            cls=TownHallGISData,
        )

    def get_natural_park_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        prefecture_code: Optional[str] = None,
        district_code: Optional[str] = None,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[NaturalParkGSIData]]:
        """
        24. 国土数値情報（自然公園地域）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。9から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが高いほど、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。

            prefecture_code (str): 都道府県コード。1桁または2桁の数字で指定します。1（北海道）～47（沖縄県）の範囲内で指定可能です。複数の都道府県を指定する場合はカンマ区切りで指定します。1桁目が0の場合は、0を取り除いた値を使用します。
                例: 'prefectureCode=13,14'。詳細は次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html

            district_code (str): 地区コード。振興局区域を一意に識別するためのコードで、1桁または2桁の数字で指定します。複数の地区を指定する場合はカンマ区切りで指定します。1桁目が0の場合は、0を取り除いた値を使用します。
                例: 'districtCode=9,10'。詳細は次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/SubprefectureNameCd.html
        """

        params = {
            "response_format": response_format,
            "z": z,
            "x": x,
            "y": y,
            "prefectureCode": prefecture_code,
            "districtCode": district_code,
        }
        return self._get_geo_data(
            request_path="/ex-api/external/XKT019",
            params=params,
            cls=NaturalParkGSIData,
        )

    def get_embankment_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[EmbankmentGISData]]:
        """
        25. 国土数値情報（大規模盛土造成地マップ）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが高いほど、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT020",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=EmbankmentGISData,
        )

    def get_landslide_prevention_district_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        prefecture_code: Optional[str] = None,
        administrative_area_code: Optional[str] = None,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[LandslidePreventionGISData]]:
        """
        26. 国土数値情報（地すべり防止地区）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの値で指定し、値が大きいほど詳細なズームレベルを表します。ズームレベルが高いほど、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。

            prefecture_code (str): 都道府県コード。形式は2桁の数字で指定し、複数の都道府県を指定する場合はカンマ区切りで指定します。
                例: 'prefectureCode=13,14'。詳細は次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html

            administrative_area_code (str): 行政コード。形式は5桁の数字で指定し、複数の行政区域を指定する場合はカンマ区切りで指定します。
                例: 'administrativeAreaCode=13101,13102'。詳細は次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx
        """

        params = {
            "response_format": response_format,
            "z": z,
            "x": x,
            "y": y,
            "prefectureCode": prefecture_code,
            "administrativeAreaCode": administrative_area_code,
        }
        return self._get_geo_data(
            request_path="/ex-api/external/XKT021",
            params=params,
            cls=LandslidePreventionGISData,
        )

    def get_steep_slope_hazard_district_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        prefecture_code: Optional[str] = None,
        administrative_area_code: Optional[str] = None,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[SteepSlopeHazardGISData]]:
        """
        27. 国土数値情報（急傾斜地崩壊危険区域）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの範囲で指定可能です。値が大きいほど詳細なズームレベルを表し、カバーする地理的領域が狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づきタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づきタイルのY座標を指定します。必須項目です。

            prefecture_code (str): 都道府県コード。形式は2桁の数字で指定します。複数の都道府県を指定する場合はカンマ区切りで指定します。
                例: 'prefectureCode=13,14'。詳細は次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html

            administrative_area_code (str): 行政コード。形式は5桁の数字で指定します。複数の行政区域を指定する場合はカンマ区切りで指定します。
                例: 'administrativeAreaCode=13101,13102'。詳細は次のリンクを参照してください: https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx
        """

        params = {
            "response_format": response_format,
            "z": z,
            "x": x,
            "y": y,
            "prefectureCode": prefecture_code,
            "administrativeAreaCode": administrative_area_code,
        }
        return self._get_geo_data(
            request_path="/ex-api/external/XKT022",
            params=params,
            cls=SteepSlopeHazardGISData,
        )

    def get_district_planning_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[DistrictPlanningGISData]]:
        """
        28. 都市計画決定GISデータ（地区計画）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの範囲で指定可能です。値が大きいほどズームレベルが高くなり、カバーする地理的領域が狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づいてタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づいてタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT023",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=DistrictPlanningGISData,
        )

    def get_high_utilization_district_gis_list(
        self,
        z: int,
        x: int,
        y: int,
        response_format: str = "geojson",
    ) -> list[GeoAPIResponseItem[HighUtilizationDistrictGISData]]:
        """
        29. 都市計画決定GISデータ（高度利用地区）API

        Attributes:
            response_format (str): 応答形式。GeoJSON応答またはバイナリベクトルタイル応答を指定します。必須項目です。
                - 'geojson': GeoJSON応答
                - 'pbf': バイナリベクトルタイル応答

            z (int): ズームレベル（縮尺）。11から15までの範囲で指定可能です。値が大きいほどズームレベルが高くなり、カバーする地理的領域は狭くなります。必須項目です。

            x (int): タイル座標のX値。XYZ方式に基づいてタイルのX座標を指定します。必須項目です。

            y (int): タイル座標のY値。XYZ方式に基づいてタイルのY座標を指定します。必須項目です。
        """

        return self._get_geo_data(
            request_path="/ex-api/external/XKT024",
            params={
                "response_format": response_format,
                "z": z,
                "x": x,
                "y": y,
            },
            cls=HighUtilizationDistrictGISData,
        )

    def _get_data(
        self,
        request_path: str,
        cls: Type[T],
        params: Optional[dict] = None,
        options: Optional[dict] = None,
    ) -> list[T]:
        resp = DataAPIResponse[T](
            **self._http_client.get_json(request_path, params, options)
        )
        return [cls(**d) for d in resp.data]

    def _get_geo_data(
        self,
        request_path: str,
        cls: Type[T],
        params: Optional[dict] = None,
        options: Optional[dict] = None,
    ) -> list[GeoAPIResponseItem[T]]:
        raw_resp = self._http_client.get_json(request_path, params, options)
        return TypeAdapter(list[GeoAPIResponseItem[T]]).validate_python(
            [{**f, "properties": cls(**f["properties"])} for f in raw_resp["features"]]
        )

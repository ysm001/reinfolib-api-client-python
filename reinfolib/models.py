from dataclasses import dataclass
from typing import Generic, Literal, Optional, TypedDict, TypeVar, Union, cast

from pydantic import BaseModel, Field, conint, field_validator, model_validator

T = TypeVar("T")


@dataclass
class DataAPIResponse(Generic[T]):
    status: str
    data: list[T]


class Geometry(BaseModel):
    type: Literal["Point", "LineString", "Polygon", "MultiPolygon"]
    coordinates: Union[
        list[float],
        list[list[float]],
        list[list[list[float]]],
        list[list[list[list[float]]]],
    ]

    @model_validator(mode="before")
    @classmethod
    def check_coordinates(cls, values):
        geometry_type = values.get("type")
        coordinates = values.get("coordinates")

        def is_all_list(l: object, max_depth=1, depth=0) -> bool:
            if depth >= max_depth:
                return isinstance(l, float)

            if not isinstance(l, list):
                return False

            if len(l) == 0:
                return True

            return is_all_list(l[0], max_depth, depth + 1)

        if geometry_type == "Point" and not is_all_list(coordinates, 1):
            raise ValueError("For 'Point', coordinates must be a list of floats.")
        if geometry_type == "LineString" and not is_all_list(coordinates, 2):
            raise ValueError("For 'LineString', coordinates must be a list of floats.")
        elif geometry_type == "Polygon" and not is_all_list(coordinates, 3):
            raise ValueError(
                "For 'Polygon', coordinates must be a list[list[list[float]]]."
            )
        elif geometry_type == "MultiPolygon" and not is_all_list(coordinates, 4):
            raise ValueError(
                "For 'MultiPolygon', coordinates must be a list[list[list[list[float]]]]."
            )

        return values


class GeoAPIResponseItem(BaseModel, Generic[T]):
    type: str
    geometry: Geometry
    properties: T


class GeoAPIResponse(BaseModel, Generic[T]):
    type: str
    name: list[str]
    crs: dict
    features: list[GeoAPIResponseItem[T]]


class FeatureAPIResponse(TypedDict):
    type: str
    name: list[str]


class PropertyBaseModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

    class Config:
        populate_by_name = True


class TransactionPrice(PropertyBaseModel):
    type_: str = Field(..., alias="Type", description="取引の種類")
    region: Optional[str] = Field(None, alias="Region", description="地区")
    municipality_code: Optional[str] = Field(
        None, alias="MunicipalityCode", description="市区町村コード"
    )
    prefecture: Optional[str] = Field(
        None, alias="Prefecture", description="都道府県名"
    )
    municipality: Optional[str] = Field(
        None, alias="Municipality", description="市区町村名"
    )
    district_name: Optional[str] = Field(
        None, alias="DistrictName", description="地区名"
    )
    trade_price: Optional[int] = Field(
        None, alias="TradePrice", description="取引価格（総額）"
    )
    price_per_unit: Optional[int] = Field(
        None, alias="PricePerUnit", description="坪単価"
    )
    floor_plan: Optional[str] = Field(None, alias="FloorPlan", description="間取り")
    area: Optional[float] = Field(
        None, alias="Area", description="面積（平方メートル）"
    )
    unit_price: Optional[float] = Field(
        None, alias="UnitPrice", description="取引価格（平方メートル単価）"
    )
    land_shape: Optional[str] = Field(None, alias="LandShape", description="土地の形状")
    frontage: Optional[float] = Field(None, alias="Frontage", description="間口")
    total_floor_area: Optional[float] = Field(
        None, alias="TotalFloorArea", description="延床面積（平方メートル）"
    )
    building_year: Optional[str] = Field(
        None, alias="BuildingYear", description="建築年"
    )
    structure: Optional[str] = Field(None, alias="Structure", description="建物の構造")
    use: Optional[str] = Field(None, alias="Use", description="用途")
    purpose: Optional[str] = Field(None, alias="Purpose", description="今後の利用目的")
    direction: Optional[str] = Field(
        None, alias="Direction", description="前面道路：方位"
    )
    classification: Optional[str] = Field(
        None, alias="Classification", description="前面道路：種類"
    )
    breadth: Optional[float] = Field(
        None, alias="Breadth", description="前面道路：幅員（m）"
    )
    city_planning: Optional[str] = Field(
        None, alias="CityPlanning", description="都市計画"
    )
    coverage_ratio: Optional[float] = Field(
        None, alias="CoverageRatio", description="建蔽率（%）"
    )
    floor_area_ratio: Optional[float] = Field(
        None, alias="FloorAreaRatio", description="容積率（%）"
    )
    period: Optional[str] = Field(None, alias="Period", description="取引時点")
    renovation: Optional[str] = Field(None, alias="Renovation", description="改装")
    remarks: Optional[str] = Field(None, alias="Remarks", description="取引の事情等")
    price_category: str = Field(
        ..., alias="PriceCategory", description="価格情報のカテゴリ"
    )


class PropertyAppraisalReport(PropertyBaseModel):
    価格時点: Optional[str] = None
    標準地番号_市区町村コード_県コード: Optional[str] = Field(
        None, alias="標準地番号 市区町村コード 県コード"
    )
    標準地番号_市区町村コード_市区町村コード: Optional[str] = Field(
        None, alias="標準地番号 市区町村コード 市区町村コード"
    )
    標準地番号_地域名: Optional[str] = Field(None, alias="標準地番号 地域名")
    標準地番号_用途区分: Optional[str] = Field(None, alias="標準地番号 用途区分")
    標準地番号_連番: Optional[str] = Field(None, alias="標準地番号 連番")
    一平米当たりの価格: Optional[float] = Field(None, alias="1㎡当たりの価格")
    路線価_年: Optional[int] = Field(None, alias="路線価 年")
    路線価_相続税路線価: Optional[float] = Field(None, alias="路線価 相続税路線価")
    路線価_倍率: Optional[float] = Field(None, alias="路線価 倍率")
    路線価_倍率種別: Optional[str] = Field(None, alias="路線価 倍率種別")
    標準地_所在地_所在地番: Optional[str] = Field(None, alias="標準地 所在地 所在地番")
    標準地_所在地_住居表示: Optional[str] = Field(None, alias="標準地 所在地 住居表示")
    標準地_所在地_仮換地番号: Optional[str] = Field(
        None, alias="標準地 所在地 仮換地番号"
    )
    標準地_地積_地積: Optional[float] = Field(None, alias="標準地 地積 地積")
    標準地_地積_内私道分: Optional[float] = Field(None, alias="標準地 地積 内私道分")
    標準地_形状_形状: Optional[str] = Field(None, alias="標準地 形状 形状")
    標準地_形状_形状比_間口: Optional[float] = Field(
        None, alias="標準地 形状 形状比 間口"
    )
    標準地_形状_形状比_奥行: Optional[float] = Field(
        None, alias="標準地 形状 形状比 奥行"
    )
    標準地_形状_方位: Optional[str] = Field(None, alias="標準地 形状 方位")
    標準地_形状_平坦: Optional[str] = Field(None, alias="標準地 形状 平坦")
    標準地_形状_傾斜度: Optional[float] = Field(None, alias="標準地 形状 傾斜度")
    標準地_土地利用の現況_現況: Optional[str] = Field(
        None, alias="標準地 土地利用の現況 現況"
    )
    標準地_土地利用の現況_構造: Optional[str] = Field(
        None, alias="標準地 土地利用の現況 構造"
    )
    標準地_土地利用の現況_地上階数: Optional[int] = Field(
        None, alias="標準地 土地利用の現況 地上階数"
    )
    標準地_土地利用の現況_地下階数: Optional[int] = Field(
        None, alias="標準地 土地利用の現況 地下階数"
    )
    標準地_周辺の利用状況: Optional[str] = Field(None, alias="標準地 周辺の利用状況")
    標準地_接面道路の状況_前面道路_方位: Optional[str] = Field(
        None, alias="標準地 接面道路の状況 前面道路 方位"
    )
    標準地_接面道路の状況_前面道路_駅前区分: Optional[str] = Field(
        None, alias="標準地 接面道路の状況 前面道路 駅前区分"
    )
    標準地_接面道路の状況_前面道路_高低位置: Optional[str] = Field(
        None, alias="標準地 接面道路の状況 前面道路 高低位置"
    )
    標準地_接面道路の状況_前面道路_道路幅員: Optional[float] = Field(
        None, alias="標準地 接面道路の状況 前面道路 道路幅員"
    )
    標準地_接面道路の状況_前面道路_舗装状況: Optional[str] = Field(
        None, alias="標準地 接面道路の状況 前面道路 舗装状況"
    )
    標準地_接面道路の状況_前面道路_道路種別: Optional[str] = Field(
        None, alias="標準地 接面道路の状況 前面道路 道路種別"
    )
    標準地_接面道路の状況_側道方位: Optional[str] = Field(
        None, alias="標準地 接面道路の状況 側道方位"
    )
    標準地_接面道路の状況_側道等接面状況: Optional[str] = Field(
        None, alias="標準地 接面道路の状況 側道等接面状況"
    )
    標準地_供給処理施設_水道: Optional[int] = Field(
        None, alias="標準地 供給処理施設 水道"
    )
    標準地_供給処理施設_ガス: Optional[int] = Field(
        None, alias="標準地 供給処理施設 ガス"
    )
    標準地_供給処理施設_下水道: Optional[int] = Field(
        None, alias="標準地 供給処理施設 下水道"
    )
    標準地_交通施設の状況_交通施設: Optional[str] = Field(
        None, alias="標準地 交通施設の状況 交通施設"
    )
    標準地_交通施設の状況_距離: Optional[float] = Field(
        None, alias="標準地 交通施設の状況 距離"
    )
    標準地_交通施設の状況_近接区分: Optional[str] = Field(
        None, alias="標準地 交通施設の状況 近接区分"
    )
    標準地_法令上の規制等_区域区分: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 区域区分"
    )
    標準地_法令上の規制等_用途地域: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 用途地域"
    )
    標準地_法令上の規制等_指定建ぺい率: Optional[int] = Field(
        None, alias="標準地 法令上の規制等 指定建ぺい率"
    )
    標準地_法令上の規制等_指定容積率: Optional[int] = Field(
        None, alias="標準地 法令上の規制等 指定容積率"
    )
    標準地_法令上の規制等_防火地域: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 防火地域"
    )
    標準地_法令上の規制等_森林法: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 森林法"
    )
    標準地_法令上の規制等_自然公園法: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 自然公園法"
    )
    標準地_法令上の規制等_その他地域地区等1: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 その他 その他地域地区等1"
    )
    標準地_法令上の規制等_その他地域地区等2: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 その他 その他地域地区等2"
    )
    標準地_法令上の規制等_その他地域地区等3: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 その他 その他地域地区等3"
    )
    標準地_法令上の規制等_高度地区1_種: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 その他 高度地区1 種"
    )
    標準地_法令上の規制等_高度地区1_高度区分: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 その他 高度地区1 高度区分"
    )
    標準地_法令上の規制等_高度地区1_高度: Optional[float] = Field(
        None, alias="標準地 法令上の規制等 その他 高度地区1 高度"
    )
    標準地_法令上の規制等_高度地区2_種: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 その他 高度地区2 種"
    )
    標準地_法令上の規制等_高度地区2_高度区分: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 その他 高度地区2 高度区分"
    )
    標準地_法令上の規制等_高度地区2_高度: Optional[float] = Field(
        None, alias="標準地 法令上の規制等 その他 高度地区2 高度"
    )
    標準地_法令上の規制等_基準建ぺい率: Optional[int] = Field(
        None, alias="標準地 法令上の規制等 基準建ぺい率"
    )
    標準地_法令上の規制等_基準容積率: Optional[int] = Field(
        None, alias="標準地 法令上の規制等 基準容積率"
    )
    標準地_法令上の規制等_自然環境等コード1: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 自然環境等コード1"
    )
    標準地_法令上の規制等_自然環境等コード2: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 自然環境等コード2"
    )
    標準地_法令上の規制等_自然環境等コード3: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 自然環境等コード3"
    )
    標準地_法令上の規制等_自然環境等文言: Optional[str] = Field(
        None, alias="標準地 法令上の規制等 自然環境等文言"
    )
    鑑定評価手法_適用取引事例比較法_比準価格: Optional[float] = Field(
        None, alias="鑑定評価手法の適用 取引事例比較法比準価格"
    )
    鑑定評価手法_適用控除法_控除後価格: Optional[float] = Field(
        None, alias="鑑定評価手法の適用 控除法 控除後価格"
    )
    鑑定評価手法_適用収益還元法_収益価格: Optional[float] = Field(
        None, alias="鑑定評価手法の適用 収益還元法 収益価格"
    )
    鑑定評価手法_適用原価法_積算価格: Optional[float] = Field(
        None, alias="鑑定評価手法の適用 原価法 積算価格"
    )
    鑑定評価手法_適用開発法_価格: Optional[float] = Field(
        None, alias="鑑定評価手法の適用 開発法 開発法による価格"
    )
    公示価格: Optional[float] = None
    変動率: Optional[float] = None
    緯度: Optional[float] = Field(None, alias="位置座標 緯度")
    経度: Optional[float] = Field(None, alias="位置座標 経度")


class Municipality(PropertyBaseModel):
    id: str = Field(..., description="市区町村コード")
    name: str = Field(..., description="市区町村名")


class PropertyTransactionGeo(PropertyBaseModel):
    point_in_time_name_ja: Optional[str] = None
    price_information_category_name_ja: Optional[str] = None
    prefecture_name_ja: Optional[str] = None
    city_code: Optional[str] = None
    city_name_ja: Optional[str] = None
    district_code: Optional[str] = None
    district_name_ja: Optional[str] = None
    transaction_contents_name_ja: Optional[str] = None
    u_transaction_price_total_ja: Optional[str] = None
    u_transaction_price_unit_price_square_meter_ja: Optional[str] = None
    u_unit_price_per_tsubo_ja: Optional[str] = None
    u_area_ja: Optional[str] = None
    land_shape_name_ja: Optional[str] = None
    u_land_frontage_ja: Optional[str] = None
    building_structure_name_ja: Optional[str] = None
    floor_plan_name_ja: Optional[str] = None
    u_building_total_floor_area_ja: Optional[str] = None
    u_construction_year_ja: Optional[str] = None
    front_road_azimuth_name_ja: Optional[str] = None
    u_front_road_width_ja: Optional[str] = None
    front_road_type_name_ja: Optional[str] = None
    land_use_name_ja: Optional[str] = None
    u_building_coverage_ratio_ja: Optional[str] = None
    u_floor_area_ratio_ja: Optional[str] = None
    future_use_purpose_name_ja: Optional[str] = None
    remark_renovation_name_ja: Optional[str] = None


class LandValuation(PropertyBaseModel):
    point_id: Optional[int] = None
    target_year_name_ja: Optional[str] = None
    land_price_type: Optional[int] = None
    duplication_flag: Optional[str] = None
    prefecture_code: Optional[str] = None
    prefecture_name_ja: Optional[str] = None
    city_code: Optional[str] = None
    use_category_name_ja: Optional[str] = None
    standard_lot_number_ja: Optional[str] = None
    city_county_name_ja: Optional[str] = None
    ward_town_village_name_ja: Optional[str] = None
    place_name_ja: Optional[str] = None
    residence_display_name_ja: Optional[str] = None
    location_number_ja: Optional[str] = None
    u_current_years_price_ja: Optional[str] = None
    last_years_price: Optional[int] = None
    year_on_year_change_rate: Optional[float] = None
    u_cadastral_ja: Optional[str] = None
    frontage_ratio: Optional[float] = None
    depth_ratio: Optional[float] = None
    building_structure_name_ja: Optional[str] = None
    u_ground_hierarchy_ja: Optional[str] = None
    u_underground_hierarchy_ja: Optional[str] = None
    front_road_name_ja: Optional[str] = None
    front_road_azimuth_name_ja: Optional[str] = None
    front_road_width: Optional[float] = None
    front_road_pavement_condition: Optional[str] = None
    side_road_azimuth_name_ja: Optional[str] = None
    side_road_name_ja: Optional[str] = None
    gas_supply_availability: Optional[str] = None
    water_supply_availability: Optional[str] = None
    sewer_supply_availability: Optional[str] = None
    nearest_station_name_ja: Optional[str] = None
    proximity_to_transportation_facilities: Optional[str] = None
    u_road_distance_to_nearest_station_name_ja: Optional[str] = None
    usage_status_name_ja: Optional[str] = None
    current_usage_status_of_surrounding_land_name_ja: Optional[str] = None
    area_division_name_ja: Optional[str] = None
    regulations_use_category_name_ja: Optional[str] = None
    regulations_altitude_district_name_ja: Optional[str] = None
    regulations_fireproof_name_ja: Optional[str] = None
    u_regulations_building_coverage_ratio_ja: Optional[str] = None
    u_regulations_floor_area_ratio_ja: Optional[str] = None
    regulations_forest_law_name_ja: Optional[str] = None
    regulations_park_law_name_ja: Optional[str] = None
    pause_flag: Optional[int] = None
    usage_category_name_ja: Optional[str] = None
    location: Optional[str] = None
    shape: Optional[str] = None
    front_road_condition: Optional[str] = None
    side_road_condition: Optional[str] = None
    park_forest_law: Optional[str] = None


class UrbanPlanningData(PropertyBaseModel):
    prefecture: Optional[str] = None
    city_code: Optional[str] = None
    city_name: Optional[str] = None
    kubun_id: Optional[int] = None
    decision_date: Optional[str] = None
    decision_classification: Optional[str] = None
    decision_maker: Optional[str] = None
    notice_number: Optional[str] = None
    area_classification_ja: Optional[str] = None
    first_decision_date: Optional[str] = None
    notice_number_s: Optional[str] = None


class UrbanPlanningYouto(PropertyBaseModel):
    youto_id: Optional[int] = None
    prefecture: Optional[str] = None
    city_code: Optional[str] = None
    city_name: Optional[str] = None
    decision_date: Optional[str] = None
    decision_classification: Optional[str] = None
    decision_maker: Optional[str] = None
    notice_number: Optional[str] = None
    use_area_ja: Optional[str] = None
    u_floor_area_ratio_ja: Optional[str] = None
    u_building_coverage_ratio_ja: Optional[str] = None
    first_decision_date: Optional[str] = None
    notice_number_s: Optional[str] = None


class MedicalFacilityGISData(BaseModel):
    P04_001: Optional[int] = None
    P04_001_name_ja: Optional[str] = None
    P04_002_ja: Optional[str] = None
    P04_003_ja: Optional[str] = None
    P04_004: Optional[str] = None
    P04_005: Optional[str] = None
    P04_006: Optional[str] = None
    P04_007: Optional[int] = None
    P04_008: Optional[int] = None
    P04_009: Optional[int] = None
    P04_010: Optional[int] = None
    medical_subject_ja: Optional[str] = None


class PreschoolGISData(BaseModel):
    administrative_area_code: Optional[str] = Field(
        None, alias="administrativeAreaCode"
    )
    preschool_name_ja: Optional[str] = Field(None, alias="preSchoolName_ja")
    school_code: Optional[str] = Field(None, alias="schoolCode")
    school_class_code: Optional[int] = Field(None, alias="schoolClassCode")
    school_class_code_name_ja: Optional[str] = Field(
        None, alias="schoolClassCode_name_ja"
    )
    location_ja: Optional[str] = Field(None, alias="location_ja")
    administrator_code: Optional[int] = Field(None, alias="administratorCode")
    close_school_code: Optional[int] = Field(None, alias="closeSchoolCode")


class SchoolGISData(BaseModel):
    P29_001: Optional[str] = None
    P29_002: Optional[str] = None
    P29_003: Optional[int] = None
    P29_003_name_ja: Optional[str] = None
    P29_004_ja: Optional[str] = None
    P29_005_ja: Optional[str] = None
    P29_006: Optional[int] = None
    P29_007: Optional[int] = None
    P29_008: Optional[str] = None
    P29_009_ja: Optional[str] = None


class JuniorHighSchoolDistrictGISData(BaseModel):
    A32_001: Optional[str] = None
    A32_002: Optional[str] = None
    A32_003: Optional[str] = None
    A32_004_ja: Optional[str] = None
    A32_005: Optional[str] = None


class ElementarySchoolDistrictGISData(BaseModel):
    A27_001: Optional[str] = None
    A27_002: Optional[str] = None
    A27_003: Optional[str] = None
    A27_004_ja: Optional[str] = None
    A27_005: Optional[str] = None


class UrbanPlanningOptimizationAreaGISData(BaseModel):
    prefecture: Optional[str] = None
    city_code: Optional[str] = None
    city_name: Optional[str] = None
    decision_date: Optional[str] = None
    decision_classification: Optional[str] = None
    decision_maker: Optional[str] = None
    notice_number: Optional[str] = None
    kubun_id: Optional[int] = None
    kubun_name_ja: Optional[str] = None
    area_classification_ja: Optional[str] = None
    first_decision_date: Optional[str] = None
    notice_number_s: Optional[str] = None


class LandslidePreventionGISData(BaseModel):
    prefecture_code: Optional[str] = None
    group_code: Optional[str] = None
    city_name: Optional[str] = None
    region_name: Optional[str] = None
    address: Optional[str] = None
    notice_date: Optional[str] = None
    notice_number: Optional[str] = None
    landslide_area: Optional[str] = None
    charge_ministry_code: Optional[int] = None
    prefecture_name: Optional[str] = None
    charge_ministry_name: Optional[str] = None


class SteepSlopeHazardGISData(BaseModel):
    prefecture_code: Optional[str] = None
    group_code: Optional[str] = None
    city_name: Optional[str] = None
    region_name: Optional[str] = None
    address: Optional[str] = None
    public_notice_date: Optional[str] = None
    public_notice_number: Optional[str] = None
    landslide_area: Optional[str] = None
    prefecture_name: Optional[str] = None


class DistrictPlanningGISData(BaseModel):
    plan_name: Optional[str] = None
    plan_type_ja: Optional[str] = None
    kubun_id: Optional[str] = None
    group_code: Optional[str] = None
    decision_date: Optional[str] = None
    decision_type_ja: Optional[str] = None
    decision_maker: Optional[str] = None
    notice_number: Optional[str] = None
    prefecture: Optional[str] = None
    city_name: Optional[str] = None
    first_decision_date: Optional[str] = None
    notice_number_s: Optional[str] = None


class HighUtilizationDistrictGISData(BaseModel):
    advanced_name: Optional[str] = None
    advanced_type_ja: Optional[str] = None
    kubun_id: Optional[str] = None
    group_code: Optional[str] = None
    decision_date: Optional[str] = None
    decision_type_ja: Optional[str] = None
    decision_maker: Optional[str] = None
    notice_number: Optional[str] = None
    prefecture: Optional[str] = None
    city_name: Optional[str] = None
    first_decision_date: Optional[str] = None
    notice_number_s: Optional[str] = None


class EmbankmentGISData(BaseModel):
    embankment_classification: Optional[str] = None
    prefecture_code: Optional[str] = None
    prefecture_name: Optional[str] = None
    city_code: Optional[str] = None
    city_name: Optional[str] = None
    embankment_number: Optional[str] = None


class LibraryGISData(BaseModel):
    P27_001: Optional[str] = None
    P27_002: Optional[str] = None
    P27_003: Optional[str] = None
    P27_003_name_ja: Optional[str] = None
    P27_004: Optional[str] = None
    P27_004_name_ja: Optional[str] = None
    P27_005_ja: Optional[str] = None
    P27_006_ja: Optional[str] = None
    P27_007: Optional[int] = None
    P27_008: Optional[int] = None
    P27_009: Optional[int] = None


class TownHallGISData(BaseModel):
    P05_001: Optional[str] = None  # 行政区域コード
    P05_002: Optional[str] = None  # 施設分類コード
    P05_002_name_ja: Optional[str] = None  # 施設分類名
    P05_003_ja: Optional[str] = None  # 名称
    P05_004_ja: Optional[str] = None  # 所在地


class ParkGSIData(BaseModel):
    object_id: int = Field(..., alias="OBJECTID")
    prefecture_cd: Optional[str] = Field(..., alias="PREFEC_CD")
    area_cd: Optional[str] = Field(None, alias="AREA_CD")
    ctv_name: Optional[str] = Field(None, alias="CTV_NAME")
    fis_year: Optional[int] = Field(None, alias="FIS_YEAR")
    thema_no: Optional[int] = Field(None, alias="THEMA_NO")
    layer_no: Optional[int] = Field(None, alias="LAYER_NO")
    area_size: Optional[int] = Field(None, alias="AREA_SIZE")
    ioside_div: Optional[int] = Field(None, alias="IOSIDE_DIV")
    remark_str: Optional[str] = Field(None, alias="REMARK_STR")
    shape_leng: Optional[float] = Field(None, alias="Shape_Leng")
    shape_area: Optional[float] = Field(None, alias="Shape_Area")
    obj_name_ja: Optional[str] = Field(None, alias="OBJ_NAME_ja")


class DisasterRiskAreaGISData(BaseModel):
    A48_001: Optional[str] = None
    A48_002: Optional[str] = None
    A48_003: Optional[str] = None
    A48_004: Optional[int] = None
    A48_005_ja: Optional[str] = None
    A48_006: Optional[str] = None
    A48_007: Optional[int] = None
    A48_007_name_ja: Optional[str] = None
    A48_008_ja: Optional[str] = None
    A48_009: Optional[str] = None
    A48_010: Optional[str] = None
    A48_011: Optional[str] = None
    A48_012: Optional[float] = None
    A48_013: Optional[str] = None


class StationPassengerData(BaseModel):
    S12_001_ja: Optional[str] = None
    S12_001c: Optional[str] = None
    S12_002_ja: Optional[str] = None
    S12_003_ja: Optional[str] = None
    S12_004: Optional[str] = None
    S12_009: Optional[int] = None
    S12_017: Optional[int] = None
    S12_025: Optional[int] = None
    S12_033: Optional[int] = None
    S12_041: Optional[int] = None
    S12_049: Optional[int] = None


class FirePreventionAreaGISData(BaseModel):
    fire_prevention_ja: Optional[str] = None
    kubun_id: Optional[int] = None
    prefecture: Optional[str] = None
    city_code: Optional[str] = None
    city_name: Optional[str] = None
    decision_date: Optional[str] = None
    decision_classification: Optional[str] = None
    decision_maker: Optional[str] = None
    notice_number: Optional[str] = None
    first_decision_date: Optional[str] = None
    notice_number_s: Optional[str] = None


class WelfareFacilityGISData(BaseModel):
    P14_001: Optional[str] = None
    P14_002: Optional[str] = None
    P14_003: Optional[str] = None
    P14_004_ja: Optional[str] = None
    P14_005: Optional[str] = None
    P14_005_name_ja: Optional[str] = None
    P14_006: Optional[str] = None
    P14_006_name_ja: Optional[str] = None
    P14_007: Optional[str] = None
    P14_008_ja: Optional[str] = None
    P14_009: Optional[int] = None
    P14_010: Optional[int] = None


class FuturePopulationMeshData(BaseModel):
    MESH_ID: Optional[int] = None
    SHICODE: Optional[int] = None
    PTN_20XX: Optional[int] = None
    HITOKU_20XX: Optional[str] = None
    GASSAN_20XX: Optional[str] = None
    PT0_20XX: Optional[int] = None
    PT1_20XX: Optional[int] = None
    PT2_20XX: Optional[int] = None

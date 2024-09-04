from dataclasses import dataclass
from typing import Generic, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field, field_validator, model_validator

T = TypeVar("T")


class DataAPIResponse(BaseModel, Generic[T]):
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


class ReinfoBaseModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

    class Config:
        populate_by_name = True


class TransactionPrice(ReinfoBaseModel):
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


# pylint: disable=C2401
class AppraisalReport(ReinfoBaseModel):
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


# pylint: enable=C2401


class Municipality(ReinfoBaseModel):
    id: str = Field(..., description="市区町村コード")
    name: str = Field(..., description="市区町村名")


class TransactionPriceGeo(ReinfoBaseModel):
    point_in_time_name_ja: Optional[str] = Field(None, description="取引時点")
    price_information_category_name_ja: Optional[str] = Field(
        None, description="価格情報区分"
    )
    prefecture_name_ja: Optional[str] = Field(None, description="都道府県名")
    city_code: Optional[str] = Field(None, description="市区町村コード")
    city_name_ja: Optional[str] = Field(None, description="市区町村名")
    district_code: Optional[str] = Field(None, description="地区コード")
    district_name_ja: Optional[str] = Field(None, description="地区名")
    transaction_contents_name_ja: Optional[str] = Field(
        None, description="取引の事情等"
    )
    u_transaction_price_total_ja: Optional[str] = Field(
        None, description="取引価格（総額）"
    )
    u_transaction_price_unit_price_square_meter_ja: Optional[str] = Field(
        None, description="取引価格（平方メートル単価）"
    )
    u_unit_price_per_tsubo_ja: Optional[str] = Field(None, description="坪単価")
    u_area_ja: Optional[str] = Field(None, description="面積")
    land_shape_name_ja: Optional[str] = Field(None, description="土地の形状")
    u_land_frontage_ja: Optional[str] = Field(None, description="間口")
    building_structure_name_ja: Optional[str] = Field(None, description="建物の構造")
    floor_plan_name_ja: Optional[str] = Field(None, description="間取り")
    u_building_total_floor_area_ja: Optional[str] = Field(
        None, description="建物の延床面積"
    )
    u_construction_year_ja: Optional[str] = Field(None, description="建築年")
    front_road_azimuth_name_ja: Optional[str] = Field(
        None, description="前面道路の方位"
    )
    u_front_road_width_ja: Optional[str] = Field(None, description="前面道路の幅員")
    front_road_type_name_ja: Optional[str] = Field(None, description="前面道路の種類")
    land_use_name_ja: Optional[str] = Field(None, description="用途地域")
    u_building_coverage_ratio_ja: Optional[str] = Field(None, description="建蔽率")
    u_floor_area_ratio_ja: Optional[str] = Field(None, description="容積率")
    future_use_purpose_name_ja: Optional[str] = Field(
        None, description="今後の利用目的"
    )
    remark_renovation_name_ja: Optional[str] = Field(None, description="改装")


class LandValuationGeo(ReinfoBaseModel):
    point_id: Optional[int] = Field(None, description="地点ID")
    target_year_name_ja: Optional[str] = Field(None, description="対象年")
    land_price_type: Optional[int] = Field(None, description="地価区分")
    duplication_flag: Optional[str] = Field(None, description="重複フラグ")
    prefecture_code: Optional[str] = Field(None, description="都道府県コード")
    prefecture_name_ja: Optional[str] = Field(None, description="都道府県名")
    city_code: Optional[str] = Field(None, description="市区町村コード")
    use_category_name_ja: Optional[str] = Field(None, description="用途区分名")
    standard_lot_number_ja: Optional[str] = Field(None, description="標準地/基準地番号")
    city_county_name_ja: Optional[str] = Field(None, description="市郡名")
    ward_town_village_name_ja: Optional[str] = Field(None, description="区町村名")
    place_name_ja: Optional[str] = Field(None, description="地名")
    residence_display_name_ja: Optional[str] = Field(None, description="住居表示")
    location_number_ja: Optional[str] = Field(None, description="所在及び地番")
    u_current_years_price_ja: Optional[str] = Field(None, description="当年価格")
    last_years_price: Optional[int] = Field(None, description="前年価格")
    year_on_year_change_rate: Optional[float] = Field(None, description="対前年変動率")
    u_cadastral_ja: Optional[str] = Field(None, description="地積")
    frontage_ratio: Optional[float] = Field(None, description="間口比率")
    depth_ratio: Optional[float] = Field(None, description="奥行き比率")
    building_structure_name_ja: Optional[str] = Field(None, description="構造")
    u_ground_hierarchy_ja: Optional[str] = Field(None, description="地上階層")
    u_underground_hierarchy_ja: Optional[str] = Field(None, description="地下階層")
    front_road_name_ja: Optional[str] = Field(None, description="前面道路区分")
    front_road_azimuth_name_ja: Optional[str] = Field(
        None, description="前面道路の方位区分"
    )
    front_road_width: Optional[float] = Field(None, description="前面道路の幅員")
    front_road_pavement_condition: Optional[str] = Field(
        None, description="前面道路の舗装状況"
    )
    side_road_azimuth_name_ja: Optional[str] = Field(None, description="側道の方位区分")
    side_road_name_ja: Optional[str] = Field(None, description="側道区分")
    gas_supply_availability: Optional[str] = Field(None, description="ガスの有無")
    water_supply_availability: Optional[str] = Field(None, description="水道の有無")
    sewer_supply_availability: Optional[str] = Field(None, description="下水道の有無")
    nearest_station_name_ja: Optional[str] = Field(None, description="最寄り駅名")
    proximity_to_transportation_facilities: Optional[str] = Field(
        None, description="交通施設との近接区分"
    )
    u_road_distance_to_nearest_station_name_ja: Optional[str] = Field(
        None, description="最寄り駅までの道路距離"
    )
    usage_status_name_ja: Optional[str] = Field(None, description="利用現況")
    current_usage_status_of_surrounding_land_name_ja: Optional[str] = Field(
        None, description="周辺の土地の利用現況"
    )
    area_division_name_ja: Optional[str] = Field(None, description="区域区分")
    regulations_use_category_name_ja: Optional[str] = Field(
        None, description="法規制・用途区分"
    )
    regulations_altitude_district_name_ja: Optional[str] = Field(
        None, description="法規制・高度地区"
    )
    regulations_fireproof_name_ja: Optional[str] = Field(
        None, description="法規制・防火・準防火"
    )
    u_regulations_building_coverage_ratio_ja: Optional[str] = Field(
        None, description="法規制・建蔽率"
    )
    u_regulations_floor_area_ratio_ja: Optional[str] = Field(
        None, description="法規制・容積率"
    )
    regulations_forest_law_name_ja: Optional[str] = Field(
        None, description="法規制・森林法"
    )
    regulations_park_law_name_ja: Optional[str] = Field(
        None, description="法規制・公園法"
    )
    pause_flag: Optional[int] = Field(None, description="休止フラグ")
    usage_category_name_ja: Optional[str] = Field(None, description="利用区分名")
    location: Optional[str] = Field(None, description="所在及び地番")
    shape: Optional[str] = Field(None, description="形状（間口：奥行き）")
    front_road_condition: Optional[str] = Field(None, description="前面道路の状況")
    side_road_condition: Optional[str] = Field(None, description="その他の接面道路")
    park_forest_law: Optional[str] = Field(
        None, description="森林法、公園法、自然環境等"
    )


class UrbanPlanningZoneGIS(ReinfoBaseModel):
    prefecture: Optional[str] = Field(None, description="都道府県名")
    city_code: Optional[str] = Field(None, description="市区町村コード")
    city_name: Optional[str] = Field(None, description="市区町村名")
    kubun_id: Optional[int] = Field(None, description="区分コード")
    decision_date: Optional[str] = Field(None, description="設定年月日")
    decision_classification: Optional[str] = Field(None, description="設定区分")
    decision_maker: Optional[str] = Field(None, description="設定者名")
    notice_number: Optional[str] = Field(None, description="告示番号")
    area_classification_ja: Optional[str] = Field(None, description="区域区分")
    first_decision_date: Optional[str] = Field(None, description="当初決定日")
    notice_number_s: Optional[str] = Field(
        None, description="告示番号S（告示番号・当初）"
    )


class UrbanPlanningUseDistrictGIS(ReinfoBaseModel):
    youto_id: Optional[int] = Field(None, description="用途地域分類")
    prefecture: Optional[str] = Field(None, description="都道府県名")
    city_code: Optional[str] = Field(None, description="市区町村コード")
    city_name: Optional[str] = Field(None, description="市区町村名")
    decision_date: Optional[str] = Field(None, description="区域設定年月日")
    decision_classification: Optional[str] = Field(None, description="設定区分")
    decision_maker: Optional[str] = Field(None, description="設定者名")
    notice_number: Optional[str] = Field(None, description="告示番号")
    use_area_ja: Optional[str] = Field(None, description="用途地域名")
    u_floor_area_ratio_ja: Optional[str] = Field(None, description="容積率")
    u_building_coverage_ratio_ja: Optional[str] = Field(None, description="建蔽率")
    first_decision_date: Optional[str] = Field(None, description="当初決定日")
    notice_number_s: Optional[str] = Field(
        None, description="告示番号S（告示番号・当初）"
    )


class UrbanPlanningLocationNormalizationGIS(ReinfoBaseModel):
    prefecture: Optional[str] = Field(None, description="都道府県名")
    city_code: Optional[str] = Field(None, description="行政区域コード")
    city_name: Optional[str] = Field(None, description="市町村名")
    decision_date: Optional[str] = Field(None, description="区域設定年月日")
    decision_classification: Optional[str] = Field(None, description="設定区分")
    decision_maker: Optional[str] = Field(None, description="設定者名")
    notice_number: Optional[str] = Field(None, description="告示番号")
    kubun_id: Optional[int] = Field(None, description="区域コード")
    kubun_name_ja: Optional[str] = Field(None, description="区域名")
    area_classification_ja: Optional[str] = Field(None, description="区域区分")
    first_decision_date: Optional[str] = Field(None, description="当初決定日")
    notice_number_s: Optional[str] = Field(
        None, description="告示番号S（告示番号・当初）"
    )


class ElementarySchoolDistrictGIS(ReinfoBaseModel):
    A27_001: Optional[str] = Field(None, description="行政区域コード")
    A27_002: Optional[str] = Field(None, description="設置主体")
    A27_003: Optional[str] = Field(None, description="学校コード")
    A27_004_ja: Optional[str] = Field(None, description="名称")
    A27_005: Optional[str] = Field(None, description="所在地")


class JuniorHighSchoolDistrictGISData(ReinfoBaseModel):
    A32_001: Optional[str] = Field(None, description="行政区域コード")
    A32_002: Optional[str] = Field(None, description="設置主体")
    A32_003: Optional[str] = Field(None, description="学校コード")
    A32_004_ja: Optional[str] = Field(None, description="名称")
    A32_005: Optional[str] = Field(None, description="所在地")


class PreschoolGISData(ReinfoBaseModel):
    # "幼稚園" or "こども園"
    administrative_area_code: Optional[str] = Field(
        None, alias="administrativeAreaCode", description="行政区域コード"
    )
    preschool_name_ja: Optional[str] = Field(
        None, alias="preSchoolName_ja", description="名称"
    )
    school_code: Optional[str] = Field(
        None, alias="schoolCode", description="学校コード"
    )
    school_class_code: Optional[int] = Field(
        None, alias="schoolClassCode", description="学校分類コード"
    )
    school_class_code_name_ja: Optional[str] = Field(
        None, alias="schoolClassCode_name_ja", description="学校分類名"
    )
    location_ja: Optional[str] = Field(None, alias="location_ja", description="所在地")
    administrator_code: Optional[int] = Field(
        None, alias="administratorCode", description="管理者コード"
    )
    close_school_code: Optional[int] = Field(
        None, alias="closeSchoolCode", description="休校コード"
    )

    # "保育園"
    welfare_facility_class_code: Optional[int] = Field(
        None, alias="welfareFacilityClassCode", description="福祉施設大分類コード"
    )
    welfare_facility_middle_class_code: Optional[int] = Field(
        None, alias="welfareFacilityMiddleClassCode", description="福祉施設中分類コード"
    )
    welfare_facility_minor_class_code: Optional[int] = Field(
        None, alias="welfareFacilityMinorClassCode", description="福祉施設小分類コード"
    )


class SchoolGISData(ReinfoBaseModel):
    P29_001: Optional[str] = Field(None, description="行政区域コード")
    P29_002: Optional[str] = Field(None, description="学校コード")
    P29_003: Optional[int] = Field(None, description="学校分類コード")
    P29_003_name_ja: Optional[str] = Field(None, description="学校分類名")
    P29_004_ja: Optional[str] = Field(None, description="名称")
    P29_005_ja: Optional[str] = Field(None, description="所在地")
    P29_006: Optional[int] = Field(None, description="管理者コード")
    P29_007: Optional[int] = Field(None, description="休校区分")
    P29_008: Optional[str] = Field(None, description="キャンパスコード")
    P29_009_ja: Optional[str] = Field(None, description="学校名備考")


class MedicalFacilityGISData(ReinfoBaseModel):
    P04_001: Optional[int] = Field(None, description="医療機関分類")
    P04_001_name_ja: Optional[str] = Field(None, description="医療機関分類名")
    P04_002_ja: Optional[str] = Field(None, description="施設名称")
    P04_003_ja: Optional[str] = Field(None, description="所在地")
    P04_004: Optional[str] = Field(None, description="診療科目１")
    P04_005: Optional[str] = Field(None, description="診療科目２")
    P04_006: Optional[str] = Field(None, description="診療科目３")
    P04_007: Optional[int] = Field(None, description="開設者分類")
    P04_008: Optional[int] = Field(None, description="病床数")
    P04_009: Optional[int] = Field(None, description="救急告示病院")
    P04_010: Optional[int] = Field(None, description="災害拠点病院")
    medical_subject_ja: Optional[str] = Field(None, description="診療科目")


class WelfareFacilityGISData(ReinfoBaseModel):
    P14_001: Optional[str] = Field(None, description="都道府県名")
    P14_002: Optional[str] = Field(None, description="市区町村名")
    P14_003: Optional[str] = Field(None, description="行政区域コード")
    P14_004_ja: Optional[str] = Field(None, description="所在地")
    P14_005: Optional[str] = Field(None, description="福祉施設大分類コード")
    P14_005_name_ja: Optional[str] = Field(None, description="福祉施設大分類名")
    P14_006: Optional[str] = Field(None, description="福祉施設中分類コード")
    P14_006_name_ja: Optional[str] = Field(None, description="福祉施設中分類名")
    P14_007: Optional[str] = Field(None, description="福祉施設小分類コード")
    P14_008_ja: Optional[str] = Field(None, description="名称")
    P14_009: Optional[int] = Field(None, description="管理者コード")
    P14_010: Optional[int] = Field(None, description="位置正確度コード")


class FuturePopulationMeshData(ReinfoBaseModel):
    mesh_id: Optional[int] = Field(
        None, alias="MESH_ID", description="分割地域メッシュコード"
    )
    shicode: Optional[int] = Field(None, alias="SHICODE", description="行政区域コード")
    PTN_20XX: Optional[int] = Field(
        None, description="20XX年男女計総数人口（秘匿なし）"
    )
    hitoku_20XX: Optional[str] = Field(
        None, alias="HITOKU_20XX", description="20XX年秘匿記号"
    )
    gassan_20XX: Optional[str] = Field(
        None, alias="GASSAN_20XX", description="20XX年合算先メッシュ"
    )
    PT0_20XX: Optional[int] = Field(None, description="20XX年男女計総数人口")
    PT1_20XX: Optional[int] = Field(None, description="20XX年男女計0～4歳人口")
    PT2_20XX: Optional[int] = Field(None, description="20XX年男女計5～9歳人口")
    PT3_20XX: Optional[int] = Field(None, description="20XX年男女計10～14歳人口")
    PT4_20XX: Optional[int] = Field(None, description="20XX年男女計15～19歳人口")
    PT5_20XX: Optional[int] = Field(None, description="20XX年男女計20～24歳人口")
    PT6_20XX: Optional[int] = Field(None, description="20XX年男女計25～29歳人口")
    PT7_20XX: Optional[int] = Field(None, description="20XX年男女計30～34歳人口")
    PT8_20XX: Optional[int] = Field(None, description="20XX年男女計35～39歳人口")
    PT9_20XX: Optional[int] = Field(None, description="20XX年男女計40～44歳人口")
    PT10_20XX: Optional[int] = Field(None, description="20XX年男女計45～49歳人口")
    PT11_20XX: Optional[int] = Field(None, description="20XX年男女計50～54歳人口")
    PT12_20XX: Optional[int] = Field(None, description="20XX年男女計55～59歳人口")
    PT13_20XX: Optional[int] = Field(None, description="20XX年男女計60～64歳人口")
    PT14_20XX: Optional[int] = Field(None, description="20XX年男女計65～69歳人口")
    PT15_20XX: Optional[int] = Field(None, description="20XX年男女計70～74歳人口")
    PT16_20XX: Optional[int] = Field(None, description="20XX年男女計75～79歳人口")
    PT17_20XX: Optional[int] = Field(None, description="20XX年男女計80～84歳人口")
    PT18_20XX: Optional[int] = Field(None, description="20XX年男女計85～89歳人口")
    PT19_20XX: Optional[int] = Field(None, description="20XX年男女計90歳以上人口")
    PTA_20XX: Optional[int] = Field(None, description="20XX年男女計0～14歳人口")
    PTB_20XX: Optional[int] = Field(None, description="20XX年男女計15～64歳人口")
    PTC_20XX: Optional[int] = Field(None, description="20XX年男女計65歳以上人口")
    PTD_20XX: Optional[int] = Field(None, description="20XX年男女計75歳以上人口")
    PTE_20XX: Optional[int] = Field(None, description="20XX年男女計80歳以上人口")
    RTA_20XX: Optional[float] = Field(None, description="20XX年男女計0～14歳人口比率")
    RTB_20XX: Optional[float] = Field(None, description="20XX年男女計15～64歳人口比率")
    RTC_20XX: Optional[float] = Field(None, description="20XX年男女計65歳以上人口比率")
    RTD_20XX: Optional[float] = Field(None, description="20XX年男女計75歳以上人口比率")
    RTE_20XX: Optional[float] = Field(None, description="20XX年男女計80歳以上人口比率")


class FirePreventionAreaGISData(ReinfoBaseModel):
    fire_prevention_ja: Optional[str] = Field(None, description="防火・準防火地域名")
    kubun_id: Optional[int] = Field(None, description="区分コード")
    prefecture: Optional[str] = Field(None, description="都道府県名")
    city_code: Optional[str] = Field(None, description="市区町村コード")
    city_name: Optional[str] = Field(None, description="市区町村名")
    decision_date: Optional[str] = Field(None, description="設定年月日")
    decision_classification: Optional[str] = Field(None, description="設定区分")
    decision_maker: Optional[str] = Field(None, description="設定者名")
    notice_number: Optional[str] = Field(None, description="告示番号")
    first_decision_date: Optional[str] = Field(None, description="当初決定日")
    notice_number_s: Optional[str] = Field(
        None, description="告示番号S（告示番号・当初）"
    )


class StationPassengerData(ReinfoBaseModel):
    S12_001_ja: Optional[str] = Field(None, description="駅名")
    S12_001c: Optional[str] = Field(None, description="駅コード")
    S12_002_ja: Optional[str] = Field(None, description="運営会社")
    S12_003_ja: Optional[str] = Field(None, description="路線名")
    S12_004: Optional[str] = Field(None, description="鉄道区分")

    S12_005: Optional[str] = Field(None, description="事業者種別")
    S12_006: Optional[int] = Field(None, description="重複コード2011")
    S12_007: Optional[int] = Field(None, description="データ有無コード2011")
    S12_008: Optional[str] = Field(None, description="備考2011")
    S12_009: Optional[int] = Field(None, description="乗降客数2011")

    S12_010: Optional[int] = Field(None, description="重複コード2012")
    S12_011: Optional[int] = Field(None, description="データ有無コード2012")
    S12_012: Optional[str] = Field(None, description="備考2012")
    S12_013: Optional[int] = Field(None, description="乗降客数2012")

    S12_014: Optional[int] = Field(None, description="重複コード2013")
    S12_015: Optional[int] = Field(None, description="データ有無コード2013")
    S12_016: Optional[str] = Field(None, description="備考2013")
    S12_017: Optional[int] = Field(None, description="乗降客数2013")

    S12_018: Optional[int] = Field(None, description="重複コード2014")
    S12_019: Optional[int] = Field(None, description="データ有無コード2014")
    S12_020: Optional[str] = Field(None, description="備考2014")
    S12_021: Optional[int] = Field(None, description="乗降客数2014")

    S12_022: Optional[int] = Field(None, description="重複コード2015")
    S12_023: Optional[int] = Field(None, description="データ有無コード2015")
    S12_024: Optional[str] = Field(None, description="備考2015")
    S12_025: Optional[int] = Field(None, description="乗降客数2015")

    S12_026: Optional[int] = Field(None, description="重複コード2016")
    S12_027: Optional[int] = Field(None, description="データ有無コード2016")
    S12_028: Optional[str] = Field(None, description="備考2016")
    S12_029: Optional[int] = Field(None, description="乗降客数2016")

    S12_030: Optional[int] = Field(None, description="重複コード2017")
    S12_031: Optional[int] = Field(None, description="データ有無コード2017")
    S12_032: Optional[str] = Field(None, description="備考2017")
    S12_033: Optional[int] = Field(None, description="乗降客数2017")

    S12_034: Optional[int] = Field(None, description="重複コード2018")
    S12_035: Optional[int] = Field(None, description="データ有無コード2018")
    S12_036: Optional[str] = Field(None, description="備考2018")
    S12_037: Optional[int] = Field(None, description="乗降客数2018")

    S12_038: Optional[int] = Field(None, description="重複コード2019")
    S12_039: Optional[int] = Field(None, description="データ有無コード2019")
    S12_040: Optional[str] = Field(None, description="備考2019")
    S12_041: Optional[int] = Field(None, description="乗降客数2019")

    S12_042: Optional[int] = Field(None, description="重複コード2020")
    S12_043: Optional[int] = Field(None, description="データ有無コード2020")
    S12_044: Optional[str] = Field(None, description="備考2020")
    S12_045: Optional[int] = Field(None, description="乗降客数2020")

    S12_046: Optional[int] = Field(None, description="重複コード2021")
    S12_047: Optional[int] = Field(None, description="データ有無コード2021")
    S12_048: Optional[str] = Field(None, description="備考2021")
    S12_049: Optional[int] = Field(None, description="乗降客数2021")

    S12_050: Optional[int] = Field(None, description="重複コード2022")
    S12_051: Optional[int] = Field(None, description="データ有無コード2022")
    S12_052: Optional[str] = Field(None, description="備考2022")
    S12_053: Optional[int] = Field(None, description="乗降客数2022")


class DisasterRiskAreaGISData(ReinfoBaseModel):
    A48_001: Optional[str] = Field(None, description="都道府県名")
    A48_002: Optional[str] = Field(None, description="市町村名")
    A48_003: Optional[str] = Field(None, description="代表行政コード")
    A48_004: Optional[int] = Field(None, description="指定主体区分")
    A48_005_ja: Optional[str] = Field(None, description="区域名")
    A48_006: Optional[str] = Field(None, description="所在地")
    A48_007: Optional[int] = Field(None, description="指定理由コード")
    A48_007_name_ja: Optional[str] = Field(None, description="指定理由")
    A48_008_ja: Optional[str] = Field(None, description="指定理由詳細")
    A48_009: Optional[str] = Field(None, description="告示年月日")
    A48_010: Optional[str] = Field(None, description="告示番号")
    A48_011: Optional[str] = Field(None, description="根拠条例")
    A48_012: Optional[float] = Field(None, description="面積")
    A48_013: Optional[str] = Field(None, description="縮尺")
    A48_014: Optional[str] = Field(None, description="その他")


class LandslidePreventionGISData(ReinfoBaseModel):
    prefecture_code: Optional[str] = Field(
        None, alias="prefecture_code", description="都道府県コード"
    )
    group_code: Optional[str] = Field(
        None, alias="group_code", description="行政コード"
    )
    city_name: Optional[str] = Field(None, alias="city_name", description="市町村名")
    region_name: Optional[str] = Field(None, alias="region_name", description="区域名")
    address: Optional[str] = Field(None, alias="address", description="所在地")
    notice_date: Optional[str] = Field(
        None, alias="notice_date", description="告示年月日"
    )
    notice_number: Optional[str] = Field(
        None, alias="notice_number", description="告示番号"
    )
    landslide_area: Optional[str] = Field(
        None, alias="landslide_area", description="指定面積（ha）"
    )
    charge_ministry_code: Optional[int] = Field(
        None, alias="charge_ministry_code", description="所管省庁コード"
    )
    prefecture_name: Optional[str] = Field(
        None, alias="prefecture_name", description="都道府県名"
    )
    charge_ministry_name: Optional[str] = Field(
        None, alias="charge_ministry_name", description="所管省庁名"
    )


class SteepSlopeHazardGISData(ReinfoBaseModel):
    prefecture_code: Optional[str] = Field(
        None, alias="prefecture_code", description="都道府県コード"
    )
    group_code: Optional[str] = Field(
        None, alias="group_code", description="行政コード"
    )
    city_name: Optional[str] = Field(None, alias="city_name", description="市町村名")
    region_name: Optional[str] = Field(None, alias="region_name", description="区域名")
    address: Optional[str] = Field(None, alias="address", description="所在地")
    public_notice_date: Optional[str] = Field(
        None, alias="public_notice_date", description="公示年月日"
    )
    public_notice_number: Optional[str] = Field(
        None, alias="public_notice_number", description="公示番号"
    )
    landslide_area: Optional[str] = Field(
        None, alias="landslide_area", description="指定面積（ha）"
    )
    prefecture_name: Optional[str] = Field(
        None, alias="prefecture_name", description="都道府県名"
    )


class DistrictPlanningGISData(ReinfoBaseModel):
    plan_name: Optional[str] = Field(None, alias="plan_name", description="計画名")
    plan_type_ja: Optional[str] = Field(
        None, alias="plan_type_ja", description="計画区分名"
    )
    kubun_id: Optional[str] = Field(None, alias="kubun_id", description="区分コード")
    group_code: Optional[str] = Field(
        None, alias="group_code", description="行政コード"
    )
    decision_date: Optional[str] = Field(
        None, alias="decision_date", description="設定年月日"
    )
    decision_type_ja: Optional[str] = Field(
        None, alias="decision_type_ja", description="設定区分名"
    )
    decision_maker: Optional[str] = Field(
        None, alias="decision_maker", description="設定者名"
    )
    notice_number: Optional[str] = Field(
        None, alias="notice_number", description="告示番号"
    )
    prefecture: Optional[str] = Field(
        None, alias="prefecture", description="都道府県名"
    )
    city_name: Optional[str] = Field(None, alias="city_name", description="市町村名")
    first_decision_date: Optional[str] = Field(
        None, alias="first_decision_date", description="当初決定日"
    )
    notice_number_s: Optional[str] = Field(
        None, alias="notice_number_s", description="告示番号S (告示番号（当初）)"
    )


class HighUtilizationDistrictGISData(ReinfoBaseModel):
    advanced_name: Optional[str] = Field(
        None, alias="advanced_name", description="高度名称"
    )
    advanced_type_ja: Optional[str] = Field(
        None, alias="advanced_type_ja", description="高度区分名"
    )
    kubun_id: Optional[str] = Field(None, alias="kubun_id", description="区分コード")
    group_code: Optional[str] = Field(
        None, alias="group_code", description="行政コード"
    )
    decision_date: Optional[str] = Field(
        None, alias="decision_date", description="設定年月日"
    )
    decision_type_ja: Optional[str] = Field(
        None, alias="decision_type_ja", description="設定区分名"
    )
    decision_maker: Optional[str] = Field(
        None, alias="decision_maker", description="設定者名"
    )
    notice_number: Optional[str] = Field(
        None, alias="notice_number", description="告示番号"
    )
    prefecture: Optional[str] = Field(
        None, alias="prefecture", description="都道府県名"
    )
    city_name: Optional[str] = Field(None, alias="city_name", description="市町村名")
    first_decision_date: Optional[str] = Field(
        None, alias="first_decision_date", description="当初決定日"
    )
    notice_number_s: Optional[str] = Field(
        None, alias="notice_number_s", description="告示番号S (告示番号（当初）)"
    )


class EmbankmentGISData(ReinfoBaseModel):
    embankment_classification: Optional[str] = Field(
        None, alias="embankment_classification", description="盛土区分"
    )
    prefecture_code: Optional[str] = Field(
        None, alias="prefecture_code", description="都道府県コード"
    )
    prefecture_name: Optional[str] = Field(
        None, alias="prefecture_name", description="都道府県名"
    )
    city_code: Optional[str] = Field(
        None, alias="city_code", description="市区町村コード"
    )
    city_name: Optional[str] = Field(None, alias="city_name", description="市区町村名")
    embankment_number: Optional[str] = Field(
        None, alias="embankment_number", description="盛土番号"
    )


class LibraryGISData(ReinfoBaseModel):
    P27_001: Optional[str] = Field(None, description="行政区域コード")
    P27_002: Optional[str] = Field(None, description="公共施設大分類")
    P27_003: Optional[str] = Field(None, description="公共施設小分類")
    P27_003_name_ja: Optional[str] = Field(None, description="公共施設小分類名")
    P27_004: Optional[str] = Field(None, description="文化施設分類")
    P27_004_name_ja: Optional[str] = Field(None, description="文化施設分類名")
    P27_005_ja: Optional[str] = Field(None, description="名称")
    P27_006_ja: Optional[str] = Field(None, description="所在地")
    P27_007: Optional[int] = Field(None, description="管理者コード")
    P27_008: Optional[int] = Field(None, description="階数")
    P27_009: Optional[int] = Field(None, description="建築年")


class TownHallGISData(ReinfoBaseModel):
    P05_001: Optional[str] = Field(None, description="行政区域コード")
    P05_002: Optional[str] = Field(None, description="施設分類コード")
    P05_002_name_ja: Optional[str] = Field(None, description="施設分類名")
    P05_003_ja: Optional[str] = Field(None, description="名称")
    P05_004_ja: Optional[str] = Field(None, description="所在地")


class NaturalParkGSIData(ReinfoBaseModel):
    object_id: int = Field(..., alias="OBJECTID", description="シェープID")
    prefecture_cd: Optional[str] = Field(
        None, alias="PREFEC_CD", description="都道府県コード"
    )
    area_cd: Optional[str] = Field(None, alias="AREA_CD", description="地区コード")
    ctv_name: Optional[str] = Field(None, alias="CTV_NAME", description="市町村名")
    fis_year: Optional[int] = Field(None, alias="FIS_YEAR", description="年度")
    thema_no: Optional[int] = Field(None, alias="THEMA_NO", description="主題番号")
    layer_no: Optional[int] = Field(None, alias="LAYER_NO", description="レイヤ番号")
    area_size: Optional[int] = Field(
        None, alias="AREA_SIZE", description="ポリゴン面積(ha)"
    )
    ioside_div: Optional[int] = Field(None, alias="IOSIDE_DIV", description="内外区分")
    remark_str: Optional[str] = Field(None, alias="REMARK_STR", description="備考")
    shape_leng: Optional[float] = Field(
        None, alias="Shape_Leng", description="シェープの長さ"
    )
    shape_area: Optional[float] = Field(
        None, alias="Shape_Area", description="シェープの面積"
    )
    obj_name_ja: Optional[str] = Field(
        None, alias="OBJ_NAME_ja", description="シェープ名"
    )

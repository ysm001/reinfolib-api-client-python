<!-- @format -->

# 不動産情報ライブラリ API Client

[不動産情報ライブラリ](https://www.reinfolib.mlit.go.jp/help/apiManual/) の Python クライアントライブラリです。

API Key の入手方法等は[公式のドキュメント](https://www.reinfolib.mlit.go.jp/help/apiManual/#titleApi2) を参照してください。

## Installation

```bash
pip install reinfolib-api-client
```

## Usage

```python
from reinfolib import Client

api_key = ...

client = Client.create(api_key=api_key)

# 不動産価格（取引価格・成約価格）情報取得API
client.get_transaction_price_list(year=2015, area="13")

# 市区町村一覧 API
resp = client.get_city_list(area="13")

# 地価公示・地価調査のポイント（点）API
client.get_land_valuation_geo_list(z=13, x=7312, y=3008, year=2020)

# 都市計画決定GISデータ（都市計画区域/区域区分）API
client.get_urban_planning_zone_gis_list(z=11, x=1809, y=806)

# 都市計画決定GISデータ（用途地域）API
client.get_urban_planning_use_district_gis_list(z=11, x=1819, y=806)

# 都市計画決定GISデータ（立地適正化計画区域）API
client.get_urban_planning_location_normalization_gis_list(z=11, x=1818, y=805)

# 国土数値情報（小学校区）API
client.get_elementary_school_district_gis_list(z=11, x=1819, y=806)

# 国土数値情報（中学校区）API
client.get_junior_high_school_district_gis_list(z=11, x=1819, y=806)

# 国土数値情報（学校）API
client.get_school_gis_list(z=13, x=7272, y=3225)

# 国土数値情報（保育園・幼稚園等）API
client.get_preschool_gis_list(z=13, x=7272, y=3225)

# 国土数値情報（医療機関）API
client.get_medical_facility_gis_list(z=13, x=7272, y=3225)

# 国土数値情報（福祉施設）API
client.get_welfare_facility_gis_list(z=13, x=7272, y=3225)

# 国土数値情報（将来推計人口250mメッシュ）API
client.get_future_population_mesh_list(z=11, x=1819, y=806)

# 都市計画決定GISデータ（防火・準防火地域）API
client.get_fire_prevention_area_gis_list(z=11, x=1819, y=806)

# 国土数値情報（駅別乗降客数）API
client.get_num_of_station_passenger_list(z=11, x=1819, y=806)

# 国土数値情報（災害危険区域）API
client.get_disaster_risk_area_gis_list(z=11, x=1819, y=806)

# 国土数値情報（図書館）API
client.get_library_gis_list(z=13, x=7272, y=3225)

# 国土数値情報（市区町村村役場及び集会施設等）API
client.get_town_hall_gis_list(z=13, x=7272, y=3225)

# 国土数値情報（自然公園地域）API
client.get_natural_park_gis_list(z=10, x=914, y=376)

# 国土数値情報（大規模盛土造成地マップ）API
client.get_embankment_gis_list(z=12, x=3657, y=1504)

# 国土数値情報（地すべり防止地区）API
client.get_landslide_prevention_district_gis_list(z=11, x=1815, y=805)

# 国土数値情報（急傾斜地崩壊危険区域）API
client.get_steep_slope_hazard_district_gis_list(z=11, x=1815, y=805)

# 都市計画決定GISデータ（地区計画）API
client.get_district_planning_gis_list(z=12, x=3657, y=1504)

# 都市計画決定GISデータ（高度利用地区）API
client.get_high_utilization_district_gis_list(z=12, x=3637, y=1612)

# 国土交通省都市局（地形区分に基づく液状化の発生傾向図）API
client.get_liquefaction_tendency_gis_list(z=12, x=3657, y=1504)

# 国土数値情報（洪水浸水想定区域（想定最大規模））API
client.get_flood_inundation_assumption_area_gis_list(z=14, x=14550, y=6451)

# 国土数値情報（高潮浸水想定区域）API
client.get_storm_surge_inundation_assumption_area_gis_list(z=13, x=7210, y=3243)

# 国土数値情報（津波浸水想定）API
client.get_tsunami_inundation_assumption_gis_list(z=14, x=14421, y=6486)

# 国土数値情報（土砂災害警戒区域）API
client.get_sediment_disaster_warning_area_gis_list(z=11, x=1819, y=806)

# 都市計画決定GISデータ（都市計画道路）API
client.get_urban_planning_road_gis_list(z=11, x=1819, y=806)

# 国土数値情報（人口集中地区）API
client.get_densely_inhabited_district_gis_list(
    z=11, x=1819, y=806, administrative_area_code="13101"
)

# 国土地理院GISデータ（指定緊急避難場所）API
client.get_emergency_evacuation_site_gis_list(z=13, x=7272, y=3225)

# 国土調査（災害履歴）API
client.get_disaster_history_geo_list(
    z=11, x=1819, y=806, disastertype_code="11"
)
```

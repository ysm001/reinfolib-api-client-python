import os
import sys

sys.path.append(".")

import dotenv

from reinfolib import Client

dotenv.load_dotenv()

api_key = os.getenv("REINFOLIB_API_KEY")
if api_key is None:
    raise ValueError("API key is not set")

client = Client.create(api_key=api_key)

# 不動産価格（取引価格・成約価格）情報取得API
resp = client.get_transaction_price_list(year=2015, area="13")
print(resp[0:5])

# 都道府県内市区町村一覧取得API
resp = client.get_city_list(area="13")
print(resp[0:5])

# 鑑定評価書情報API
resp = client.get_apraisal_report_list(year=2022, area="01", division="00")
print(resp[0:5])

# 不動産価格（取引価格・成約価格）情報のポイント (点) API
resp = client.get_transaction_price_geo_list(
    z=13,
    x=7312,
    y=3008,
    from_yyyyn="20223",
    to_yyyyn="20234",
)
print(resp[0:5])

# 市区町村一覧 API
resp = client.get_city_list(area="13")
print(resp[0:5])

# 地価公示・地価調査のポイント（点）API
resp = client.get_land_valuation_geo_list(z=13, x=7312, y=3008, year=2020)
print(resp[0:5])

# 都市計画決定GISデータ（都市計画区域/区域区分）API
resp = client.get_urban_planning_zone_gis_list(z=11, x=1809, y=806)
print(resp[0:5])

# 都市計画決定GISデータ（用途地域）API
resp = client.get_urban_planning_use_district_gis_list(z=11, x=1819, y=806)
print(resp[0:5])

# 都市計画決定GISデータ（立地適正化計画区域）API
resp = client.get_urban_planning_location_normalization_gis_list(z=11, x=1818, y=805)
print(resp[0:5])

# 国土数値情報（小学校区）API
resp = client.get_elementary_school_district_gis_list(z=11, x=1819, y=806)
print(resp[0:5])

# 国土数値情報（中学校区）API
resp = client.get_junior_high_school_district_gis_list(z=11, x=1819, y=806)
print(resp[0:5])

# 国土数値情報（学校）API
resp = client.get_school_gis_list(z=13, x=7272, y=3225)
print(resp[0:5])

# 国土数値情報（保育園・幼稚園等）API
resp = client.get_preschool_gis_list(z=13, x=7272, y=3225)
print(resp[0:5])

# 国土数値情報（医療機関）API
resp = client.get_medical_facility_gis_list(z=13, x=7272, y=3225)
print(resp[0:5])

# 国土数値情報（福祉施設）API
resp = client.get_welfare_facility_gis_list(z=13, x=7272, y=3225)
print(resp[0:5])

# 国土数値情報（将来推計人口250mメッシュ）API
resp = client.get_future_population_mesh_list(z=11, x=1819, y=806)
print(resp[0:5])

# 都市計画決定GISデータ（防火・準防火地域）API
resp = client.get_fire_prevention_area_gis_list(z=11, x=1819, y=806)
print(resp[0:5])

# 国土数値情報（駅別乗降客数）API
resp = client.get_num_of_station_passenger_list(z=11, x=1819, y=806)
print(resp[0:5])

# 国土数値情報（災害危険区域）API
resp = client.get_disaster_risk_area_gis_list(z=11, x=1819, y=806)
print(resp[0:5])

# 国土数値情報（図書館）API
resp = client.get_library_gis_list(z=13, x=7272, y=3225)
print(resp[0:5])

# 国土数値情報（市区町村村役場及び集会施設等）API
resp = client.get_town_hall_gis_list(z=13, x=7272, y=3225)
print(resp[0:5])

# 国土数値情報（自然公園地域）API
resp = client.get_natural_park_gis_list(z=10, x=914, y=376)
print(resp[0:5])

# 国土数値情報（大規模盛土造成地マップ）API
resp = client.get_embankment_gis_list(z=12, x=3657, y=1504)
print(resp[0:5])

# 国土数値情報（地すべり防止地区）API
resp = client.get_landslide_prevention_district_gis_list(z=11, x=1815, y=805)
print(resp[0:5])

# 国土数値情報（急傾斜地崩壊危険区域）API
resp = client.get_steep_slope_hazard_district_gis_list(z=11, x=1815, y=805)
print(resp[0:5])

# 都市計画決定GISデータ（地区計画）API
resp = client.get_district_planning_gis_list(z=12, x=3657, y=1504)
print(resp[0:5])

# 都市計画決定GISデータ（高度利用地区）API
resp = client.get_high_utilization_district_gis_list(z=12, x=3637, y=1612)
print(resp[0:5])

# 国土交通省都市局（地形区分に基づく液状化の発生傾向図）API
resp = client.get_liquefaction_tendency_gis_list(z=12, x=3657, y=1504)
print(resp[0:5])

# 国土数値情報（洪水浸水想定区域（想定最大規模））API
resp = client.get_flood_inundation_assumption_area_gis_list(z=14, x=14550, y=6451)
print(resp[0:5])

# 国土数値情報（高潮浸水想定区域）API
resp = client.get_storm_surge_inundation_assumption_area_gis_list(z=13, x=7210, y=3243)
print(resp[0:5])

# 国土数値情報（津波浸水想定）API
resp = client.get_tsunami_inundation_assumption_gis_list(z=14, x=14421, y=6486)
print(resp[0:5])

# 国土数値情報（土砂災害警戒区域）API
resp = client.get_sediment_disaster_warning_area_gis_list(z=11, x=1819, y=806)
print(resp[0:5])

# 都市計画決定GISデータ（都市計画道路）API
resp = client.get_urban_planning_road_gis_list(z=11, x=1819, y=806)
print(resp[0:5])

# 国土数値情報（人口集中地区）API
resp = client.get_densely_inhabited_district_gis_list(
    z=11, x=1819, y=806, administrative_area_code="13101"
)
print(resp[0:5])

# 国土地理院GISデータ（指定緊急避難場所）API
resp = client.get_emergency_evacuation_site_gis_list(z=13, x=7272, y=3225)
print(resp[0:5])

# 国土調査（災害履歴）API
resp = client.get_disaster_history_geo_list(
    z=11, x=1819, y=806, disastertype_code="11"
)
print(resp[0:5])

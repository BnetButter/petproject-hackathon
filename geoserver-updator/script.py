import requests
import geopandas as gpd
from sqlalchemy import create_engine
import os
import time


db_host = "postgis"
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_port = 5432


url = "http://airflow-gateway:5000/inspection-data/latest"

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

while True:

    response = requests.get(url)
    if response.status_code != 200:
        continue

    data = response.json()
    gdf = gpd.GeoDataFrame.from_features(data['features'], crs="EPSG:4326")
    gdf.to_postgis('inspection_data', engine, if_exists='replace')
    print("data updated")
    time.sleep(86400)

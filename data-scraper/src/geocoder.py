import requests
import pandas as pd
import sys
import os
import time
input_file, output_file = sys.argv[1:]

df = pd.read_csv(input_file)

api_key = os.environ["GEOCODE_API"]

def google_to_single_feature(api_response):
    # Assume the first result is the desired feature
    result = api_response.get('results', [])[0] if api_response.get('results') else {}
    
    geometry = result.get('geometry', {})
    location = geometry.get('location', {})
    
    if location:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [location.get('lng'), location.get('lat')]
            },
            "properties": {
                "address": result.get('formatted_address')
            }
        }
        return feature
    
    return None


columns = [ "id", "addressLine1", "addressLine2", "addressLine3" ]

subdf = df[columns].fillna('')

results = []


for i, row in subdf.iterrows():
    id = row["id"]
    a1 = row["addressLine1"]
    a2 = row["addressLine2"]
    a3 = row["addressLine3"]

    address = f"{a1} {a2} {a3}"
    query = address.replace(" ", "+").replace(",", "+").replace("++", "+")
    if "PO+BOX" in query:
        results.append({"id": id, "geojson": None})

        continue
    
    
# Prepare the URL with the query and API key
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={query}&key={api_key}"
    result = requests.get(url)
    if result.status_code == 200:
        geojson = result.json()
        results.append({"id": id, "geojson": google_to_single_feature(geojson) })
        print(f"{id}: ok")
    else:
        results.append({"id": id, "geojson": None})
        print(f"{id}: error")
    

    

geo_df = pd.DataFrame(results)
print(geo_df)
geo_df.to_csv(output_file, index=False)
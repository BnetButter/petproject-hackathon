import sys
import pandas as pd
import json

merged1, address, summary, output = sys.argv[1:]


merged_df = pd.read_csv(merged1)
address_df = pd.read_csv(address)
summary_df = pd.read_csv(summary)


merged_address_df = pd.merge(merged_df, address_df, on='id')
final_merged_df = pd.merge(merged_address_df, summary_df, on='id')

final_merged_df['inspectionDate'] = pd.to_datetime(final_merged_df['inspectionDate'])

# Group by the individual (assuming 'id' is the unique identifier for individuals)
aggregated_df = final_merged_df.groupby('customerNumber').agg({
    'critical': 'sum',
    'direct': 'sum',
    'nonCritical': 'sum',
    'summary': ' '.join,  # Concatenate summary strings
    'legalName': 'first',  # Preserve the legalName
    'geojson': 'first',
    'addressLine1': 'first',
    'addressLine3': 'first',
    'inspectionDate': 'max'
}).reset_index()


# Convert the aggregated dataframe into GeoJSON features
features = []
for _, row in aggregated_df.iterrows():
    properties = {
        'customerNumber': row['customerNumber'],
        'critical': row['critical'],
        'direct': row['direct'],
        'nonCritical': row['nonCritical'],
        'summary': row['summary'],
        'legalName': row['legalName'],
        'address': row['addressLine1'] + row['addressLine3'],
        'latestInspection': row['inspectionDate'].strftime('%Y-%m-%d')
    }
    if row['geojson']:
        geometry = json.loads(row['geojson'].replace("'",'"'))['geometry']
        feature = {
            "type": "Feature",
            "geometry": geometry,
            "properties": properties
        }
        features.append(feature)

# Create a GeoJSON FeatureCollection
feature_collection = {
    "type": "FeatureCollection",
    "features": features
}


print(json.dumps(feature_collection, indent=2))
with open(output, "w") as fp:
# Convert the feature collection to a JSON string
    geojson_str = json.dump(feature_collection, fp, indent=2)


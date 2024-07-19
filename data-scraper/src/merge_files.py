import sys
import pandas as pd


licensee_file, violations_file, output_file = sys.argv[1:]


license_df = pd.read_csv(licensee_file)
violations_df = pd.read_csv(violations_file)

# filter out all rows with violations
violation_columns = [ 'critical', 'direct', 'nonCritical', ]
filtered_df = violations_df[ (violations_df['critical'] != 0) | (violations_df['direct'] != 0) | (violations_df['nonCritical'])]

# Merge inspection data with licensee data
result_df = pd.merge(filtered_df, license_df, on='customerNumber', how='inner')
result_df = result_df[ result_df['certStatus'] == 'Active' ]

# Dropping 'Unnamed' columns if they exist
result_df = result_df.loc[:, ~result_df.columns.str.contains('^Unnamed')]

# Resetting the index to add it as a column
result_df.reset_index(drop=True, inplace=True)
result_df.reset_index(inplace=True)
result_df.rename(columns={'index': 'id'}, inplace=True)

print(result_df)
result_df.to_csv(output_file, index=False)

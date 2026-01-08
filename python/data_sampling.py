import pandas as pd
import numpy as np

# Load the dataset
path = "online_retail_data.csv"
df = pd.read_csv(path)

# For each column, fill missing values by random sampling from existing non-null values
for col in df.columns:
    if df[col].isnull().any():
        non_null_values = df[col].dropna().values
        if len(non_null_values) > 0:
            df.loc[df[col].isnull(), col] = np.random.choice(
                non_null_values, size=df[col].isnull().sum(), replace=True
            )

# Save the filled dataset
output_path = "online_retail_data_filled_random.csv"
df.to_csv(output_path, index=False)

output_path
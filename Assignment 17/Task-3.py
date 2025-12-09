import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from datetime import datetime

# Load the dataset
print("Loading IoT sensor dataset...")
df = pd.read_csv('iot_sensor.csv')

print(f"Original dataset shape: {df.shape}")
print(f"Original columns: {df.columns.tolist()}\n")

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Sort by timestamp and sensor_id to ensure proper order for forward fill
df = df.sort_values(['timestamp', 'sensor_id']).reset_index(drop=True)

# Display initial missing values
print("="*60)
print("INITIAL MISSING VALUES")
print("="*60)
print(f"Missing temperature: {df['temperature'].isna().sum()}")
print(f"Missing humidity: {df['humidity'].isna().sum()}")
print(f"Total missing values: {df[['temperature', 'humidity']].isna().sum().sum()}\n")

# Handle missing values using forward fill
print("="*60)
print("HANDLING MISSING VALUES USING FORWARD FILL")
print("="*60)

# Store original missing counts
temp_missing_before = df['temperature'].isna().sum()
humidity_missing_before = df['humidity'].isna().sum()

# Convert to numeric
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')

# Forward fill missing values (carry forward last known value)
# Group by sensor_id to forward fill within each sensor's data
df['temperature'] = df.groupby('sensor_id')['temperature'].ffill()
df['humidity'] = df.groupby('sensor_id')['humidity'].ffill()

# If still missing (first values for a sensor), use backward fill
df['temperature'] = df.groupby('sensor_id')['temperature'].bfill()
df['humidity'] = df.groupby('sensor_id')['humidity'].bfill()

# If still missing, fill with overall mean
if df['temperature'].isna().any():
    df['temperature'] = df['temperature'].fillna(df['temperature'].mean())
if df['humidity'].isna().any():
    df['humidity'] = df['humidity'].fillna(df['humidity'].mean())

print(f"Temperature: {temp_missing_before} missing values handled")
print(f"Humidity: {humidity_missing_before} missing values handled")
print(f"\nRemaining missing values:")
print(f"  - Temperature: {df['temperature'].isna().sum()}")
print(f"  - Humidity: {df['humidity'].isna().sum()}\n")

# Remove sensor drift using rolling mean
print("="*60)
print("REMOVING SENSOR DRIFT USING ROLLING MEAN")
print("="*60)

# Apply rolling mean to smooth out sensor drift
# Using window size of 3 (can be adjusted based on data frequency)
window_size = 3

# Calculate rolling mean for each sensor separately
df['temperature_rolling_mean'] = df.groupby('sensor_id')['temperature'].transform(
    lambda x: x.rolling(window=window_size, min_periods=1, center=True).mean()
)
df['humidity_rolling_mean'] = df.groupby('sensor_id')['humidity'].transform(
    lambda x: x.rolling(window=window_size, min_periods=1, center=True).mean()
)

# Replace original values with rolling mean to remove drift
df['temperature'] = df['temperature_rolling_mean']
df['humidity'] = df['humidity_rolling_mean']

# Drop the intermediate rolling mean columns
df = df.drop(['temperature_rolling_mean', 'humidity_rolling_mean'], axis=1)

print(f"Applied rolling mean with window size: {window_size}")
print("Sensor drift removed from temperature and humidity readings\n")

# Normalize readings using standard scaling (z-score normalization)
print("="*60)
print("NORMALIZING READINGS USING STANDARD SCALING")
print("="*60)

# Store original values for comparison
df['temperature_original'] = df['temperature'].copy()
df['humidity_original'] = df['humidity'].copy()

# Apply standard scaling (z-score normalization)
# StandardScaler: (x - mean) / std
scaler_temp = StandardScaler()
scaler_humidity = StandardScaler()

df['temperature_normalized'] = scaler_temp.fit_transform(df[['temperature']])
df['humidity_normalized'] = scaler_humidity.fit_transform(df[['humidity']])

# Replace original columns with normalized values
df['temperature'] = df['temperature_normalized']
df['humidity'] = df['humidity_normalized']

# Drop intermediate columns
df = df.drop(['temperature_normalized', 'humidity_normalized'], axis=1)

print("Standard scaling applied:")
print(f"  Temperature - Mean: {scaler_temp.mean_[0]:.2f}, Std: {scaler_temp.scale_[0]:.2f}")
print(f"  Humidity - Mean: {scaler_humidity.mean_[0]:.2f}, Std: {scaler_humidity.scale_[0]:.2f}")
print(f"\nNormalized temperature range: [{df['temperature'].min():.4f}, {df['temperature'].max():.4f}]")
print(f"Normalized humidity range: [{df['humidity'].min():.4f}, {df['humidity'].max():.4f}]\n")

# Encode categorical sensor IDs
print("="*60)
print("ENCODING CATEGORICAL SENSOR IDs")
print("="*60)

# Use LabelEncoder for integer encoding
label_encoder = LabelEncoder()
df['sensor_id_encoded'] = label_encoder.fit_transform(df['sensor_id'])

# Also create one-hot encoded columns (optional, for reference)
sensor_onehot = pd.get_dummies(df['sensor_id'], prefix='sensor')
df = pd.concat([df, sensor_onehot], axis=1)

print(f"Unique sensor IDs: {df['sensor_id'].unique()}")
print(f"Encoded sensor IDs: {df['sensor_id_encoded'].unique()}")
print("\nLabel encoding mapping:")
for i, sensor in enumerate(label_encoder.classes_):
    print(f"  {sensor} -> {i}")
print("\nOne-hot encoding columns created:", sensor_onehot.columns.tolist())

# Display summary statistics
print("\n" + "="*60)
print("PREPROCESSING SUMMARY")
print("="*60)
print(f"\nFinal dataset shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")

print(f"\nOriginal Temperature Statistics:")
print(df['temperature_original'].describe())
print(f"\nNormalized Temperature Statistics:")
print(df['temperature'].describe())

print(f"\nOriginal Humidity Statistics:")
print(df['humidity_original'].describe())
print(f"\nNormalized Humidity Statistics:")
print(df['humidity'].describe())

# Save preprocessed dataset
output_file = 'iot_sensor_preprocessed.csv'
# Save main columns (excluding original columns for cleaner output)
columns_to_save = ['timestamp', 'sensor_id', 'sensor_id_encoded', 'temperature', 'humidity'] + sensor_onehot.columns.tolist()
df[columns_to_save].to_csv(output_file, index=False)
print(f"\nPreprocessed dataset saved to: {output_file}")

# Display sample of preprocessed data
print("\n" + "="*60)
print("SAMPLE OF PREPROCESSED DATA")
print("="*60)
sample_cols = ['timestamp', 'sensor_id', 'sensor_id_encoded', 'temperature', 'humidity']
print(df[sample_cols].head(15).to_string(index=False))

print("\n" + "="*60)
print("SENSOR-WISE STATISTICS")
print("="*60)
for sensor in df['sensor_id'].unique():
    sensor_data = df[df['sensor_id'] == sensor]
    print(f"\nSensor {sensor}:")
    print(f"  Count: {len(sensor_data)}")
    print(f"  Temperature (normalized): mean={sensor_data['temperature'].mean():.4f}, std={sensor_data['temperature'].std():.4f}")
    print(f"  Humidity (normalized): mean={sensor_data['humidity'].mean():.4f}, std={sensor_data['humidity'].std():.4f}")

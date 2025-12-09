import pandas as pd
import numpy as np
from datetime import datetime

# Load the dataset
print("Loading financial dataset...")
df = pd.read_csv('financial_data.csv')

print(f"Original dataset shape: {df.shape}")
print(f"Original columns: {df.columns.tolist()}\n")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Sort by date to ensure chronological order
df = df.sort_values('date').reset_index(drop=True)

# Display initial missing values
print("="*60)
print("INITIAL MISSING VALUES")
print("="*60)
print(f"Missing closing_price: {df['closing_price'].isna().sum()}")
print(f"Missing volume: {df['volume'].isna().sum()}\n")

# Handle missing values in closing_price and volume
print("="*60)
print("HANDLING MISSING VALUES")
print("="*60)

# For closing_price: forward fill, then backward fill (carry forward last known price)
# This is common in financial data as prices are continuous
closing_price_missing = df['closing_price'].isna().sum()
df['closing_price'] = pd.to_numeric(df['closing_price'], errors='coerce')
df['closing_price'] = df['closing_price'].ffill().bfill()

# If still missing (first row), use mean
if df['closing_price'].isna().any():
    df['closing_price'] = df['closing_price'].fillna(df['closing_price'].mean())

print(f"Closing price: {closing_price_missing} missing values handled (forward fill, backward fill, then mean)")

# For volume: fill with median (less sensitive to outliers than mean)
volume_missing = df['volume'].isna().sum()
df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
df['volume'] = df['volume'].fillna(df['volume'].median())

print(f"Volume: {volume_missing} missing values handled (filled with median)")

# Verify no missing values remain
print(f"\nRemaining missing values after handling:")
print(f"  - Closing price: {df['closing_price'].isna().sum()}")
print(f"  - Volume: {df['volume'].isna().sum()}\n")

# Create lag features (1-day and 7-day returns)
print("="*60)
print("CREATING LAG FEATURES")
print("="*60)

# Calculate 1-day return: (price_today - price_yesterday) / price_yesterday
df['return_1day'] = df['closing_price'].pct_change(periods=1) * 100  # as percentage
df['return_1day'] = df['return_1day'].fillna(0)  # First row will be NaN, fill with 0

# Calculate 7-day return: (price_today - price_7days_ago) / price_7days_ago
df['return_7day'] = df['closing_price'].pct_change(periods=7) * 100  # as percentage
df['return_7day'] = df['return_7day'].fillna(0)  # First 7 rows will be NaN, fill with 0

print("Created lag features:")
print(f"  - return_1day: 1-day percentage return")
print(f"  - return_7day: 7-day percentage return")
print(f"\nSample returns:")
print(df[['date', 'closing_price', 'return_1day', 'return_7day']].head(10).to_string(index=False))

# Normalize volume column using log-scaling
print("\n" + "="*60)
print("NORMALIZING VOLUME USING LOG-SCALING")
print("="*60)

# Add small constant to avoid log(0) if any volume is 0
df['volume_log'] = np.log1p(df['volume'])  # log1p = log(1 + x), handles 0 values better

print("Created normalized volume column: volume_log")
print(f"Original volume range: [{df['volume'].min():.2f}, {df['volume'].max():.2f}]")
print(f"Log-scaled volume range: [{df['volume_log'].min():.4f}, {df['volume_log'].max():.4f}]")

# Detect outliers in closing price using IQR method
print("\n" + "="*60)
print("DETECTING OUTLIERS USING IQR METHOD")
print("="*60)

# Calculate IQR (Interquartile Range)
Q1 = df['closing_price'].quantile(0.25)
Q3 = df['closing_price'].quantile(0.75)
IQR = Q3 - Q1

# Define outlier bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers
outlier_mask = (df['closing_price'] < lower_bound) | (df['closing_price'] > upper_bound)
outliers = df[outlier_mask].copy()

print(f"IQR Statistics:")
print(f"  Q1 (25th percentile): {Q1:.2f}")
print(f"  Q3 (75th percentile): {Q3:.2f}")
print(f"  IQR: {IQR:.2f}")
print(f"  Lower bound (Q1 - 1.5*IQR): {lower_bound:.2f}")
print(f"  Upper bound (Q3 + 1.5*IQR): {upper_bound:.2f}")
print(f"\nOutliers detected: {outlier_mask.sum()}")

if outlier_mask.sum() > 0:
    print("\nOutlier details:")
    print(outliers[['date', 'closing_price', 'volume']].to_string(index=False))
    
    # Add outlier flag column
    df['is_outlier'] = outlier_mask.astype(int)
else:
    print("No outliers detected.")
    df['is_outlier'] = 0

# Display summary statistics
print("\n" + "="*60)
print("PREPROCESSING SUMMARY")
print("="*60)
print(f"\nFinal dataset shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nClosing Price Statistics:")
print(df['closing_price'].describe())
print(f"\nVolume Statistics (original):")
print(df['volume'].describe())
print(f"\nVolume Statistics (log-scaled):")
print(df['volume_log'].describe())
print(f"\nReturn Statistics:")
print(f"1-day return: mean={df['return_1day'].mean():.2f}%, std={df['return_1day'].std():.2f}%")
print(f"7-day return: mean={df['return_7day'].mean():.2f}%, std={df['return_7day'].std():.2f}%")

# Save preprocessed dataset
output_file = 'financial_data_preprocessed.csv'
df.to_csv(output_file, index=False)
print(f"\nPreprocessed dataset saved to: {output_file}")

# Display sample of preprocessed data
print("\n" + "="*60)
print("SAMPLE OF PREPROCESSED DATA")
print("="*60)
print(df[['date', 'closing_price', 'volume', 'volume_log', 'return_1day', 
          'return_7day', 'is_outlier']].head(10).to_string(index=False))

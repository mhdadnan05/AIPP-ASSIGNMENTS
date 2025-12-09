import pandas as pd
import re
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Download required NLTK data if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('social_media.csv')

print(f"Original dataset shape: {df.shape}")
print(f"Original columns: {df.columns.tolist()}\n")

# Function to clean text: remove stopwords, punctuation, and special symbols
def clean_text(text):
    """
    Clean text by removing HTML tags, special symbols, punctuation, and stopwords.
    """
    if pd.isna(text):
        return ""
    
    # Convert to string
    text = str(text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    
    # Remove special characters and punctuation, keep only alphanumeric and spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    cleaned_words = [word for word in words if word not in stop_words and len(word) > 1]
    
    return ' '.join(cleaned_words)

# Clean the post_text column
print("Cleaning post text (removing stopwords, punctuation, special symbols)...")
df['cleaned_text'] = df['post_text'].apply(clean_text)

# Handle missing values in likes and shares columns
print("Handling missing values in likes and shares columns...")
# Count missing values before conversion
likes_missing = df['likes'].isna().sum() + (df['likes'] == '').sum()
shares_missing = df['shares'].isna().sum() + (df['shares'] == '').sum()

# Fill missing values with 0 (assuming missing means no likes/shares)
df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(0).astype(int)
df['shares'] = pd.to_numeric(df['shares'], errors='coerce').fillna(0).astype(int)

# Convert timestamp to datetime and extract features
print("Converting timestamp to datetime and extracting features...")
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df['hour'] = df['timestamp'].dt.hour
df['weekday'] = df['timestamp'].dt.day_name()

# Detect and remove duplicate posts
print("Detecting duplicate posts...")
# Consider posts with identical cleaned text as duplicates
duplicate_mask = df.duplicated(subset=['cleaned_text'], keep='first')
duplicate_count = duplicate_mask.sum()
print(f"Found {duplicate_count} duplicate posts based on cleaned text")

# Remove duplicates, keeping the first occurrence
df_cleaned = df[~duplicate_mask].copy()

# Detect spam posts (optional: posts with very short cleaned text or repeated patterns)
print("Detecting spam posts...")
# Consider posts with cleaned text length < 3 characters as potential spam
spam_mask = df_cleaned['cleaned_text'].str.len() < 3
spam_count = spam_mask.sum()
print(f"Found {spam_count} potential spam posts (very short cleaned text)")

# Remove spam posts
df_cleaned = df_cleaned[~spam_mask].copy()

# Display summary
print("\n" + "="*60)
print("CLEANING SUMMARY")
print("="*60)
print(f"Original dataset: {df.shape[0]} posts")
print(f"After removing duplicates: {df_cleaned.shape[0]} posts")
print(f"Removed: {df.shape[0] - df_cleaned.shape[0]} posts")
print("\nMissing values handled:")
print(f"  - Likes: {likes_missing} missing values filled with 0")
print(f"  - Shares: {shares_missing} missing values filled with 0")

# Display sample of cleaned data
print("\n" + "="*60)
print("SAMPLE OF CLEANED DATA")
print("="*60)
print("\nFirst 5 rows of cleaned dataset:")
print(df_cleaned[['post_id', 'user', 'post_text', 'cleaned_text', 'likes', 'shares', 
                  'timestamp', 'hour', 'weekday']].head().to_string(index=False))

# Save preprocessed dataset
output_file = 'social_media_preprocessed.csv'
df_cleaned.to_csv(output_file, index=False)
print(f"\nPreprocessed dataset saved to: {output_file}")

# Display statistics
print("\n" + "="*60)
print("DATASET STATISTICS")
print("="*60)
print(f"\nTotal posts after cleaning: {len(df_cleaned)}")
print(f"\nLikes statistics:")
print(df_cleaned['likes'].describe())
print(f"\nShares statistics:")
print(df_cleaned['shares'].describe())
print(f"\nPosts by weekday:")
print(df_cleaned['weekday'].value_counts().sort_index())
print(f"\nPosts by hour:")
print(df_cleaned['hour'].value_counts().sort_index())

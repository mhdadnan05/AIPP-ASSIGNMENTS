import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
print("Loading movie reviews dataset...")
df = pd.read_csv('movie_reviews.csv')

print(f"Original dataset shape: {df.shape}")
print(f"Original columns: {df.columns.tolist()}\n")

# Store original data for comparison
df_original = df.copy()

# Display initial statistics
print("="*60)
print("BEFORE PREPROCESSING - DATASET STATISTICS")
print("="*60)
print(f"Total reviews: {len(df)}")
print(f"Missing ratings: {df['rating'].isna().sum()}")
print(f"Rating statistics:")
print(df['rating'].describe())
print(f"\nSample review texts (first 3):")
for idx, row in df.head(3).iterrows():
    print(f"  Review {row['review_id']}: {row['review_text'][:50]}...")

# Standardize text (lowercase, remove HTML tags)
print("\n" + "="*60)
print("STANDARDIZING TEXT")
print("="*60)

def standardize_text(text):
    """
    Standardize text by:
    - Converting to lowercase
    - Removing HTML tags
    - Removing extra whitespace
    """
    if pd.isna(text):
        return ""
    
    # Convert to string
    text = str(text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Apply text standardization
df['review_text_standardized'] = df['review_text'].apply(standardize_text)

print("Text standardization completed:")
print(f"  - Converted to lowercase")
print(f"  - Removed HTML tags")
print(f"  - Normalized whitespace")
print(f"\nSample standardized texts:")
for idx, row in df.head(3).iterrows():
    print(f"  Original: {row['review_text']}")
    print(f"  Standardized: {row['review_text_standardized']}\n")

# Handle missing ratings (fill with median)
print("="*60)
print("HANDLING MISSING RATINGS")
print("="*60)

missing_ratings_before = df['rating'].isna().sum()
median_rating = df['rating'].median()

# Fill missing ratings with median
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating'] = df['rating'].fillna(median_rating)

print(f"Missing ratings before: {missing_ratings_before}")
print(f"Median rating: {median_rating:.2f}")
print(f"Missing ratings after: {df['rating'].isna().sum()}")

# Store original ratings for normalization
df['rating_original'] = df['rating'].copy()

# Normalize ratings (0-10 → 0-1 scale)
print("\n" + "="*60)
print("NORMALIZING RATINGS (0-10 to 0-1 SCALE)")
print("="*60)

# Using MinMaxScaler to normalize from 0-10 to 0-1
scaler = MinMaxScaler(feature_range=(0, 1))
# Assuming ratings are on 0-10 scale
df['rating_normalized'] = scaler.fit_transform(df[['rating']])

# Alternative: Manual normalization (rating / 10)
df['rating_normalized_manual'] = df['rating'] / 10.0

# Use the MinMaxScaler result
df['rating'] = df['rating_normalized']

print(f"Rating normalization completed:")
print(f"  Original range: [{df['rating_original'].min():.2f}, {df['rating_original'].max():.2f}]")
print(f"  Normalized range: [{df['rating'].min():.4f}, {df['rating'].max():.4f}]")
print(f"\nSample normalized ratings:")
print(df[['review_id', 'rating_original', 'rating']].head(5).to_string(index=False))

# Tokenize and encode reviews using TF-IDF
print("\n" + "="*60)
print("TOKENIZING AND ENCODING REVIEWS USING TF-IDF")
print("="*60)

# Initialize TF-IDF Vectorizer
# Using common parameters for text analysis
tfidf_vectorizer = TfidfVectorizer(
    max_features=100,  # Limit to top 100 features for demonstration
    ngram_range=(1, 2),  # Unigrams and bigrams
    min_df=1,  # Minimum document frequency
    max_df=0.95,  # Maximum document frequency (ignore very common words)
    stop_words='english'  # Remove English stopwords
)

# Fit and transform the standardized reviews
tfidf_matrix = tfidf_vectorizer.fit_transform(df['review_text_standardized'])

# Convert to DataFrame for better visualization
feature_names = tfidf_vectorizer.get_feature_names_out()
df_tfidf = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=[f'tfidf_{name}' for name in feature_names]
)

# Add TF-IDF features to main dataframe
df = pd.concat([df, df_tfidf], axis=1)

print(f"TF-IDF encoding completed:")
print(f"  Vocabulary size: {len(feature_names)}")
print(f"  Feature matrix shape: {tfidf_matrix.shape}")
print(f"\nTop 10 TF-IDF features:")
# Get mean TF-IDF scores for each feature
feature_importance = pd.Series(
    tfidf_matrix.mean(axis=0).A1,
    index=feature_names
).sort_values(ascending=False)
print(feature_importance.head(10))

# Display sample TF-IDF encoding for first review
print(f"\nSample TF-IDF encoding for first review:")
first_review_features = df_tfidf.iloc[0]
top_features = first_review_features.nlargest(5)
print("Top 5 features:")
for feature, score in top_features.items():
    print(f"  {feature}: {score:.4f}")

# Generate before vs after summary report
print("\n" + "="*60)
print("BEFORE VS AFTER SUMMARY REPORT")
print("="*60)

print("\n" + "-"*60)
print("1. DATASET OVERVIEW")
print("-"*60)
print(f"  Before: {df_original.shape[0]} reviews, {df_original.shape[1]} columns")
print(f"  After:  {df.shape[0]} reviews, {df.shape[1]} columns")
print(f"  New features added: {df.shape[1] - df_original.shape[1]}")

print("\n" + "-"*60)
print("2. TEXT PREPROCESSING")
print("-"*60)
print("  Before:")
print(f"    - Text contains HTML tags: {df_original['review_text'].str.contains('<', na=False).sum()} reviews")
print(f"    - Mixed case text")
print(f"    - Sample: '{df_original['review_text'].iloc[0]}'")
print("  After:")
print(f"    - HTML tags removed: {df['review_text_standardized'].str.contains('<', na=False).sum()} reviews with tags")
print(f"    - All lowercase")
print(f"    - Sample: '{df['review_text_standardized'].iloc[0]}'")

print("\n" + "-"*60)
print("3. MISSING VALUES HANDLING")
print("-"*60)
print(f"  Before:")
print(f"    - Missing ratings: {df_original['rating'].isna().sum()}")
print(f"    - Missing percentage: {(df_original['rating'].isna().sum() / len(df_original) * 100):.2f}%")
print(f"  After:")
print(f"    - Missing ratings: {df['rating'].isna().sum()}")
print(f"    - Filled with median: {median_rating:.2f}")

print("\n" + "-"*60)
print("4. RATING STATISTICS")
print("-"*60)
print("  Before (Original 0-10 scale):")
print(f"    - Mean: {df_original['rating'].mean():.2f}")
print(f"    - Median: {df_original['rating'].median():.2f}")
print(f"    - Std: {df_original['rating'].std():.2f}")
print(f"    - Min: {df_original['rating'].min():.2f}")
print(f"    - Max: {df_original['rating'].max():.2f}")
print("  After (Normalized 0-1 scale):")
print(f"    - Mean: {df['rating'].mean():.4f}")
print(f"    - Median: {df['rating'].median():.4f}")
print(f"    - Std: {df['rating'].std():.4f}")
print(f"    - Min: {df['rating'].min():.4f}")
print(f"    - Max: {df['rating'].max():.4f}")

print("\n" + "-"*60)
print("5. TEXT ENCODING (TF-IDF)")
print("-"*60)
print("  Before:")
print(f"    - Raw text only")
print(f"    - No numerical representation")
print("  After:")
print(f"    - TF-IDF features: {len(feature_names)}")
print(f"    - Feature matrix: {tfidf_matrix.shape}")
print(f"    - Top features: {', '.join(feature_importance.head(5).index.tolist())}")

print("\n" + "-"*60)
print("6. DATA QUALITY IMPROVEMENTS")
print("-"*60)
print("  [OK] Text standardized (lowercase, no HTML)")
print("  [OK] Missing ratings handled")
print("  [OK] Ratings normalized to 0-1 scale")
print("  [OK] Reviews encoded using TF-IDF")
print("  [OK] Ready for machine learning models")

# Save preprocessed dataset
output_file = 'movie_reviews_preprocessed.csv'
# Save main columns (excluding TF-IDF features for readability, but include key columns)
columns_to_save = ['review_id', 'review_text', 'review_text_standardized', 
                   'rating_original', 'rating'] + [col for col in df.columns if col.startswith('tfidf_')]
df[columns_to_save].to_csv(output_file, index=False)
print(f"\n" + "="*60)
print(f"Preprocessed dataset saved to: {output_file}")
print("="*60)

# Save summary report to file
summary_file = 'preprocessing_summary_report.txt'
with open(summary_file, 'w') as f:
    f.write("="*60 + "\n")
    f.write("MOVIE REVIEWS PREPROCESSING SUMMARY REPORT\n")
    f.write("="*60 + "\n\n")
    f.write(f"Dataset: movie_reviews.csv\n")
    f.write(f"Total Reviews: {len(df)}\n")
    f.write(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("BEFORE PREPROCESSING:\n")
    f.write(f"  - Missing ratings: {df_original['rating'].isna().sum()}\n")
    f.write(f"  - HTML tags present: {df_original['review_text'].str.contains('<', na=False).sum()} reviews\n")
    f.write(f"  - Rating range: {df_original['rating'].min():.2f} - {df_original['rating'].max():.2f}\n\n")
    
    f.write("AFTER PREPROCESSING:\n")
    f.write(f"  - Missing ratings: {df['rating'].isna().sum()}\n")
    f.write(f"  - HTML tags removed: [OK]\n")
    f.write(f"  - Text standardized: [OK]\n")
    f.write(f"  - Rating range: {df['rating'].min():.4f} - {df['rating'].max():.4f}\n")
    f.write(f"  - TF-IDF features: {len(feature_names)}\n")
    f.write(f"  - Ready for ML: [OK]\n")

print(f"Summary report saved to: {summary_file}")

# Display final sample
print("\n" + "="*60)
print("FINAL PREPROCESSED DATA SAMPLE")
print("="*60)
sample_cols = ['review_id', 'review_text_standardized', 'rating_original', 'rating']
print(df[sample_cols].head(10).to_string(index=False))

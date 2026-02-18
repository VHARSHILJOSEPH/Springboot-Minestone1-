# ==========================================
# AMAZON DATASET COMPLETE PIPELINE
# Data Cleaning + Data Extraction
# Data Insertion + Data Analysis + Plotting
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. DATA EXTRACTION
# -----------------------------
df = pd.read_csv("amazon.csv")
print("Original Shape:", df.shape)

# -----------------------------
# 2. DATA CLEANING
# -----------------------------

# Remove duplicates
df = df.drop_duplicates()

# Clean price columns (remove ₹ and commas)
df['discounted_price'] = df['discounted_price'].astype(str)\
    .str.replace('₹','', regex=False)\
    .str.replace(',','', regex=False)

df['actual_price'] = df['actual_price'].astype(str)\
    .str.replace('₹','', regex=False)\
    .str.replace(',','', regex=False)

# Convert to numeric
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')

# Clean discount %
df['discount_percentage'] = df['discount_percentage'].astype(str)\
    .str.replace('%','', regex=False)

df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')

# Clean rating and rating_count
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

df['rating_count'] = df['rating_count'].astype(str)\
    .str.replace(',','', regex=False)

df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

# Handle missing values (numeric columns)
df.fillna(df.median(numeric_only=True), inplace=True)

print("After Cleaning Shape:", df.shape)

# -----------------------------
# 3. DATA INSERTION (Feature Engineering)
# -----------------------------

# Savings column
df['savings'] = df['actual_price'] - df['discounted_price']

# Extract main category
df['main_category'] = df['category'].apply(lambda x: str(x).split('|')[0])

print("New Columns Added: savings, main_category")

# -----------------------------
# 4. DATA ANALYSIS
# -----------------------------

print("\nTop 5 Expensive Products:")
print(df.sort_values(by='discounted_price', ascending=False)
      [['product_name','discounted_price']].head())

print("\nTop 5 Highest Rated Products (>1000 reviews):")
print(df[df['rating_count'] > 1000]
      .sort_values(by='rating', ascending=False)
      [['product_name','rating','rating_count']].head())

# -----------------------------
# 5. DATA PLOTTING
# -----------------------------

# Price Distribution
plt.figure()
plt.hist(df['discounted_price'], bins=30)
plt.title("Discounted Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()

# Rating vs Price
plt.figure()
plt.scatter(df['discounted_price'], df['rating'])
plt.title("Rating vs Price")
plt.xlabel("Price")
plt.ylabel("Rating")
plt.show()

# Top 10 Categories
top_categories = df['main_category'].value_counts().head(10)

plt.figure()
top_categories.plot(kind='bar')
plt.title("Top 10 Categories")
plt.xlabel("Category")
plt.ylabel("Number of Products")
plt.show()

print("\nFULL PIPELINE EXECUTED SUCCESSFULLY")

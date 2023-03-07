import pandas as pd


# Read in the data
info = pd.read_csv("info.csv")
finance = pd.read_csv("finance.csv")
reviews = pd.read_csv("reviews.csv")
traffic = pd.read_csv("traffic.csv")
brands = pd.read_csv("brands.csv")

# Merge the data
df = info.merge(finance, on="product_id", how="outer")
df = df.merge(reviews, on="product_id", how="outer")
df = df.merge(traffic, on="product_id", how="outer")
df = df.merge(brands, on="product_id", how="outer")

# Drop null values
df.dropna(inplace=True)

# Add price labels based on listing_price quartiles
df["price_label"] = pd.qcut(df["listing_price"], 4, labels=["Budget", "Average", "Expensive", "Elite"])

# Group by brand and price_label to get volume and mean revenue
adidas_vs_nike = df.groupby(["brand", "price_label"]).agg({"price_label": "count", "revenue": "mean"})

# Upper description length limits
lengthes = [0, 99, 199, 299, 399, 499, 599, 699]

# Description length labels
labels = ["99", "199", "299", "399", "499", "599", "699"]

# Store the length of each description
df["word_limit"] = df["description"].str.len()

# Cut into bins
df["word_limit"] = pd.cut(df["word_limit"], bins=lengthes, labels=labels)

# Group by the bins
descriptions = df.groupby("word_limit", as_index=False).agg({"rating": "mean", "reviews": "count"})

# Copy the DataFrame to avoid overwriting or filtering the original data
shoes = df.copy(deep=True)

# List of footwear keywords
mylist = "shoe*|trainer*|foot*"

# Filter for footwear products
shoes = df[df["description"].str.contains(mylist)]

# Filter for clothing products
clothing = df[~df.isin(shoes["product_id"])]

# Remove null product_id values from clothing DataFrame
clothing.dropna(inplace=True)

# Create product_types DataFrame for compare footwear and clothing products
product_types = pd.DataFrame({"clothing_products": len(clothing), 
                              "clothing_revenue": clothing["revenue"].median(), 
                              "footwear_products": len(shoes), 
                              "footwear_revenue": shoes["revenue"].median()}, 
                              index=[0])

# the results
revenue_analysis = {"brand_analysis": adidas_vs_nike,
                    "description_analysis": descriptions,
                    "product_analysis": product_types}

# the answer
# print(revenue_analysis)

for key, value in revenue_analysis.items():
    print(key, " : \n", value, '\n')
import pandas as pd
import ast

# Load your original file
#df = pd.read_csv("output_dataframe.csv")
df = pd.read_csv("cleaned_ev_stations.csv")

# Keep only required columns
df_key = df[[
    "title", "address", "reviews", "popularTimesHistogram.Su", "popularTimesHistogram.Mo",
    "popularTimesHistogram.Tu", "popularTimesHistogram.We", "popularTimesHistogram.Th",
    "popularTimesHistogram.Fr", "popularTimesHistogram.Sa", "rank", "location.lat", "location.lng"
]]

# Extract review text snippets
def extract_review_text(raw):
    try:
        reviews = ast.literal_eval(raw) if isinstance(raw, str) else raw
        if isinstance(reviews, list):
            return " | ".join([r.get("snippet", "") for r in reviews if isinstance(r, dict)])
    except:
        return ""
    return ""

df_key["review_snippets"] = df_key["reviews"].apply(extract_review_text)

# Fill missing popularTimesHistogram.* fields
popular_cols = [col for col in df_key.columns if col.startswith("popularTimesHistogram.")]
df_key[popular_cols] = df_key[popular_cols].fillna("[]")

# Normalize title and address
df_key["title"] = df_key["title"].fillna("").astype(str)
df_key["address"] = df_key["address"].fillna("").astype(str)

# Final DataFrame for PandasAI
df_ready = df_key[[
    "title", "address", "review_snippets", "rank", "location.lat", "location.lng"
] + popular_cols]

# Save cleaned file
df_ready.to_csv("cleaned_ev_stations.csv", index=False)
print("✅ Cleaned file saved as 'cleaned_ev_stations.csv'")


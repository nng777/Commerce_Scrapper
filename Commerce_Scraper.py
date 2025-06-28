import requests
import pandas as pd
import numpy as np

# Step 1: Call the Platzi Fake Store API
url = "https://publicapi.dev/platzi-fake-store-api/products"

response = requests.get(url)
response.raise_for_status()  # Raise error if failed
data = response.json()

# Step 2: Extract product info
products = []

for item in data:
    name = item.get("title", "N/A")
    price = item.get("price", 0)

    # Some products have ratings nested
    rating_data = item.get("rating", {})
    rating = rating_data.get("rate", 0.0)

    products.append({
        "Name": name,
        "Price": price,
        "Rating": rating
    })

# Step 3: Create DataFrame
df = pd.DataFrame(products)

# Step 4: Calculate averages
average_price = np.mean(df["Price"])
average_rating = np.mean(df["Rating"])

# Step 5: Show output
print(df.head())
print("\n📊 Average Price: ${:,.2f}".format(average_price))
print("⭐ Average Rating: {:.2f}".format(average_rating))

from __future__ import annotations

import numpy as np
import pandas as pd
import requests

from typing import Any, List, Dict

API_URL = "https://api.escuelajs.co/api/v1/products"


def extract_rating(product: Dict[str, Any]) -> float:
    """Return the numeric rating for ``product`` if present."""
    rating = product.get("rating")
    if isinstance(rating, dict):
        rating = rating.get("rate")
    try:
        return float(rating)
    except (TypeError, ValueError):
        return np.nan


def fetch_all_products(url: str = API_URL) -> pd.DataFrame:
    """Fetch all products from ``url`` and return them as a DataFrame."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()

    items: List[Dict[str, Any]] = []
    for prod in data:
        name = prod.get("title", "")
        price = prod.get("price")
        items.append({"Name": name, "Price": price})

    return pd.DataFrame(items)


def main() -> None:
    """Download product data and print average price."""
    df = fetch_all_products()
    print(df)

    avg_price = np.nanmean(df["Price"])

    print(f"Average Price: {avg_price}")


if __name__ == "__main__":
    main()
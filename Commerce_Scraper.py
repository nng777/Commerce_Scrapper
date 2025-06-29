import numpy as np
import pandas as pd
import requests
from typing import Any, List, Dict

API_URL = "https://api.escuelajs.co/api/v1/products"


class CommerceScraper:
    """Utility class for downloading and processing product data."""

    api_url: str = API_URL

    @staticmethod
    def price_rating(price):
        """Return the rating category for ``price``."""
        try:
            value = float(price)
        except (TypeError, ValueError):
            return np.nan

        if value <= 50:
            return 1
        if value <= 100:
            return 2
        return 3

    @staticmethod
    def extract_rating(product):
        """Return the numeric rating for ``product`` if present."""
        rating = product.get("rating")
        if isinstance(rating, dict):
            rating = rating.get("rate")
        try:
            return float(rating)
        except (TypeError, ValueError):
            return np.nan

    def fetch_all_products(self):
        """Fetch all products from the API and return them as a DataFrame."""
        response = requests.get(self.api_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        items: List[Dict[str, Any]] = []
        for prod in data:
            name = prod.get("title", "")
            price = prod.get("price")
            items.append({
                "Name": name,
                "Price": price,
                "Price Rating": self.price_rating(price),
            })

        return pd.DataFrame(items)

    def report(self):
        """Download product data and print average statistics."""
        df = self.fetch_all_products()
        print(df)

        avg_price = np.nanmean(df["Price"])
        avg_price_rating = np.nanmean(df["Price Rating"])

        print(f"Average Price: {avg_price:.2f}")
        print(f"Average Price Rating: {avg_price_rating:.2f}")


def main():
    """Run the command line interface."""
    CommerceScraper().report()


if __name__ == "__main__":
    main()

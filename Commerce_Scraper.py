'''Scrape product details (name, price, rating) from a single category of an e-commerce website.
Use Pandas to store the data and NumPy to find the average price and rating.'''

import numpy as np
import pandas as pd
import requests
from typing import Any, List, Dict

API_URL = "https://api.escuelajs.co/api/v1/products"


class CommerceScraper:

    api_url: str = API_URL

    @staticmethod
    def price_rating(price):
        #Return the rating category for price
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
        #Return the numeric rating for product
        rating = product.get("rating")
        if isinstance(rating, dict):
            rating = rating.get("rate")
        try:
            return float(rating)
        except (TypeError, ValueError):
            return np.nan

    def fetch_all_products(self):
        #Fetch all products from the API and return them as a DataFrame
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

    def generate_html_report(self, output_file: str = "products.html"):
        """Generate an HTML page containing the product comparison table."""
        df = self.fetch_all_products()

        avg_price = np.nanmean(df["Price"])
        avg_price_rating = np.nanmean(df["Price Rating"])

        table_html = df.to_html(index=False, classes="product-table", border=0)

        html = f"""<!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <title>Product Comparison</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .product-table {{
                border-collapse: collapse;
                width: 100%;
            }}
            .product-table th, .product-table td {{
                border: 1px solid #ddd;
                padding: 8px;
            }}
            .product-table th {{
                background-color: #f2f2f2;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <h1>Product Comparison</h1>
        {table_html}
        <p><strong>Average Price:</strong> {avg_price:.2f}</p>
        <p><strong>Average Price Rating:</strong> {avg_price_rating:.2f}</p>
    </body>
    </html>"""

        with open(output_file, "w", encoding="utf-8") as fh:
            fh.write(html)

        print(f"HTML report saved to {output_file}")

    def report(self):
        #Fetch product data and print average statistics.
        df = self.fetch_all_products()
        print(df)

        avg_price = np.nanmean(df["Price"])
        avg_price_rating = np.nanmean(df["Price Rating"])

        print(f"Average Price: {avg_price:.2f}")
        print(f"Average Price Rating: {avg_price_rating:.2f}")


def main():

    scraper = CommerceScraper()
    scraper.report()
    scraper.generate_html_report()


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import json

def fetch_filament_data():
    url = "https://www.esun3d.com/pla-pro-product/"  # Replace with the actual URL
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    filaments = []

    product_title = soup.select_one(".product-title").text.strip()
    product_desc = soup.select_one(".product-desc").text.strip()
    colors = [color.text.strip() for color in soup.select(".attr-color-item p")]
    diameter_sizes = [size.text.strip() for size in soup.select(".attr-opt-item span.opt-item-btn")]
    net_weight = soup.select_one(".attr-cell-cont").text.strip().split()[-1]

    filaments.append({
        "name": product_title,
        "description": product_desc,
        "colors": colors,
        "diameter_sizes": diameter_sizes,
        "net_weight": net_weight
    })

    with open("filament_data.json", "w") as f:
        json.dump(filaments, f)

if __name__ == "__main__":
    fetch_filament_data()

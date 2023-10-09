from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def fetch_filament_data():
    url = "https://www.esun3d.com/pla-pro-product/"
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

    return filaments

@app.route('/api/filamentData', methods=['GET'])
def get_filament_data():
    data = fetch_filament_data()
    if not data:
        return jsonify({"error": "Unable to fetch filament data"}), 500
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5000)  # This will start the Flask app on port 5000

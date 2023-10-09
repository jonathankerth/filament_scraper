from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import os

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
    
    # Print a message to the console when the API is accessed
    print("API accessed. Data fetched successfully.")
    
    return jsonify(data)

# Add a route handler for the root URL '/'
@app.route('/', methods=['GET'])
def root():
    # Return a simple message to indicate that the server is running
    return "Server is running!"

# Add a route handler for the 'favicon.ico' path
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    # Return an empty response for favicon requests
    return '', 204

if __name__ == "__main__":
    # Get the port provided by Heroku or use 5000 if running locally
    port = int(os.environ.get("PORT", 5000))
    
    # Print a message indicating that the server is starting
    print("Starting Flask app...")
    
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify, render_template
from scraper import compare_product, extract_asin
from database import insert_comparison, create_database
import sqlite3

app = Flask(__name__)

# Initialize the database
create_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare_products', methods=['POST'])
def compare_products():
    try:
        data = request.json
        url = data['url']
        product_id = extract_asin(url)

        # Get comparison data using PriceAPI
        comparison_data = compare_product(product_id)
        
        if comparison_data:
            # Optionally, save the comparison data to a database
            for product in comparison_data:
                if product['type'] == 'target':  # Only save the target product's price
                    insert_comparison(product_id, product['price'])
            
            # Return the comparison data to the frontend
            return jsonify({'comparison': comparison_data})
        else:
            return jsonify({'error': 'Failed to retrieve comparison data'}), 500
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

if __name__ == "__main__":
    app.run(debug=True)

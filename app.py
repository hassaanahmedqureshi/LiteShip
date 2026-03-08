from flask import Flask, request, jsonify
from repositories.price_repository import PriceRepository
from services.pricing_engine import PricingEngine
from repositories.db_manager import DatabaseManager

app = Flask(__name__)

def round_values(data, decimals=2):
    if isinstance(data, dict):
        return {k: round_values(v, decimals) for k, v in data.items()}
    elif isinstance(data, float):
        return round(data, decimals)
    return data

@app.route('/api/quote', methods=['POST'])
def calculate_quote():
    """
    Calculate shipping quote
    Body: {
        "client_code": "ALFA001",
        "weight": 4,
        "accessories": ["fuel", "cod"]
    }
    """
    try:
        data = request.json

        repo = PriceRepository()
        engine = PricingEngine()

        # Get master list
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM master_list LIMIT 1")
        master_id = cursor.fetchone()[0]
        conn.close()

        master = repo.get_master_list(master_id)
        sales = repo.get_sales_list_by_client_code(data['client_code'])

        quote = engine.calculate_quote(
            master,
            sales,
            weight=data['weight'],
            accessories_needed=data.get('accessories', [])
        )

        return jsonify({
            "success": True,
            "data": round_values(quote)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "LiteShip Pricing Engine"})

if __name__ == '__main__':
    print("LiteShip API running on http://localhost:5000")
    print("Docs: POST /api/quote | GET /api/health")
    app.run(debug=True, port=5000)

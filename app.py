from flask import Flask, request, jsonify
from repositories.price_repository import PriceRepository
from services.pricing_engine import PricingEngine

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

        master = repo.get_first_master_list()
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

@app.route('/api/clients', methods=['POST'])
def create_client():
    try:
        data = request.json
        repo = PriceRepository()
        client_id = repo.create_client(data['name'], data['code'])
        return jsonify({
            "success": True,
            "client_id": client_id,
            "message": "Client created successfully"
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/sales-list', methods=['POST'])
def create_sales_list():
    try:
        data = request.json
        repo = PriceRepository()
        sales_list_id = repo.create_sales_list(
            data['client_code'],
            data['master_list_id'],
            data['markup_rules']
        )
        return jsonify({
            "success": True,
            "sales_list_id": sales_list_id,
            "message": "Sales price list created successfully"
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "LiteShip Pricing Engine"})

if __name__ == '__main__':
    print("LiteShip API running on http://localhost:5000")
    print("Endpoints:")
    print("  POST /api/clients - Create new client")
    print("  POST /api/sales-list - Create new sales price list")
    print("  POST /api/quote - Calculate shipping quote")
    print("  GET /api/health - Health check")
    app.run(debug=True, port=5000)

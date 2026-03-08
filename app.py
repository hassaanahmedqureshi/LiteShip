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

@app.route('/api/clients', methods=['POST'])
def create_client():
    """
    Create new client
    Body: {
        "name": "Gamma",
        "code": "GAMMA001"
    }
    """
    try:
        data = request.json
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()

        # Check if client code already exists
        cursor.execute("SELECT id FROM clients WHERE code = ?", (data['code'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({"success": False, "error": "Client code already exists"}), 400

        # Create client
        cursor.execute(
            "INSERT INTO clients (name, code) VALUES (?, ?)",
            (data['name'], data['code'])
        )
        client_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "client_id": client_id,
            "message": "Client created successfully"
        }), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/sales-list', methods=['POST'])
def create_sales_list():
    """
    Create new sales price list
    Body: {
        "client_code": "BETA001",
        "master_list_id": 1,
        "markup_rules": [
            {"applies_to": "freight", "calc_type": "percent", "value": 15},
            {"applies_to": "handling", "calc_type": "fixed", "value": 2.0},
            {"applies_to": "cod", "calc_type": "override", "value": 2.5}
        ]
    }
    """
    try:
        data = request.json
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()

        # Get client ID
        cursor.execute("SELECT id FROM clients WHERE code = ?", (data['client_code'],))
        client_row = cursor.fetchone()
        if not client_row:
            conn.close()
            return jsonify({"success": False, "error": "Client not found"}), 404

        # Create sales list
        cursor.execute(
            "INSERT INTO sales_list (client_id, master_list_id) VALUES (?, ?)",
            (client_row[0], data['master_list_id'])
        )
        sales_list_id = cursor.lastrowid

        # Add markup rules
        for rule in data['markup_rules']:
            cursor.execute(
                "INSERT INTO markup_rules (sales_list_id, applies_to, calc_type, value) VALUES (?, ?, ?, ?)",
                (sales_list_id, rule['applies_to'], rule['calc_type'], rule['value'])
            )

        conn.commit()
        conn.close()

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

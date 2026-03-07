import sys

sys.path.append('.')

from repositories.price_repository import PriceRepository
from services.pricing_engine import PricingEngine

def check_db():
    from repositories.db_manager import DatabaseManager
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM master_list")
    print(f"Master lists in DB: {cursor.fetchone()[0]}")

    cursor.execute("SELECT * FROM master_list")
    print(f"Data: {cursor.fetchall()}")
    conn.close()

def test_alfa_quote():
    repo = PriceRepository()
    engine = PricingEngine()

    # Load data - get the first master list dynamically
    from repositories.db_manager import DatabaseManager
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM master_list LIMIT 1")
    master_id = cursor.fetchone()[0]
    conn.close()

    master = repo.get_master_list(master_id)
    sales = repo.get_sales_list_by_client_code('ALFA001')

    # Calculate quote: 4kg with COD
    quote = engine.calculate_quote(master, sales, weight=4, accessories_needed=['fuel', 'cod'])

    print("\n=== QUOTE FOR CLIENT ALFA ===")
    print(f"Weight: 4kg | Accessories: Fuel, COD\n")
    print(f"Base Cost:   €{quote['base_cost']:.2f}")
    print(f"Sales Price: €{quote['sales_price']:.2f}")
    print(f"Margin:      €{quote['margin']:.2f}\n")

    print("Breakdown:")
    print(f"  Base Freight:  €{quote['breakdown']['base_freight']:.2f}")
    print(f"  Sales Freight: €{quote['breakdown']['sales_freight']:.2f} (+20%)")
    print(f"  Fuel:          €{quote['breakdown']['sales_accessories']['fuel']:.2f}")
    print(f"  COD:           €{quote['breakdown']['sales_accessories']['cod']:.2f}")
    print(f"  Handling:      €{quote['breakdown']['handling']:.2f}")

    # Verify expected result
    expected = 10.92
    if abs(quote['sales_price'] - expected) < 0.01:
        print(f"\nSuccess: Expected €{expected:.2f}, got €{quote['sales_price']:.2f}")
    else:
        print(f"\nError: Expected €{expected:.2f}, got €{quote['sales_price']:.2f}")


if __name__ == '__main__':
    check_db()
    test_alfa_quote()

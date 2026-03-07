import sys
sys.path.append('.')

from repositories.db_manager import DatabaseManager

def seed_database():
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()

    # Master List (SDA)
    cursor.execute("INSERT INTO master_list (name, courier) VALUES (?, ?)",
                   ("SDA Contract 2024", "SDA"))
    master_id = cursor.lastrowid

    # Add Freight Rates
    cursor.execute("""
        INSERT INTO freight_rates (master_list_id, weight_min, weight_max, price)
        VALUES (?, ?, ?, ?)
    """, (master_id, 0, 5, 6.00))

    cursor.execute("""
        INSERT INTO freight_rates (master_list_id, weight_min, weight_max, price)
        VALUES (?, ?, ?, ?)
    """, (master_id, 5, 10, 9.00))

    # Add Accessories
    cursor.execute("""
        INSERT INTO accessories (master_list_id, type, calc_type, value)
        VALUES (?, ?, ?, ?)
    """, (master_id, 'fuel', 'percent', 10))

    cursor.execute("""
        INSERT INTO accessories (master_list_id, type, calc_type, value)
        VALUES (?, ?, ?, ?)
    """, (master_id, 'cod', 'fixed', 1.50))

    # Create Client Alfa
    cursor.execute("INSERT INTO clients (name, code) VALUES (?, ?)",
                   ("Alfa", "ALFA001"))
    client_id = cursor.lastrowid

    # Create Sales List for Alfa
    cursor.execute("""
        INSERT INTO sales_list (client_id, master_list_id)
        VALUES (?, ?)
    """, (client_id, master_id))
    sales_id = cursor.lastrowid

    # Add Markup Rules for Alfa
    # Freight +20%
    cursor.execute("""
        INSERT INTO markup_rules (sales_list_id, applies_to, calc_type, value)
        VALUES (?, ?, ?, ?)
    """, (sales_id, 'freight', 'percent', 20))

    # Handling +€1.00
    cursor.execute("""
        INSERT INTO markup_rules (sales_list_id, applies_to, calc_type, value)
        VALUES (?, ?, ?, ?)
    """, (sales_id, 'handling', 'fixed', 1.00))

    # COD override to €2.00
    cursor.execute("""
        INSERT INTO markup_rules (sales_list_id, applies_to, calc_type, value)
        VALUES (?, ?, ?, ?)
    """, (sales_id, 'cod', 'override', 2.00))

    conn.commit()
    conn.close()
    print("Database seeded with example data")

if __name__ == '__main__':
    seed_database()

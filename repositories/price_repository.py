from repositories.db_manager import DatabaseManager
from models.master_list import MasterList
from models.freight_rate import FreightRate
from models.accessory import Accessory
from models.client import Client
from models.sales_list import SalesList
from models.markup_rule import MarkupRule


class PriceRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def get_first_master_list(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM master_list LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise ValueError("No master list found")
        return self.get_master_list(row[0])

    def get_master_list(self, master_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Get master list
        cursor.execute("SELECT * FROM master_list WHERE id = ?", (master_id,))
        row = cursor.fetchone()
        master = MasterList(id=row[0], name=row[1], courier=row[2])

        # Get freight rates
        cursor.execute("SELECT * FROM freight_rates WHERE master_list_id = ?", (master_id,))
        for row in cursor.fetchall():
            rate = FreightRate(id=row[0], master_list_id=row[1],
                               weight_min=row[2], weight_max=row[3], price=row[4])
            master.add_freight_rate(rate)

        # Get accessories
        cursor.execute("SELECT * FROM accessories WHERE master_list_id = ?", (master_id,))
        for row in cursor.fetchall():
            acc = Accessory(id=row[0], master_list_id=row[1],
                            type=row[2], calc_type=row[3], value=row[4])
            master.add_accessory(acc)

        conn.close()
        return master

    def get_sales_list_by_client_code(self, client_code):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Get client
        cursor.execute("SELECT * FROM clients WHERE code = ?", (client_code,))
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Client {client_code} not found")

        # Get sales list
        cursor.execute("SELECT * FROM sales_list WHERE client_id = ?", (row[0],))
        sales_row = cursor.fetchone()
        sales = SalesList(id=sales_row[0], client_id=sales_row[1],
                          master_list_id=sales_row[2])

        # Get markup rules
        cursor.execute("SELECT * FROM markup_rules WHERE sales_list_id = ?", (sales.id,))
        for row in cursor.fetchall():
            rule = MarkupRule(id=row[0], sales_list_id=row[1],
                              applies_to=row[2], calc_type=row[3], value=row[4])
            sales.add_markup_rule(rule)

        conn.close()
        return sales

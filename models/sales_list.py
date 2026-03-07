class SalesList:
    def __init__(self,
                 id=None,
                 client_id=None,
                 master_list_id=None):
        self.id = id
        self.client_id = client_id
        self.master_list_id = master_list_id
        self.markup_rules = []

    def add_markup_rule(self, rule):
        self.markup_rules.append(rule)

    def __repr__(self):
        return f"SalesList(id={self.id}, client_id={self.client_id})"
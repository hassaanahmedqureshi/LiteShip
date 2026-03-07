class MarkupRule:
    def __init__(self,
                 id=None,
                 sales_list_id=None,
                 applies_to=None,
                 calc_type=None,
                 value=None):
        self.id = id
        self.sales_list_id = sales_list_id
        self.applies_to = applies_to
        self.calc_type = calc_type
        self.value = value

    def apply(self, base_amount):
        if self.calc_type == 'percent':
            return base_amount * (1 + self.value / 100)
        elif self.calc_type == 'fixed':
            return base_amount + self.value
        elif self.calc_type == 'override':
            return self.value
        return base_amount

    def __repr__(self):
        return f"MarkupRule({self.applies_to}: {self.calc_type} {self.value})"
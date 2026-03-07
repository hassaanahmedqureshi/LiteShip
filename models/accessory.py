class Accessory:
    def __init__(self, id=None,
                 master_list_id=None,
                 type=None,
                 calc_type = None,
                 value=None):
            self.id = id
            self.master_list_id = master_list_id
            self.type = type
            self.calc_type = calc_type
            self.value = value

    def calculate(self, base_amount=0):
        if self.calc_type == 'fixed':
            return self.value
        if self.calc_type == 'percent':
            return base_amount * (self.value / 100)
        return self.value

    def __repr__(self):

        return f"Accessory(type=`{self.type}`, {self.calc_type}: {self.value}"
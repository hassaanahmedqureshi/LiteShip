class FreightRate:
    def __init__(self, id=None,
                 master_list_id=None,
                 weight_min=None,
                 weight_max=None,
                 price=None):
        self.id = id
        self.master_list_id = master_list_id
        self.weight_min = weight_min
        self.weight_max = weight_max
        self.price = price

    def applies_to_weight(self, weight):
        return self.weight_min <= weight <= self.weight_max

    def __repr__(self):
        return f"FreightRate({self.weight_min}-{self.weight_max}kg: €{self.price})"

class  MasterList:
    def __init__(self, id=None, name=None, courier=None):
        self.id = id
        self.name = name
        self.courier = courier
        self.freight_rates = []
        self.accessories = []

    def add_freight_rate(self, freight_rate):
        self.freight_rates.append(freight_rate)

    def add_accessory(self, accessory):
        self.accessories.append(accessory)

    def __repr__(self):
        return f"MasterList(id={self.id}, name = `{self.name}`, courier = `{self.courier}`)"

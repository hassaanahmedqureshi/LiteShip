from models.freight_rate import FreightRate
from models.accessory import Accessory
from models.markup_rule import MarkupRule

class PricingEngine:
    def calculate_quote(self,
                        master_list,
                        sales_list,
                        weight,
                        accessories_needed):

        freight_rate = self._find_freight_rate(master_list.freight_rates, weight)
        base_freight = freight_rate.price
        base_accessories = {}

        for acc in master_list.accessories:
            if acc.type in accessories_needed:
                if acc.type == 'fuel':
                    base_accessories[acc.type] = acc.calculate(base_freight)
                else:
                    base_accessories[acc.type] = acc.calculate()

        base_cost = base_freight + sum(base_accessories.values())

        sales_freight = self._apply_markup(base_freight, sales_list.markup_rules, 'freight')
        sales_accessories = {}

        for acc_type, base_value in base_accessories.items():
            sales_accessories[acc_type] = self._apply_markup(base_value, sales_list.markup_rules, acc_type)

        handling = self._get_handling_fee(sales_list.markup_rules)

        if 'fuel' in sales_accessories:
            fuel_acc = next(a for a in master_list.accessories if a.type == 'fuel')
            sales_accessories['fuel'] = fuel_acc.calculate(sales_freight)

        total = sales_freight + sum(sales_accessories.values()) + handling

        return {
            'base_cost': base_cost,
            'sales_price': total,
            'margin': total - base_cost,
            'breakdown': {
                'base_freight': base_freight,
                'sales_freight': sales_freight,
                'base_accessories': base_accessories,
                'sales_accessories': sales_accessories,
                'handling': handling
            }
        }

    def _find_freight_rate(self, rates, weight):
        for rate in rates:
            if rate.applies_to_weight(weight):
                return rate
        raise ValueError(f"No freight rate found for weight {weight}kg")

    def _apply_markup(self, base_value, rules, applies_to):
        for rule in rules:
            if rule.applies_to == applies_to:
                return rule.apply(base_value)
        return base_value

    def _get_handling_fee(self, rules):
        for rule in rules:
            if rule.applies_to == 'handling':
                return rule.value
        return 0.0
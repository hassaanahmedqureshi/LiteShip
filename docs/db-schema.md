# Database Schema - LiteShip

## Tables:

### master_list (Stores courier contracts)
- id INT PK
- name TEXT -- "SDA Contract 2024"
- courier TEXT -- "SDA"

### freight_rates (Weight-based prices from master list)
- id INT PK
- master_list_id INT FK → master_list.id
- weight_min REAL -- 0
- weight_max REAL -- 5
- price REAL -- 6.00

### accessories (Extra services (fuel, COD) from master list)
- id INT PK
- master_list_id INT FK → master_list.id
- type TEXT -- 'fuel', 'cod'
- calc_type TEXT -- 'percent', 'fixed'
- value REAL -- 10 (for 10%), or 1.50 (for €1.50)

### clients (Our customers)
- id INT PK
- name TEXT -- "Alfa"
- code TEXT UNIQUE -- "ALFA001"

### sales_list (Links client to a master list)
- id INT PK
- client_id INT FK → clients.id
- master_list_id INT FK → master_list.id

### markup_rules (How to modify master prices for each client)
- id INT PK
- sales_list_id INT FK → sales_list.id
- applies_to TEXT -- 'freight', 'handling', 'cod'
- calc_type TEXT -- 'percent', 'fixed', 'override'
- value REAL -- 20 (for +20%), 1.00 (for +€1.00)

## Example: Client Alfa orders 4kg with COD**
- Find Alfa's `sales_list` → points to SDA master 
- Get freight from `freight_rates`: 0-5kg = €6.00 
- Get fuel from `accessories`: 10% = €0.60
- Get COD from `accessories`: €1.50
- Apply `markup_rules`:
   - Freight +20% → €7.20
   - Handling +€1.00 → €1.00
   - COD override → €2.00
- Total: €7.20 + €0.72 (fuel) + €2.00 + €1.00 = €10.92

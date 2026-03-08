# LiteShip - Motore di Calcolo Tariffe

Motore di calcolo per tariffe di spedizione basato su listini master di acquisto e ricarichi configurabili per cliente.

## Caratteristiche

- Modellazione gerarchica dei listini (Master → Vendita)
- Tre tipi di ricarico: Percentuale Trasporto, Gestione Fissa, Override Accessori
- Calcolo dinamico per fasce di peso
- Database SQLite normalizzato
- Architettura OOP pulita (pattern Repository + Service)
- API REST con Flask

## Installazione

```bash
# Installa dipendenze
pip install -r requirements.txt

# Crea il database (prima volta)
python repositories/db_manager.py

# Carica dati di esempio
python scripts/seed_data.py
```

## Utilizzo

### 1. Esegui Test di Calcolo
```bash
python scripts/test_calculation.py
```

**Output Atteso:**
```
=== PREVENTIVO PER CLIENTE ALFA ===
Peso: 4kg | Accessori: Carburante, Contrassegno

Costo Base:     €8.10
Prezzo Vendita: €10.92
Margine:        €2.82
```

### 2. Avvia Server API
```bash
python app.py
```

### 3. Calcola Preventivo via API
```bash
curl -X POST http://localhost:5000/api/quote \
  -H "Content-Type: application/json" \
  -d '{
    "client_code": "ALFA001",
    "weight": 4,
    "accessories": ["fuel", "cod"]
  }'
```

**Risposta:**
```json
{
  "success": true,
  "data": {
    "base_cost": 8.1,
    "sales_price": 10.92,
    "margin": 2.82,
    "breakdown": {
      "base_freight": 6.0,
      "sales_freight": 7.2,
      "base_accessories": {"fuel": 0.6, "cod": 1.5},
      "sales_accessories": {"fuel": 0.72, "cod": 2.0},
      "handling": 1.0
    }
  }
}
```

## Struttura Progetto

```
LiteShip/
├── models/          # Modelli di dominio (Client, MasterList, ecc.)
├── repositories/    # Livello di accesso ai dati
├── services/        # Logica di business (PricingEngine)
├── scripts/         # Utility (seed_data, test)
├── data/            # Database SQLite
├── docs/            # Schema database
└── app.py           # API Flask
```

## Schema Database

Vedi [docs/db-schema.md](docs/db-schema.md)

## Esempio di Calcolo

**Cliente Alfa - Spedizione 4kg con Contrassegno:**

| Voce | Prezzo Master | Regola Ricarico | Prezzo Vendita |
|------|---------------|-----------------|----------------|
| Trasporto (0-5kg) | €6.00 | +20% | €7.20 |
| Carburante (10%) | €0.60 | Ereditato | €0.72 |
| Contrassegno | €1.50 | Override €2.00 | €2.00 |
| Gestione | €0.00 | +€1.00 | €1.00 |
| **Totale** | **€8.10** | | **€10.92** |

**Margine:** €2.82

## Tecnologie

- Python 3.10+
- SQLite
- Flask
- Pattern di Design OOP (Repository, Strategy)

---

# LiteShip - Pricing Engine

Shipping rate calculation engine based on master purchase price lists and configurable client-specific markups.

## Features

- Hierarchical price list modeling (Master → Sales)
- Three markup types: Freight %, Fixed Handling, Accessory Overrides
- Dynamic weight range calculation
- Normalized SQLite database
- Clean OOP architecture (Repository + Service patterns)
- REST API with Flask

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Create database (first time)
python repositories/db_manager.py

# Seed example data
python scripts/seed_data.py
```

## Usage

### 1. Run Test Calculation
```bash
python scripts/test_calculation.py
```

**Expected Output:**
```
=== QUOTE FOR CLIENT ALFA ===
Weight: 4kg | Accessories: Fuel, COD

Base Cost:   €8.10
Sales Price: €10.92
Margin:      €2.82
```

### 2. Start API Server
```bash
python app.py
```

### 3. Calculate Quote via API
```bash
curl -X POST http://localhost:5000/api/quote \
  -H "Content-Type: application/json" \
  -d '{
    "client_code": "ALFA001",
    "weight": 4,
    "accessories": ["fuel", "cod"]
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "base_cost": 8.1,
    "sales_price": 10.92,
    "margin": 2.82,
    "breakdown": {
      "base_freight": 6.0,
      "sales_freight": 7.2,
      "base_accessories": {"fuel": 0.6, "cod": 1.5},
      "sales_accessories": {"fuel": 0.72, "cod": 2.0},
      "handling": 1.0
    }
  }
}
```

## Project Structure

```
LiteShip/
├── models/          # Domain models (Client, MasterList, etc.)
├── repositories/    # Data access layer
├── services/        # Business logic (PricingEngine)
├── scripts/         # Utilities (seed_data, test)
├── data/            # SQLite database
├── docs/            # Database schema
└── app.py           # Flask API
```

## Database Schema

See [docs/db-schema.md](docs/db-schema.md)

## Example Calculation

**Client Alfa - 4kg shipment with COD:**

| Item | Master Price | Markup Rule | Sales Price |
|------|--------------|-------------|-------------|
| Freight (0-5kg) | €6.00 | +20% | €7.20 |
| Fuel (10%) | €0.60 | Inherited | €0.72 |
| COD | €1.50 | Override €2.00 | €2.00 |
| Handling | €0.00 | +€1.00 | €1.00 |
| **Total** | **€8.10** | | **€10.92** |

**Margin:** €2.82

## Technologies

- Python 3.10+
- SQLite
- Flask
- OOP Design Patterns (Repository, Strategy)

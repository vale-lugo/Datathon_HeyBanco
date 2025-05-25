# Data Loading Script for PostgreSQL

This script loads data from CSV files into a PostgreSQL database using SQLAlchemy.

## Prerequisites

- Python 3.6 or higher
- PostgreSQL database
- `.env` file with `POSTGRES_URI` variable

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Make sure your `.env` file contains the `POSTGRES_URI` variable with the correct PostgreSQL connection string:

```
POSTGRES_URI=postgres://username:password@localhost:5432/database_name
```

2. Run the script:

```bash
python load_data.py
```

## Data Models

The script creates two tables in the database:

### Clients Table

- `client_pk`: Auto-incrementing primary key
- `id`: Original client ID from CSV (used for relationship)
- `fecha_nacimiento`: Birth date
- `fecha_alta`: Registration date
- `id_municipio`: Municipality ID
- `id_estado`: State ID
- `tipo_persona`: Person type
- `genero`: Gender
- `actividad_empresarial`: Business activity

### Transactions Table

- `transaction_id`: Auto-incrementing primary key
- `client_id`: Foreign key to clients table
- `fecha`: Transaction date
- `comercio`: Merchant name
- `giro_comercio`: Merchant category
- `tipo_venta`: Sale type (digital or physical)
- `monto`: Amount

## Relationship

The relationship between the tables is established through the `id` column in the clients table and the `client_id` column in the transactions table.
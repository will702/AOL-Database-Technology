# AOL_DB - Online Retail Database Project

A comprehensive data pipeline for processing, normalizing, and managing online retail data. This project includes data sampling, normalization, database import, and SQL utilities for managing a structured online retail database.

## Project Structure

```
AOL_DB/
├── python/
│   ├── data_sampling.py      # Fill missing data values using random sampling
│   ├── importdata.py         # Import normalized data into MySQL database
│   └── normalizedata.py      # Normalize raw data into relational tables
└── sql/
    ├── schema.sql            # Database schema and table definitions
    ├── queries.sql           # Sample queries and data insertion examples
    └── advanced.sql          # Advanced SQL queries and operations
```

## Components

### Python Scripts

#### `data_sampling.py`
Handles missing value imputation in the dataset using random sampling from existing non-null values. Reads from CSV files and outputs cleaned datasets.

**Dependencies:**
- pandas
- numpy

#### `normalizedata.py`
Transforms raw online retail data into a normalized relational database structure with the following tables:
- **Country**: Geographic information
- **Customers**: Customer details linked to countries
- **Products**: Product inventory with stock and pricing
- **Invoices**: Transaction headers
- **InvoiceItems**: Line items for each invoice

**Input:** Excel file with raw retail data
**Output:** Normalized tables saved to Excel format

#### `importdata.py`
Imports normalized data from Excel files into a MySQL database. Includes:
- Safe price parsing with currency format handling (supports European format like "1.234,56")
- MySQL connection handling
- Data validation and insertion

**Dependencies:**
- pandas
- mysql-connector-python

### SQL Scripts

#### `schema.sql`
Defines the complete database schema including:
- **Country**: Country master data
- **Customers**: Customer information with foreign key to Country
- **Products**: Product catalog with stock levels and pricing
- **Invoices**: Invoice headers with timestamps
- **InvoiceItems**: Invoice line items with quantity and unit pricing

Features:
- Primary and foreign key constraints
- Check constraints for data validation (non-negative quantities/prices)
- Cascade and restrict referential integrity rules

#### `queries.sql`
Contains sample INSERT queries demonstrating:
- Product insertion
- Invoice creation
- Invoice item addition
- Stock adjustments and returns

#### `advanced.sql`
(Advanced SQL operations and complex queries)

## Database Schema

### Tables

| Table | Purpose |
|-------|---------|
| Country | Store country information |
| Customers | Store customer data with country reference |
| Products | Maintain product catalog |
| Invoices | Record transaction headers |
| InvoiceItems | Record individual items within invoices |

## Usage

### 1. Data Preparation
```bash
python python/data_sampling.py
```
Fills missing values in CSV datasets.

### 2. Data Normalization
```bash
python python/normalizedata.py
```
Normalizes raw data into relational structure.

### 3. Database Import
```bash
python python/importdata.py
```
Imports normalized data into MySQL database.

### 4. Database Setup
Execute schema creation:
```bash
mysql -u root -p < sql/schema.sql
```

## Database Configuration

The project uses MySQL with the following default configuration (in `importdata.py`):
- **Host:** localhost
- **User:** root
- **Database:** Tokopee
- **Password:** (update with your actual password)

⚠️ **Security Note:** Update credentials in production. Consider using environment variables for sensitive data.

## Requirements

- Python 3.7+
- pandas
- numpy
- mysql-connector-python
- MySQL 5.7+
- openpyxl (for Excel file handling)

## Data Flow

```
Raw Data (CSV) 
    ↓
data_sampling.py (Handle missing values)
    ↓
normalizedata.py (Normalize structure)
    ↓
Excel: normalized_tables.xlsx
    ↓
importdata.py (Load to MySQL)
    ↓
MySQL Database (Tokopee)
```

## Notes

- Currency values are parsed flexibly to handle different formats
- Stock quantities and prices include validation constraints
- Invoice items support both sales (positive quantity) and returns (negative quantity)
- Foreign key constraints ensure referential integrity

## License

(Add your license information here)

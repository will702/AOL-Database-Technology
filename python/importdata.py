import pandas as pd
import mysql.connector

# =========================
# HELPER: SAFE PRICE PARSER
# =========================
def parse_price(val):
    if pd.isna(val):
        return 0.0

    if isinstance(val, (int, float)):
        return max(float(val), 0.0)

    s = str(val).strip()
    if s == "":
        return 0.0

    # format Eropa: 1.234,56
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")

    try:
        return max(float(s), 0.0)
    except:
        return 0.0


# =========================

# =========================
# 1. DATABASE CONNECTION
# =========================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpassword1!",
    database="Tokopee"
)

cursor = conn.cursor()

# =========================
# 2. LOAD EXCEL FILE
# =========================
excel_path = "normalized_tables.xlsx"

df_country = pd.read_excel(excel_path, sheet_name="Country")
df_customers = pd.read_excel(excel_path, sheet_name="Customers")
df_products = pd.read_excel(excel_path, sheet_name="Products")
df_invoices = pd.read_excel(excel_path, sheet_name="Invoices")
df_invoice_items = pd.read_excel(excel_path, sheet_name="InvoiceItems")

# =========================
# 3. COUNTRY
# =========================
for _, row in df_country.iterrows():
    cursor.execute("""
        INSERT INTO Country (CountryID, CountryName)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE CountryName = VALUES(CountryName)
    """, (int(row["CountryID"]), row["CountryName"]))
conn.commit()

# =========================
# 4. CUSTOMERS
# =========================
for _, row in df_customers.iterrows():
    cursor.execute("""
        INSERT INTO Customers (CustomerID, CustomerName, CustomerEmail, CountryID)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            CustomerName = VALUES(CustomerName),
            CustomerEmail = VALUES(CustomerEmail),
            CountryID = VALUES(CountryID)
    """, (
        int(row["CustomerID"]),
        row["CustomerName"],
        row["CustomerEmail"],
        int(row["CountryID"])
    ))
conn.commit()

# =========================
# 5. PRODUCTS (SAFE)
# =========================
df_products["StockCode"] = (
    df_products["StockCode"]
    .astype(str)
    .str.strip()
    .str.upper()
)

for _, row in df_products.iterrows():
    unit_price = parse_price(row["UnitPrice"])

    cursor.execute("""
        INSERT INTO Products (StockCode, StockQuantity, Description, UnitPrice)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Description = VALUES(Description),
            UnitPrice = VALUES(UnitPrice)
    """, (
        row["StockCode"],
        0,                      # stok awal sementara
        row["Description"],
        unit_price
    ))
conn.commit()

# =========================
# 6. INVOICES
# =========================
df_invoices["InvoiceID"] = (
    df_invoices["InvoiceID"]
    .astype(str)
    .str.strip()
)

for _, row in df_invoices.iterrows():
    cursor.execute("""
        INSERT INTO Invoices (InvoiceID, CustomerID, InvoiceDate)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            CustomerID = VALUES(CustomerID),
            InvoiceDate = VALUES(InvoiceDate)
    """, (
        row["InvoiceID"],
        int(row["CustomerID"]),
        row["InvoiceDate"]
    ))
conn.commit()

# =========================
# 7. NORMALIZE INVOICE ITEMS
# =========================
df_invoice_items["InvoiceID"] = (
    df_invoice_items["InvoiceID"]
    .astype(str)
    .str.strip()
)

df_invoice_items["StockCode"] = (
    df_invoice_items["StockCode"]
    .astype(str)
    .str.strip()
    .str.upper()
)

df_invoice_items["Quantity"] = df_invoice_items["Quantity"].astype(int)

# =========================
# 8. AGGREGATE (ANTI DUPLICATE PK)
# =========================
df_items_grouped = (
    df_invoice_items
    .groupby(["InvoiceID", "StockCode"], as_index=False)
    .agg({
        "Quantity": "sum",
        "UnitPrice": "max"
    })
)

print("✅ InvoiceItems normalized & aggregated")

# =========================
# 9. CALCULATE INITIAL STOCK PER PRODUCT
# =========================
stock_required = (
    df_items_grouped[df_items_grouped["Quantity"] > 0]
    .groupby("StockCode")["Quantity"]
    .sum()
)

for stockcode, qty in stock_required.items():
    cursor.execute("""
        UPDATE Products
        SET StockQuantity = %s
        WHERE StockCode = %s
    """, (int(qty), stockcode))

conn.commit()
print("✅ Initial stock calculated from sales data")

# =========================
# 10. INSERT INVOICE ITEMS (TRIGGER SAFE)
# =========================
for _, row in df_items_grouped.iterrows():
    unit_price = parse_price(row["UnitPrice"])

    cursor.execute("""
        INSERT INTO InvoiceItems (InvoiceID, StockCode, Quantity, UnitPrice)
        VALUES (%s, %s, %s, %s)
    """, (
        row["InvoiceID"],
        row["StockCode"],
        int(row["Quantity"]),
        unit_price
    ))

conn.commit()

# =========================
# 11. CLOSE
# =========================
cursor.close()
conn.close()

print("IMPORT SELESAI 100%")
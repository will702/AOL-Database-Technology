import pandas as pd

# === LOAD DATA ===
df = pd.read_excel("aoldbcsv.xlsx")

# =========================
# 1. COUNTRY
# =========================
country_df = (
    df[["Country"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

country_df["CountryID"] = country_df.index + 1
country_df = country_df[["CountryID", "Country"]]
country_df.rename(columns={"Country": "CountryName"}, inplace=True)

# =========================
# 2. CUSTOMERS
# =========================
customers_df = (
    df[["CustomerID", "Country"]]
    .drop_duplicates()
    .merge(country_df, left_on="Country", right_on="CountryName")
)

customers_df["CustomerName"] = customers_df["CustomerID"].apply(
    lambda x: f"Customer {int(x)}"
)

customers_df["CustomerEmail"] = customers_df["CustomerID"].apply(
    lambda x: f"customer{int(x)}@example.com"
)

customers_df = customers_df[
    ["CustomerID", "CustomerName", "CustomerEmail", "CountryID"]
]

# =========================
# 3. PRODUCTS
# =========================
products_df = (
    df.groupby("StockCode")
    .agg({
        "Quantity": "sum",
        "Description": "first",
        "Price": "first"
    })
    .reset_index()
)

products_df.rename(columns={
    "Quantity": "StockQuantity",
    "Price": "UnitPrice"
}, inplace=True)

# =========================
# 4. INVOICES
# =========================
invoices_df = (
    df.groupby(["Invoice", "CustomerID"])
    .agg({
        "Quantity": "sum",
        "Price": "mean",
        "InvoiceDate": "first"
    })
    .reset_index()
)

invoices_df["TotalPrice"] = invoices_df["Quantity"] * invoices_df["Price"]

invoices_df = invoices_df[
    ["Invoice", "CustomerID", "TotalPrice", "InvoiceDate"]
]

invoices_df.rename(columns={"Invoice": "InvoiceID"}, inplace=True)

# =========================
# 5. INVOICE ITEMS
# =========================
invoice_items_df = df[[
    "Invoice",
    "StockCode",
    "Quantity",
    "Price"
]]

invoice_items_df.rename(columns={
    "Invoice": "InvoiceID",
    "Price": "UnitPrice"
}, inplace=True)

# =========================
# EXPORT KE EXCEL (5 SHEET)
# =========================
with pd.ExcelWriter("normalized_tables.xlsx", engine="openpyxl") as writer:
    country_df.to_excel(writer, sheet_name="Country", index=False)
    customers_df.to_excel(writer, sheet_name="Customers", index=False)
    products_df.to_excel(writer, sheet_name="Products", index=False)
    invoices_df.to_excel(writer, sheet_name="Invoices", index=False)
    invoice_items_df.to_excel(writer, sheet_name="InvoiceItems", index=False)

print("✅ Data successfully split into 5 normalized tables")


-- 1. Country Table
CREATE TABLE Country (
    CountryID INT PRIMARY KEY,
    CountryName VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(50) NOT NULL,
    CustomerEmail VARCHAR(100),
    CountryID INT NOT NULL,
    CONSTRAINT FK_Customers_Country FOREIGN KEY (CountryID)
        REFERENCES Country(CountryID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- 3. Products Table
CREATE TABLE Products (
    StockCode VARCHAR(20) PRIMARY KEY,
    StockQuantity INT NOT NULL DEFAULT 0 CHECK (StockQuantity >= 0),
    Description VARCHAR(255) NOT NULL,
    UnitPrice DECIMAL(15, 2) NOT NULL CHECK (UnitPrice >= 0)
);

-- 4. Invoices Table
CREATE TABLE Invoices (
    InvoiceID VARCHAR(20) PRIMARY KEY,
    CustomerID INT NOT NULL,
    TotalPrice DECIMAL(15, 2) DEFAULT 0.00,
    InvoiceDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_Invoices_Customers FOREIGN KEY (CustomerID)
        REFERENCES Customers(CustomerID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- 5. InvoiceItems Table
CREATE TABLE InvoiceItems (
    InvoiceID VARCHAR(20) NOT NULL,
    StockCode VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity <> 0),
    UnitPrice DECIMAL(15, 2) NOT NULL CHECK (UnitPrice >= 0),
    PRIMARY KEY (InvoiceID, StockCode),
    CONSTRAINT FK_Items_Invoices FOREIGN KEY (InvoiceID)
        REFERENCES Invoices(InvoiceID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FK_Items_Products FOREIGN KEY (StockCode)
        REFERENCES Products(StockCode)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
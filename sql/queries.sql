
INSERT INTO Products (StockCode, Description, UnitPrice)
VALUES ('NEW001', 'Premium Gift Box', 250000.00);



-- Create the Header
INSERT INTO Invoices (InvoiceID, CustomerID, InvoiceDate)
VALUES ('INV90001', 13085, NOW());

-- Add Items (Triggers will handle Stock deduction and TotalPrice update)
INSERT INTO InvoiceItems (InvoiceID, StockCode, Quantity, UnitPrice)
VALUES 
    ('INV90001', '85048', 2, 6.95),
    ('INV90001', '79323P', 1, 6.75);



-- Create a new header record in the Invoices table
INSERT INTO Invoices (InvoiceID, CustomerID, InvoiceDate)
VALUES ('INV90002', 13085, NOW());

-- Insert item details into the InvoiceItems table
-- Note: A Quantity of -1 is often interpreted as a stock return
INSERT INTO InvoiceItems (InvoiceID, StockCode, Quantity, UnitPrice)
VALUES ('INV90002', '85048', -1, 6.95);




SELECT 
    C.CustomerID,
    C.CustomerName,
    SUM(Ii.Quantity * Ii.UnitPrice) AS TotalSpending
FROM Customers C
JOIN Invoices I ON C.CustomerID = I.CustomerID
JOIN InvoiceItems Ii ON I.InvoiceID = Ii.InvoiceID
GROUP BY C.CustomerID, C.CustomerName
ORDER BY TotalSpending DESC
LIMIT 10;




SELECT 
    MONTH(I.InvoiceDate) AS MonthNum,
    DATE_FORMAT(I.InvoiceDate, '%M') AS MonthName,
    SUM(Ii.Quantity * Ii.UnitPrice) AS Revenue
FROM Invoices I
JOIN InvoiceItems Ii ON I.InvoiceID = Ii.InvoiceID
WHERE YEAR(I.InvoiceDate) = 2011
GROUP BY MONTH(I.InvoiceDate), DATE_FORMAT(I.InvoiceDate, '%M')
ORDER BY Revenue DESC
LIMIT 1;
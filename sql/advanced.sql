DELIMITER $$

CREATE TRIGGER trg_UpdateInventory_AfterInsert
AFTER INSERT ON InvoiceItems
FOR EACH ROW
BEGIN
    UPDATE Products
    SET StockQuantity = StockQuantity - NEW.Quantity
    WHERE StockCode = NEW.StockCode;
END$$

DELIMITER ;



DELIMITER $$

-- Trigger for Insert
CREATE TRIGGER trg_UpdateInvoiceTotal_Insert
AFTER INSERT ON InvoiceItems
FOR EACH ROW
BEGIN
    UPDATE Invoices
    SET TotalPrice = (
        SELECT COALESCE(SUM(Quantity * UnitPrice), 0)
        FROM InvoiceItems
        WHERE InvoiceID = NEW.InvoiceID
    )
    WHERE InvoiceID = NEW.InvoiceID;
END$$

-- Trigger for Delete (Crucial for data integrity)
CREATE TRIGGER trg_UpdateInvoiceTotal_Delete
AFTER DELETE ON InvoiceItems
FOR EACH ROW
BEGIN
    UPDATE Invoices
    SET TotalPrice = (
        SELECT COALESCE(SUM(Quantity * UnitPrice), 0)
        FROM InvoiceItems
        WHERE InvoiceID = OLD.InvoiceID
    )
    WHERE InvoiceID = OLD.InvoiceID;
END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE GetCustomerInvoiceHistory(IN cid INT)
BEGIN
    SELECT 
        I.InvoiceID,
        I.InvoiceDate,
        COUNT(Ii.StockCode) as TotalItems,
        I.TotalPrice
    FROM Invoices I
    LEFT JOIN InvoiceItems Ii ON I.InvoiceID = Ii.InvoiceID
    WHERE I.CustomerID = cid
    GROUP BY I.InvoiceID, I.InvoiceDate, I.TotalPrice
    ORDER BY I.InvoiceDate DESC;
END$$

DELIMITER ;
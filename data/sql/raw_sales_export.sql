SELECT
    o.OrderID,
    OrderDate,
    o.CustomerID,
    CustomerName,
    p.ProductID,
    ProductName,
    Quantity,
    Price,
    Quantity * Price AS LineTotal
FROM Orders o
JOIN OrderDetails od ON o.OrderID = od.OrderID
JOIN Products p ON od.ProductID = p.ProductID
JOIN Customers c ON o.CustomerID = c.CustomerID;
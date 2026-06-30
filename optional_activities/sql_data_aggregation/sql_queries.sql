--1
SELECT Salesperson.salesperson_name, SUM(Sale.quantity * Product.unit_price) as total_revenue FROM Salesperson
JOIN Sale
    ON Salesperson.salesperson_id = Sale.salesperson_id
JOIN Product
    ON Sale.product_id = Product.product_id
GROUP BY Salesperson.salesperson_name
ORDER BY total_revenue DESC;

--2
SELECT Product.product_id, Product.product_name, SUM(Sale.quantity) as total_units_sold FROM Product
JOIN Sale
    ON Product.product_id = Sale.product_id
GROUP BY Product.product_id
ORDER BY total_units_sold DESC
LIMIT 1;

--3
SELECT Product.product_name, SUM(Sale.quantity * Product.unit_price) as total_revenue, SUM(Sale.quantity * Product.unit_cost) as total_cost, SUM((Sale.quantity * Product.unit_price) - (Sale.quantity * Product.unit_cost)) as total_profit FROM Product
JOIN Sale
    ON Product.product_id = Sale.product_id
GROUP BY Product.product_id
ORDER BY total_profit DESC;

WITH GrossProfit AS (
SELECT sod.SalesOrderDetailID,
		sod.SalesOrderID,
		(sod.UnitPrice - p.StandardCost) * sod.OrderQty as GrossProfit
FROM Sales.SalesOrderDetail sod
JOIN Production.Product p
    ON sod.ProductID = p.ProductID),

OrderMonthProfit AS (
SELECT gp.SalesOrderID,
		DATENAME(MONTH, soh.OrderDate) as OrderMonth,
		soh.OrderDate,
		gp.GrossProfit
FROM GrossProfit gp
JOIN Sales.SalesOrderHeader soh 
	ON gp.SalesOrderID = soh.SalesOrderID )

SELECT OrderMonth,
		ROUND(SUM(GrossProfit),2)
FROM OrderMonthProfit
WHERE YEAR(OrderDate) = 2013 --Last full year data inside the database
GROUP BY OrderMonth
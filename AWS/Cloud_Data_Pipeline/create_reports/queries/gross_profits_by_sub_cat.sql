WITH GrossProfit AS (
SELECT sod.SalesOrderDetailID,
		p.ProductSubcategoryID,
		(sod.UnitPrice - p.StandardCost) * sod.OrderQty as GrossProfit
FROM Sales.SalesOrderDetail sod
JOIN Production.Product p
    ON sod.ProductID = p.ProductID)

SELECT ps.Name,
		ROUND(SUM(gp.GrossProfit),2)
FROM GrossProfit gp
JOIN Production.ProductSubcategory ps 
	ON gp.ProductSubcategoryID  = ps.ProductSubcategoryID 
GROUP BY ps.Name 
ORDER BY 2 DESC
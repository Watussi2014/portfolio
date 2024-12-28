SELECT ps.Name,
		ROUND(SUM(sod.LineTotal),2)
FROM Sales.SalesOrderDetail sod
JOIN Production.Product p
    ON sod.ProductID = p.ProductID
JOIN Production.ProductSubcategory ps 
	ON p.ProductSubcategoryID  = ps.ProductSubcategoryID 
GROUP BY ps.Name
ORDER BY 2 DESC
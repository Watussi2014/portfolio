SELECT 	cr.Name,
		ROUND(SUM(sod.LineTotal),2)
FROM Sales.SalesOrderDetail sod
JOIN Sales.SalesOrderHeader soh
	ON sod.SalesOrderID  = soh.SalesOrderID  
JOIN Sales.Customer c 
	on soh.CustomerID = c.CustomerID
JOIN Sales.SalesTerritory st 
	on c.TerritoryID = st.TerritoryID 
JOIN Person.CountryRegion cr 
	on st.CountryRegionCode = cr.CountryRegionCode 
GROUP BY cr.Name 
ORDER BY 2 DESC
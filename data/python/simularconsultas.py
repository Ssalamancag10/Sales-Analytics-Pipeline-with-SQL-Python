import pandas as pd

# Cargamos dimensiones
dim_product = pd.read_csv("analytics/starschema/DimProduct.csv")
dim_customer = pd.read_csv("analytics/starschema/DimCustomer.csv")
dim_date = pd.read_csv("analytics/starschema/DimDate.csv")

# Cargamos fact table
fact_sales = pd.read_csv("analytics/starschema/FactSales.csv")

# Unir FactSales con DimProduct
sales_by_product = fact_sales.merge(dim_product, on='ProductID', how='left')

# Agregamos total vendido por producto
sales_summary = sales_by_product.groupby('ProductName').agg(
    total_sales=('LineTotal', 'sum'),
    total_quantity=('Quantity', 'sum')
).sort_values('total_sales', ascending=False)

print(sales_summary.head(10))  # Top 10 productos

# Unir FactSales con DimCustomer
sales_by_customer = fact_sales.merge(dim_customer, on='CustomerID', how='left')

# Total vendido por cliente
customer_summary = sales_by_customer.groupby('CustomerName').agg(
    total_sales=('LineTotal', 'sum'),
    total_orders=('OrderID', 'nunique')
).sort_values('total_sales', ascending=False)

print(customer_summary.head(10))  # Top 10 clientes

# Unir FactSales con DimDate
sales_with_date = fact_sales.merge(dim_date[['OrderDateID', 'Year', 'Month', 'Quarter']], on='OrderDateID', how='left')

# Total ventas por mes
monthly_sales = sales_with_date.groupby(['Year', 'Month']).agg(
    total_sales=('LineTotal', 'sum'),
    total_quantity=('Quantity', 'sum')
).reset_index()

print(monthly_sales.head())
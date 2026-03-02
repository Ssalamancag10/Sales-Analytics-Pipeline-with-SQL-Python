import pandas as pd

# 1. Load raw data
df = pd.read_csv("raw/northwind_raw.csv")

# 2. Basic validation
#print("Rows:", len(df))#Cuantas filas hay
#print(df.head())#Primeras 5 filas

# 3. Data types
#print(df.dtypes)#Tipo de variable de las columnas

# 4. Convert OrderDate to datetime
df["OrderDate"] = pd.to_datetime(df["OrderDate"])#Cambia tipo a fecha

# 5. Check result
#print(df["OrderDate"].dtype)

# 6. Create analytical date columns
df["Year"] = df["OrderDate"].dt.year
df["Month"] = df["OrderDate"].dt.month
df["YearMonth"] = df["OrderDate"].dt.to_period("M").astype(str)

#print(df[["OrderDate", "Year", "Month", "YearMonth"]].head())

# 7. Data quality checks Manejo de errores
assert df["Quantity"].min() > 0, "Quantity has invalid values"
assert df["Price"].min() > 0, "Price has invalid values"
assert df["LineTotal"].sum() > 0, "Total sales is zero"

# 8. Save cleaned data
df.to_csv("processed/sales_cleaned.csv", index=False)
# 9. Monthly sales metrics
monthly_sales = (
    df.groupby("YearMonth")
    .agg(
        total_sales=("LineTotal", "sum"),
        total_quantity=("Quantity", "sum"),
        orders=("OrderID", "nunique")
    )
    .reset_index()
)

print(monthly_sales.head())
# 10. Product sales metrics
product_sales = (
    df.groupby(["ProductID", "ProductName"])
    .agg(
        total_sales=("LineTotal", "sum"),
        total_quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("total_sales", ascending=False)
)

print(product_sales.head())
# 11. Customer sales metrics
customer_sales = (
    df.groupby(["CustomerID", "CustomerName"])
    .agg(
        total_sales=("LineTotal", "sum"),
        orders=("OrderID", "nunique")
    )
    .reset_index()
    .sort_values("total_sales", ascending=False)
)

print(customer_sales.head())

# 12. Save analytics datasets
monthly_sales.to_csv("analytics/monthly_sales.csv", index=False)
product_sales.to_csv("analytics/product_sales.csv", index=False)
customer_sales.to_csv("analytics/customer_sales.csv", index=False)
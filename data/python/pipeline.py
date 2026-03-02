import pandas as pd

df = pd.read_csv("raw/northwind_raw.csv")

df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["Year"] = df["OrderDate"].dt.year
df["Month"] = df["OrderDate"].dt.month
df["YearMonth"] = df["OrderDate"].dt.to_period("M").astype(str)

assert df["Quantity"].min() > 0, "Quantity has invalid values"
assert df["Price"].min() > 0, "Price has invalid values"
assert df["LineTotal"].sum() > 0, "Total sales is zero"
df.to_csv("processed/sales_cleaned.csv", index=False)

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

monthly_sales.to_csv("analytics/monthly_sales.csv", index=False)
product_sales.to_csv("analytics/product_sales.csv", index=False)
customer_sales.to_csv("analytics/customer_sales.csv", index=False)

import pandas as pd


#Load Data
def load_data(path):
    print("Loading raw data...")
    df = pd.read_csv(path)
    print(f"Rows loaded: {len(df)}")
    return df


#Clean Data
def clean_data(df):
    print("Cleaning data...")

    
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])

    df["Year"] = df["OrderDate"].dt.year
    df["Month"] = df["OrderDate"].dt.month
    df["YearMonth"] = df["OrderDate"].dt.to_period("M").astype(str)

    assert df["Quantity"].min() > 0, "Invalid Quantity detected"
    assert df["Price"].min() > 0, "Invalid UnitPrice detected"
    assert df["LineTotal"].sum() > 0, "Total Sales is zero"

    print("Data cleaned successfully.")
    return df


#Create Analytics
def create_analytics(df):
    print("Creating analytics datasets...")

    monthly_sales = (
        df.groupby("YearMonth")
        .agg(
            total_sales=("LineTotal", "sum"),
            total_quantity=("Quantity", "sum"),
            orders=("OrderID", "nunique")
        )
        .reset_index()
    )

    product_sales = (
        df.groupby(["ProductID", "ProductName"])
        .agg(
            total_sales=("LineTotal", "sum"),
            total_quantity=("Quantity", "sum")
        )
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )

    customer_sales = (
        df.groupby(["CustomerID", "CustomerName"])
        .agg(
            total_sales=("LineTotal", "sum"),
            orders=("OrderID", "nunique")
        )
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )

    print("Analytics datasets created.")
    return monthly_sales, product_sales, customer_sales


#Save Results
def save_data(df, monthly, product, customer):
    print("Saving datasets...")

    df.to_csv("processed/sales_cleaned.csv", index=False)
    monthly.to_csv("analytics/monthly_sales.csv", index=False)
    product.to_csv("analytics/product_sales.csv", index=False)
    customer.to_csv("analytics/customer_sales.csv", index=False)

    print("All files saved successfully.")


#Main Execution
def main():
    raw_path = "raw/northwind_raw.csv"

    df = load_data(raw_path)
    df_clean = clean_data(df)
    monthly, product, customer = create_analytics(df_clean)
    save_data(df_clean, monthly, product, customer)

    print("Pipeline executed successfully.")

#Pipeline run
if __name__ == "__main__":
    main()

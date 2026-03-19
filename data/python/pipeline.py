import pandas as pd
import matplotlib.pyplot as plt
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

RAW_CSV = "processed/sales_cleaned.csv"
DIM_PRODUCT_CSV = "analytics/starschema/DimProduct.csv"
DIM_CUSTOMER_CSV = "analytics/starschema/DimCustomer.csv"
DIM_DATE_CSV = "analytics/starschema/DimDate.csv"
FACT_SALES_CSV = "analytics/starschema/FactSales.csv"

#Load 
def load_data(path):
    logging.info("Loading raw data...")
    df = pd.read_csv(path)
    logging.info(f"Rows loaded: {len(df)}")
    return df

#  Dimensions
def create_dimensions(df):
    logging.info("Creating DimProduct...")
    dim_product = df[['ProductID', 'ProductName', 'Price']].drop_duplicates().reset_index(drop=True)
    dim_product.to_csv(DIM_PRODUCT_CSV, index=False)

    logging.info("Creating DimCustomer...")
    dim_customer = df[['CustomerID', 'CustomerName']].drop_duplicates().reset_index(drop=True)
    dim_customer.to_csv(DIM_CUSTOMER_CSV, index=False)

    logging.info("Creating DimDate...")
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    dim_date = df[['OrderDate']].drop_duplicates().reset_index(drop=True)
    dim_date['Year'] = dim_date['OrderDate'].dt.year
    dim_date['Month'] = dim_date['OrderDate'].dt.month
    dim_date['Quarter'] = dim_date['OrderDate'].dt.quarter
    dim_date['OrderDateID'] = dim_date.index + 1
    dim_date.to_csv(DIM_DATE_CSV, index=False)

    return dim_product, dim_customer, dim_date

#Create Fact Table
def create_fact_sales(df, dim_date):
    logging.info("Creating FactSales...")
    fact_sales = df.merge(dim_date[['OrderDate','OrderDateID']], on='OrderDate', how='left')
    fact_sales = fact_sales[['OrderID','ProductID','CustomerID','OrderDateID','Quantity','Price','LineTotal']]
    fact_sales.to_csv(FACT_SALES_CSV, index=False)
    return fact_sales

# Create Dashboard
def create_dashboard():
    logging.info("Creating dashboard...")
    # Cargar dimensiones y fact
    dim_product = pd.read_csv(DIM_PRODUCT_CSV)
    dim_customer = pd.read_csv(DIM_CUSTOMER_CSV)
    dim_date = pd.read_csv(DIM_DATE_CSV)
    fact_sales = pd.read_csv(FACT_SALES_CSV)
    # Top productos
    sales_by_product = fact_sales.merge(dim_product, on='ProductID', how='left')
    top_products = sales_by_product.groupby('ProductName').agg(total_sales=('LineTotal','sum')).sort_values('total_sales',ascending=False).head(10)
    # Top clientes
    sales_by_customer = fact_sales.merge(dim_customer, on='CustomerID', how='left')
    top_customers = sales_by_customer.groupby('CustomerName').agg(total_sales=('LineTotal','sum')).sort_values('total_sales',ascending=False).head(10)
    # Ventas mensuales
    sales_with_date = fact_sales.merge(dim_date[['OrderDateID','Year','Month']], on='OrderDateID', how='left')
    monthly_sales = sales_with_date.groupby(['Year','Month']).agg(total_sales=('LineTotal','sum')).reset_index()
    monthly_sales['YearMonth'] = monthly_sales['Year'].astype(str) + '-' + monthly_sales['Month'].astype(str)
    # Gráficos
    plt.style.use('ggplot')
    fig, axes = plt.subplots(3,1,figsize=(12,18))
    
    axes[0].barh(top_products.index[::-1], top_products['total_sales'][::-1], color='skyblue')
    axes[0].set_title("Top 10 Productos por Ventas")
    axes[0].set_xlabel("Ventas Totales")

    axes[1].barh(top_customers.index[::-1], top_customers['total_sales'][::-1], color='lightgreen')
    axes[1].set_title("Top 10 Clientes por Ventas")
    axes[1].set_xlabel("Ventas Totales")

    axes[2].plot(monthly_sales['YearMonth'], monthly_sales['total_sales'], marker='o', color='coral')
    axes[2].set_title("Ventas Mensuales")
    axes[2].set_xlabel("Mes")
    axes[2].set_ylabel("Ventas Totales")
    axes[2].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()
    logging.info("Dashboard created successfully!")

# Main
def main():
    if not os.path.exists(RAW_CSV):
        logging.error(f"No se encuentra el CSV raw: {RAW_CSV}")
        return
    df = load_data(RAW_CSV)
    dim_product, dim_customer, dim_date = create_dimensions(df)
    fact_sales = create_fact_sales(df, dim_date)
    create_dashboard()
    logging.info("ETL + DW + Dashboard pipeline completed!")

if __name__ == "__main__":
    main()main()

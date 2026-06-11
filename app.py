import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="Smart Agrovet Sales Analytics Dashboard",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Smart Agrovet Sales Analytics Dashboard")
st.write("Analyze sales for animal feeds, mineral salts, veterinary products, and agrochemicals.")

# Upload CSV file
st.sidebar.header("Upload Sales CSV")

uploaded_file = st.sidebar.file_uploader(
    "Upload your sales CSV file",
    type=["csv"]
)

# Load data


@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df["date"] = pd.to_datetime(df["date"])
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["total_sales"] = df["quantity"] * df["unit_price"]
    return df


if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success("CSV file uploaded successfully.")
else:
    df = load_data("data/sample_sales.csv")
    st.info("Using sample sales data. Upload your own CSV file from the sidebar.")

# Sidebar filters
st.sidebar.header("Filter Sales Data")

categories = st.sidebar.multiselect(
    "Select Product Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

payment_methods = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["payment_method"].unique(),
    default=df["payment_method"].unique()
)

sales_people = st.sidebar.multiselect(
    "Select Sales Person",
    options=df["sales_person"].unique(),
    default=df["sales_person"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["date"].min(), df["date"].max())
)

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = df[
        (df["category"].isin(categories)) &
        (df["payment_method"].isin(payment_methods)) &
        (df["sales_person"].isin(sales_people)) &
        (df["date"] >= start_date) &
        (df["date"] <= end_date)
    ]
else:
    filtered_df = df[
        (df["category"].isin(categories)) &
        (df["payment_method"].isin(payment_methods)) &
        (df["sales_person"].isin(sales_people))
    ]

# Key metrics
total_revenue = filtered_df["total_sales"].sum()
total_orders = filtered_df["invoice_no"].nunique()
total_quantity = filtered_df["quantity"].sum()

best_product = (
    filtered_df.groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

top_category = (
    filtered_df.groupby("category")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"KES {total_revenue:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Total Quantity Sold", total_quantity)

if not best_product.empty:
    col4.metric("Best Selling Product", best_product.index[0])
else:
    col4.metric("Best Selling Product", "No data")

st.divider()

# Charts
col5, col6 = st.columns(2)

with col5:
    st.subheader("Sales by Category")
    category_sales = filtered_df.groupby("category", as_index=False)[
        "total_sales"].sum()
    fig_category = px.bar(
        category_sales,
        x="category",
        y="total_sales",
        title="Revenue by Product Category",
        labels={"total_sales": "Total Sales", "category": "Category"}
    )
    st.plotly_chart(fig_category, width="stretch")

with col6:
    st.subheader("Payment Method Breakdown")
    payment_sales = filtered_df.groupby("payment_method", as_index=False)[
        "total_sales"].sum()
    fig_payment = px.pie(
        payment_sales,
        names="payment_method",
        values="total_sales",
        title="Sales by Payment Method"
    )
    st.plotly_chart(fig_payment, width="stretch")

col7, col8 = st.columns(2)

with col7:
    st.subheader("Top Products by Revenue")
    product_sales = (
        filtered_df.groupby("product_name", as_index=False)["total_sales"]
        .sum()
        .sort_values(by="total_sales", ascending=False)
    )
    fig_products = px.bar(
        product_sales,
        x="product_name",
        y="total_sales",
        title="Top Products by Revenue",
        labels={"product_name": "Product", "total_sales": "Total Sales"}
    )
    st.plotly_chart(fig_products, width="stretch")

with col8:
    st.subheader("Sales Trend Over Time")
    daily_sales = filtered_df.groupby("date", as_index=False)[
        "total_sales"].sum()
    fig_trend = px.line(
        daily_sales,
        x="date",
        y="total_sales",
        markers=True,
        title="Daily Sales Trend",
        labels={"date": "Date", "total_sales": "Total Sales"}
    )
    st.plotly_chart(fig_trend, width="stretch")

st.divider()

st.divider()

st.subheader("Customer Analysis")

customer_sales = (
    filtered_df.groupby("customer_name", as_index=False)["total_sales"]
    .sum()
    .sort_values(by="total_sales", ascending=False)
)

col9, col10 = st.columns(2)

with col9:
    st.write("Top Customers by Revenue")
    st.dataframe(customer_sales.head(10), width="stretch")

with col10:
    fig_customers = px.bar(
        customer_sales.head(10),
        x="customer_name",
        y="total_sales",
        title="Top 10 Customers by Revenue",
        labels={"customer_name": "Customer", "total_sales": "Total Sales"}
    )
    st.plotly_chart(fig_customers, width="stretch")

st.divider()

st.subheader("Stock Movement Analysis")

product_movement = (
    filtered_df.groupby("product_name", as_index=False)
    .agg(
        total_quantity_sold=("quantity", "sum"),
        total_revenue=("total_sales", "sum")
    )
    .sort_values(by="total_quantity_sold", ascending=False)
)

fast_moving = product_movement.head(5)
slow_moving = product_movement.tail(5).sort_values(
    by="total_quantity_sold", ascending=True)

col11, col12 = st.columns(2)

with col11:
    st.write("Fast-Moving Products")
    st.dataframe(fast_moving, width="stretch")

with col12:
    st.write("Slow-Moving Products")
    st.dataframe(slow_moving, width="stretch")

st.divider()

st.subheader("Monthly Sales Forecast")

monthly_sales = (
    filtered_df
    .groupby(filtered_df["date"].dt.to_period("M"))["total_sales"]
    .sum()
    .reset_index()
)

monthly_sales["date"] = monthly_sales["date"].astype(str)
monthly_sales["month_number"] = range(1, len(monthly_sales) + 1)

if len(monthly_sales) >= 2:
    X = monthly_sales[["month_number"]]
    y = monthly_sales["total_sales"]

    model = LinearRegression()
    model.fit(X, y)

    next_month_number = np.array([[len(monthly_sales) + 1]])
    predicted_sales = model.predict(next_month_number)[0]

    st.metric("Predicted Sales for Next Month", f"KES {predicted_sales:,.0f}")

    forecast_df = monthly_sales.copy()
    forecast_df = forecast_df.rename(columns={"total_sales": "sales"})

    next_month_label = "Next Month"
    forecast_df.loc[len(forecast_df)] = [
        next_month_label,
        len(monthly_sales) + 1,
        predicted_sales
    ]

    fig_forecast = px.line(
        forecast_df,
        x="date",
        y="sales",
        markers=True,
        title="Monthly Sales Trend and Forecast",
        labels={"date": "Month", "sales": "Sales"}
    )

    st.plotly_chart(fig_forecast, width="stretch")

else:
    st.warning(
        "At least 2 months of sales data are needed to generate a forecast.")

# Smart insights
st.subheader("Smart Business Insights")

if not filtered_df.empty:
    highest_category = top_category.index[0]
    highest_category_sales = top_category.iloc[0]

    top_customer = (
        filtered_df.groupby("customer_name")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.success(
        f"{highest_category} generated the highest revenue: KES {highest_category_sales:,.0f}.")
    st.info(
        f"The top customer is {top_customer.index[0]} with purchases worth KES {top_customer.iloc[0]:,.0f}.")
    st.warning(
        f"The fastest moving product is {best_product.index[0]} with {best_product.iloc[0]} units sold.")
else:
    st.warning("No data available for the selected filters.")

# Raw data
with st.expander("View Sales Data"):
    st.dataframe(filtered_df)

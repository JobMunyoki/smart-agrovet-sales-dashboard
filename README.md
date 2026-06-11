# Smart Agrovet Sales Analytics Dashboard

A Python-based sales analytics dashboard designed for agrovet and animal feeds businesses. The dashboard analyzes sales data for animal feeds, mineral salts, veterinary products, and agrochemicals. It provides business insights such as total revenue, best-selling products, customer analysis, stock movement, payment method breakdown, and monthly sales forecasting.

## Project Overview

The Smart Agrovet Sales Analytics Dashboard helps agrovet businesses understand their sales performance using interactive data visualization and machine learning. Users can upload a CSV sales file and instantly view key metrics, charts, customer trends, product performance, and predicted future sales.

This project was inspired by real-world sales and inventory operations in animal feeds, veterinary products, mineral salts, and agrochemical businesses.

## Features

- Upload sales data using a CSV file
- View total revenue, total orders, and total quantity sold
- Analyze sales by product category
- Identify best-selling products
- View payment method breakdown
- Analyze top customers by revenue
- Identify fast-moving and slow-moving products
- View sales trends over time
- Generate smart business insights
- Forecast next month’s sales using machine learning

## Product Categories

The dashboard supports agrovet-related categories such as:

- Animal Feeds
- Mineral Salts
- Veterinary Products
- Agrochemicals

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn

## Project Structure

```text
smart-agrovet-sales-dashboard/
│
├── app.py
├── README.md
├── requirements.txt
└── data/
    └── sample_sales.csv
```

## CSV File Format

The uploaded CSV file should contain the following columns:

```csv
date,invoice_no,customer_name,product_name,category,quantity,unit_price,payment_method,branch,sales_person
```

Example:

```csv
date,invoice_no,customer_name,product_name,category,quantity,unit_price,payment_method,branch,sales_person
2026-03-01,INV001,Kamau Farms,Dairy Meal,Animal Feeds,10,2800,M-Pesa,Embu,John
2026-03-02,INV002,Wanjiku Agrovet,Dewormer,Veterinary Products,5,850,Cash,Embu,Mary
```

The dashboard automatically calculates total sales using:

```text
quantity × unit_price
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/smart-agrovet-sales-dashboard.git
```

### 2. Open the project folder

```bash
cd smart-agrovet-sales-dashboard
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows PowerShell:

```bash
venv\Scripts\activate
```

For Git Bash:

```bash
source venv/Scripts/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Streamlit app

```bash
streamlit run app.py
```

The dashboard will open in your browser at:

```text
http://localhost:8501
```

## Dashboard Sections

### Sales Summary

Displays total revenue, number of orders, total quantity sold, and best-selling product.

### Sales by Category

Shows revenue performance across animal feeds, mineral salts, veterinary products, and agrochemicals.

### Payment Method Breakdown

Shows how customers pay using methods such as Cash, M-Pesa, and Bank.

### Top Products by Revenue

Ranks products based on total revenue generated.

### Sales Trend Over Time

Displays sales performance over time using a line chart.

### Customer Analysis

Shows the top customers based on revenue.

### Stock Movement Analysis

Identifies fast-moving and slow-moving products based on quantity sold.

### Monthly Sales Forecast

Uses Linear Regression to estimate next month’s sales based on previous monthly sales trends.

## Machine Learning Component

The dashboard uses a simple Linear Regression model from Scikit-learn to forecast future sales. The model analyzes monthly sales patterns and predicts the next month’s expected sales.

## Business Value

This dashboard can help agrovet businesses:

- Track sales performance
- Understand customer buying behavior
- Identify high-performing product categories
- Monitor fast-moving and slow-moving products
- Improve stock planning
- Support better business decisions using data

## Author

Job Munyoki

## License

This project is for business analytics.

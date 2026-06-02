import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# my data is for electronic sales 

data1 = {
    'DATE': ['01/03/26', '02/03/26', '03/03/26', '04/03/26', '05/03/26',
             '06/03/26', '07/03/26', '08/03/26', '09/03/26', '10/03/26'],
    'PRODUCTS': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop',
                 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 'Mouse'],
    'CITY': ['Mumbai', 'Bhopal', 'Indore', 'Delhi', 'Mumbai',
             'Indore', 'Delhi', 'Bhopal', 'Indore', 'Mumbai'],
    'SALES_PERSON': ['Rahul Verma', 'Aman Kushwah', 'Neha Jamle',
                     'Ravi Kushwah', 'Sneha Sharma',
                     'Rahul Karma', 'Aman Chauhan',
                     'Neha Saste', 'Ravi Gupta', 'Sneha Gupta'],
    'UNITS_SOLD': [5, 20, 15, 7, 3, 25, 10, 4, 6, 30],
    'PRICE': [55000, 500, 1200, 15000, 60000,
              450, 1100, 14000, 58000, 480]
}

data2 = {
    'DATE': ['11/03/26', '12/03/26', '13/03/26', '14/03/26', '15/03/26',
             '16/03/26', '17/03/26', '18/03/26', '19/03/26', '20/03/26'],
    'PRODUCTS': ['Keyboard', 'Monitor', 'Laptop', 'Mouse', 'Keyboard',
                 'Monitor', 'Laptop', 'Mouse', 'Keyboard', 'Monitor'],
    'CITY': ['KHARGONE', 'UJJAIN', 'OMKARESHWAR', 'KHAMMAM', 'UJJAIN',
             'OMKARESHWAR', 'KHARGONE', 'UJJAIN', 'OMKARESHWAR', 'KHARGONE'],
    'SALES_PERSON': ['Ritik Pal', 'Hemant Kushwah', 'Manav Jamle',
                     'Lokesh Kushwah', 'Shruti Sharma',
                     'Suhani Karma', 'Nikhil Patidar',
                     'Anjali Gupta', 'Divyanshu Verma',
                     'Chetan Kushwah'],
    'UNITS_SOLD': [12, 8, 4, 18, 20, 6, 10, 22, 14, 5],
    'PRICE': [1100, 14000, 58000, 480, 1200,
              15000, 55000, 500, 1200, 15000]
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

combined_df = pd.concat([df1, df2], ignore_index=True)

# DATA CLEANING

combined_df['DATE'] = pd.to_datetime(
    combined_df['DATE'],
    format='%d/%m/%y'
)

combined_df['CITY'] = combined_df['CITY'].str.title()
combined_df['SALES_PERSON'] = combined_df['SALES_PERSON'].str.title()

# Revenue Column
combined_df['TOTAL_REVENUE'] = (
    combined_df['UNITS_SOLD'] *
    combined_df['PRICE'] 
)


# SQLITE DATABASE


conn = sqlite3.connect(':memory:')

combined_df.to_sql(
    'electronic_sales',
    conn,
    index=False,
    if_exists='replace'
)

# PRODUCT ANALYSIS

product_query = """
SELECT PRODUCTS,
       SUM(TOTAL_REVENUE) AS Total_Sales
FROM electronic_sales
GROUP BY PRODUCTS
ORDER BY Total_Sales DESC
"""

product_result = pd.read_sql_query(product_query, conn)

print("\nPRODUCT SALES")
print(product_result)

# CITY ANALYSIS

city_query = """
SELECT CITY,
       SUM(TOTAL_REVENUE) AS Revenue
FROM electronic_sales
GROUP BY CITY
ORDER BY Revenue DESC
"""

city_result = pd.read_sql_query(city_query, conn)

print("\nCITY SALES")
print(city_result)

# TOP SALESPERSON

salesperson_query = """
SELECT SALES_PERSON,
       SUM(TOTAL_REVENUE) AS Revenue
FROM electronic_sales
GROUP BY SALES_PERSON
ORDER BY Revenue DESC
LIMIT 5
"""

salesperson_result = pd.read_sql_query(
    salesperson_query,
    conn
)

print("\nTOP 5 SALESPERSON")
print(salesperson_result)

# BUSINESS INSIGHTS

top_product = product_result.loc[
    product_result['Total_Sales'].idxmax(),
    'PRODUCTS'
]

lowest_product = product_result.loc[
    product_result['Total_Sales'].idxmin(),
    'PRODUCTS'
]

top_city = city_result.loc[
    city_result['Revenue'].idxmax(),
    'CITY'
    
]

print("\n===== BUSINESS INSIGHTS =====")
print("Top Product :", top_product)
print("Lowest Product :", lowest_product)
print("Top City :", top_city)
print("Average Revenue :",
      round(product_result['Total_Sales'].mean(), 2))

# BAR CHART

plt.figure(figsize=(10, 6))

plt.bar(
    product_result['PRODUCTS'],
    product_result['Total_Sales']
)

plt.title('Product Wise Revenue')
plt.xlabel('Products')
plt.ylabel('Revenue (₹)')
plt.show()

# PIE CHART

plt.figure(figsize=(8, 8))

plt.pie(
    product_result['Total_Sales'],
    labels=product_result['PRODUCTS'],
    autopct='%1.1f%%'

)
plt.title('Revenue Distribution')
plt.tight_layout()
plt.show()

# HORIZONTAL BAR

plt.figure(figsize=(10, 6))

plt.barh(
    product_result['PRODUCTS'],
    product_result['Total_Sales']
)

plt.title('Product Revenue Comparison')
plt.xlabel('Revenue')
plt.ylabel('Products')
plt.tight_layout()
plt.show()

# DAILY TREND

daily_sales = combined_df.groupby(
    'DATE'
)['TOTAL_REVENUE'].sum()

plt.figure(figsize=(12, 5))

plt.plot(
    daily_sales.index,
    daily_sales.values,
    marker='o'
)

plt.title('Daily Revenue Trend')
plt.xlabel('Date')
plt.ylabel('Revenue (₹)')
plt.grid(True)
plt.tight_layout()
plt.show()

# TOP CITY GRAPH

plt.figure(figsize=(10, 6))

plt.bar(
    city_result['CITY'],
    city_result['Revenue']
)

plt.title('City Wise Revenue')
plt.xlabel('City')
plt.ylabel('Revenue (₹)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("suggestions for business growth:")
if top_product :
    print("high stock of", top_product, "should be maintained to meet customer demand.")
elif lowest_product :
    print("lowest product stock of", lowest_product, "should be monitored.")
# DATABASE CLOSE

conn.close()


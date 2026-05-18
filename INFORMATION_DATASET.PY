import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

 
data1 = {
    'DATE': ['01/03/26', '02/03/26', '03/03/26', '04/03/26', '05/03/26', '06/03/26', '07/03/26', '08/03/26', '09/03/26', '10/03/26'],
    'PRODUCTS': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 'Mouse'],
    'CITY': ['Mumbai', 'Bhopal', 'Indore', 'Delhi', 'Mumbai', 'Indore', 'Delhi', 'Bhopal', 'Indore', 'Mumbai'],
    'SALES_PERSON': ['Rahul verma', 'Aman kushwah', 'Neha jamle', 'Ravi kushwah', 'Sneha sharma ', 'Rahul karma', 'Aman chouham', 'Neha saste', 'Ravi gupta', 'Sneha gupta'],
    'UNITS_SOLD': [5, 20, 15, 7, 3, 25, 10, 4, 6, 30],
    'PRICE': [55000, 500, 1200, 15000, 60000, 450, 1100, 14000, 58000, 480]
}

df1 = pd.DataFrame(data1)

data2={
    'DATE':['11/03/26', '12/03/26', '13/03/26', '14/03/26', '15/03/26', '16/03/26', '17/03/26', '18/03/26', '19/03/26', '20/03/26'],
    'PRODUCTS':['Keyboard', 'Monitor', 'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 'Mouse', 'Keyboard', 'Monitor'],
    'CITY':['KHARGONE','UJJAIN','OMKARESHWAR','KHAMMAM','UJJAIN','OMKARESHWAR','KHARGONE','UJJAIN','OMKARESHWAR','KHARGONE'],
    'SALES_PERSON':['Ritik pal', 'Hemant kushwah', 'Manav jamle', 'Lokesh kushwah', 'Shruti sharma ', 'Suhani karma', 'Nikhil patidar', 'Anjali gupta', 'Divyanshu verma', 'Chetan kushwah'],
    'UNITS_SOLD':[12, 8, 4, 18, 20, 6, 10, 22, 14, 5],
    'PRICE':[1100, 14000, 58000, 480, 1200, 15000, 55000, 500, 1200, 15000]
}
df2 = pd.DataFrame(data2)
combined_df=pd.concat([df1, df2])

# Pandas ka use karke calculation
combined_df['TOTAL_REVENUE'] = combined_df['UNITS_SOLD'] * combined_df['PRICE']


# Ek temporary SQL Database banate hain # permanent memory ke leye mujhe ('file_name.db')ka use karna padega 
conn = sqlite3.connect(':memory:')
combined_df.to_sql('electronic_sales', conn, index=False, if_exists='replace')

# mujhe sql query likhne pade  Product-wise total sale nikalne ke liye
query = """
SELECT PRODUCTS, SUM(TOTAL_REVENUE) as Total_Sales 
FROM electronic_sales 
GROUP BY PRODUCTS 
ORDER BY Total_Sales DESC
"""
sql_result = pd.read_sql_query(query, conn)

# fir mujhe represt karna hai data ko graph ke form me
plt.figure(figsize=(10, 6))
plt.bar(sql_result['PRODUCTS'], sql_result['Total_Sales'], color=['red', 'blue', 'green', 'orange'])
plt.title('Product-wise Total Revenue (SQL + Pandas Analysis)')
plt.xlabel('Products')
plt.ylabel('Revenue (in ₹)')
if sql_result['Total_Sales'].max() > 100000:
    print("Top-selling product is:", sql_result.loc[sql_result['Total_Sales'].idxmax(), 'PRODUCTS'])
else:
    print("No product has sales exceeding ₹100,000.")
plt.show()
print("SQL Query Ka Result:")
print(sql_result)
plt.pie(sql_result['Total_Sales'], labels=sql_result['PRODUCTS'], autopct='%1.1f%%', startangle=140)
plt.title('Revenue Distribution by Product')
plt.axis('equal')
plt.show()

plt.figure(figsize=(10, 6))
plt.barh(sql_result['PRODUCTS'], sql_result['Total_Sales'], color=['red', 'blue', 'green', 'orange'])
plt.title('Product-wise Total Revenue (SQL + Pandas Analysis)')
plt.xlabel('Products')
plt.ylabel('Revenue (in ₹)')
plt.show()



  
if sql_result['Total_Sales'].min() < 50000:
    print("Lowest-selling product is:", sql_result.loc[sql_result['Total_Sales'].idxmin(), 'PRODUCTS'])
else:
    print("No product has sales below ₹50,000.")

if sql_result['Total_Sales'].max() > 100000:
    print("Top-selling product is:", sql_result.loc[sql_result['Total_Sales'].idxmax(), 'PRODUCTS'])


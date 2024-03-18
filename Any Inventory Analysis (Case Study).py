#!/usr/bin/env python
# coding: utf-8

# # Any Invetory Analysis

# # About Dataset
# ## Case Study: Inventory Analysis for Any Manufacturing Company
# 
# ### Background:
# Any Manufacturing Company is a medium-sized manufacturing company that produces electronic components. They have a wide range of products and maintain an inventory of raw materials, work-in-progress (WIP), and finished goods. The company has been experiencing issues with inventory management, including stockouts, excess inventory, and increased carrying costs. The management team wants to conduct an inventory analysis to identify areas for improvement and optimize their inventory management practices.

# ## Objective:
# - Identify opportunities to reduce stockouts and excess inventory.
# - Streamline the procurement and production processes to improve efficiency.
# - Develop a sustainable inventory management strategy for future growth.

# ## Key Analysis Componebts:
# - **Demand forecasting:** Analyze historical sales data to forecast future demand for different products accurately.
# - **ABC analysis:** Classify inventory items based on their value and importance to prioritize management efforts.
# - **Economic Order Quantity (EOQ) analysis:** Determine the optimal order quantity for raw materials to minimize ordering and carrying costs.
# - **Reorder point analysis:** Calculate the reorder point for each product to avoid stockouts.
# - **Lead time analysis:** Assess the lead time for raw materials and production to optimize inventory levels.
# - **Carrying cost analysis:** Calculate the carrying costs associated with inventory to identify areas for cost reduction.

# # Setting up the Environment/Data Exploration

# In[2]:


# load library packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


# Import csv files to read the data

purchase_price_list = pd.read_csv('2017PurchasePricesDec.csv')
beginning_inventory = pd.read_csv('BegInvFINAL12312016.csv')
end_inventory = pd.read_csv('EndInvFINAL12312016.csv')
invoice_purchases = pd.read_csv('InvoicePurchases12312016.csv')
purchase = pd.read_csv('PurchasesFINAL12312016.csv')
sales = pd.read_csv('SalesFINAL12312016.csv')


# In[4]:


purchase_price_list.head()


# In[5]:


beginning_inventory.head()


# In[6]:


end_inventory.head()


# In[7]:


invoice_purchases.head()


# In[8]:


purchase.head()


# In[9]:


sales.head()


# In[10]:


# Check to observe all the data info

print('\nPURCHASE PRICE LIST INFO:')
purchase_price_list.info()

print('\nBEGINNING INVENTORY INFO:')
beginning_inventory.info()

print('\nEND INVENTORY INFO:')
end_inventory.info()

print('\nINVOICE PURCHASES INFO:')
invoice_purchases.info()

print('\nPURCHASE INFO:')
purchase.info()

print('\nSALES INFO:')
sales.info()


# # Data Processing
# 
# **Detecting and Deleting the data rows with Null value:**

# In[11]:


purchase_price_list.isnull().sum()


# In[12]:


beginning_inventory.isnull().sum()


# In[13]:


end_inventory.isnull().sum()


# In[14]:


invoice_purchases.isnull().sum()


# In[15]:


purchase.isnull().sum()


# In[16]:


sales.isnull().sum()


# In[17]:


# Drop the rows with Null Values

purchase_price_list.dropna(inplace = True)
purchase.dropna(inplace = True)


# #### Handling duplicates:

# In[18]:


# Drop the duplicate values

purchase_price_list.drop_duplicates()
beginning_inventory.drop_duplicates()
end_inventory.drop_duplicates()
invoice_purchases.drop_duplicates()
purchase.drop_duplicates()
sales.drop_duplicates()


# ### Formating the Date columns appropriately:

# In[19]:


# beginning_inventory DataFrame
beginning_inventory['startDate'] = pd.to_datetime(beginning_inventory['startDate']).replace('startDate')

# end_inventory_DataFrame
end_inventory['endDate'] = pd.to_datetime(end_inventory['endDate']).replace('endDate')

# invoice_purchase DataFrame
invoice_purchases['InvoiceDate'] = pd.to_datetime(invoice_purchases['InvoiceDate']).replace('InvoiceDate')
invoice_purchases['PODate'] = pd.to_datetime(invoice_purchases['PODate']).replace('PODate')
invoice_purchases['PayDate'] = pd.to_datetime(invoice_purchases['PayDate']).replace('PayDate')

# urchase DataFrame
purchase['PODate'] = pd.to_datetime(purchase['PODate']).replace('PODate')
purchase['ReceivingDate'] = pd.to_datetime(purchase['ReceivingDate']).replace('ReceivingDate')
purchase['InvoiceDate'] = pd.to_datetime(purchase['InvoiceDate']).replace('InvoiceDate')
purchase['PayDate'] = pd.to_datetime(purchase['PayDate']).replace('PayDate')

# sales DataFrane
sales['SalesDate'] = pd.to_datetime(sales['SalesDate']).replace('SalesDate')


# # ABC Inventory Analysis

# In[20]:


# Summarize the Beginning and the End Inventories by product's Description 

beginning_summary = beginning_inventory.groupby(['Description'])['onHand'].sum().sort_values(ascending=False)
end_summary = end_inventory.groupby(['Description'])['onHand'].sum().sort_values(ascending=False)


# In[21]:


# Filter the summaries into High and Low Value products each; based on their availability

# Beginning Inventroy
print("\nTop 10 HIGH VALUE products at the Beginning of the year:\n", beginning_summary.head(10))
print("\nTop 10 LOW VALUE products at the Beginning of the year:\n", beginning_summary.tail(10))


# 
# 
# 

# In[22]:


# End Inventory
print("\nTop 10 HIGH VALUE products at the End of the year:\n", end_summary.head(10))
print("\nTop 10 LOW VALUE products at the End of the year:\n", end_summary.tail(10))


# # Sales Analysis
# **Determining the Most and the Least selling products:**

# In[23]:


# Analyze to summarize sales category by Fast and Low selling products

products_sales_category = sales.groupby(['Brand', 'Description']).agg({'SalesQuantity': 'sum'}).sort_values(by='SalesQuantity', ascending=False)


# In[24]:


# Top 10 Fast selling products

print("Top 10 Fast Selling Products:")
print(products_sales_category.head(10))


# In[25]:


# Top 10 Slow selling products

print("Top 10 Slow Selling Products:")
print(products_sales_category.tail(10))


# In[26]:


# Extend the data columns; creating additional column by extracting the transaction months from the sales's 'SalesDate'

sales['TransactionMonth'] = sales['SalesDate'].dt.month
sales.head()


# In[27]:


# Analyze (with visualization) to filter the sales transactions; grouping by the month of transaction 

sales_by_month = sales.groupby('TransactionMonth').agg({'TransactionMonth':'count'})
sns.countplot(x='TransactionMonth', data=sales)
plt.show()
print(sales_by_month)


# The above report shows that there were only two months (January and February) period of sales accounted in the dataset.
# However, the January month dominated the sales record with the ratio 9:1

# In[28]:


# Analyze (with visualization) to summarize the rate of revenue generated in each day of the months

revenue_per_month = sales.groupby('SalesDate').agg({'SalesDollars': 'sum'})
revenue_per_month.plot(figsize=(12,4), title= 'Periodic Sales Revenue')
plt.ylabel('Sum of Revenue')
plt.xlabel('Monthly Revenue in Days')


# The above report telescopes the periodic analysis; presenting the daily transactions within the months.
# This reveals the transaction trend to be on the average, though with a zig-zag pattern from the early days of the month with a major push up in the end days of the month, yet reversed with a major pull at the end of the month/beginning of february; causing a huge fall to the sales traffic.
# Further, the sales remained on the low throughout the february month; also with a slight and steady zig-zag pattern all through the month of february. 
# So it is recommended to monitor and reduce the stocking rate in the month to avoid overstocking while moderating the production.

# In[29]:


# Analyze (with visualization) to summarize the rate of revenue generated by top 10 vendors

revenue_by_vendor = sales.groupby('VendorName').agg({'SalesDollars':'sum'})['SalesDollars'].nlargest(10)
plt.figure(figsize=(10, 4))
revenue_by_vendor.plot(kind='bar', color='navy')
plt.title('Sales Revenue by top 10 Vendors')
plt.ylabel('Sum of Revenue(M)')
plt.xlabel('Vendor Name')
revenue_by_vendor


# The above report presents the sum of top 10 sales revenue as generated by each repective vendor.

# In[30]:


# Analyze (with visualization) to summarize; filtering out the top 10 inventories with high sales rate

sales_by_inventory = sales.groupby('InventoryId').agg({'SalesQuantity':'sum'})['SalesQuantity'].nlargest(10)

plt.figure(figsize=(10, 4))
sales_by_inventory.plot(kind='bar', color='purple')
plt.title('Sales by top 10 Inventories')
plt.ylabel('Sales Flow')
plt.xlabel('Inventories')
plt.xticks(rotation=85)
sales_by_inventory


# Furthering on the products restock adequacy by specific factor, the report above specifies the particular inventories to consider for the timely restock and monitoring for sales stability.

# # Conclusion
# ## ABC Inventory Analysis
# Comparing the top 10 high value products at the beginning of the year with those at the end of the year:
# It is evident that **Smirnoff 80 Proof** being on top of the list at the beginning of the year did not make it to the top 10 list at the end of the year.
# Furthering the Sale Analysis; **Jameson Irish Whiskey** gained up relevance and made it to the list of the top 10 stocked products of the year, possibly due to its sales attraction leading to more production hence restock, thereby sustaining sales continuity.
# Meanwhile, every other products remained on the relevant list all through the year; while **Capt Morgan Spiced Rum** took the head on the list; replacing Smirnoff 80 Proof.
# 
# 
# ## Sales Analysis
# ### General Product Sales:
# The **Fast** and the **Slow* selling products dataframes present the **Most** and the **Least** purchased products from the inventories, thereby drawing deserving attention to the **Fast selling** products for a better sales continuity and stability, while, also, more attention to the **Slow selling** products so as to mitigate the sales traffic downness whilst moderate the stock (especially in terms of production and restock) until there is a positive uptrend in their sales traffic.
# 
# ### Monthly Sales:
# The uptrend sales in the month of **January** implies that there usually is more traffic in the month; way more than it is in **February**. So it is recommendable to adequately prepare the inventory for the period.
# Meanwhile the sales remained on the low throughout the February month. So it is recommended to monitor and reduce the restocking rate in the month of February to avoid overstocking whilst moderate to **reduce the cost of production**.
# 
# ### Revenue Rate by Vendor:
# The sales revenue by vendors report presents the sum of top 10 sales revenue as generated by each repective vendor. This is to include that these enumerated vendors' inventories should be marked and assigned for adequate supply with respect to their stock variance. While the sales by InventoryId further reveals the inventories with higher transactional traffics; to be considered for the follow-up and the restock proper.

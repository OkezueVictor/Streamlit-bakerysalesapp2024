import streamlit as st
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    file = 'bakerysales.csv'
    df = pd.read_csv(file)
    df.rename(columns = {'Unnamed: 0': 'Id',
            'article': 'Product',
           'Quantity': 'quantity'},
                inplace=True)
    df.unit_price = df.unit_price.str.replace(",",".").str.replace("€","").str.strip()
    df.unit_price = df.unit_price.astype('float')
    # Calculate Sales
    df['sales'] = df.quantity * df.unit_price
    # Drop columns with zero sales
    df.drop(df[df.sales == 0].index, inplace= True)
    # convert date Column to date format
    df['date']=pd.to_datetime(df.date)
    return df

# load the dataset
df = load_data()

# App title
st.title("BAKERY SALES APP")

# Display the table
# st.dataframe(df.head(50))

# select and display specific products
# add filters

products = df['Product'].unique()
selected_product = st.sidebar.multiselect(
                    "Choose Product",
                    products,
                    [products[0],
                    products [2]
                    ])
filtered_table = df[df['Product'].isin(selected_product)]

# Display Matrices
# Total_sales = 0
if len (filtered_table) > 0:
    total_sales = filtered_table['sales'].sum()
else:
    total_sales = df.sales.sum()

# total_qty = df.quantity.sum()
if len (filtered_table) > 0:
    total_qty = filtered_table['quantity'].sum()
else:
    total_qty = df.quantity.sum()

# total_transactions = df.Id.count()
if len (filtered_table) > 0:
    total_transactions = filtered_table['Id'].count()
else:
    total_transactions = df.Id.count()

st.subheader("Calculations")
col1, col2, col3 = st.columns(3)

col1.metric("No of transactions", total_transactions)
col2.metric("Total Quantity", total_qty)
col3.metric("Total Sales", total_sales)

# end of metrics

# Display the filtered table
# with specific columns
st.dataframe(filtered_table[["date", "Product",
                             "quantity", "unit_price",
                             "sales"]])

# Bar chart
try:
    st.write("# Total sales of selected products")
    bar1 = filtered_table.groupby(['Product'])['sales'].sum().sort_values(ascending=True)
    st.bar_chart(bar1)
    xlabel = "Price"
    ylabel = "Products"
except ValueError as e:
    st.error(
        """ Error: """ % e.reason
    )

# Sales analysis
try:
    if len(filtered_table) > 0:
        daily_sales = filtered_table.groupby('date')['sales'].sum()
    else:
        daily_sales = df.groupby('date')['sales'].sum()

    daily_sales_df = daily_sales.reset_index().rename(columns={'sales':'total sales'})
    st.area_chart(daily_sales_df,
                      x='date',
                      y='total sales')
except ValueError as e:
    st.error(
        """ Error: """ % e.reason
    )


st.button("Re-run")
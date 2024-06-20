import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)


# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently


# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)

# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()


categories = df["Category"].unique()
cat_select = st.selectbox("Category Selection", categories)
filtered_data = df[df['Category'] == cat_select]

sub_categories = filtered_data['Sub_Category'].unique()
selected_sub_categories = st.multiselect('Select sub-categories:', sub_categories)
if selected_sub_categories:
    filtered_data = filtered_data[filtered_data['Sub_Category'].isin(selected_sub_categories)]


sales_data = filtered_data.groupby('Order_Date')['Sales'].sum().reset_index()

st.line_chart(sales_data, x='Order_Date',  y='Sales')

total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()
overall_profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0


overall_sales = df['Sales'].sum()
overall_profit = df['Profit'].sum()
overall_avg_profit_margin = (overall_profit / overall_sales) * 100 if overall_sales != 0 else 0
delta = overall_profit_margin - overall_avg_profit_margin


st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
st.metric(label="Overall Profit Margin (%)", value=f"{overall_profit_margin:.2f}%", delta=f"{delta:.2f}%")




st.write("## Your additions") 
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)") #done
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)") #done
st.write("### (3) show a line chart of sales for the selected items in (2)") #done
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)") #done
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)") #done

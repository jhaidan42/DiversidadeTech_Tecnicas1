
import numpy as np
import pandas as pd  
import plotly.express as px 
import streamlit as st  
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="✅",
    layout="wide",
)

df_month_revenue = pd.read_csv('monthly_revenue.csv')
df_all_sells = pd.read_csv('all_sales.csv')
#df_consolidate = pd.read_csv('consolidate.csv')
df_consolidate = pd.read_csv('monthly_sales.csv')

#adaptações do dataframe para nosso projeto:
df_consolidate.drop(columns=['balance', 'year'], inplace=True)
df_consolidate.index = df_consolidate['month']
df_consolidate.drop(columns='month', inplace=True)
df_consolidate = df_consolidate.T
df_consolidate.reset_index(names='product', inplace = True)
df_consolidate['balance'] = df_consolidate.sum(axis=1)
df_consolidate['type'] = 'Kg'
df_consolidate.loc[df_consolidate['product'] == "prod_1", 'type'] = 'Unit'
df_consolidate.loc[df_consolidate['product'] == "prod_2", 'type'] = 'Unit'
df_consolidate.loc[df_consolidate['product'] == "prod_3", 'type'] = 'Unit'
df_consolidate.loc[df_consolidate['product'] == "prod_4", 'type'] = 'Unit'
df_consolidate.loc[df_consolidate['product'] == "prod_5", 'type'] = 'Unit'
df_consolidate.loc[df_consolidate['product'] == "prod_6", 'type'] = 'Unit'
df_consolidate.loc[df_consolidate['product'] == "prod_7", 'type'] = 'Unit'

# dashboard title
st.title("Sales Dashboard")

# top-level filters

# creating a single-element container
placeholder = st.empty()

# near real-time / live feed simulation

sells = df_all_sells.shape[0]
month = df_month_revenue.shape[0]

# creating KPIs
balance = np.sum(df_month_revenue['balance'])


with placeholder.container():

    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Sellings ⏳",
        value=round(sells),
        delta=round(sells) - 10,
    )
    
    kpi2.metric(
        label="Months ",
        value=int(month),
        delta=-1 + month,
    )
    
    kpi3.metric(
        label="Balance ＄",
        value=f"$ {round(balance,2)} ",
        delta=-round(balance) * 100,
    )

    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Balance for Product")
        
        sum_balance = np.sum(df_consolidate['balance'])
        df_consolidate.loc[df_consolidate['balance'] < 0.05*sum_balance, 'product'] = 'Other' # Represent only large countries
        fig = px.pie(df_consolidate, names='product', values='balance', title='Product balance')
        st.write(fig)
        
    with fig_col2:
        st.markdown("### Balance for Type")
        
        fig2 = px.pie(df_consolidate, names='type', values='balance', title='Type balance')
        st.write(fig2)


 # create two columns for charts
    fig_col3, fig_col4 = st.columns(2)
    with fig_col3:
        st.markdown("### Balance for Product")
        _filter = st.selectbox("Select the product", df_month_revenue.columns.drop(['month','year','balance']))
        fig3 = px.line(data_frame=df_month_revenue, y=_filter, x='month', color='year', markers=True)
        st.write(fig3)
        
    with fig_col4:
        st.markdown("### Total Balance")
        fig4 = px.line(data_frame=df_month_revenue, y='balance', x='month', color='year', markers=True)
        st.write(fig4)


    st.markdown("### Detailed Data View")
    st.dataframe(df_month_revenue)
    
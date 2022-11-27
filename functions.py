from datetime import datetime

import numpy as np
import numpy.random as rd
import random
import pandas as pd
import requests

PRODUCT_UNIT = ["prod_1","prod_2","prod_3","prod_4","prod_5","prod_6","prod_7"]
PRODUCT_KG = ["prod_8","prod_9","prod_10","prod_11","prod_12","prod_13",
              "prod_14","prod_15","prod_16","prod_17","prod_18","prod_19",
              "prod_20"]
COLUMNS_ORDER = ['id','date','week','month_year','month','year'] + PRODUCT_UNIT + PRODUCT_KG


def data_clearing(data: dict):
    '''
    Function for data clearing
    All data will be format (date in date format, products between 1 and 7 for
    int values, products between 8 and 20 for float value). Sales with
    quantitative smaller than zero  and  products outside the range 1 to 20
    will be erased
    : param data: a dictionary with the sales
    : return: a pd.DataFrame affer data clearing
    '''
    for i in range(len(data)):
      clean_data = data[i].copy()
      clean_data['date'] = datetime.fromtimestamp(data[i]['date']).strftime("%d-%m-%Y")
      clean_data['week'] = datetime.fromtimestamp(data[i]['date']).strftime("%U")
      clean_data['month_year'] = datetime.fromtimestamp(data[i]['date']).strftime("%m-%Y")
      clean_data['month'] = datetime.fromtimestamp(data[i]['date']).month         # Date-formatted value
      clean_data['year'] = datetime.fromtimestamp(data[i]['date']).year

      for key, value in data[i].items():                                          # Clean data
        if key not in ['id','date']:
          if value <= 0:
            clean_data.pop(key)                                                   # Erase product sales with quantitative smaller than zero
          elif key in PRODUCT_UNIT:
            clean_data[key] = int(data[i][key])                                   # Int-formatted values ​​for products between 1 and 7
          elif key in PRODUCT_KG:
            clean_data[key] = float(data[i][key])                                 # Float-formatted values ​​for products between 8 and 20
          else:
            clean_data.pop(key)                                                   # Erase product sales for products not between 1 and 20          
      
      for j in PRODUCT_UNIT:
        if j not in clean_data:
          clean_data[j] = 0	
          
      for j in PRODUCT_KG:
        if j not in clean_data:
          clean_data[j] = 0.0
          
      data[i] = clean_data.copy()
    return pd.DataFrame(data)

def request_server(url: str ='http://localhost:3000/api/ep1'): 
    sales_week  = requests.get(url).json()
    sales_week = data_clearing(sales_week)
    sales_week = sales_week[COLUMNS_ORDER]      
    return sales_week

def all_sales(df_sales_week, file: str = 'all_sales.csv'):
    try: 
        df_all_sales = pd.read_csv(file)
    except FileNotFoundError:
        with open('all_sales.csv', 'w') as f:
            f.write('id,date,week,month_year,month,year,prod_1,prod_2,prod_3,prod_4,prod_5,prod_6,prod_7,prod_8,prod_9,prod_10,prod_11,prod_12,prod_13,prod_14,prod_15,prod_16,prod_17,prod_18,prod_19,prod_20\n')
        df_all_sales = pd.read_csv(file)
    df_sales_week.to_csv(file, mode='a', index= False, header=False)

def monthly_sales(df_sales_week, url: str ='http://localhost:3000/api/ep1', file: str ='monthly_sales.csv'):
    '''
    Function for monthly sales
    : param url: url for the request
    : param file: file for the monthly sales
    : return: a csv file with the monthly sales
    '''
    try: 
        df_monthly_sales = pd.read_csv(file)
    except FileNotFoundError:
        with open('monthly_sales.csv', 'w') as f:
            f.write('year,month,prod_1,prod_2,prod_3,prod_4,prod_5,prod_6,prod_7,prod_8,prod_9,prod_10,prod_11,prod_12,prod_13,prod_14,prod_15,prod_16,prod_17,prod_18,prod_19,prod_20,balance\n')
        df_monthly_sales = pd.read_csv(file)
    
    
    if not df_monthly_sales.empty:
        df_sales = df_sales_week.groupby(['year','month']).sum(numeric_only=True)
        df_sales['balance'] = df_sales.loc[:,list(PRODUCT_UNIT + PRODUCT_KG)].sum(axis = 1)
        df_monthly_sales = df_monthly_sales.groupby(['year','month']).sum(numeric_only=True)
        df_monthly_sales = df_monthly_sales.add(df_sales, fill_value=0)                  # Grouping by date
    else:
        df_monthly_sales = df_sales_week.groupby(['year','month']).sum(numeric_only=True)
        df_monthly_sales['balance'] = df_monthly_sales.loc[:,list(PRODUCT_UNIT + PRODUCT_KG)].sum(axis = 1)

    

    with open('monthly_sales.csv', 'w') as f:
            f.write('year,month,prod_1,prod_2,prod_3,prod_4,prod_5,prod_6,prod_7,prod_8,prod_9,prod_10,prod_11,prod_12,prod_13,prod_14,prod_15,prod_16,prod_17,prod_18,prod_19,prod_20,balance\n')
    df_monthly_sales.to_csv(file, mode='a', header=False)                        # Saving the data in a csv file
    return df_monthly_sales

def weekly_price(df_sales_week, file: str ='weekly_price.csv'):
    '''
    Function for the weekly update of products prices
    ''' 
    # Tentativa de abertura do .csv
    try:
        weekly_price = pd.read_csv(file)
    
    # Caso o .csv não exista, um novo arquivo será criado contendo os cabeçalhos
    except FileNotFoundError:
        with open('weekly_price.csv', 'w') as f:
            f.write('week,year,prod_1,prod_2,prod_3,prod_4,prod_5,prod_6,prod_7,prod_8,prod_9,prod_10,prod_11,prod_12,prod_13,prod_14,prod_15,prod_16,prod_17,prod_18,prod_19,prod_20\n')
        weekly_price = pd.read_csv(file)

    # Numero da semana atual
    current_week = int(df_sales_week['week'][0])
    next_week = current_week + 1 if current_week <52 else 1
    current_year = int(df_sales_week['year'][0])
    next_year = current_year if current_week <52 else current_year + 1

    # Precos iniciais
    if weekly_price.empty:
        #Atualizei para preencher aleatoriamente o preço inicial em uma rotina do produto 1 ao 20
        weekly_price.loc[0,'week'] = current_week
        weekly_price.loc[1,'week'] = next_week
        weekly_price.loc[0,'year'] = current_year
        weekly_price.loc[1,'year'] = next_year
        for i in range(1,21):
            product_str = f'prod_{i}'
            weekly_price.loc[0, product_str] = round(np.random.uniform(10,50), 2)
            weekly_price.loc[1, product_str] = weekly_price.loc[0, product_str]

        weekly_price.to_csv(file, mode='a', index= False, header=False)

    # Precos na semanas posteriores
    else:
        # Dados de vendas da semana anterior
        df_last_sales = pd.read_csv('all_sales.csv')

        last_week = df_last_sales['week'].iloc[-(df_sales_week.shape[0] + 1)]
        last_year = df_last_sales['year'].iloc[-(df_sales_week.shape[0] + 1)]

        df_last_sales = df_last_sales[(df_last_sales.week == last_week) & (df_last_sales.year == last_year)]
        df_last_sales = df_last_sales.drop(['id','date','week','month_year','month','year'], axis = 1)
        
        # Cópia do dataframe contendo as vendas da semana e remoção dos dados que não serão utilizados
        df_current_sales = df_sales_week.copy().drop(['id','date','week','month_year','month','year'], axis = 1)
        # Precos atualizados
        new_prices = {'week':next_week,'year':next_year}

        for product in df_current_sales:
            # Media de vendas da semana atual
            current_average_sales = df_current_sales[product].mean()
            # Media de vendas da semana anterior
            last_average_sales =  df_last_sales[product].mean()
            # Preco da semana anterior
            current_price = float(weekly_price[product].iloc[-1]) #mudei o nome de last para current, pois precisamos apenas do preço atual para determinar o futuro (P(t) e P(t-1))

            if last_average_sales == 0:
                v = current_average_sales
            else:
                v = (current_average_sales - last_average_sales) / last_average_sales

            f = 0.5 + 1 / (1 + np.exp(-v))
            # Preco corrigido para semana atual
            next_P = round(f * current_price, 2) #mudei o nome (na verdade o antigo P é igual a current_price, que é o antigo last_price)
            
            new_prices[product] = next_P
        weekly_price = pd.DataFrame([new_prices])
        weekly_price.to_csv(file, mode='a', index= False, header=False)
    return weekly_price
            
def revenue(df_sales, df_price):
    df_revenue = df_sales.copy()
    for product in list(PRODUCT_UNIT + PRODUCT_KG):
      df_revenue[product] = df_sales.iloc[0][product] * df_price.iloc[0][product]
    df_revenue['balance'] = df_revenue.loc[:,list(PRODUCT_UNIT + PRODUCT_KG)].sum(axis = 1)
    return df_revenue

def monthly_revenue(df_sales_week, file: str ='monthly_revenue.csv'):
    '''
    Function for monthly revenue
    : param file: file for the monthly revenue
    : return: a csv file with the monthly revenue
    '''
    try: 
        df_monthly_revenue = pd.read_csv(file)
    except FileNotFoundError:
        with open(file, 'w') as f:
            f.write('year,month,prod_1,prod_2,prod_3,prod_4,prod_5,prod_6,prod_7,prod_8,prod_9,prod_10,prod_11,prod_12,prod_13,prod_14,prod_15,prod_16,prod_17,prod_18,prod_19,prod_20,balance\n')
        df_monthly_revenue = pd.read_csv(file)
    
    df_weekly_price = pd.read_csv('weekly_price.csv')

    # Numero da semana atual
    current_week = int(df_sales_week.loc[0,'week'])
    current_year = df_sales_week.loc[0,'year']

    df_sales = df_sales_week.groupby(['year','month'], as_index= False).sum(numeric_only=True)
    df_price = df_weekly_price.loc[(df_weekly_price['week'] == current_week) & (df_weekly_price['year'] == current_year)]

    df_revenue = revenue(df_sales, df_price)

    if not df_monthly_revenue.empty:
        df_revenue = df_revenue.groupby(['year','month']).sum(numeric_only=True)
        df_monthly_revenue = df_monthly_revenue.groupby(['year','month']).sum(numeric_only=True)
        df_monthly_revenue = df_monthly_revenue.add(df_revenue, fill_value=0)                  # Grouping by date
    else:
        df_monthly_revenue = df_revenue.groupby(['year','month']).sum(numeric_only=True)

    with open(file, 'w') as f:
            f.write('year,month,prod_1,prod_2,prod_3,prod_4,prod_5,prod_6,prod_7,prod_8,prod_9,prod_10,prod_11,prod_12,prod_13,prod_14,prod_15,prod_16,prod_17,prod_18,prod_19,prod_20,balance\n')
    df_monthly_revenue.to_csv(file, mode='a', header=False)                        # Saving the data in a csv file
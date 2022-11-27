from functions import *

while True:
    df_sales_week = request_server()
    all_sales(df_sales_week)
    monthly_sales(df_sales_week)
    weekly_price(df_sales_week)
    monthly_revenue(df_sales_week)
    input() # Press enter to continue generating
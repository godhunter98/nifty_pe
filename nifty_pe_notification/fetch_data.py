from nsepython import *
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd

# symbol = "NIFTY 50"
# start_date = "01-Jan-2025"
# # end_date = "20-Mar-2025"
# end_date = datetime.today().date() 
# data = index_pe_pb_div(symbol,start_date,end_date)
# print(data[['DATE','pe']])



def last_10_year_data():
    today = dt.datetime.today().date()
    ten_year_ago = today - relativedelta(years=1)
    end_date = today.strftime('%d-%b-%Y')  
    start_date = ten_year_ago.strftime('%d-%b-%Y')

    symbol = 'NIFTY 50'
    pe_data = index_pe_pb_div(symbol,start_date,end_date)
    price_data = index_history(symbol,start_date,end_date)

    final_output = pd.merge(pe_data,price_data,left_on='DATE',right_on='HistoricalDate')
    useless_cols = ['RequestNumber_x','RequestNumber_y', 'Index Name_y', 'INDEX_NAME', 'HistoricalDate','OPEN', 'HIGH', 'LOW',]
    final_output.drop(useless_cols,inplace=True,axis=1)
    final_output= final_output.set_index('DATE')


    return final_output[::-1]

print(last_10_year_data())
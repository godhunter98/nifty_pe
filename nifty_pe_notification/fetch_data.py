from nsepython import *
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import sqlite3

try:
    with sqlite3.connect('test_db.db') as conn:
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)

# symbol = "NIFTY 50"
# start_date = "01-Jan-2025"
# # end_date = "20-Mar-2025"
# end_date = datetime.today().date() 
# data = index_pe_pb_div(symbol,start_date,end_date)
# print(data[['DATE','pe']])



def last_10_year_data():
    today = dt.datetime.today().date()
    ten_year_ago = today - relativedelta(years=20)
    end_date = today.strftime('%d-%b-%Y')  
    start_date = ten_year_ago.strftime('%d-%b-%Y')

    symbol = 'NIFTY 50'
    pe_data = index_pe_pb_div(symbol,start_date,end_date)
    price_data = index_history(symbol,start_date,end_date)


    final_output = pd.merge(pe_data,price_data,left_on='DATE',right_on='HistoricalDate')

    # remove some useless columns
    useless_cols = ['RequestNumber_x','RequestNumber_y', 'Index Name_y', 'INDEX_NAME', 'HistoricalDate']
    final_output.drop(useless_cols,inplace=True,axis=1)

    # set index to date
    final_output= final_output.set_index('DATE')

    # we convert this to float as the API returns those columns as str, not float
    final_output['Earnings'] = final_output['CLOSE'].astype(float) / final_output['pe'].astype(float)
    final_output['Earnings_growth'] = final_output['Earnings'].pct_change().round(3)


    return final_output[::-1]

x = last_10_year_data()

# doing some preprocessing so that dates can be easily taken care of in our db
x.index = pd.to_datetime(x.index, format='%d %b %Y')
x.index = x.index.strftime('%Y-%m-%d')
x.to_sql('nifty_data',conn,if_exists='replace')
print(x)


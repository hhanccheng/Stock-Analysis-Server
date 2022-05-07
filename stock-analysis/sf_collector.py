import requests
import json
import numpy as np
import pandas as pd
import os

# find stock id list
def tradv_geter():
    site = "https://scanner.tradingview.com/america/scan"
    response = requests.get(site)
    data = json.loads(response.text)
    df = pd.DataFrame(data['data'])
    id_list = []
    df.to_csv('temp.csv')
    f = open('temp.csv')
    line = f.readline()
    line = f.readline()
    while line:
        new_line = line.split(',')
        temp_list = new_line[1].split(':')
        if(temp_list[0] == 'NASDAQ'):
            id_list.append(temp_list[1])
        line = f.readline()
    os.remove('temp.csv')
    print(len(id_list))
    return id_list

# search a stock data during a time
def stock_collect(stockid,start,end):
    try:
        site = "https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=%d&period2=%d&interval=1d&events=history&=hP2rOschxO0" % (stockid,start,end)
        response = requests.get(site)
        data = json.loads(response.text)
        df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0], index=pd.to_datetime(np.array(data['chart']['result'][0]['timestamp'])*1000*1000*1000))
        df = df[['open', 'high', 'close', 'low', 'volume']]
        return df
    except:
        return None



    

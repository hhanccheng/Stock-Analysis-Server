import requests
import json
import numpy as np
import pandas as pd
import os
import time

# search a stock data during a time
def stock_collect(stockid,start,end):
    try:
        site = "https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=%d&period2=%d&interval=1d&events=history&=hP2rOschxO0" % (stockid,start,end)
        print (site)
        response = requests.get(site)
        data = json.loads(response.text)
        df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0], index=pd.to_datetime(np.array(data['chart']['result'][0]['timestamp'])*1000*1000*1000))
        df = df[['open', 'high', 'close', 'low', 'volume']]
        print (df)
        return df
    except:
        return None



end = int(time.time())
start = end - (3600*24*600)
stock_collect("AMD",start,end)    

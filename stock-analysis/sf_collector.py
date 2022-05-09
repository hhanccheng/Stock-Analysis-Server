import requests
import json
import pandas as pd
import numpy as np

# search a stock data during a time
def stock_collect(stockid,start,end):
    try:
        site = "https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=%d&period2=%d&interval=1d&events=history&=hP2rOschxO0" % (stockid,start,end)
        myheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/99.0'}
        response = requests.get(site,headers=myheaders)
        data = json.loads(response.text)
        df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0], index=pd.to_datetime(np.array(data['chart']['result'][0]['timestamp'])*1000*1000*1000))
        df = df[['open', 'high', 'close', 'low', 'volume']]
        return df
    except TypeError:
        return None


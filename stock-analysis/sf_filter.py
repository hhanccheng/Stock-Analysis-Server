import requests
import json
import pandas as pd
import time
import sf_reader
import sf_collector
import sf_progressbar
import sf_indicators
import sf_writer

#filter stock by lastday kline, if have lower shadowline
def ls_filter(ori_dic, filter_dic):
    end = int(time.time())
    start = end - (3600*24*10)
    stock_list =[]
    #id_list = sf_reader.stockid_reader(ori_dic)
    id_list = sf_reader.filter_reader(ori_dic)
    filter_lis = []
    stock_count = 0
    sf_progressbar.printProgress(stock_count,len(id_list))
    for stockid in id_list:
        stock_count += 1
        try:
            df = sf_collector.stock_collect(stockid,start,end)
            openprice_list, closeprice_list, highprice_list, lowprice_list, volume_list = sf_reader.data_reader(df)
            if(sf_indicators.lower_shadow(openprice_list[-1],closeprice_list[-1],highprice_list[-1],lowprice_list[-1])):
                filter_lis.append(stockid)
            sf_progressbar.printProgress(stock_count,len(id_list))
        except AttributeError:
            sf_progressbar.printProgress(stock_count,len(id_list))
    sf_writer.file_writer(filter_dic, filter_lis)

# filter with macd if the macd lower than 0, and diff <= dea
def macd_filter(ori_dic,filter_dic):
    end = int(time.time())
    start = end - (3600*12*60)
    stock_list =[]
    id_list = sf_reader.filter_reader(ori_dic)
    filter_lis = []
    stock_count = 0
    sf_progressbar.printProgress(stock_count,len(id_list))
    for stockid in id_list:
        stock_count += 1
        try:
            df = sf_collector.stock_collect(stockid,start,end)
            openprice_list, closeprice_list, highprice_list, lowprice_list, volume_list = sf_reader.data_reader(df)
            dif, dea, macd = sf_indicators.macd(closeprice_list, highprice_list, lowprice_list)
            if(dif[-1] <= dea[-1] and dea[-1] <= 0):
                filter_lis.append(stockid)
            sf_progressbar.printProgress(stock_count,len(id_list))
        except AttributeError:
            sf_progressbar.printProgress(stock_count,len(id_list))
        except IndexError:
            sf_progressbar.printProgress(stock_count,len(id_list))
    sf_writer.file_writer(filter_dic, filter_lis)

# filter with macd, macd严格金叉
def macdx_filter(ori_dic,filter_dic):
    end = int(time.time())
    start = end - (3600*12*60)
    stock_list =[]
    id_list = sf_reader.filter_reader(ori_dic)
    filter_lis = []
    stock_count = 0
    sf_progressbar.printProgress(stock_count,len(id_list))
    for stockid in id_list:
        stock_count += 1
        try:
            df = sf_collector.stock_collect(stockid,start,end)
            openprice_list, closeprice_list, highprice_list, lowprice_list, volume_list = sf_reader.data_reader(df)
            dif, dea, macd = sf_indicators.macd(closeprice_list, highprice_list, lowprice_list)
            if(dea[-1] < 0 and dif[-1] < 0):
                if(dif[-2] < dea[-2]):
                    if(dif[-1] > dif[-2] and dea[-1] < dea[-2]):
                        filter_lis.append(stockid)
            sf_progressbar.printProgress(stock_count,len(id_list))
        except AttributeError:
            sf_progressbar.printProgress(stock_count,len(id_list))
        except IndexError:
            sf_progressbar.printProgress(stock_count,len(id_list))
    sf_writer.file_writer(filter_dic, filter_lis)

# Ascending Crane Crows 升势鹤鸦
def acc_filter(ori_dic,filter_dic):
    end = int(time.time())
    start = end - (3600*12*15)
    stock_list =[]
    id_list = sf_reader.filter_reader(ori_dic)
    filter_lis = []
    stock_count = 0
    sf_progressbar.printProgress(stock_count,len(id_list))
    for stockid in id_list:
        stock_count += 1
        try:
            df = sf_collector.stock_collect(stockid,start,end)
            openprice_list, closeprice_list, highprice_list, lowprice_list, volume_list = sf_reader.data_reader(df)
            space1 = lowprice_list[-4] - (highprice_list[-5])
            space2 = lowprice_list[-3] - (highprice_list[-5])
            if(space1 >= 0 and space2 >= 0):
                filter_lis.append(stockid)
            sf_progressbar.printProgress(stock_count,len(id_list))
        except AttributeError:
            sf_progressbar.printProgress(stock_count,len(id_list))
        except IndexError:
            sf_progressbar.printProgress(stock_count,len(id_list))
    sf_writer.file_writer(filter_dic, filter_lis)
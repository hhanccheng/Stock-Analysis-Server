import requests
import json
import pandas as pd
import time
import sf_reader
import sf_collector
import sf_progressbar
import sf_mkformat
import sf_indicators
import sf_writer
import sf_graph

def parse_kline(filter_dic,htmlname):
    end = int(time.time())
    start = end - (3600*24*600)
    stock_count = 0
    filter_lis = sf_reader.filter_reader(filter_dic)
    print(filter_lis)
    sf_progressbar.printProgress(stock_count,len(filter_lis))
    for i in filter_lis:
        stock_count += 1
        try:
            df = sf_collector.stock_collect(i,start,end)
            sf_graph.kline(df, i)
            sf_progressbar.printProgress(stock_count,len(filter_lis))
        except ValueError:
            sf_progressbar.printProgress(stock_count,len(filter_lis))
        except AttributeError:
            sf_progressbar.printProgress(stock_count,len(filter_lis))
    content_list = sf_mkformat.html_kmaker(filter_lis)
    sf_writer.html_writer('/usr/share/nginx/html/%s' % (htmlname),content_list) 

def parse_pondraw(filter_dic,htmlname):
    end = int(time.time())
    start = end - (3600*24*600)
    stock_count = 0
    filter_lis = sf_reader.filter_reader(filter_dic)
    print(filter_lis)
    sf_progressbar.printProgress(stock_count,len(filter_lis))
    for i in filter_lis:
        stock_count += 1
        try:
            df = sf_collector.stock_collect(i,start,end)
            sf_graph.pondraw(df,i)
            sf_progressbar.printProgress(stock_count,len(filter_lis))
        except ValueError:
            sf_progressbar.printProgress(stock_count,len(filter_lis))
        except AttributeError:
            sf_progressbar.printProgress(stock_count,len(filter_lis))
    content_list = sf_mkformat.html_pmaker(filter_lis)
    sf_writer.html_writer('/usr/share/nginx/html/%s' % (htmlname),content_list) 
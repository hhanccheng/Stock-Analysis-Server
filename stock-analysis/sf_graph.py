import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from pandas import DataFrame, Series
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import pylab
import sf_indicators
import time



def kline(df,stockid):
    
    MA1 = 5
    MA2 = 10
    MA3 = 30
    MA4 = 60
    MA5 = 120
    MA6 = 240

    dfreshape = df.reset_index()
    dfreshape['datetime'] = mdates.date2num(df.index.values.astype(dt.date))/1000
    
    # clean day data for candle view 
    dfreshape.drop('volume', axis=1, inplace = True)
    dfreshape = dfreshape.reindex(columns=['datetime','open','high','low','close'])
    
    Av1 = sf_indicators.movingaverage(dfreshape.close.values, MA1)
    Av2 = sf_indicators.movingaverage(dfreshape.close.values, MA2)
    Av3 = sf_indicators.movingaverage(dfreshape.close.values, MA3)
    Av4 = sf_indicators.movingaverage(dfreshape.close.values, MA4)
    Av5 = sf_indicators.movingaverage(dfreshape.close.values, MA5)
    Av6 = sf_indicators.movingaverage(dfreshape.close.values, MA6)

    #SP = len(dfreshape.datetime.values[MA6:])
    SP = 168
    fig = plt.figure(facecolor='black',figsize=(15,10))
    
    ax1 = plt.subplot2grid((13,6), (4,0), rowspan=5, colspan=6, facecolor='black')
    candlestick_ohlc(ax1, dfreshape.values[-SP:], width=1, colorup='red', colordown='green')

    Label1 = str(MA1)+' SMA'
    Label2 = str(MA2)+' SMA'
    Label3 = str(MA3)+' SMA'
    Label4 = str(MA4)+' SMA'
    Label5 = str(MA5)+' SMA'
    Label6 = str(MA6)+' SMA'
    sar = sf_indicators.sar(dfreshape.close.values,dfreshape.high.values,dfreshape.low.values)

    
    ax1.plot(dfreshape.datetime.values[-SP:],Av1[-SP:],'tomato',label=Label1, linewidth=.8)
    ax1.plot(dfreshape.datetime.values[-SP:],Av2[-SP:],'orange',label=Label2, linewidth=.8)
    ax1.plot(dfreshape.datetime.values[-SP:],Av3[-SP:],'gold',label=Label3, linewidth=.8)
    ax1.plot(dfreshape.datetime.values[-SP:],Av4[-SP:],'lime',label=Label4, linewidth=.8)
    ax1.plot(dfreshape.datetime.values[-SP:],Av5[-SP:],'aqua',label=Label5, linewidth=.8)
    ax1.plot(dfreshape.datetime.values[-SP:],Av6[-SP:],'violet',label=Label6, linewidth=.8)
    ax1.scatter(dfreshape.datetime.values[-SP:],sar[-SP:], s=8, label='SAR')

    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color("w")
    ax1.spines['bottom'].set_color("white")
    ax1.spines['top'].set_color("white")
    ax1.spines['left'].set_color("white")
    ax1.spines['right'].set_color("white")
    ax1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')

    # plot an RSI indicator on top
    
    ax0 = plt.subplot2grid((13,6), (0,0), sharex=ax1, rowspan=2, colspan=6, facecolor='black')
    rsi6 = sf_indicators.rsi(dfreshape.close.values,6)
    #rsi12 = sf_indicators.rsi(dfreshape.close.values,12)
    rsi24 = sf_indicators.rsi(dfreshape.close.values,24)
    rsi6Col = 'green'
    #rsi12Col = 'yellow'
    rsi24Col = 'red'
    posCol = 'darkgreen'
    negCol = 'darkred'
    
    ax0.plot(dfreshape.datetime.values[-SP:], rsi6[-SP:], rsi6Col, label = 'rsi6', linewidth=1)
    #ax0.plot(dfreshape.datetime.values[-SP:], rsi12[-SP:], rsi12Col,label = 'rsi12', linewidth=1)
    ax0.plot(dfreshape.datetime.values[-SP:], rsi24[-SP:], rsi24Col, label = 'rsi24', linewidth=1)
    ax0.axhline(80, color=negCol)
    ax0.axhline(70, color=negCol)
    ax0.axhline(50, color='white')
    ax0.axhline(30, color=posCol)
    ax0.axhline(20, color=posCol)

    ax0.fill_between(dfreshape.datetime.values[-SP:], rsi6[-SP:], 80, facecolor=negCol, edgecolor=negCol, alpha=0.4)
    ax0.fill_between(dfreshape.datetime.values[-SP:], rsi6[-SP:], 20, facecolor=posCol, edgecolor=posCol, alpha=0.4)
    #ax0.fill_between(dfreshape.datetime.values[-SP:], rsi12[-SP:], 80, facecolor=negCol, edgecolor=negCol, alpha=0.25)
    #ax0.fill_between(dfreshape.datetime.values[-SP:], rsi12[-SP:], 20, facecolor=posCol, edgecolor=posCol, alpha=0.25)
    ax0.fill_between(dfreshape.datetime.values[-SP:], rsi24[-SP:], 70, facecolor=negCol, edgecolor=negCol, alpha=0.4)
    ax0.fill_between(dfreshape.datetime.values[-SP:], rsi24[-SP:], 20, facecolor=posCol, edgecolor=posCol, alpha=0.4)
    ax0.set_yticks([20,30,50,70,80])
    ax0.yaxis.label.set_color("w")
    ax0.spines['bottom'].set_color("white")
    ax0.spines['top'].set_color("white")
    ax0.spines['left'].set_color("white")
    ax0.spines['right'].set_color("white")
    ax0.tick_params(axis='y', colors='w')
    ax0.tick_params(axis='x', colors='w')
    plt.ylabel('RSI')

    volumeMin = 0
    ax1v = ax1.twinx()
    ax1v.fill_between(dfreshape.datetime.values[-SP:], volumeMin, df.volume.values[-SP:], facecolor='lightblue', alpha=.4)
    ax1v.axes.yaxis.set_ticklabels([])
    ax1v.grid(False)
    ###Edit this to 3, so it's a bit larger
    ax1v.set_ylim(0, 3*df.volume.values.max())
    ax1v.spines['bottom'].set_color("white")
    ax1v.spines['top'].set_color("white")
    ax1v.spines['left'].set_color("white")
    ax1v.spines['right'].set_color("white")
    ax1v.tick_params(axis='x', colors='w')
    ax1v.tick_params(axis='y', colors='w')

    # plot an MACD indicator
    ax2 = plt.subplot2grid((13,6), (9,0), sharex=ax1, rowspan=2, colspan=6, facecolor='black')
    fillcolor = 'yellow'
    dif, dea, macd = sf_indicators.macd(dfreshape.close.values,dfreshape.high.values,dfreshape.low.values)
    ax2.plot(dfreshape.datetime.values[-SP:], dif[-SP:], color='green', lw=2)
    ax2.plot(dfreshape.datetime.values[-SP:], dea[-SP:], color='red', lw=1)
    ax2.bar(dfreshape.datetime.values[-SP:], macd[-SP:], 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax2.spines['bottom'].set_color("white")
    ax2.spines['top'].set_color("white")
    ax2.spines['left'].set_color("white")
    ax2.spines['right'].set_color("white")
    ax2.tick_params(axis='x', colors='w')
    ax2.tick_params(axis='y', colors='w')
    plt.ylabel('MACD', color='w')
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))
    
    # plot an KDJ indicator
    
    ax3 = plt.subplot2grid((13,6), (2,0), sharex=ax1, rowspan=2, colspan=6, facecolor='black')
    k, d, j = sf_indicators.kdj(dfreshape.close.values,dfreshape.high.values,dfreshape.low.values)
    kCol = 'yellow'
    dCol = 'red'
    jCol = 'lightblue'
    posCol = 'darkgreen'
    negCol = 'darkred'
    outCol = 'w'
    
    ax3.plot(dfreshape.datetime.values[-SP:], k[-SP:], kCol, label = 'k', linewidth=1)
    ax3.plot(dfreshape.datetime.values[-SP:], d[-SP:], dCol,label = 'd', linewidth=1)
    ax3.plot(dfreshape.datetime.values[-SP:], j[-SP:], jCol, label = 'j', linewidth=1)
    ax3.fill_between(dfreshape.datetime.values[-SP:],k[-SP:],j[-SP:],facecolor='lightgreen', alpha=.4)
    ax3.axhline(100, color=outCol)
    ax3.axhline(80, color=negCol)
    ax3.axhline(50, color='white')
    ax3.axhline(20, color=posCol)
    ax3.axhline(0, color=outCol)
    ax3.set_yticks([0,20,50,80,100])
    ax3.yaxis.label.set_color("w")
    ax3.spines['bottom'].set_color("white")
    ax3.spines['top'].set_color("white")
    ax3.spines['left'].set_color("white")
    ax3.spines['right'].set_color("white")
    ax3.tick_params(axis='y', colors='w')
    ax3.tick_params(axis='x', colors='w')
    plt.ylabel('KDJ')

    # BIAS 
    ax4 = plt.subplot2grid((13,6), (11,0), sharex=ax1, rowspan=2, colspan=6, facecolor='black')
    y1 = sf_indicators.bias(dfreshape.close.values,6)
    y2 = sf_indicators.bias(dfreshape.close.values,24)
    y3 = sf_indicators.bias(dfreshape.close.values,72)
    y1Col = 'green'
    y3Col = 'red'
    y2Col = 'yellow'
    
    ax4.plot(dfreshape.datetime.values[-SP:], y1[-SP:], y1Col, label = 'k', linewidth=1)
    ax4.plot(dfreshape.datetime.values[-SP:], y2[-SP:], y2Col,label = 'd', linewidth=1)
    ax4.plot(dfreshape.datetime.values[-SP:], y3[-SP:], y3Col, label = 'j', linewidth=1)
    ax4.axhline(0, color='white')
    ax4.yaxis.label.set_color("w")
    ax4.spines['bottom'].set_color("white")
    ax4.spines['top'].set_color("white")
    ax4.spines['left'].set_color("white")
    ax4.spines['right'].set_color("white")
    ax4.tick_params(axis='y', colors='w')
    ax4.tick_params(axis='x', colors='w')
    plt.ylabel('BIAS')

    plt.suptitle(stockid,color='w')
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    pic_name = '/usr/share/nginx/html/kline/' +stockid + '.jpg'
    plt.savefig(pic_name)
    plt.close()

def pondraw(df,stockid):

    #format data
    dfreshape = df.reset_index()
    dfreshape['datetime'] = dfreshape.index.values.astype(dt.date)
    dfreshape.drop('volume', axis=1, inplace = True)
    dfreshape = dfreshape.reindex(columns=['datetime','open','high','low','close'])
    SP = 72
    fig = plt.figure(facecolor='black',figsize=(18,12))

    ##################################################################################
    axkline = plt.subplot2grid((16,10), (4,0), rowspan=6, colspan=10, facecolor='black')

    axrsi = plt.subplot2grid((16,10), (0,0), sharex=axkline, rowspan=2, colspan=10, facecolor='black')
    
    axv = plt.subplot2grid((16,10), (10,0), sharex=axkline, rowspan=2, colspan=10, facecolor='black')
    
    axmacd = plt.subplot2grid((16,10), (12,0), sharex=axkline, rowspan=2, colspan=10, facecolor='black')
    
    axkdj = plt.subplot2grid((16,10), (2,0), sharex=axkline, rowspan=2, colspan=10, facecolor='black')

    axbias = plt.subplot2grid((16,10), (14,0), sharex=axkline, rowspan=2, colspan=10, facecolor='black')
    ##################################################################################

    #candlestick
    MA1 = 10
    MA2 = 30
    MA3 = 72
    Av1 = sf_indicators.movingaverage(dfreshape.close.values, MA1)
    Av2 = sf_indicators.movingaverage(dfreshape.close.values, MA2)
    Av3 = sf_indicators.movingaverage(dfreshape.close.values, MA3)
    sar = sf_indicators.sar(dfreshape.close.values,dfreshape.high.values,dfreshape.low.values)
    candlestick_ohlc(axkline, dfreshape.values[-SP:], width=0.6, colorup='red', colordown='green')
    axkline.plot(dfreshape.datetime.values[-SP:],Av1[-SP:],'lime',linewidth=1)
    axkline.plot(dfreshape.datetime.values[-SP:],Av2[-SP:],'yellow',linewidth=1)
    axkline.plot(dfreshape.datetime.values[-SP:],Av3[-SP:],'tomato',linewidth=1)
    axkline.scatter(dfreshape.datetime.values[-SP:],sar[-SP:], s=5)
    axkline.grid(True, color='w')
    axkline.yaxis.label.set_color("w")
    axkline.spines['bottom'].set_color("white")
    axkline.spines['top'].set_color("white")
    axkline.spines['left'].set_color("white")
    axkline.spines['right'].set_color("white")
    axkline.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    axkline.tick_params(axis='x', colors='w')
    

    #RSI
    rsi6 = sf_indicators.rsi(dfreshape.close.values,6)
    rsi24 = sf_indicators.rsi(dfreshape.close.values,24)
    rsi6Col = 'lime'
    rsi24Col = 'tomato'
    posCol = 'darkgreen'
    negCol = 'darkred'
    axrsi.plot(dfreshape.datetime.values[-SP:], rsi6[-SP:], rsi6Col, linewidth=1)
    axrsi.plot(dfreshape.datetime.values[-SP:], rsi24[-SP:], rsi24Col, linewidth=1)
    axrsi.axhline(80, color=negCol,linewidth=.8)
    axrsi.axhline(70, color=negCol,linewidth=.8)
    axrsi.axhline(50, color='w',linewidth=.8)
    axrsi.axhline(30, color=posCol,linewidth=.8)
    axrsi.axhline(20, color=posCol,linewidth=.8)
    axrsi.grid(True)
    axrsi.yaxis.label.set_color("w")
    axrsi.spines['bottom'].set_color("white")
    axrsi.spines['top'].set_color("white")
    axrsi.spines['left'].set_color("white")
    axrsi.spines['right'].set_color("white")
    axrsi.tick_params(axis='y', colors='w')
    axrsi.tick_params(axis='x', colors='w')

    #volume
    axv.bar(dfreshape.datetime.values[-SP:], df.volume.values[-SP:], facecolor='lightskyblue', alpha=1)
    vav5 = sf_indicators.volumeaverage(df.volume.values,5)
    vav10 = sf_indicators.volumeaverage(df.volume.values,10)
    vav20 = sf_indicators.volumeaverage(df.volume.values,20)
    axv.plot(dfreshape.datetime.values[-SP:], vav5[-SP:], 'lime', linewidth=1)
    axv.plot(dfreshape.datetime.values[-SP:], vav10[-SP:], 'yellow', linewidth=1)
    axv.plot(dfreshape.datetime.values[-SP:], vav20[-SP:], 'tomato', linewidth=1)
    axv.grid(True)
    axv.spines['bottom'].set_color("white")
    axv.spines['top'].set_color("white")
    axv.spines['left'].set_color("white")
    axv.spines['right'].set_color("white")
    axv.tick_params(axis='x', colors='w')
    axv.tick_params(axis='y', colors='w')

    #MACD
    fillcolor = 'yellow'
    dif, dea, macd = sf_indicators.macd(dfreshape.close.values,dfreshape.high.values,dfreshape.low.values)
    axmacd.plot(dfreshape.datetime.values[-SP:], dif[-SP:], color='lime', lw=1)
    axmacd.plot(dfreshape.datetime.values[-SP:], dea[-SP:], color='tomato', lw=1)
    axmacd.bar(dfreshape.datetime.values[-SP:], macd[-SP:], 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    axmacd.axhline(0,c='y',lw=0.8)
    axmacd.grid(True)
    axmacd.spines['bottom'].set_color("white")
    axmacd.spines['top'].set_color("white")
    axmacd.spines['left'].set_color("white")
    axmacd.spines['right'].set_color("white")
    axmacd.tick_params(axis='x', colors='w')
    axmacd.tick_params(axis='y', colors='w')
    axmacd.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))

    #KDJ
    k, d, j = sf_indicators.kdj(dfreshape.close.values,dfreshape.high.values,dfreshape.low.values)
    kCol = 'yellow'
    dCol = 'tomato'
    jCol = 'lime'
    posCol = 'darkgreen'
    negCol = 'darkred'
    axkdj.plot(dfreshape.datetime.values[-SP:], k[-SP:], kCol, label = 'k', linewidth=1)
    axkdj.plot(dfreshape.datetime.values[-SP:], d[-SP:], dCol,label = 'd', linewidth=1)
    axkdj.plot(dfreshape.datetime.values[-SP:], j[-SP:], jCol, label = 'j', linewidth=1)
    axkdj.axhline(100, color=negCol,lw=0.8)
    axkdj.axhline(80, color=negCol,lw=0.8)
    axkdj.axhline(50, color='w',lw=0.8)
    axkdj.axhline(20, color=posCol,lw=0.8)
    axkdj.axhline(0, color=posCol,lw=0.8)
    axkdj.yaxis.label.set_color("w")
    axkdj.grid(True)
    axkdj.spines['bottom'].set_color("white")
    axkdj.spines['top'].set_color("white")
    axkdj.spines['left'].set_color("white")
    axkdj.spines['right'].set_color("white")
    axkdj.tick_params(axis='y', colors='w')
    axkdj.tick_params(axis='x', colors='w')

    #BIAS 
    axbias = plt.subplot2grid((15,10), (13,0), sharex=axkline, rowspan=2, colspan=10, facecolor='black')
    y1 = sf_indicators.bias(dfreshape.close.values,6)
    y2 = sf_indicators.bias(dfreshape.close.values,24)
    y3 = sf_indicators.bias(dfreshape.close.values,72)
    y1Col = 'lime'
    y3Col = 'tomato'
    y2Col = 'yellow'
    axbias.plot(dfreshape.datetime.values[-SP:], y1[-SP:], y1Col, label = 'k', linewidth=1)
    axbias.plot(dfreshape.datetime.values[-SP:], y2[-SP:], y2Col,label = 'd', linewidth=1)
    axbias.plot(dfreshape.datetime.values[-SP:], y3[-SP:], y3Col, label = 'j', linewidth=1)
    axbias.axhline(0, color='white',lw=0.3)
    axbias.yaxis.label.set_color("w")
    axbias.grid(True)
    axbias.spines['bottom'].set_color("white")
    axbias.spines['top'].set_color("white")
    axbias.spines['left'].set_color("white")
    axbias.spines['right'].set_color("white")
    axbias.tick_params(axis='y', colors='w')
    axbias.tick_params(axis='x', colors='w')

    now = time.strftime("%Y-%m-%d-%H_%M",time.localtime(time.time()))
    plt.suptitle(stockid +' '+ now,color='w')
    plt.setp(axkline.get_xticklabels(), visible=False)
    plt.setp(axmacd.get_xticklabels(), visible=False)
    plt.setp(axrsi.get_xticklabels(), visible=False)
    plt.setp(axv.get_xticklabels(), visible=False)
    plt.setp(axkdj.get_xticklabels(), visible=False)
    plt.setp(axbias.get_xticklabels(), visible=False)

    # save
    pic_name = '/usr/share/nginx/html/pondraw/' +stockid + '.jpg'
    plt.savefig(pic_name)
    plt.close()
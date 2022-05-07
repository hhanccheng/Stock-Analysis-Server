import sf_filter
import sf_parse
import time

stock = "stock"
option = "option"

#filter file
stock_filter = "stock_filter"
option_filter = "option_filter"

#html file
stock_html = "stock.html"
option_html = "option.html"

# 长下影线过滤法
lsoption_filter = "option_lsfilter"
lsoption_html = "lsoption.html"
lsmacdoption_filter = "option_lsmacdfilter"
lsmacdoprion_html = "lsmacdoption.html"

def do_filter():

    #长下影线过滤法
    sf_filter.ls_filter(option,lsoption_filter)

    # 长下影线 + macd
    sf_filter.macd_filter(lsoption_filter,lsmacdoption_filter)

    #macd 0线金叉过滤法 macdx
    sf_filter.macdx_filter(option,option_filter)
    sf_filter.macdx_filter(stock,stock_filter)
    
    # 升势鹤鸦
    #sf_filter.acc_filter(stock,stock_filter)

def do_parse():
    # Kline解析
    sf_parse.parse_kline(lsoption_filter,lsoption_html)

    # pondraw解析
    sf_parse.parse_pondraw(option_filter,option_html)
    sf_parse.parse_pondraw(lsmacdoption_filter,lsmacdoprion_html)
    sf_parse.parse_pondraw(stock_filter,stock_html)

start = time.time()
do_filter()
do_parse()
end = time.time()
print (end-start)

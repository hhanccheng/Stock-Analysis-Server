import sf_parse
import time

stock = "stock"

#filter file
stock_filter = "stock_filter"
option_filter = "option_filter"

#html file
kline_html = "kline.html"
pondraw_html = "pondraw.html" 


def do_parse():
    # Kline解析
    sf_parse.parse_kline(stock,kline_html)

    # pondraw解析
    sf_parse.parse_pondraw(stock,pondraw_html)

start = time.time()
do_parse()
end = time.time()
print (end-start)

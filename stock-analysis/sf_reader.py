
# normal reader
def filter_reader(fname):
    f = open(fname)
    line = f.readline()
    id_list = line.split(" ")
    return id_list[:-1]

# stock data reader
def data_reader(df):
    lowprice_list = df.low.values
    closeprice_list = df.close.values
    volume_list = df.volume.values
    openprice_list = df.open.values
    highprice_list = df.high.values

    return openprice_list, closeprice_list, highprice_list, lowprice_list, volume_list


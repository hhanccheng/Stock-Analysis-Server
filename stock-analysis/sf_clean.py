# stock id reader with "<"
def txt_clean(fname):
    f = open(fname)
    line = f.readline()
    id_list = []
    while line:
        temp_lis = line.split("<")
        id_list.append(temp_lis[1])
        line = f.readline()
    f.close()
    f = open(fname,'w')
    for i in id_list:
        f.write(i + " ")
    f.close()

txt_clean('stock.txt')
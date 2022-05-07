from numpy import *

# RSI
# RSI can only be used as a warning of overbought or oversold, not necessarily as a signal to enter the market. 
# In a bull market or bear market, overbought and oversold can stay for a period of time, 
# never see RSI below 20 or above 80 and immediately take action to buy or sell, otherwise you will only fall into the RSI trap.

def lower_shadow(openprice,closeprice,highprice,lowprice):
    if(openprice < closeprice):
        higher = highprice - openprice
        lower = openprice - lowprice
        if(higher <= lower):
            return True
        else:
            return False
    else:
        higher = highprice - closeprice
        lower = closeprice - lowprice
        if(higher <= lower):
            return True
        else:
            return False

def higher_shadow(openprice,closeprice,highprice,lowprice):
    if(openprice > closeprice):
        higher = highprice - openprice
        lower = openprice - lowprice
        if(higher >= lower):
            return True
        else:
            return False
    else:
        higher = highprice - closeprice
        lower = closeprice - lowprice
        if(higher >= lower):
            return True
        else:
            return False

def movingaverage(closevalues, MA):
    av_lis = []
    count = 0
    while (count + MA) < len(closevalues):
        sum = 0
        for i in closevalues[count:MA+count]:
            sum += i
        avg = sum / MA
        av_lis.append(avg)
        count += 1
    return av_lis

def volumeaverage(volume_list,MA):
    av_lis = []
    count = 0
    while (count + MA) < len(volume_list):
        sum = 0
        for i in volume_list[count:MA+count]:
            sum += i
        avg = sum / MA
        av_lis.append(avg)
        count += 1
    return av_lis

def rsi(closeprice_list , period):
    #print(closeprice_list)
    rsi_lis = []
    count = 0
    while (count + period) < len(closeprice_list):
        lastprice = closeprice_list[count]
        up_sum = 0
        down_sum = 0
        up_count = 0
        down_count = 0
        up_avg = 0
        down_avg = 0
        for closeprice in closeprice_list[count+1:period+count]:
            if(lastprice > closeprice):
                down_sum += (lastprice - closeprice)
                down_count += 1
            elif(lastprice < closeprice):
                up_sum += (closeprice - lastprice)
                up_count += 1
            lastprice = closeprice
        
        if(up_count == 0):
            up_count = 1
        if(down_count == 0):
            down_count = 1
        up_avg = up_sum/up_count
        down_avg = down_sum/down_count
        if (down_sum != 0):
            rsi = up_avg/(up_avg + down_avg) * 100
        else:
            if (len(rsi_lis)>=1):
                rsi = rsi_lis[-1]
            else:
                rsi = 0
        rsi_lis.append(rsi)
        count += 1
    return rsi_lis


def macd(closeprice_list,highprice_list,lowprice_list):
    DIF_lis = []
    DEA_lis = []
    MACD_lis = []
    di_lis = []
    for i in range(len(closeprice_list)):
        di = (closeprice_list[i]*2 + highprice_list[i] + lowprice_list[i])/4
        di_lis.append(di)
    lastclose = di_lis[0]
    i = di_lis[1]
    lastEMA12 = 2/13 * i + 11/13 * lastclose
    lastEMA26 = 2/27 * i + 25/27 * lastclose
    DIF = lastEMA12 - lastEMA26
    lastDEA = 2/10 *DIF
    lastclose = i
    for i in di_lis[2:]:
        EMA12 = 2/13 * i + 11/13 * lastEMA12
        EMA26 = 2/27 * i + 25/27 * lastEMA26
        lastEMA12 = EMA12
        lastEMA26 = EMA26
        DIF = EMA12 - EMA26
        DEA = 2/10 * DIF + 8/10 * lastDEA
        lastDEA = DEA
        MACD = DIF-DEA
        DIF_lis.append(DIF)
        DEA_lis.append(DEA)
        MACD_lis.append(MACD)
        lastclose = i
    
    return DIF_lis, DEA_lis, MACD_lis

# kdj
def kdj(closeprice_list,highprice_list,lowprice_list):
    day = 0
    k_lis = []
    d_lis = []
    j_lis = []
    c = closeprice_list[day+8]
    h = max(highprice_list[day:day+8])
    l = min(lowprice_list[day:day+8])
    if (h-l == 0 ):
        rsv = (c-l + 1)/(h-l +1) *100
    else:
        rsv = (c-l)/(h-l) *100
    lastk = 50 + rsv / 3
    lastd = 50 + lastk/3
    day += 1
    while (day + 8 <= len(closeprice_list) - 1):
        c = closeprice_list[day+8]
        h = max(highprice_list[day:day+8])
        l = min(lowprice_list[day:day+8])
        if (h-l == 0 ):
            rsv = (c-l + 1)/(h-l +1) *100
        else:
            rsv = (c-l)/(h-l) *100
        k = lastk * 2/3 + rsv/3
        d = lastd * 2/3 + k/3
        j = 3*k - 2*d
        k_lis.append(k)
        d_lis.append(d)
        j_lis.append(j) 
        lastk = k
        lastd = d
        day += 1
    
    return k_lis, d_lis, j_lis

# bias 乖离率
def bias(closeprice_list, period):
    day = 0
    y_lis = []
    while(day + period <= len(closeprice_list)-1):
        close_avg = mean(closeprice_list[day:day+period])
        y = (closeprice_list[day + period] - close_avg)/close_avg
        y_lis.append(y)
        day += 1
    return y_lis

# stop and reveres, SAR DMI
def sar(closeprice_list,highprice_list,lowprice_list):
    day = 1
    period = 1
    sar_lis = []
    periodstart = day #[0-5][1-6][2-7][3-8][4-9][5-10]
    periodend = day + period
    lastup = True
    af = 0.02
    if(closeprice_list[periodend] >= closeprice_list[periodstart]):
        t0 = min(lowprice_list[periodstart-1:periodend-1])
        ep = max(highprice_list[periodstart-1:periodend-1])
        if(max(highprice_list[periodstart-1:periodend-1]) < max(highprice_list[periodstart:periodend])):
            af += 0.02
    else:
        t0 = max(highprice_list[periodstart-1:periodend-1])
        ep = min(lowprice_list[periodstart-1:periodend-1])
        if(min(lowprice_list[periodstart-1:periodend-1]) > min(lowprice_list[periodstart:periodend])):
            af -= 0.02
        lastup = False
    lastsar = t0
    while (day + period <= len(closeprice_list)-1):
        periodstart = day #[0-5][1-6][2-7][3-8][4-9][5-10]
        periodend = day + period
        if(af > 0.2):
            af = 0.02
        sar = lastsar + af * (ep-lastsar)
        if(closeprice_list[periodend] > closeprice_list[periodstart]):
            ep = max(highprice_list[periodstart-1:periodend-1])
            if (lastup == False):
                af = 0.02
            if(max(highprice_list[periodstart-1:periodend-1]) < max(highprice_list[periodstart:periodend])):
                af += 0.02
            lastup = True
            if(periodend <  len(closeprice_list)-1):
                if(sar >= min(lowprice_list[periodstart:periodend+1])):
                    sar = min(lowprice_list[periodstart:periodend+1])
            else:
                if(sar >= min(lowprice_list[periodstart:])):
                    sar = min(lowprice_list[periodstart:])
        else:
            ep =  min(lowprice_list[periodstart-1:periodend-1])
            if (lastup):
                af = 0.02
            if( min(lowprice_list[periodstart-1:periodend-1]) >  min(lowprice_list[periodstart:periodend])):
                af -= 0.02
            lastup = False
            if(periodend <  len(closeprice_list)-1):
                if(sar <= max(highprice_list[periodstart:periodend+1])):
                    sar = max(highprice_list[periodstart:periodend+1])
            else:
                if(sar <= max(highprice_list[periodstart:periodend])):
                    sar = max(highprice_list[periodstart:periodend])
        lastsar = sar
        sar_lis.append(sar)
        day += 1
    
    return sar_lis
    








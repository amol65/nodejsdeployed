#!/usr/bin/env python
# coding: utf-8

# In[ ]:
client_id = 'DO3OHPAO1D-100'
secret_key='6WMPXU4GKD'

redirect_uri = 'https://trade.fyers.in/api-login/redirect-uri/index.html'

from datetime import datetime, timedelta, date, time as TT
import pytz, time
from fyers_api import fyersModel
import pandas as pd
from fyers_api import accessToken
from datetime import datetime, timedelta
import requests


# In[ ]:


fyers = fyersModel.FyersModel(client_id=client_id, token=token, log_path='fv2/')


# In[ ]:


fyers.get_profile()


# In[ ]:


def getLTP(symbol,fyersObj):
    data = {"symbols":symbol}
    res = fyersObj.quotes(data)
    return res['d'][0]['v']['lp']


# In[ ]:


fyers.quotes( {"symbols":'NSE:SBIN-EQ,NSE:HDFC-EQ'})


# In[ ]:


allowedSegment = [14] 
fno_url = 'http://public.fyers.in/sym_details/NSE_FO.csv'
fno_symbolList = pd.read_csv(fno_url,header =None)
fno_symbolList.columns =  ['FyersToken', 'Name', 'Instrument', 'lot', 'tick', 'ISIN','TradingSession', 'Lastupdatedate', 'Expirydate', 'Symbol', 'Exchange', 'Segment','ScripCode','ScripName','LTP','STRIKE','OPT_TYPE']
fno_symbolList =fno_symbolList[fno_symbolList['Instrument'].isin(allowedSegment)]
fno_symbolList['Expirydate'] = pd.to_datetime(fno_symbolList['Expirydate'],unit='s').apply(lambda x: x.date())
fno_symbolList = fno_symbolList[(fno_symbolList['Expirydate'] == date(2022,9,8)) & (fno_symbolList['ScripName'] =='NIFTY') ]
splitList = fno_symbolList[fno_symbolList.columns[1]].str.split(' ',expand =True)
col_len = len(splitList.columns) -1
fno_symbolList['STRIKE'] = splitList[col_len-1].astype(float,errors ='ignore')
fno_symbolList['OPT_TYPE'] = splitList[col_len]
fno_symbolList


# In[ ]:


symbolOC = fno_symbolList.copy() 
symbolOC['STRIKE'] = symbolOC['STRIKE'].astype(float,errors ='ignore')

premium =  60
spotltp = getLTP('NSE:NIFTY50-INDEX',fyers)
symbol ='NIFTY'
for optn_type in ['CE','PE']:
    if optn_type == 'CE':
        pespotltp = spotltp*(1+0.03)
        filterSymbolOC = symbolOC[(symbolOC.OPT_TYPE =='PE') & (symbolOC.STRIKE <= pespotltp) &  (symbolOC.ScripName == symbol)].sort_values(by = 'STRIKE',ascending = False)

    else:
        cespotltp = spotltp*(1-0.03)
        filterSymbolOC = symbolOC[(symbolOC.OPT_TYPE =='CE') & (symbolOC.STRIKE >= cespotltp) & (symbolOC.ScripName == symbol)].sort_values(by = 'STRIKE')

    x = filterSymbolOC[:49]['Symbol'].tolist()
    symbols = ""
    for i in x:
        symbols = f'{symbols}{i},'
    symbols = symbols[:-1]
    data = {"symbols":symbols}
    res = fyers.quotes(data)
    ltpdict = {}
    if 's' in res and res['s'] == 'ok':
        for i in res['d']:
            ltpdict.update({i['n'] : i['v']['lp']})


    intialValue = 100000
    filterStock = None
    for optsymbol , optltp in ltpdict.items():
        if  abs(optltp - premium) < intialValue :
            intialValue = abs(optltp - premium)
            filterStock = optsymbol

    print(filterStock)


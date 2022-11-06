client_id = 'DO3OHPAO1D-100'
secret_key='6WMPXU4GKD'
redirect_uri = 'https://trade.fyers.in/api-login/redirect-uri/index.html'

from fyers_api import fyersModel,accessToken
from fyers_api.Websocket import ws
import os, time
import pandas as pd
import threading

def get_access_token():
    if not os.path.exists("access_token.txt"):
        session=accessToken.SessionModel(client_id=client_id,secret_key=secret_key,redirect_uri=redirect_uri, response_type='code', grant_type='authorization_code')
        response = session.generate_authcode()
        print("login url: ", response)
        auth_code = input("Enter auth code: ")
        session.set_token(auth_code)
        response = session.generate_token()
        access_token = response["access_token"]
        with open("access_token.txt","w") as f:
            f.write(access_token)
    else:
        with open("access_token.txt","r") as f:
            access_token = f.read()
    return access_token
access_token = get_access_token()
fyers = fyersModel.FyersModel(client_id='DO3OHPAO1D-100', token=access_token)
print(fyers.positions())

def exitAllPositions(profit, loss):
    while True:
        positions = fyers.positions()
        pl_total = fyers.positions()["overall"]["pl_total"]
        data={}
        print(pl_total)
        if pl_total <= loss or pl_total >= profit:
            res = fyers.exit_positions(data)
            print(res["message"])
            break
        time.sleep(1)

def exitIndividualPositions(posId, profit, loss):
    positions = fyers.positions()["netPositions"]
    for x in positions:
        if posId == x['id']:
            data = {'id':x['id']}
            if x['pl'] <= loss or x['pl'] > profit:
                res = fyers.exit_positions(data)
                print(res["message"])

def getOpenPositions():
    positionList=[]
    positions = fyers.positions()["netPositions"]
    for x in positions:
        if x['realized_profit'] != x['pl']:
            positionList.append(x['id'])

    return positionList

profit = float(input("Enter profit you want: "))
loss = float(input("Enter loss you can take: "))
exitAllPositions(profit, -loss)
# threading.Thread(target=exitAllPositions,args=(profit,-loss,)).start()
# exitIndividualPositions()
openPositionList = getOpenPositions()
print(openPositionList)
# exitIndividualPositions('NSE:NIFTY22OCT17800PE-INTRADAY',profit, -loss)

# for pos in openPositionList:
#     threading.Thread(target=exitIndividualPositions,args=(pos,)).start()







import pandas as pd
import numpy as np
from binance.client import Client
from binance.websockets import BinanceSocketManager
import talib
import json
from twisted.internet import reactor
from matplotlib import pyplot as plt

"""
Auuthor : Bui Nguyen Franck
"""

api_key = 'lEXQTBWmhUxhpscgGYF866yM36zjkaQ34qUuF9cHzyg6HpxXq6xY6OxjQ5CxVHyx'
api_secret = 'P13JsQ8haOwqDI5T706cM36DddcvKENeziM6oIrvxbjEux7tMCAWmdGJtv1zyJoQ'
client = Client(api_key,api_secret)
client.API_URL = 'https://testnet.binance.vision/api'
info = client.get_account()
df = client.get_historical_klines("ETHUSDT",Client.KLINE_INTERVAL_1HOUR,"1 Jan, 2020","09 Mar, 2021")
df = pd.DataFrame(df, columns=['OpenTime','Open','High','Low','Close','Volume','CloseTime','QuoteAssetVolume','NumbTrade','TakerBuybase','TakerBuyQuote','Ignore'])
btc_price = {'error':False}

def btc_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    if msg['e'] != 'error':
        print(msg['c'])
        btc_price['last'] = msg['c']
        btc_price['bid'] = msg['b']
        btc_price['last'] = msg['a']
    else:
        btc_price['error'] = True

bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_trade_history)
bsm.start()
bsm.end()

bsm.stop_socket(conn_key)

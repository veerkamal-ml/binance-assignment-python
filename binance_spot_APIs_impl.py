#import libraries request for creating request
#panda for dataframe APIs
# prometheus for prometheus martrix foramt for ts database

import pandas as pd
import requests
from prometheus_client import start_http_server, Gauge
import time


class BinancePythonClient:
    BASE_URL = 'https://api.binance.com/api'

    def __init__(self):
        self.BASE_URL = self.BASE_URL
        self.prom_gauge = Gauge('absolute_delta_value',
                                'Absolute Delta Value of Price Spread', ['symbol'])

    def health_check(self):
        """Test Binance API status"""
        spot_api_uri = "/v3/ping"

        r = requests.get(self.BASE_URL + spot_api_uri)

        if r.status_code != 200:
            raise Exception("Spot API not reachable.")


    # Return the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order in data frames.

    def get_top_five_symbols(self, asset, field, output=False):

        spot_api_uri = "/v3/ticker/24hr"

        r = requests.get(self.BASE_URL + spot_api_uri)
        df = pd.DataFrame(r.json())
        df = df[['symbol', field]]
        df = df[df.symbol.str.contains(r'(?!$){}$'.format(asset))]
        df[field] = pd.to_numeric(df[field], downcast='float', errors='coerce')
        df = df.sort_values(by=[field], ascending=False).head(5)

        if output:
            print("\n Top Symbols for %s by %s" % (asset, field))
            print(df)

        return df


    """ the total notional value of the top 200 bids-and-asks currently on each order book """
    def top_get_notional_value(self, asset, field, output=False):

        spot_api_uri = "/v3/depth"

        symbols = self.get_top_five_symbols(asset, field, output=False)
        notional_list = {}

        for s in symbols['symbol']:
            payload = {'symbol': s, 'limit': 500}
            r = requests.get(self.BASE_URL + spot_api_uri, params=payload)
            for col in ["bids", "asks"]:
                df = pd.DataFrame(data=r.json()[col], columns=["price", "quantity"], dtype=float)
                df = df.sort_values(by=['price'], ascending=False).head(200)
                df['notional'] = df['price'] * df['quantity']
                df['notional'].sum()
                notional_list[s + '_' + col] = df['notional'].sum()

        if output:
            print("\n Total Notional value of %s by %s" % (asset, field))
            print(notional_list)

        return notional_list


    """ price spread for each of the symbols from Q2 """
    def get_price_spread_from_q2(self, asset, field, output=False):

        spot_api_uri = '/v3/ticker/bookTicker'

        symbols = self.get_top_five_symbols(asset, field)
        spread_list = {}

        for s in symbols['symbol']:
            payload = {'symbol': s}
            r = requests.get(self.BASE_URL + spot_api_uri, params=payload)
            price_spread = r.json()
            spread_list[s] = float(price_spread['askPrice']) - float(price_spread['bidPrice'])

        if output:
            print("\n Price Spread for %s by %s" % (asset, field))
            print(spread_list)

        return spread_list

    def get_spread_delta(self, asset, field, output=False):

        delta = {}
        old_spread = self.get_price_spread_from_q2(asset, field)
        time.sleep(10)
        new_spread = self.get_price_spread_from_q2(asset, field)

        for key in old_spread:
            delta[key] = abs(old_spread[key] - new_spread[key])

        for key in delta:
            self.prom_gauge.labels(key).set(delta[key])

        if output:
            print("\n Absolute Delta for %s" % asset)
            print(delta)


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8080)
    client = BinancePythonClient()
    client.health_check()

    # To Print Details
    client.get_top_five_symbols('BTC', 'volume', True)
    client.get_top_five_symbols('USDT', 'count', True)
    client.top_get_notional_value('BTC', 'volume', True)
    client.get_price_spread_from_q2('USDT', 'count', True)

    while True:
        client.get_spread_delta('USDT', 'count', True)

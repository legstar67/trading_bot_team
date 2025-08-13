import requests
from enum import Enum
import hashlib
import hmac
import time
import urllib.parse

class ApiBroker:
    def __init__(self, api_key: str, api_secret: str, endpoints: dict):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoints = endpoints


    
    def __send_simple_request__(self, method: str,url : str, endpoint: str, params: dict = None):
        """Send a request to the API to get the price

        Args:
            method (str): _description_
            url (str): _description_
            endpoint (str): _description_
            params (dict, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        url = f"{url}{endpoint}"
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        #debug
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Params: {params}")
        response = requests.request(method, url, headers=headers, params=params)
        return response.json()


    def get_price(self, pair: str):
        
        endpoint = self.endpoints[Endpt_name.Get_price_pair]#"/futures/data/delivery-price"
        url = self.endpoints[Endpt_name.URL]
        params = {"symbol": pair}
        return self.__send_simple_request__("GET",url, endpoint, params)

    def get_data_interval_pair(self, pair:str,  interval = "1d",    ):
        """Get data for a specific pair and interval
        Args:
            pair (str): The trading pair to get data for
            interval (str, optional): The interval for the data. Defaults to "1d".
        Raises:
            ValueError: If the interval is not valid
        Returns:
            dict: The data for the pair and interval
        """
        interval_available = ['1s', '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
        endpoint = self.endpoints[Endpt_name.Get_data_interval_pair]
        if interval not in interval_available:
            raise ValueError(f"Invalid interval: {interval}. Available intervals: {interval_available}")

        url = self.endpoints[Endpt_name.URL]
        params = {"symbol": pair,
                  "interval": interval,
                  "limit": 1,
                  "timeZone" : "02:00",
                  "startTime" : None,
                  "endTime" : None} #what is this ? 
        response = self.__send_simple_request__("GET", url, endpoint, params)
        return {"open_time" : response[0][0],
                "open_price" : response[0][1],
                "high_price" : response[0][2],
                "low_price" : response[0][3],
                "close_price" : response[0][4],
                "volume" : response[0][5],
                "close_time" : response[0][6],
                "quote_asset_volume" : response[0][7],
                "number_trades" : response[0][8],
                "taker_buy_base_asset_volume" : response[0][9],
                "taker_buy_quote_asset_volume" : response[0][10]}


    def create_order_spot(self, symbol: str,
                            side: str,
                            type : str, 
                            quantity: float, 
                            price: float):
        # check if enough ressources to place the order TODO
        #pass

        # place the order 
        params = {
            "symbol" : symbol,
            "side" : side, #"BUY" or "SELL"
            "type" : type, # "LIMIT" "MARKET" "STOP_LOSS" "STOP_LOSS_LIMIT" "TAKE_PROFIT" "TAKE_PROFIT_LIMIT" "LIMIT_MAKER"
            "timeInForce": None,  # ENUM, optional
            "quantity": quantity,     # DECIMAL, optional
            "quoteOrderQty": None, # DECIMAL, optional
            "price": price,        # DECIMAL, optional
            "newClientOrderId": None, # STRING, optional
            "strategyId": None,   # LONG, optional
            "strategyType": None, # INT, optional
            "stopPrice": None,    # DECIMAL, optional
            "trailingDelta": None, # LONG, optional
            "icebergQty": None,   # DECIMAL, optional
            "newOrderRespType": None, # ENUM, optional (ACK, RESULT, FULL)
            "selfTradePreventionMode": None, # ENUM, optional
            "recvWindow": None,   # LONG, optional, <= 60000
            "timestamp": int(time.time()) # mandatory, LONG
        }


    def get_account_info(self):
        # Implementation for getting account information
        pass

    def __get_signature__(self, params):

        query_string = urllib.parse.urlencode(params)

        signature = hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        return signature
    

    def __send_request_with_signature__(self, method: str,url : str, endpoint: str, params: dict = None):


        signature = self.__get_signature__(params)
        new_params = params.copy()
        new_params["signature"] = signature

        response = self.__send_simple_request__(method, url=url, endpoint=endpoint,params=new_params)
        return response


    def get_info_account(self):
        endpoint = self.endpoints[Endpt_name.Get_account_info]
        url = self.endpoints[Endpt_name.URL]
        params = {
            "timestamp": self.__get_local_time__(),
        }
        response = self.__send_request_with_signature__("GET", url, endpoint, params)
        return response

    def get_time_server(self):
        endpoint = self.endpoints[Endpt_name.Get_time_server]
        url = self.endpoints[Endpt_name.URL]
        # params = {
        #     "timestamp": int(time.time()),
        # }
        response = self.__send_simple_request__("GET", url, endpoint)
        return response
    def __get_local_time__(self):
        return int(time.time()*1000)

class Endpt_name(Enum):
    URL = "url" 
    Get_price_pair = "get_price_pair"
    Get_account_info = "get_account_info"
    Create_order = "create_order"
    Get_data_interval_pair = "get_price_change24h_pair"
    Create_order_test = "create_order_test"
    Get_time_server = "get_time_server"

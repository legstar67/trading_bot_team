import requests
from enum import Enum
import hashlib
import hmac
import time
import urllib.parse

#choose to not take care of the rate limit, as on binance it's large enough. Can be added later if needed.
class ApiBroker:
    def __init__(self, api_key: str, api_secret: str, endpoints: dict):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoints = endpoints


    
    def _send_simple_request(self, method: str,url : str, endpoint: str, params: dict = None):
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
        """Get the current price of a trading pair
        Args:
            pair (str): The trading pair to get the price for, e.g., "BTCUSDT"
        Returns:
            dict: A dictionary containing the price information
        Raises:
            ValueError: If the pair is not valid or not found
        """
        
        endpoint = self.endpoints[Endpt_name.Get_price_pair]#"/futures/data/delivery-price"
        url = self.endpoints[Endpt_name.URL]
        params = {"symbol": pair}
        return self._send_simple_request("GET",url, endpoint, params)

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
        response = self._send_simple_request("GET", url, endpoint, params)
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
        endpoint = self.endpoints[Endpt_name.Create_order_spot]
        url = self.endpoints[Endpt_name.URL]
        response = self._send_request_with_signature("POST", url, endpoint, params)
        return response

    def create_order_futures(self, symbol: str, side : str, positionside : str, type: str, timeInForce: str, quantity: float, reducedOnly: str, price: float, orderID: str,
                             stopPrice: float = None, closePosition: str = None, activationPrice: float = None, callbackRate: float = None,
                             workingType: str = None, priceProtect: str = None, newOrderRespType: str = None, priceMatch: str = None,
                             selfTradePreventionMode: str = None, goodTillDate: int = None, recvWindow: int = None):
        """Create a futures order on the exchange.
        Args:
            symbol (str): The trading pair symbol, e.g., "BTCUSDT".
            side (str): "BUY" or "SELL".
            positionSide (str): "BOTH", "LONG", or "SHORT". Required for Hedge Mode.
            type (str): Order type, e.g., "LIMIT", "MARKET", "STOP", etc.
            timeInForce (str): Time in force, e.g., "GTC", "IOC", etc.
            quantity (float): Quantity of the asset to trade.
            reducedOnly (str): "true" or "false". Default is "false".
            price (float): Price for LIMIT orders.
            orderID (str): A unique ID for the order.
            stopPrice (float, optional): Used with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders.
            closePosition (str, optional): "true" or "false". Close-All position.
            activationPrice (float, optional): Used with TRAILING_STOP_MARKET orders.
            callbackRate (float, optional): Used with TRAILING_STOP_MARKET orders.
            workingType (str, optional): "MARK_PRICE" or "CONTRACT_PRICE". Default is "CONTRACT_PRICE".
            priceProtect (str, optional): "TRUE" or "FALSE". Default is "FALSE".
            newOrderRespType (str, optional): "ACK" or "RESULT". Default is "ACK".
            priceMatch (str, optional): Matching strategy for the order.
            selfTradePreventionMode (str, optional): Self-trade prevention mode.
            goodTillDate (int, optional): Timestamp in ms for GTD orders.
            recvWindow (int, optional): The number of milliseconds after timestamp the request is valid for.
        Returns:
            dict: The response from the exchange containing order details.
        Raises:
            ValueError: If the provided parameters are invalid.
        Docs: 
            https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api
        """
        params = {
                    "symbol": symbol,
                    "side": side,                   # Mandatory: "BUY" or "SELL"
                    "positionSide": None,           # Optional: "BOTH", "LONG", "SHORT". Required for Hedge Mode. Default "BOTH".
                    "type": type,                   # Mandatory: e.g., "LIMIT", "MARKET", "STOP", "TAKE_PROFIT", etc.
                    "timeInForce": None,            # Optional: e.g., "GTC", "IOC", "FOK", "GTD"
                    "quantity": quantity,           # Optional: Cannot be sent with closePosition=true
                    "reduceOnly": None,             # Optional: "true" or "false". Default is "false".
                    "price": price,                 # Optional: Required for LIMIT orders.
                    "newClientOrderId": orderID,    # Optional: A unique ID for the order.
                    "stopPrice": None,              # Optional: Used with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders.
                    "closePosition": None,          # Optional: "true" or "false". Close-All position.
                    "activationPrice": None,        # Optional: Used with TRAILING_STOP_MARKET orders.
                    "callbackRate": None,           # Optional: Used with TRAILING_STOP_MARKET orders (e.g., 1 for 1%).
                    "workingType": None,            # Optional: "MARK_PRICE", "CONTRACT_PRICE". Default is "CONTRACT_PRICE".
                    "priceProtect": None,           # Optional: "TRUE" or "FALSE". Default is "FALSE".
                    "newOrderRespType": None,       # Optional: "ACK" or "RESULT". Default is "ACK".
                    "priceMatch": None,             # Optional: "OPPONENT", "QUEUE", etc. for specific order matching strategies.
                    "selfTradePreventionMode": None,# Optional: "EXPIRE_TAKER", "EXPIRE_MAKER", "EXPIRE_BOTH", "NONE". Default is "NONE".
                    "goodTillDate": None,           # Optional: Timestamp in ms for GTD orders.
                    "recvWindow": None,             # Optional: The number of milliseconds after timestamp the request is valid for.
                    "timestamp": self._get_local_time()# Mandatory: Current server time in milliseconds.
                }
        endpoint = self.endpoints[Endpt_name.Create_order_futures]
        url = self.endpoints[Endpt_name.URL]
        response = self._send_request_with_signature("POST", url, endpoint, params)
        return response
            


    def get_account_info_futures(self):
        """Get account information for futures trading.
        Returns:
            dict: A dictionary containing account information for futures trading.
        Docs:
            https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Account-Information-V3
        """
        endpoint = self.endpoints[Endpt_name.Get_account_info_futures]
        url = self.endpoints[Endpt_name.URL]
        params = {
            "timestamp": self._get_local_time(),
        }
        response = self._send_request_with_signature("GET", url, endpoint, params)
        return response

    def _get_signature(self, params):

        query_string = urllib.parse.urlencode(params)

        signature = hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        return signature
    
    def _send_request_with_signature(self, method: str,url : str, endpoint: str, params: dict = None):


        signature = self._get_signature(params)
        new_params = params.copy()
        new_params["signature"] = signature

        response = self._send_simple_request(method, url=url, endpoint=endpoint,params=new_params)
        return response


    def get_info_account(self):
        endpoint = self.endpoints[Endpt_name.Get_account_info]
        url = self.endpoints[Endpt_name.URL]
        params = {
            "timestamp": self._get_local_time(),
        }
        response = self._send_request_with_signature("GET", url, endpoint, params)
        return response

    def get_time_server(self):
        endpoint = self.endpoints[Endpt_name.Get_time_server]
        url = self.endpoints[Endpt_name.URL]
        # params = {
        #     "timestamp": int(time.time()),
        # }
        response = self._send_simple_request("GET", url, endpoint)
        return response
    def _get_local_time(self):
        return int(time.time()*1000)

class Endpt_name(Enum):
    URL = "url" 
    Get_price_pair = "get_price_pair"
    Get_account_info = "get_account_info"
    Create_order_spot = "create_order_spot"
    Get_data_interval_pair = "get_price_change24h_pair"
    Create_order_test = "create_order_test"
    Get_time_server = "get_time_server"
    Create_order_futures = "create_order_futures"
    Get_account_info_futures = "get_account_info_futures"

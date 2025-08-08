import requests
from enum import Enum

class ApiBroker:
    def __init__(self, api_key: str, api_secret: str, endpoints: dict):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoints = endpoints



    def __send_request__(self, method: str,url : str, endpoint: str, params: dict = None):
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
        return self.__send_request__("GET",url, endpoint, params)

    def create_order(self, symbol: str, side: str, quantity: float, price: float):
        # Implementation for creating an order
        pass
    def get_account_info(self):
        # Implementation for getting account information
        pass






class Endpt_name(Enum):
    URL = "url" 
    Get_price_pair = "get_price_pair"
    Get_account_info = "get_account_info"
    Create_order = "create_order"
import os
from api_broker import ApiBroker
from api_broker import Endpt_name
import dotenv

dotenv.load_dotenv()
secret_key = os.getenv("SECRET_KEY")
api_key = os.getenv("API_KEY")

endpoints_Binance = {
    Endpt_name.URL : "https://api.binance.com",
    Endpt_name.Get_price_pair :"/api/v3/ticker/price", #"/fapi/v1/ticker/price" #"/futures/data/delivery-price",
    Endpt_name.Get_data_interval_pair: "/api/v3/klines",
    Endpt_name.Create_order_test: "/api/v3/order/test"

    # "get_account_info": "/v1/account",
    # "create_order": "/v1/order"
}   




endpoints_Binance_test = {
    Endpt_name.URL : "https://testnet.binance.vision/",
    Endpt_name.Get_price_pair :"/api/v3/ticker/price", #"/fapi/v1/ticker/price" #"/futures/data/delivery-price",
    Endpt_name.Get_data_interval_pair: "/api/v3/klines",
    Endpt_name.Create_order: "/api/v3/order/test"

    # "get_account_info": "/v1/account",
    # "create_order": "/v1/order"
}  


binanceApi = ApiBroker(secret_key, api_key, endpoints_Binance)


#print(binanceApi.get_price("BTCUSDT"))
print(binanceApi.get_data_interval_pair("BTCUSDT", "1h"))
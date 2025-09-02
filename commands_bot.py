import api_broker

async def send_futures_balance_assets(bot, channelId, apiBroker : api_broker.ApiBroker):
    response = await apiBroker.get_account_info_futures()
    paragraphs = [("Total", 
                  f"totalWalletBalance : {response['totalWalletBalance']}\n" + 
                  f"totalUnrealizedProfit : {response['totalUnrealizedProfit']}" + 
                  f"availableBalance : {response['availableBalance']}")]
    
    for asset in response['assets']:
        paragraphs.append((f"{asset['symbol']} : {asset['balance']}", f"walletBalance : {asset['walletBalance']}\n" +
                          f"unrealizedProfit : {asset['unrealizedProfit']}" + f"availableBalance : {asset['availableBalance']}"))
        

async def send_futures_positions(bot, channelId, apiBroker : api_broker.ApiBroker):
    response = await apiBroker.get_futures_positions()
    paragraphs = [("Total", 
                  f"totalWalletBalance : {response['totalWalletBalance']}\n" + 
                  f"totalUnrealizedProfit : {response['totalUnrealizedProfit']}" + 
                  f"availableBalance : {response['availableBalance']}")]

    for position in response['positions']:
        paragraphs.append((f"{position['symbol']} : {position['balance']}", f"walletBalance : {position['walletBalance']}\n" +
                          f"unrealizedProfit : {position['unrealizedProfit']}" + f"availableBalance : {position['availableBalance']}"))
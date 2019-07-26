from . import trading_client

trading_client.Client.authorize()

client = trading_client.Client()
client.main_menu()

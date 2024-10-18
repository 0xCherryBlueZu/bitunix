# Bitunix Python Client

An unofficial opensource Python client for interacting with the Bitunix cryptocurrency exchange API.

## Installation
You can install the BitUnix Client package using pip:
```bash
pip install bitunix
```

## Usage

```python
from bitunix import BitunixClient

# Initialize the client with your API key and secret
client = BitunixClient(api_key, api_secret)
    
# Get latest price for BTC/USDT
latest_price = client.get_latest_price("BTCUSDT")
print(f"Latest BTC/USDT price: {latest_price}")

# Get depth data for ETH/USDT with precision 4
depth_data = client.get_depth_data("ETHUSDT", 4)
print(f"ETH/USDT depth data: {depth_data}")

# Get 1-hour K-line data for BNB/USDT
kline_data = client.get_kline_data("BNBUSDT", "60")
print(f"BNB/USDT 1-hour K-line data: {kline_data}")

# Get all trading pairs
trading_pairs = client.get_trading_pairs()
print(f"Trading pairs: {trading_pairs}")

# Get rate data
rate_data = client.get_rate_data()
print(f"Rate data: {rate_data}")

# Get token data
token_data = client.get_token_data()
print(f"Token data: {token_data}")

# Get account balance
account_balance = client.get_account_balance()
print(f"Account balance: {account_balance}")

# Place an order
order = client.place_order(side=2, order_type=1, volume="0.001",price="30000", symbol="BTCUSDT")
print(f"Placed order: {order}")

# Place batch orders
batch_orders = client.place_batch_orders([
    {"side": 2, "type": 1, "volume": "0.001", "price": "30000", "symbol": "BTCUSDT"},
    {"side": 1, "type": 1, "volume": "0.1", "price": "2000", "symbol": "ETHUSDT"}
])
print(f"Placed batch orders: {batch_orders}")

# Cancel orders
cancel_result = client.cancel_orders([
    {"orderId": "123456", "symbol": "BTCUSDT"},
    {"orderId": "789012", "symbol": "ETHUSDT"}
])
print(f"Cancelled orders: {cancel_result}")

# Query matching orders
matching_orders = client.query_matching_orders(order_id="123456",symbol="BTCUSDT")
print(f"Matching orders: {matching_orders}")

# Query order history
order_history = client.query_order_history(symbol="BTCUSDT", page=1,page_size=10)
print(f"Order history: {order_history}")

# Query current orders
current_orders = client.query_current_orders(symbol="BTCUSDT")
print(f"Current orders: {current_orders}")


```

## Documentation

For more details, please refer to the [Bitunix API documentation](https://api-doc.bitunix.com/en_us/).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Support the author of this project project:
ETH:  
0xefFC273c7452B6A7753B757333FCF7022785d44E

SOL:  
3FdyCqV7rebU4zJXwQ6vfb9TVkPs25y64NDkAQdSLFf6



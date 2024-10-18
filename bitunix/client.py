import requests
import hashlib
import base64
import json
import time
from typing import Dict, Any, List
from urllib.parse import urlencode
import secrets

class BitunixClient:
    """
    A client for interacting with the BitUnix cryptocurrency exchange API.

    This class provides methods for various API endpoints, including market data retrieval,
    account information, and trading operations. It handles authentication and request
    signing for secure API interactions.

    Attributes:
        api_key (str): The API key for authentication.
        api_secret (str): The API secret for request signing.
        session (requests.Session): A session object for making HTTP requests.

    Methods:
        Market Data:
            get_latest_price(symbol: str) -> Dict[str, Any]
            get_depth_data(symbol: str, precision: int) -> Dict[str, Any]
            get_kline_data(symbol: str, interval: str) -> Dict[str, Any]
            get_trading_pairs() -> Dict[str, Any]
            get_rate_data() -> Dict[str, Any]
            get_token_data() -> Dict[str, Any]

        Account Information:
            get_account_balance() -> Dict[str, Any]

        Trading Operations:
            place_order(side: int, order_type: int, volume: str, price: str, symbol: str) -> Dict[str, Any]
            place_batch_orders(order_list: List[Dict[str, Any]]) -> Dict[str, Any]
            cancel_orders(order_id_list: List[Dict[str, str]]) -> Dict[str, Any]
            query_matching_orders(order_id: str, symbol: str) -> Dict[str, Any]
            query_order_history(symbol: str, ...) -> Dict[str, Any]
            query_current_orders(symbol: str) -> Dict[str, Any]

    Usage:
        client = BitUnixClient(api_key, api_secret)
        latest_price = client.get_latest_price("BTCUSDT")
    """

    BASE_URL = "https://openapi.bitunix.com"

    def __init__(self, api_key, api_secret):
        """
        Initialize the BitUnixClient.

        :param api_key: The API key for authentication
        :param api_secret: The API secret for request signing
        :raises ValueError: If API key or secret is not provided
        """
        if not api_key or not api_secret:
            raise ValueError("API key and secret must be provided")
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()

    def sign_request(self, nonce: str, timestamp: str, 
                     query_params: Dict[str, Any] = None, 
                     body: Dict[str, Any] = None) -> str:
        """
        Generate a signature for BitUnix API requests.

        :param nonce: Random string (32 bits)
        :param timestamp: Current timestamp in milliseconds
        :param query_params: Query parameters
        :param body: Request body
        :return: The generated signature
        """
        query_string = urlencode(sorted(query_params.items())) if query_params else ""
        body_string = json.dumps(body, separators=(',', ':')) if body else ""
        message = f"{nonce}{timestamp}{self.api_key}{query_string}{body_string}"

        # First SHA256 encryption
        digest = hashlib.sha256(message.encode()).hexdigest()

        # Second SHA256 encryption
        sign = hashlib.sha256((digest + self.api_secret).encode()).hexdigest()

        return sign

    def _get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Helper method to make GET requests.

        :param endpoint: API endpoint to call
        :param params: Query parameters for the request
        :return: JSON response from the API
        """
        response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_latest_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get the latest price for a trading pair.

        :param symbol: Trading pair symbol
        :return: Latest price data
        """
        endpoint = "/api/spot/v1/market/last_price"
        params = {"symbol": symbol}
        return self._get(endpoint, params)

    def get_depth_data(self, symbol: str, precision: int) -> Dict[str, Any]:
        """
        Get depth data for a trading pair.

        :param symbol: Trading pair symbol
        :param precision: Token precision
        :return: Depth data
        """
        endpoint = "/api/spot/v1/market/depth"
        params = {"symbol": symbol, "precision": precision}
        return self._get(endpoint, params)

    def get_kline_data(self, symbol: str, interval: str) -> Dict[str, Any]:
        """
        Get K-Line data for a trading pair.

        :param symbol: Trading pair symbol
        :param interval: K-line interval (1,3,5,15,30,60,120,240,360,720,D,M,W)
        :return: K-Line data
        """
        endpoint = "/api/spot/v1/market/kline"
        params = {"symbol": symbol, "interval": interval}
        return self._get(endpoint, params)

    def get_trading_pairs(self) -> Dict[str, Any]:
        """
        Query trading pair data.

        :return: List of trading pairs and their details
        """
        endpoint = "/api/spot/v1/common/coin_pair/list"
        return self._get(endpoint)

    def get_rate_data(self) -> Dict[str, Any]:
        """
        Query rate data.

        :return: List of rate data
        """
        endpoint = "/api/spot/v1/common/rate/list"
        return self._get(endpoint)

    def get_token_data(self) -> Dict[str, Any]:
        """
        Query token data.

        :return: List of tokens and their details
        """
        endpoint = "/api/spot/v1/common/coin/coin_network/list"
        return self._get(endpoint)

    def _get_authenticated(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Helper method to make authenticated GET requests.

        :param endpoint: API endpoint to call
        :param params: Query parameters for the request
        :return: JSON response from the API
        """
        timestamp = str(int(time.time() * 1000))
        nonce = self._generate_nonce()
        
        headers = {
            "api-key": self.api_key,  
            "timestamp": timestamp,   
            "nonce": nonce,           
        }
        
        query_string = urlencode(sorted(params.items())) if params else ""
        signature = self.sign_request(nonce, timestamp, query_params=params)
        headers["sign"] = signature  

        response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_account_balance(self) -> Dict[str, Any]:
        """
        Query account balance.

        :return: Account balance information
        """
        endpoint = "/api/spot/v1/user/account"
        return self._get_authenticated(endpoint)

    def _generate_nonce(self) -> str:
        """
        Generate a nonce for API requests.

        :return: A string of 32 random bytes
        """
        random_bytes = secrets.token_bytes(32)
        return base64.b64encode(random_bytes).decode('utf-8')
    
    def _post_authenticated(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Helper method to make authenticated POST requests.

        :param endpoint: API endpoint to call
        :param data: Request body data
        :return: JSON response from the API
        """
        timestamp = str(int(time.time() * 1000))
        nonce = self._generate_nonce()
        
        headers = {
            "X-BX-APIKEY": self.api_key,
            "X-BX-TIMESTAMP": timestamp,
            "X-BX-NONCE": nonce,
        }
        
        signature = self.sign_request(nonce, timestamp, body=data)
        headers["X-BX-SIGN"] = signature

        response = self.session.post(f"{self.BASE_URL}{endpoint}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def place_order(self, side: int, order_type: int, volume: str, price: str, symbol: str) -> Dict[str, Any]:
        """
        Place an order.

        :param side: Side (1 Sell, 2 Buy)
        :param order_type: Order Type (1: Limit, 2: Market)
        :param volume: Amount
        :param price: Price
        :param symbol: Trading pair
        :return: Order details
        """
        endpoint = "/api/spot/v1/order/place_order"
        data = {
            "side": side,
            "type": order_type,
            "volume": volume,
            "price": price,
            "symbol": symbol
        }
        return self._post_authenticated(endpoint, data)

    def place_batch_orders(self, order_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Place batch orders.

        :param order_list: List of orders to place
        :return: Batch order details
        """
        endpoint = "/api/spot/v1/order/place_order/batch"
        data = {"orderList": order_list}
        return self._post_authenticated(endpoint, data)

    def cancel_orders(self, order_id_list: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Cancel orders.

        :param order_id_list: List of orders to cancel
        :return: Cancellation result
        """
        endpoint = "/api/spot/v1/order/cancel"
        data = {"orderIdList": order_id_list}
        return self._post_authenticated(endpoint, data)

    def query_matching_orders(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """
        Query matching orders.

        :param order_id: Order ID
        :param symbol: Trading Pair
        :return: Matching order details
        """
        endpoint = "/api/spot/v1/order/deal/list"
        data = {"orderId": order_id, "symbol": symbol}
        return self._post_authenticated(endpoint, data)

    def query_order_history(self, symbol: str, page: int = None, page_size: int = None,
                            start_time: str = None, end_time: str = None, status: str = None,
                            side: str = None, order_type: str = None) -> Dict[str, Any]:
        """
        Query order history.

        :param symbol: Trading pair
        :param page: Page number
        :param page_size: Display amount
        :param start_time: Order creation starting time (ISO8601)
        :param end_time: Order creation ending time (ISO8601)
        :param status: Order status
        :param side: Side (1 Sell, 2 Buy)
        :param order_type: Order type (1 Limit, 2 Market)
        :return: Order history details
        """
        endpoint = "/api/spot/v1/order/history/page"
        data = {"symbol": symbol}
        if page is not None:
            data["page"] = page
        if page_size is not None:
            data["pageSize"] = page_size
        if start_time is not None:
            data["startTime"] = start_time
        if end_time is not None:
            data["endTime"] = end_time
        if status is not None:
            data["status"] = status
        if side is not None:
            data["side"] = side
        if order_type is not None:
            data["type"] = order_type
        return self._post_authenticated(endpoint, data)

    def query_current_orders(self, symbol: str) -> Dict[str, Any]:
        """
        Query current orders.

        :param symbol: Trading pair
        :return: Current order details
        """
        endpoint = "/api/spot/v1/order/pending/list"
        data = {"symbol": symbol}
        return self._post_authenticated(endpoint, data)


from typing import Dict, Any, Optional, List
from binance.exceptions import BinanceAPIException
from logger import setup_logger

logger = setup_logger(__name__)


class OrderManager:
    """Handles all order-related operations"""
    
    def __init__(self, client):
        self.client = client
        logger.info("OrderManager initialized")
    
    def _validate_params(self, symbol: str, side: str, quantity: float):
        """Validate basic order parameters"""
        if not symbol:
            raise ValueError("Symbol is required")
        
        if side.upper() not in ['BUY', 'SELL']:
            raise ValueError("Side must be 'BUY' or 'SELL'")
        
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """
        Place a market order
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Amount to trade
            
        Returns:
            Order response dictionary
        """
        symbol = symbol.upper()
        side = side.upper()
        self._validate_params(symbol, side, quantity)
        
        try:
            logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            logger.info(f"✓ Market order executed - Order ID: {order['orderId']}")
            logger.debug(f"Order details: {order}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"✗ Market order failed: {e}")
            raise
        except Exception as e:
            logger.error(f"✗ Unexpected error: {e}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, 
                         price: float, time_in_force: str = 'GTC') -> Dict[str, Any]:
        """
        Place a limit order
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Amount to trade
            price: Limit price
            time_in_force: Time in force (GTC, IOC, FOK)
            
        Returns:
            Order response dictionary
        """
        symbol = symbol.upper()
        side = side.upper()
        self._validate_params(symbol, side, quantity)
        
        if price <= 0:
            raise ValueError("Price must be positive")
        
        try:
            logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ ${price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce=time_in_force
            )
            
            logger.info(f"✓ Limit order placed - Order ID: {order['orderId']}")
            logger.debug(f"Order details: {order}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"✗ Limit order failed: {e}")
            raise
        except Exception as e:
            logger.error(f"✗ Unexpected error: {e}")
            raise
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float,
                              stop_price: float, limit_price: float,
                              time_in_force: str = 'GTC') -> Dict[str, Any]:
        """
        Place a stop-limit order
        
        Args:
            symbol: Trading pair
            side: 'BUY' or 'SELL'
            quantity: Amount to trade
            stop_price: Stop trigger price
            limit_price: Limit price after stop is triggered
            time_in_force: Time in force
            
        Returns:
            Order response dictionary
        """
        symbol = symbol.upper()
        side = side.upper()
        self._validate_params(symbol, side, quantity)
        
        if stop_price <= 0 or limit_price <= 0:
            raise ValueError("Stop price and limit price must be positive")
        
        try:
            logger.info(f"Placing STOP-LIMIT order: {side} {quantity} {symbol}")
            logger.info(f"  Stop Price: ${stop_price}, Limit Price: ${limit_price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price,
                timeInForce=time_in_force
            )
            
            logger.info(f"✓ Stop-limit order placed - Order ID: {order['orderId']}")
            logger.debug(f"Order details: {order}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"✗ Stop-limit order failed: {e}")
            raise
        except Exception as e:
            logger.error(f"✗ Unexpected error: {e}")
            raise
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all open orders
        
        Args:
            symbol: Optional symbol to filter by
            
        Returns:
            List of open orders
        """
        try:
            if symbol:
                symbol = symbol.upper()
            
            orders = self.client.futures_get_open_orders(symbol=symbol)
            logger.info(f"Retrieved {len(orders)} open order(s)")
            
            return orders
            
        except BinanceAPIException as e:
            logger.error(f"Failed to get open orders: {e}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an open order
        
        Args:
            symbol: Trading pair
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
        """
        try:
            symbol = symbol.upper()
            logger.info(f"Cancelling order {order_id} for {symbol}")
            
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.info(f"✓ Order {order_id} cancelled")
            return result
            
        except BinanceAPIException as e:
            logger.error(f"✗ Cancel order failed: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get status of a specific order
        
        Args:
            symbol: Trading pair
            order_id: Order ID
            
        Returns:
            Order status information
        """
        try:
            symbol = symbol.upper()
            order = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.info(f"Order {order_id} status: {order['status']}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Failed to get order status: {e}")
            raise
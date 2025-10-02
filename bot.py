from typing import Optional, Dict, Any, List
from binance.client import Client
from binance.exceptions import BinanceAPIException
from config import Config
from orders import OrderManager
from logger import setup_logger

logger = setup_logger(__name__)


class TradingBot:
    """Main trading bot class"""
    
    def __init__(self):
        """Initialize the trading bot"""
        logger.info("=" * 60)
        logger.info("Initializing Binance Futures Trading Bot")
        logger.info("=" * 60)
        
        # Initialize Binance client
        if Config.USE_TESTNET:
            self.client = Client(Config.API_KEY, Config.API_SECRET, testnet=True)
            self.client.API_URL = Config.TESTNET_URL
            logger.info("Bot initialized in TESTNET mode")
        else:
            self.client = Client(Config.API_KEY, Config.API_SECRET)
            logger.info("Bot initialized in LIVE mode")
        
        # Initialize order manager
        self.order_manager = OrderManager(self.client)
        
        # Validate connection
        self._validate_connection()
    
    def _validate_connection(self) -> bool:
        """Validate API connection and credentials"""
        try:
            account = self.client.futures_account()
            balance = account.get('totalWalletBalance', 'N/A')
            
            logger.info("✓ Connection validated successfully")
            logger.info(f"✓ Account Balance: {balance} USDT")
            logger.info("=" * 60)
            
            return True
            
        except BinanceAPIException as e:
            logger.error(f"✗ API Connection failed: {e}")
            raise
        except Exception as e:
            logger.error(f"✗ Unexpected error during validation: {e}")
            raise
    
    # Account Information Methods
    def get_account_balance(self) -> List[Dict[str, Any]]:
        """Get account balance information"""
        try:
            balance = self.client.futures_account_balance()
            logger.debug(f"Retrieved account balance")
            return balance
        except BinanceAPIException as e:
            logger.error(f"Error fetching balance: {e}")
            raise
    
    def get_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get position information"""
        try:
            if symbol:
                symbol = symbol.upper()
            
            positions = self.client.futures_position_information(symbol=symbol)
            logger.debug(f"Retrieved position information")
            return positions
            
        except BinanceAPIException as e:
            logger.error(f"Error fetching positions: {e}")
            raise
    
    def set_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """
        Set leverage for a symbol
        
        Args:
            symbol: Trading pair
            leverage: Leverage value (1-125)
            
        Returns:
            Leverage change response
        """
        try:
            symbol = symbol.upper()
            logger.info(f"Setting leverage to {leverage}x for {symbol}")
            
            result = self.client.futures_change_leverage(
                symbol=symbol,
                leverage=leverage
            )
            
            logger.info(f"✓ Leverage set to {leverage}x for {symbol}")
            return result
            
        except BinanceAPIException as e:
            logger.error(f"Error setting leverage: {e}")
            raise
    
    def get_current_price(self, symbol: str) -> float:
        """
        Get current market price for a symbol
        
        Args:
            symbol: Trading pair
            
        Returns:
            Current price as float
        """
        try:
            symbol = symbol.upper()
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            
            logger.info(f"Current price for {symbol}: ${price:,.2f}")
            return price
            
        except BinanceAPIException as e:
            logger.error(f"Error fetching price: {e}")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get symbol information and trading rules"""
        try:
            symbol = symbol.upper()
            exchange_info = self.client.futures_exchange_info()
            
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    logger.debug(f"Retrieved info for {symbol}")
                    return s
            
            raise ValueError(f"Symbol {symbol} not found")
            
        except BinanceAPIException as e:
            logger.error(f"Error fetching symbol info: {e}")
            raise
    
    # Order Methods (delegated to OrderManager)
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """Place a market order"""
        return self.order_manager.place_market_order(symbol, side, quantity)
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, 
                         price: float) -> Dict[str, Any]:
        """Place a limit order"""
        return self.order_manager.place_limit_order(symbol, side, quantity, price)
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float,
                              stop_price: float, limit_price: float) -> Dict[str, Any]:
        """Place a stop-limit order"""
        return self.order_manager.place_stop_limit_order(
            symbol, side, quantity, stop_price, limit_price
        )
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get open orders"""
        return self.order_manager.get_open_orders(symbol)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Cancel an order"""
        return self.order_manager.cancel_order(symbol, order_id)
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Get order status"""
        return self.order_manager.get_order_status(symbol, order_id)
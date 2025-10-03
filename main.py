from src.bot import TradingBot
from logs.logger import setup_logger

logger = setup_logger(__name__)


def print_banner():
    """Print bot banner"""
    banner = """
    ╔════════════════════════════════════════════════╗
    ║   BINANCE FUTURES TRADING BOT - TESTNET        ║
    ║   Market | Limit | Stop-Limit Orders           ║
    ╚════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Print main menu"""
    menu = """
    ═══════════════════ MAIN MENU ═══════════════════
    
    [1] Place Market Order
    [2] Place Limit Order
    [3] Place Stop-Limit Order
    [4] View Open Orders
    [5] Cancel Order
    [6] Check Order Status
    [7] View Account Balance
    [8] View Positions
    [9] Set Leverage
    [10] Get Current Price
    [0] Exit
    
    ═════════════════════════════════════════════════
    """
    print(menu)


def get_user_input(prompt: str, input_type=str):
    """Get and validate user input"""
    while True:
        try:
            value = input(prompt)
            if value.strip().lower() == 'q':
                return None
            
            converted_value = input_type(value)
            return converted_value
            
        except ValueError:
            print(f"❌ Invalid input type. Expected {input_type.__name__}")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            return None


def main():
    """Main CLI interface"""
    print_banner()
    
    try:
        # Initialize bot (uses credentials from config.py)
        print("\n🔄 Initializing bot...")
        bot = TradingBot()
        print("✅ Bot initialized successfully!\n")
        
        while True:
            print_menu()
            choice = get_user_input("Select an option: ", int)
            
            if choice is None or choice == 0:
                print("\n👋 Goodbye!")
                break
            
            try:
                if choice == 1:  # Market Order
                    print("\n📊 MARKET ORDER")
                    symbol = get_user_input("Symbol (e.g., BTCUSDT): ").upper()
                    side = get_user_input("Side (BUY/SELL): ").upper()
                    quantity = get_user_input("Quantity: ", float)
                    
                    if None not in [symbol, side, quantity]:
                        order = bot.place_market_order(symbol, side, quantity)
                        print(f"\n✅ Order placed successfully!")
                        print(f"Order ID: {order['orderId']}")
                        print(f"Status: {order['status']}")
                        print(f"Executed Quantity: {order['executedQty']}")
                
                elif choice == 2:  # Limit Order
                    print("\n📊 LIMIT ORDER")
                    symbol = get_user_input("Symbol (e.g., BTCUSDT): ").upper()
                    side = get_user_input("Side (BUY/SELL): ").upper()
                    quantity = get_user_input("Quantity: ", float)
                    price = get_user_input("Limit Price: ", float)
                    
                    if None not in [symbol, side, quantity, price]:
                        order = bot.place_limit_order(symbol, side, quantity, price)
                        print(f"\n✅ Order placed successfully!")
                        print(f"Order ID: {order['orderId']}")
                        print(f"Status: {order['status']}")
                        print(f"Price: {order['price']}")
                
                elif choice == 3:  # Stop-Limit Order
                    print("\n📊 STOP-LIMIT ORDER")
                    symbol = get_user_input("Symbol (e.g., BTCUSDT): ").upper()
                    side = get_user_input("Side (BUY/SELL): ").upper()
                    quantity = get_user_input("Quantity: ", float)
                    stop_price = get_user_input("Stop Price: ", float)
                    limit_price = get_user_input("Limit Price: ", float)
                    
                    if None not in [symbol, side, quantity, stop_price, limit_price]:
                        order = bot.place_stop_limit_order(
                            symbol, side, quantity, stop_price, limit_price
                        )
                        print(f"\n✅ Order placed successfully!")
                        print(f"Order ID: {order['orderId']}")
                        print(f"Status: {order['status']}")
                        print(f"Stop Price: {stop_price}")
                        print(f"Limit Price: {limit_price}")
                
                elif choice == 4:  # View Open Orders
                    print("\n📋 OPEN ORDERS")
                    symbol = get_user_input("Symbol (press Enter for all): ")
                    if symbol:
                        symbol = symbol.upper()
                    else:
                        symbol = None
                    
                    orders = bot.get_open_orders(symbol)
                    
                    if orders:
                        print(f"\nFound {len(orders)} open order(s):\n")
                        for order in orders:
                            print(f"Order ID: {order['orderId']}")
                            print(f"Symbol: {order['symbol']}")
                            print(f"Side: {order['side']}")
                            print(f"Type: {order['type']}")
                            print(f"Price: {order['price']}")
                            print(f"Quantity: {order['origQty']}")
                            print(f"Status: {order['status']}")
                            print("-" * 50)
                    else:
                        print("\nNo open orders found")
                
                elif choice == 5:  # Cancel Order
                    print("\n❌ CANCEL ORDER")
                    symbol = get_user_input("Symbol: ").upper()
                    order_id = get_user_input("Order ID: ", int)
                    
                    if None not in [symbol, order_id]:
                        result = bot.cancel_order(symbol, order_id)
                        print(f"\n✅ Order {order_id} cancelled successfully!")
                
                elif choice == 6:  # Check Order Status
                    print("\n🔍 ORDER STATUS")
                    symbol = get_user_input("Symbol: ").upper()
                    order_id = get_user_input("Order ID: ", int)
                    
                    if None not in [symbol, order_id]:
                        order = bot.get_order_status(symbol, order_id)
                        print(f"\nOrder ID: {order['orderId']}")
                        print(f"Symbol: {order['symbol']}")
                        print(f"Status: {order['status']}")
                        print(f"Type: {order['type']}")
                        print(f"Side: {order['side']}")
                        print(f"Price: {order['price']}")
                        print(f"Executed Qty: {order['executedQty']}/{order['origQty']}")
                
                elif choice == 7:  # View Balance
                    print("\n💰 ACCOUNT BALANCE")
                    balance = bot.get_account_balance()
                    
                    print("\nAsset Balances:")
                    for asset in balance:
                        bal = float(asset['balance'])
                        if bal > 0:
                            print(f"{asset['asset']}: {bal}")
                
                elif choice == 8:  # View Positions
                    print("\n📍 OPEN POSITIONS")
                    positions = bot.get_positions()
                    
                    found_positions = False
                    for pos in positions:
                        if float(pos['positionAmt']) != 0:
                            found_positions = True
                            print(f"\nSymbol: {pos['symbol']}")
                            print(f"Position Amount: {pos['positionAmt']}")
                            print(f"Entry Price: ${pos['entryPrice']}")
                            print(f"Mark Price: ${pos['markPrice']}")
                            print(f"Unrealized PnL: ${pos['unrealizedProfit']}")
                            print(f"Leverage: {pos['leverage']}x")
                            print("-" * 50)
                    
                    if not found_positions:
                        print("\nNo open positions")
                
                elif choice == 9:  # Set Leverage
                    print("\n⚡ SET LEVERAGE")
                    symbol = get_user_input("Symbol: ").upper()
                    leverage = get_user_input("Leverage (1-125): ", int)
                    
                    if None not in [symbol, leverage]:
                        if 1 <= leverage <= 125:
                            bot.set_leverage(symbol, leverage)
                            print(f"\n✅ Leverage set to {leverage}x for {symbol}")
                        else:
                            print("\n❌ Leverage must be between 1 and 125")
                
                elif choice == 10:  # Get Price
                    print("\n💲 CURRENT PRICE")
                    symbol = get_user_input("Symbol: ").upper()
                    
                    if symbol:
                        price = bot.get_current_price(symbol)
                        print(f"\n{symbol}: ${price:,.2f}")
                
                else:
                    print("\n❌ Invalid option. Please try again.")
            
            except Exception as e:
                print(f"\n❌ Error: {e}")
                logger.error(f"Operation failed: {e}", exc_info=True)
            
            input("\nPress Enter to continue...")
    
    except Exception as e:
        print(f"\n❌ Bot initialization failed: {e}")
        logger.error(f"Initialization failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()
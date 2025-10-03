# Binance Futures Testnet Trading Bot

A simplified trading bot for Binance USDT-M Futures Testnet, built in Python.  
This project is part of the application task for the "Junior Python Developer – Crypto Trading Bot" position.

---

## Features

- **Market and Limit Orders:** Place buy/sell orders on Binance Futures Testnet (USDT-M).
- **Stop-Limit Orders:** (Bonus) Advanced order type supported.
- **Command-Line Interface:** Interactive CLI for order placement and account management.
- **Logging:** All API requests, responses, and errors are logged to `trading_bot.log`.
- **Error Handling:** Robust input validation and exception handling.
- **Modular Codebase:** Designed for reusability and clarity.

---

## Setup Instructions

### 1. Register on Binance Futures Testnet

- Sign up at [Binance Futures Testnet](https://testnet.binancefuture.com).
- Generate your API Key and Secret.

### 2. Clone the Repository

```sh
git clone <your-repo-url>
cd Binance-TestNet-Bot
```

### 3. Configure API Credentials

- Open [`config.py`](config.py).
- Replace `'Your API Key'` and `'Your API Secret'` with your DEMO Account API Key credentials.

```python
class Config:
    API_KEY = 'Your API Key'
    API_SECRET = 'Your API Secret'
    TESTNET_URL = 'https://testnet.binancefuture.com'
    USE_TESTNET = True
    # ...
```

### 4. Install Dependencies

```sh
pip install -r requirements.txt
```

### 5. Run the Bot

```sh
python main.py
```

---

## Usage

- Follow the CLI prompts to place market, limit, or stop-limit orders.
- View open orders, cancel orders, check order status, and manage account settings.
- All actions and errors are logged in [`trading_bot.log`](trading_bot.log).

---

## Project Structure

- [`main.py`](main.py): CLI entry point.
- [`bot.py`](bot.py): Main trading bot logic.
- [`orders.py`](orders.py): Order management (market, limit, stop-limit).
- [`config.py`](config.py): Configuration and credentials.
- [`logger.py`](logger.py): Logging setup.
- [`requirements.txt`](requirements.txt): Python dependencies.

---

## Example

```
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

Select an option: 1
Symbol (e.g., BTCUSDT): BTCUSDT
Side (BUY/SELL): BUY
Quantity: 0.001
```

---

## Logging

- All API requests, responses, and errors are logged to [`trading_bot.log`](trading_bot.log).
- Example log entry:
  ```
  2024-06-01 12:34:56 - INFO - Placing MARKET order: BUY 0.001 BTCUSDT
  ```

---

## Requirements

- Python 3.8+
- [`python-binance`](https://python-binance.readthedocs.io/en/latest/)
- Internet connection

---

## Bonus Features

- **Stop-Limit Orders:** Place advanced stop-limit orders via the CLI.
- **Extensible Design:** Easily add more order types (e.g., OCO, TWAP).
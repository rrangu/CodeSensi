

"""Simple Flask server providing a /get_stock endpoint that returns the current
price, change, and percent change for a given stock symbol using yfinance.

This module exposes a POST endpoint for use by a frontend, enabling cross-origin
requests (CORS) and returning JSON data. It uses yfinance to fetch the stock's
latest price and previous close to compute the change and change percentage.
"""

from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import yfinance as yf # type: ignore

app = Flask(__name__)
CORS(app)  # Enables the frontend to access this server

@app.route('/get_stock', methods=['POST'])
def get_stock():
    data = request.json
    symbol = data.get('symbol', 'AAPL')

    try:
        stock = yf.Ticker(symbol)

        # 'fast_info' is often faster than 'info' for current price
        current_price = stock.fast_info['last_price']
        previous_close = stock.fast_info['previous_close']

        # Calculate change
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100

        return jsonify({
            "symbol": symbol.upper(),
            "price": round(current_price, 2),
            "change": round(change, 2),
            "changePercent": round(change_percent, 2),
            # You can add more data here (market cap, volume, etc.)
        })

    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Stock not found"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)

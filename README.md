# Crypto Signal Tool

A professional Flask-based web application for real-time Bitcoin trading signals using RSI (14) and SMA (10/50) indicators. Features live price updates, dynamic charts, and auto-refresh functionality. Powered by CoinGecko API.

## Features
- **Trading Signals**: LONG (Buy), SHORT (Sell), or HOLD based on RSI overbought/oversold and SMA crossovers.
- **Live Data**: Current BTC/USD price and 24-hour price chart with Chart.js.
- **Indicators Display**: RSI, SMA10, and SMA50 values with tooltips.
- **UI Enhancements**: Glassmorphic design, icons (Font Awesome), responsive layout, loading spinners, and auto-refresh every 5 minutes.
- **Error Handling**: Graceful handling of API failures.
- **Modular Code**: Logic separated into utils for maintainability.

## Tech Stack
- Backend: Flask, pandas, ta (technical analysis library), requests.
- Frontend: Bootstrap 5, Chart.js, Font Awesome.
- Data Source: CoinGecko API (free tier).

## Setup Instructions
1. Clone or create the project folder: `mkdir crypto-signal-tool && cd crypto-signal-tool`
2. Create the folder structure:
   - `static/css`, `static/js`, `static/images`
   - `templates`
   - `utils`
3. Copy the provided files into their respective locations.
4. Install dependencies: `pip install -r requirements.txt`
5. (Optional) Add `static/images/btc-logo.png` for the Bitcoin icon.
6. Run the app: `python app.py`
7. Open in browser: http://127.0.0.1:5000/

## API Endpoints
- `/`: Main dashboard (renders index.html with initial signal).
- `/api/price`: Returns current BTC/USD price (JSON).
- `/chart-data`: Returns 24h chart data, signal, and indicators (JSON).

## Customization
- **Add More Cryptos**: Modify `utils/signals.py` to support other coins (e.g., Ethereum) by changing CoinGecko IDs.
- **Caching**: For production, add Flask-Caching to reduce API calls.
- **Deployment**: Use Gunicorn/NGINX for hosting (e.g., on Heroku or VPS).
- **Alerts**: Extend JS to add browser notifications for signal changes.

## Potential Improvements
- Integrate WebSockets for real-time updates (e.g., via Flask-SocketIO).
- Add user authentication for personalized signals.
- Backtesting module for historical data analysis.
- 
<img width="1060" height="318" alt="c2" src="https://github.com/user-attachments/assets/27bfaf98-6fd8-46a7-bf14-5ea4b508b711" />

<img width="1054" height="526" alt="c3" src="https://github.com/user-attachments/assets/f600803e-ab02-402a-bba4-1f3a283ed73f" />


Built with ❤️ by Zubair. For issues, check console logs or extend `utils/signals.py`. Contributions welcome!

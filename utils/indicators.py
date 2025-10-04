# Server-side: fetch market data from CoinGecko, compute EMA, RSI, and decide signal
import requests
import pandas as pd
import numpy as np
from time import time
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)

# Simple cache to avoid hitting API too often (seconds)
_CACHE_TTL = 25  # seconds
_last_fetch_time = 0
_last_result = None

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
DEFAULT_PARAMS = {"vs_currency": "usd", "days": "1"}  # Removed 'interval' – auto granularity

def _ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def _rsi(series, period=14):
    # Standard RSI with min_periods=1 for early values
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(window=period, min_periods=1).mean()
    ma_down = down.rolling(window=period, min_periods=1).mean()
    rs = ma_up / (ma_down + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def fetch_indicator_data():
    """
    Fetches market chart from CoinGecko, processes into JSON serializable structure,
    and computes signal using EMA9/EMA26 crossover + RSI filter.
    Uses a small in-memory TTL cache to reduce rate-limit issues.
    """
    global _last_fetch_time, _last_result

    now = time()
    if _last_result is not None and (now - _last_fetch_time) < _CACHE_TTL:
        logging.info("Using cached data")
        return _last_result

    try:
        logging.info("Fetching fresh data from CoinGecko...")
        resp = requests.get(COINGECKO_URL, params=DEFAULT_PARAMS, timeout=15)  # Increased timeout
        resp.raise_for_status()
        j = resp.json()
    except Exception as e:
        logging.error(f"API fetch error: {e}")
        # If API fails and we have an old result, return it with a warning
        if _last_result is not None:
            logging.warning("Returning cached data due to API error")
            return _last_result
        raise RuntimeError(f"Failed to fetch data from CoinGecko: {e}")

    prices = j.get("prices")
    if not prices:
        raise RuntimeError("API returned no price data")

    # Convert to DataFrame
    df = pd.DataFrame(prices, columns=["ts", "price"])
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["dt"] = pd.to_datetime(df["ts"], unit="ms")
    df.set_index("dt", inplace=True)

    # Optional: reduce to last 720 points to keep payload light
    if len(df) > 720:
        df = df.tail(720)

    # Indicators (full series for chart)
    df["ema9"] = _ema(df["price"], span=9)
    df["ema26"] = _ema(df["price"], span=26)
    df["rsi"] = _rsi(df["price"], period=14)

    latest = df.iloc[-1]
    price_now = float(latest["price"])
    ema9 = float(latest["ema9"])
    ema26 = float(latest["ema26"])
    rsi_now = float(latest["rsi"]) if not np.isnan(latest["rsi"]) else None

    # Signal logic: EMA crossover + RSI filter
    signal = "HOLD"
    if ema9 > ema26 and (rsi_now is None or rsi_now < 80):
        signal = "LONG"
    elif ema9 < ema26 and (rsi_now is None or rsi_now > 20):
        signal = "SHORT"
    else:
        signal = "HOLD"

    # Prepare labels (HH:MM) and prices
    labels = [dt.strftime("%H:%M") for dt in df.index]
    prices_list = [float(x) for x in df["price"].tolist()]

    # Full EMA series for chart lines
    ema9_list = [float(x) for x in df["ema9"].tolist()]
    ema26_list = [float(x) for x in df["ema26"].tolist()]

    result = {
        "signal": signal,
        "price": round(price_now, 2),  # Rounded for display
        "rsi": None if rsi_now is None else round(rsi_now, 2),
        "ema_short": round(ema9, 2),
        "ema_long": round(ema26, 2),
        "labels": labels,
        "prices": prices_list,
        "ema_short_series": ema9_list,  # For chart line
        "ema_long_series": ema26_list,  # For chart line
    }

    _last_fetch_time = now
    _last_result = result
    logging.info(f"Data ready: Signal={signal}, Price=${price_now}, Points={len(prices_list)}")
    return result
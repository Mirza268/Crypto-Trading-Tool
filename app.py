from flask import Flask, render_template, jsonify
from utils.indicators import fetch_indicator_data
import logging
from datetime import datetime

app = Flask(__name__, static_folder="static", template_folder="templates")

logging.basicConfig(level=logging.INFO)

# Sample Blog Posts (Professional Content – Add more later)
BLOGS = [
    {
        "slug": "crypto-basics-for-beginners",
        "title": "Crypto Basics for Beginners: From Bitcoin to Blockchain",
        "excerpt": "Understand the fundamentals of cryptocurrency, how blockchain works, and why Bitcoin is the king of crypto.",
        "date": "2025-10-01",
        "author": "Zubair Ahmed",
        "content": """
        <h2>Introduction to Crypto</h2>
        <p>Cryptocurrency has revolutionized finance since Bitcoin's launch in 2009. It's digital money secured by cryptography, running on decentralized networks like blockchain.</p>
        
        <h2>What is Blockchain?</h2>
        <p>Blockchain is a distributed ledger – think of it as a chain of blocks where each block contains transactions. No central authority, tamper-proof via consensus (e.g., Proof-of-Work).</p>
        
        <h3>Bitcoin: The Pioneer</h3>
        <p>Created by Satoshi Nakamoto, BTC is store of value. Current price ~$60K, market cap $1.2T. Use cases: Payments, hedging inflation.</p>
        
        <h2>Getting Started</h2>
        <ul>
            <li>Buy on exchanges like Binance/Coinbase.</li>
            <li>Store in wallets (hardware like Ledger for security).</li>
            <li>Start small – DYOR (Do Your Own Research).</li>
        </ul>
        
        <p>Pro Tip: Diversify – 60% BTC, 30% ETH, 10% alts.</p>
        
        <h2>Risks & Rewards</h2>
        <p>High volatility (20% swings daily), but 1000x returns possible. Regulate emotions with strategies like DCA (Dollar-Cost Averaging).</p>
        
        <p>Stay tuned for more – next: Trading Strategies!</p>
        """
    },
    {
        "slug": "ema-crossover-trading-strategy",
        "title": "EMA Crossover: A Simple Yet Powerful Trading Strategy",
        "excerpt": "Learn how Exponential Moving Average (EMA) crossovers can signal buy/sell in crypto markets – with real examples.",
        "date": "2025-10-03",
        "author": "Zubair Ahmed",
        "content": """
        <h2>What is EMA?</h2>
        <p>EMA gives more weight to recent prices than SMA. Formula: EMA = (Close * α) + (Previous EMA * (1-α)), where α = 2/(period+1).</p>
        
        <h2>Crossover Strategy</h2>
        <p>Use EMA9 (short) and EMA26 (long). When EMA9 crosses above EMA26 = Bullish (LONG). Below = Bearish (SHORT).</p>
        
        <h3>Example: BTC 2024 Rally</h3>
        <p>In March 2024, EMA9 crossed EMA26 at $45K – signalled 50% pump to $70K. RSI filter: Avoid if RSI >80 (overbought).</p>
        
        <h2>Implementation Tips</h2>
        <ul>
            <li>Timeframe: 1H/4H for swing trading.</li>
            <li>Stop-Loss: 5% below entry.</li>
            <li>Take-Profit: 2x risk-reward.</li>
        </ul>
        
        <p>Backtest on TradingView – 65% win rate in volatile markets.</p>
        
        <p>Try it in our Signal Tool – real-time EMA alerts!</p>
        """
    },
    {
        "slug": "risk-management-in-crypto-trading",
        "title": "Risk Management: The Key to Long-Term Trading Success",
        "excerpt": "Don't let emotions ruin your portfolio – master position sizing, stop-losses, and diversification in crypto.",
        "date": "2025-10-04",
        "author": "Zubair Ahmed",
        "content": """
        <h2>Why Risk Management Matters</h2>
        <p>90% traders lose money due to poor risk control. Crypto's 24/7 volatility amplifies mistakes.</p>
        
        <h2>Core Rules</h2>
        <ol>
            <li><strong>Position Sizing</strong>: Risk max 1-2% per trade. E.g., $10K portfolio = $100 risk max.</li>
            <li><strong>Stop-Loss</strong>: Always set – 5-10% below entry. Trailing stops for profits.</li>
            <li><strong>Diversification</strong>: No more than 5% in one altcoin. 70% BTC/ETH, 30% alts.</li>
        </ol>
        
        <h3>Tools</h3>
        <p>Use Kelly Criterion for sizing: f = (bp - q)/b, where b=odds, p=win prob, q=loss prob.</p>
        
        <h2>Psychological Tips</h2>
        <p>FOMO kills – journal trades. Take breaks after losses. Aim for 1% daily gains, not 100% overnight.</p>
        
        <p>Success Rate: Traders with RM survive 5+ years. Start with paper trading!</p>
        """
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/blogs")
def blogs():
    """Blog listing page"""
    return render_template("blogs.html", blogs=BLOGS)

@app.route("/blog/<slug>")
def blog_post(slug):
    """Single blog post"""
    post = next((p for p in BLOGS if p["slug"] == slug), None)
    if not post:
        return "Post not found", 404
    post["formatted_date"] = datetime.strptime(post["date"], "%Y-%m-%d").strftime("%B %d, %Y")
    return render_template("blog_post.html", post=post)

@app.route("/api/data")
def api_data():
    """
    Returns JSON with signal, price, indicators, and chart data.
    """
    try:
        data = fetch_indicator_data()
        return jsonify(data)
    except Exception as e:
        logging.exception("Error in /api/data")
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
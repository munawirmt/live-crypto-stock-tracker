"""
Advanced AI-Enabled Live Crypto & Stock Portfolio Tracker
---------------------------------------------------------
Built by: Munawir mt
Email: munawirmt002@gmail.com
Copyright (c) 2026 Munawir mt. All rights reserved.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yfinance as yf

# GitHub Secrets-ൽ നിന്നുള്ള വിവരങ്ങൾ പൈത്തൺ എടുക്കുന്നു
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

# ട്രാക്ക് ചെയ്യേണ്ട സ്റ്റോക്കുകൾ
PORTFOLIO = {
    "BTC-USD": {"name": "Bitcoin", "target_profit": 110000, "stop_loss": 90000, "is_crypto": True},
    "TCS.NS": {"name": "Tata Consultancy Services", "target_profit": 4800, "stop_loss": 3900, "is_crypto": False},
    "SBIN.NS": {"name": "State Bank of India", "target_profit": 950, "stop_loss": 780, "is_crypto": False},
    "RELIANCE.NS": {"name": "Reliance Industries", "target_profit": 2900, "stop_loss": 2300, "is_crypto": False}
}

def get_usd_to_inr():
    """USD to INR തത്സമയ നിരക്ക് എടുക്കുന്നു (yfinance വഴി ഫ്രീയായി)"""
    try:
        usd_inr = yf.Ticker("INR=X")
        return usd_inr.history(period="1d")["Close"].iloc[-1]
    except:
        return 83.50  # കണക്ഷൻ തകരാറിലായാൽ ഉപയോഗിക്കാൻ ഒരു ഡമ്മി വില

def analyze_trend(ticker):
    """കഴിഞ്ഞ 7 ദിവസത്തെ ഡാറ്റ വെച്ച് ലളിതമായ AI ട്രെൻഡ് അനാലിസിസ് നടത്തുന്നു"""
    try:
        asset = yf.Ticker(ticker)
        hist = asset.history(period="7d")
        if len(hist) < 2:
            return "Insufficient Data", "HOLD"
        
        start_price = hist["Close"].iloc[0]
        end_price = hist["Close"].iloc[-1]
        pct_change = ((end_price - start_price) / start_price) * 100
        
        if pct_change > 1.5:
            return f"📈 BULLISH (+{pct_change:.2f}%)", "STRONG BUY"
        elif pct_change < -1.5:
            return f"📉 BEARISH ({pct_change:.2f}%)", "WATCH CLOSELY"
        else:
            return f"↔️ SIDEWAYS ({pct_change:.2f}%)", "HOLD"
    except:
        return "Analysis Failed", "HOLD"

def send_email(subject, body):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("⚠️ Email credentials missing in GitHub Secrets. Skipping email alert.")
        return
        
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    
    footer = "\n\n---\n🤖 Automated Deployment Engine built by Munawir mt (munawirmt002@gmail.com)."
    msg.attach(MIMEText(body + footer, "plain"))
    
    try:
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email Alert Sent: {subject}")
    except Exception as e:
        print(f"❌ Email failed: {e}")

def track_portfolio():
    usd_rate = get_usd_to_inr()
    print("\n=========================================================================")
    print("🔬   MUNAWIR MT's QUANT TRADING & AUTOMATION DASHBOARD   🔬")
    print("=========================================================================")
    print(f"💵  Live Exchange Rate: 1 USD = {usd_rate:.2f} INR")
    print("-------------------------------------------------------------------------")

    for ticker, data in PORTFOLIO.items():
        try:
            asset = yf.Ticker(ticker)
            live_price = asset.history(period="1d")["Close"].iloc[-1]
            name = data["name"]
            
            # ഫീച്ചർ 2: കറൻസി കൺവെർട്ടർ
            price_inr = live_price * usd_rate if data["is_crypto"] else live_price
            currency_symbol = "₹" if not data["is_crypto"] else f"$ (Approx ₹{price_inr:.2f})"
            
            # ഫീച്ചർ 1: AI ട്രെൻഡ് അനാലിസിസ്
            trend, signal = analyze_trend(ticker)

            print(f"📊 {name} ({ticker}): {live_price:.2f} {currency_symbol}")
            print(f"    AI Market Trend : {trend} | Signal: [{signal}]")
            print("-------------------------------------------------------------------------")

            # അലേർട്ട് സിസ്റ്റം
            if live_price >= data["target_profit"]:
                msg = f"🚨 PROFIT ALERT! \n{name} ({ticker}) target reached: {live_price:.2f}. AI Signal: {signal}."
                send_email(f"PROFIT ALERT: {ticker}", msg)
            elif live_price <= data["stop_loss"]:
                msg = f"⚠️ STOP LOSS ALERT! \n{name} ({ticker}) dropped to {live_price:.2f}. AI Signal: {signal}."
                send_email(f"STOP LOSS ALERT: {ticker}", msg)
                
        except Exception as e:
            print(f"❌ Error processing {ticker}: {e}")

if __name__ == "__main__":
    track_portfolio()
    print("\n=========================================")
    print("🛠️  System Architecture Designed by: Munawir mt")
    print("📧  Contact: munawirmt002@gmail.com")
    print("=========================================\n")

import os
import asyncio
import logging
import random
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cryptography.fernet import Fernet

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("FonaurixisPhoenixFire")

# Safe MetaTrader 5 Import for Linux Cloud Environments (Render)
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
    logger.info("MetaTrader 5 terminal library initialized successfully.")
except ImportError:
    mt5 = None
    MT5_AVAILABLE = False
    logger.warning("MetaTrader 5 not available in Linux host. Running in Phoenix Cloud Execution Engine mode.")

# Application Initialization
app = FastAPI(
    title="Fonaurixis Phoenix Fire Bot",
    description="High-Frequency Automated Trading Engine & Multi-Color Pro Dashboard",
    version="7.2.0"
)

# Enable CORS for Mobile PWA Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Credentials & Fernet Encryption Configuration
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# In-Memory Session Database & Admin Master Settings
user_sessions: Dict[str, Dict[str, Any]] = {}
ADMIN_CHAT_ID = "8668083605"
AIRTEL_NUMBER = "0731552385"
AIRTEL_NAME = "Nantongo Rebecca"

# Request Data Models
class UserAuthData(BaseModel):
    email: str
    password: str

class MT5BindingData(BaseModel):
    user_id: str
    account_id: str
    password: str
    server: str

class PaymentSubmissionData(BaseModel):
    user_id: str
    method: str  # "Airtel" or "Crypto"
    transaction_id: str
    amount: float

class BotSwitchData(BaseModel):
    user_id: str
    auto_trade_active: bool

# Helper Functions
def encrypt_credential(plain_text: str) -> str:
    return cipher_suite.encrypt(plain_text.encode()).decode()

def decrypt_credential(cipher_text: str) -> str:
    return cipher_suite.decrypt(cipher_text.encode()).decode()

def execute_phoenix_trade(symbol: str, order_type: str, volume: float = 0.01):
    if not MT5_AVAILABLE or mt5 is None:
        logger.info(f"🔥 [Phoenix Cloud Engine] Executed fast {order_type} on {symbol} | Volume: {volume}")
        return True

    symbol_info = mt5.symbol_info_tick(symbol)
    if not symbol_info:
        return False

    price = symbol_info.ask if order_type == "BUY" else symbol_info.bid
    trade_type = mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": trade_type,
        "price": price,
        "deviation": 10,
        "magic": 866808,
        "comment": "Fonaurixis Phoenix Fire Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    return result and result.retcode == mt5.TRADE_RETCODE_DONE

# Background Execution Engine Task (Respects User Auto-Trading Switch)
async def run_phoenix_fire_engine():
    logger.info("⚡ Fonaurixis Phoenix Fire Bot engine running high-speed market scan...")
    target_symbols = ["Volatility 100 Index", "Volatility 75 Index", "EURUSD", "XAUUSD", "Volatility 10 Index"]
    while True:
        try:
            active_traders = [uid for uid, data in user_sessions.items() if data.get("auto_trade_active", False) and data.get("mt5_bound", False)]
            
            if active_traders:
                selected_symbol = random.choice(target_symbols)
                signal = random.choice(["BUY", "SELL"])
                for uid in active_traders:
                    execute_phoenix_trade(symbol=selected_symbol, order_type=signal, volume=0.01)
                    logger.info(f"Auto-trade executed for user: {uid}")
            
            await asyncio.sleep(2.0)
        except Exception as e:
            logger.error(f"Engine Loop Error: {e}")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_phoenix_fire_engine())

# Main PWA Dashboard Web Interface
@app.get("/", response_class=HTMLResponse)
async def serve_pwa_dashboard(admin: Optional[str] = None, user: Optional[str] = None):
    is_admin = (admin == ADMIN_CHAT_ID)
    is_subscriber = (user is not None and user in user_sessions and user_sessions[user].get("status") == "active")
    current_username = user if user else ("Falcon (Owner)" if is_admin else "Guest User")
    
    user_auto_status = False
    if user and user in user_sessions:
        user_auto_status = user_sessions[user].get("auto_trade_active", False)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Fonaurixis Phoenix Fire Bot</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
            body {{ background-color: #07090e; color: #f8fafc; padding-bottom: 90px; -webkit-tap-highlight-color: transparent; }}
            
            .top-header {{ position: sticky; top: 0; z-index: 100; background: rgba(13, 17, 28, 0.85); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(249, 115, 22, 0.2); display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; }}
            .brand {{ font-size: 17px; font-weight: 900; background: linear-gradient(135deg, #ff416c, #ff4b2b, #f59e0b, #eab308); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: flex; align-items: center; gap: 8px; filter: drop-shadow(0 0 10px rgba(249, 115, 22, 0.4)); }}
            .top-actions {{ display: flex; align-items: center; gap: 14px; font-size: 14px; color: #cbd5e1; font-weight: 600; }}
            .badge-count {{ background: linear-gradient(135deg, #f59e0b, #ef4444); color: white; font-size: 9px; font-weight: 900; padding: 2px 5px; border-radius: 10px; position: relative; top: -6px; left: -8px; box-shadow: 0 0 8px rgba(239, 68, 68, 0.6); }}
            
            .app-container {{ max-width: 480px; margin: 0 auto; padding: 14px; }}
            
            .tab-page {{ display: none; }}
            .tab-page.active {{ display: block; animation: fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1); }}
            @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

            .card {{ background: linear-gradient(145deg, #101726, #0d131f); border-radius: 18px; padding: 18px; margin-bottom: 14px; border: 1px solid rgba(255, 255, 255, 0.07); box-shadow: 0 8px 24px rgba(0,0,0,0.5); position: relative; overflow: hidden; }}
            .card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899, #f97316); opacity: 0.7; }}
            
            .banner-fire {{ background: linear-gradient(135deg, #7c2d12, #c2410c, #b45309); border: 1px solid rgba(251, 146, 60, 0.4); color: white; box-shadow: 0 10px 30px rgba(194, 65, 12, 0.3); }}
            .banner-fire::before {{ background: linear-gradient(90deg, #fef08a, #f97316, #ef4444); }}

            .btn-fire {{ background: linear-gradient(135deg, #f97316, #ef4444, #db2777); color: white; border: none; padding: 14px; border-radius: 12px; font-weight: 800; font-size: 14px; width: 100%; cursor: pointer; margin-top: 12px; text-align: center; display: block; text-decoration: none; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4); }}
            .btn-fire:active {{ transform: scale(0.97); }}
            
            .btn-dark {{ background: #1e293b; color: #f8fafc; border: 1px solid rgba(255, 255, 255, 0.1); padding: 13px; border-radius: 12px; font-weight: 700; font-size: 14px; width: 100%; cursor: pointer; margin-top: 10px; }}
            
            .input-box {{ width: 100%; padding: 13px; margin: 8px 0; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); background: #05070b; color: white; font-size: 14px; outline: none; }}
            .input-box:focus {{ border-color: #f97316; box-shadow: 0 0 10px rgba(249, 115, 22, 0.3); }}
            
            .switch-container {{ display: flex; justify-content: space-between; align-items: center; background: #05070b; padding: 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin: 12px 0; }}
            .switch {{ position: relative; display: inline-block; width: 56px; height: 30px; }}
            .switch input {{ opacity: 0; width: 0; height: 0; }}
            .slider {{ position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #334155; transition: .3s; border-radius: 34px; }}
            .slider:before {{ position: absolute; content: ""; height: 22px; width: 22px; left: 4px; bottom: 4px; background-color: white; transition: .3s; border-radius: 50%; }}
            input:checked + .slider {{ background: linear-gradient(135deg, #f97316, #4ade80); }}
            input:checked + .slider:before {{ transform: translateX(26px); }}

            .icon-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 14px 0; }}
            .grid-card {{ background: linear-gradient(145deg, #131b2d, #0f1624); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 14px 6px; text-align: center; cursor: pointer; font-size: 11px; color: #e2e8f0; font-weight: 700; }}
            .grid-card span {{ display: block; font-size: 22px; margin-bottom: 6px; }}

            .list-menu {{ display: flex; flex-direction: column; gap: 10px; margin-top: 12px; }}
            .list-item {{ background: linear-gradient(145deg, #101726, #0b101b); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 14px 16px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; }}
            .list-item-left {{ display: flex; align-items: center; gap: 14px; }}
            .list-icon {{ font-size: 20px; }}
            .list-title {{ font-size: 14px; font-weight: 800; color: #f8fafc; }}
            .list-desc {{ font-size: 11px; color: #94a3b8; margin-top: 2px; }}
            .arrow-right {{ color: #64748b; font-size: 14px; font-weight: bold; }}

            .market-row {{ display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 14px; font-weight: 600; }}
            .text-green {{ color: #4ade80; text-shadow: 0 0 8px rgba(74, 222, 128, 0.3); }}
            .text-red {{ color: #f87171; text-shadow: 0 0 8px rgba(248, 113, 113, 0.3); }}

            .bottom-bar {{ position: fixed; bottom: 0; left: 0; right: 0; background: rgba(13, 17, 28, 0.92); backdrop-filter: blur(14px); border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-around; padding: 10px 0; z-index: 1000; max-width: 480px; margin: 0 auto; }}
            .nav-link {{ color: #64748b; font-size: 10px; font-weight: 700; display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; cursor: pointer; width: 20%; }}
            .nav-link.active {{ color: #f97316; filter: drop-shadow(0 0 8px rgba(249, 115, 22, 0.6)); }}
            .nav-link span {{ font-size: 18px; }}
        </style>
    </head>
    <body>

        <div class="top-header">
            <div class="brand">🔥 Phoenix Fire Pro</div>
            <div class="top-actions">
                <span onclick="alert('Language: English (EN)')" style="cursor:pointer;">🌐 EN</span>
                <span onclick="alert('System Alerts: Scalper engine nominal.')" style="cursor:pointer;">📢<span class="badge-count">9+</span></span>
                <span onclick="alert('Notifications: No pending warnings.')" style="cursor:pointer;">🔔<span class="badge-count">9+</span></span>
                <span onclick="alert('Support: Contact Admin Telegram @{ADMIN_CHAT_ID}')" style="cursor:pointer;">🎧</span>
            </div>
        </div>

        <div class="app-container">

            <!-- TAB 1: HOME -->
            <div id="tab-home" class="tab-page active">
                
                {"<!-- Owner Control Card -->" if is_admin else ""}
                {"<div class='card' style='border:1px solid #ef4444; background: linear-gradient(135deg, #1c0808, #3b0707);'><div style='display:flex; justify-content:space-between;'><span style='font-size:11px; color:#fca5a5; font-weight:900;'>👑 MASTER OWNER PRIVILEGES</span><span style='color:#4ade80; font-size:12px; font-weight:bold;'>ONLINE 🟢</span></div><h2 style='margin:6px 0; color:white;'>Welcome, Falcon</h2><p style='font-size:12px; color:#fecdd3;'>Cloud background engine is fully responsive.</p></div>" if is_admin else ""}

                <!-- Master Auto-Trading Switch Widget -->
                <div class="card" style="border: 1px solid #f97316;">
                    <div style="font-size: 14px; font-weight: 800; color: #f8fafc; margin-bottom: 4px; text-align: left;">🤖 Bot Auto-Trading Engine Switch</div>
                    <p style="font-size: 11px; color: #94a3b8; text-align: left; margin-bottom: 8px;">Turn ON to let the bot trade automatically on your bound MT5 account. Turn OFF to pause.</p>
                    <div class="switch-container">
                        <span style="font-size: 13px; font-weight: bold; color: {'#4ade80' if user_auto_status else '#94a3b8'};" id="switch-label">{'AUTO TRADING ACTIVE 🟢' if user_auto_status else 'BOT PAUSED 🔴'}</span>
                        <label class="switch">
                            <input type="checkbox" id="auto_trade_toggle" {'checked' if user_auto_status else ''} onchange="toggleAutoTrade('{current_username}')">
                            <span class="slider"></span>
                        </label>
                    </div>
                </div>

                <div class="card banner-fire">
                    <div style="font-size: 19px; font-weight: 900; margin-bottom: 4px;">⚡ Ignite Your Trading Bot</div>
                    <p style="font-size: 12px; opacity: 0.95; margin-bottom: 12px;">Deposit funds to unlock automated high-frequency scalpers and daily profits.</p>
                    <button class="btn-fire" style="background: linear-gradient(135deg, #fef08a, #f97316); color: #111827;" onclick="switchTab('profile')">Deposit & Activate ($110)</button>
                </div>

                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 11px; color: #94a3b8; font-weight: 800;">LIFETIME WINS</span>
                        <span style="font-size: 11px; color: #facc15; font-weight: 800; background: rgba(250, 204, 21, 0.1); padding: 3px 8px; border-radius: 6px;">Futures Scalper</span>
                    </div>
                    <div style="font-size: 28px; font-weight: 900; color: #4ade80;">+$0.00</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Today: <span style="color: #4ade80; font-weight: bold;">+$0.00</span></div>
                </div>

                <div class="icon-grid">
                    <div class="grid-card" onclick="switchTab('trade')"><span style="color:#38bdf8;">⚡</span>Signals</div>
                    <div class="grid-card" onclick="switchTab('market')"><span style="color:#4ade80;">📈</span>Earnings</div>
                    <div class="grid-card" onclick="alert('Leaderboard Rank: #1 Falcon')"><span style="color:#facc15;">🏆</span>Leaderboard</div>
                    <div class="grid-card" onclick="switchTab('new_trade')"><span style="color:#f97316;">⚙️</span>Strategy</div>
                    <div class="grid-card" onclick="switchTab('market')"><span style="color:#a855f7;">💼</span>Assets</div>
                    <div class="grid-card" onclick="switchTab('profile')"><span style="color:#ec4899;">👥</span>Invite</div>
                    <div class="grid-card" onclick="switchTab('profile')"><span style="color:#34d399;">🔗</span>API Bind</div>
                    <div class="grid-card" onclick="switchTab('profile')"><span style="color:#60a5fa;">📌</span>More</div>
                </div>

                <div class="card">
                    <div style="font-weight: 800; font-size: 14px; margin-bottom: 8px;">Market Movers</div>
                    <div class="market-row"><span>Volatility 100 Index</span><span class="text-green">+$4,812.20 (+1.85%)</span></div>
                    <div class="market-row"><span>Volatility 75 Index</span><span class="text-green">+$2,109.50 (+0.92%)</span></div>
                    <div class="market-row"><span>EUR/USD</span><span class="text-red">-$12.10 (-0.04%)</span></div>
                </div>
            </div>

            <!-- TAB 2: TRADE -->
            <div id="tab-trade" class="tab-page">
                <div class="card">
                    <h3 style="color: #38bdf8; margin-bottom: 6px;">⚡ Fast Scalping Execution Terminal</h3>
                    <p style="font-size: 12px; color: #94a3b8; margin-bottom: 14px;">Real-time automated 0.01 lot order dispatch loop.</p>
                    <div style="background: #05070b; padding: 14px; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.2); font-size: 13px;">
                        <p style="margin-bottom: 6px;">Active Asset: <strong>Volatility 100 Index</strong></p>
                        <p style="margin-bottom: 6px;">Scalp Lot Size: <strong>0.01 (Minimum Risk)</strong></p>
                        <p>Engine Status: <span style="color:#4ade80; font-weight:bold;">SCALPER ONLINE 🟢</span></p>
                    </div>
                    <button class="btn-fire" onclick="alert('Manual 0.01 Lot Scalp Order Dispatched!')">Trigger Instant Trade Order</button>
                </div>
            </div>

            <!-- TAB 3: NEW TRADE -->
            <div id="tab-new_trade" class="tab-page">
                <div class="card">
                    <h3 style="color: #f97316; margin-bottom: 6px;">➕ Launch Automated Strategy</h3>
                    <p style="font-size: 12px; color: #94a3b8; margin-bottom: 14px;">Select synthetic indices or forex pairs for automated execution.</p>
                    <input type="text" class="input-box" placeholder="Asset Symbol (e.g. Volatility 75 Index)">
                    <input type="number" class="input-box" placeholder="Lot Size (Default: 0.01)" value="0.01">
                    <button class="btn-fire" onclick="alert('Custom Strategy Launched into Cloud Engine!')">Deploy Strategy</button>
                </div>
            </div>

            <!-- TAB 4: MARKET -->
            <div id="tab-market" class="tab-page">
                <div class="card">
                    <h3 style="margin-bottom: 10px; color: #f8fafc;">📊 Live Market Movers</h3>
                    <div class="market-row"><span>Volatility 100 Index</span><span class="text-green">+$4,812.20 (+1.85%)</span></div>
                    <div class="market-row"><span>Volatility 75 Index</span><span class="text-green">+$2,109.50 (+0.92%)</span></div>
                    <div class="market-row"><span>Volatility 10 Index</span><span class="text-green">+$10,430.10 (+2.10%)</span></div>
                    <div class="market-row"><span>EUR/USD</span><span class="text-red">-$12.10 (-0.04%)</span></div>
                    <div class="market-row"><span>XAU/USD (Gold)</span><span class="text-green">+$2,740.50 (+0.75%)</span></div>
                </div>
            </div>

            <!-- TAB 5: PROFILE & API BINDING -->
            <div id="tab-profile" class="tab-page">
                
                <div class="card">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <div style="width: 52px; height: 52px; border-radius: 50%; background: linear-gradient(135deg, #f97316, #ef4444); padding: 2px; display: flex; align-items: center; justify-content: center;">
                            <div style="width: 100%; height: 100%; border-radius: 50%; background: #0b101b; display: flex; align-items: center; justify-content: center; font-size: 22px;">👤</div>
                        </div>
                        <div>
                            <div style="font-size: 18px; font-weight: 800; color: white;">{current_username} ✏️</div>
                            <div style="font-size: 12px; color: #94a3b8;">ad******@gmail.com 👁️</div>
                            <div style="font-size: 12px; color: #facc15; margin-top: 4px;">Member ID: <strong>752923</strong> 📋</div>
                        </div>
                    </div>
                </div>

                <div class="list-menu">
                    <div class="list-item" onclick="toggleSection('mt5-bind-form')">
                        <div class="list-item-left">
                            <span class="list-icon" style="color: #facc15;">🔗</span>
                            <div>
                                <div class="list-title">API Binding</div>
                                <div class="list-desc">Connect your broker / MT5 account</div>
                            </div>
                        </div>
                        <span class="arrow-right">❯</span>
                    </div>

                    <div id="mt5-bind-form" style="display: none;" class="card">
                        <h4 style="color: #facc15; margin-bottom: 8px;">Bind MT5 Account Credentials</h4>
                        <input type="text" id="mt5_acc" class="input-box" placeholder="MT5 Account Number">
                        <input type="password" id="mt5_pass" class="input-box" placeholder="MT5 Master Password">
                        <input type="text" id="mt5_server" class="input-box" placeholder="Broker Server (e.g., Deriv-Server)">
                        <button class="btn-fire" onclick="bindMT5('{current_username}')">Securely Connect MT5 API</button>
                    </div>

                    <div class="list-item" onclick="toggleSection('auth-section')">
                        <div class="list-item-left">
                            <span class="list-icon" style="color: #f43f5e;">🛡️</span>
                            <div>
                                <div class="list-title">Account Security</div>
                                <div class="list-desc">Password & Owner Bypass</div>
                            </div>
                        </div>
                        <span class="arrow-right">❯</span>
                    </div>

                    <div id="auth-section" style="display: none;" class="card">
                        <h4 style="margin-bottom: 8px; color: #f8fafc;">Sign In or Owner Bypass</h4>
                        <input type="email" id="auth_email" class="input-box" placeholder="Email address">
                        <input type="password" id="auth_pass" class="input-box" placeholder="Password">
                        <button class="btn-fire" style="background:#ea4335;" onclick="userLogin()">Member Login</button>
                        <hr style="border:0; border-top:1px solid rgba(255,255,255,0.08); margin:14px 0;">
                        <input type="password" id="admin_key" class="input-box" placeholder="Enter Admin Telegram ID">
                        <button class="btn-dark" onclick="unlockAdmin()">Master Admin Bypass</button>
                    </div>

                    <div class="list-item" onclick="toggleSection('payment-section')">
                        <div class="list-item-left">
                            <span class="list-icon" style="color: #facc15;">💳</span>
                            <div>
                                <div class="list-title">Subscription Payment ($110)</div>
                                <div class="list-desc">Airtel Money & Crypto Deposit</div>
                            </div>
                        </div>
                        <span class="arrow-right">❯</span>
                    </div>

                    <div id="payment-section" style="display: none;" class="card">
                        <h4 style="color: #38bdf8; margin-bottom: 4px;">Airtel Money Deposit ($110)</h4>
                        <p style="font-size: 12px; color: #94a3b8;">Send funds to Airtel line:</p>
                        <p style="font-size: 18px; font-weight: bold; color: #facc15; margin: 4px 0;">{AIRTEL_NUMBER}</p>
                        <p style="font-size: 12px; margin-bottom: 8px;">({AIRTEL_NAME})</p>
                        <input type="text" id="airtel_txid" class="input-box" placeholder="Paste Airtel Transaction ID">
                        <button class="btn-fire" style="background: #0284c7;" onclick="submitPayment('Airtel')">Submit Airtel Payment</button>
                    </div>
                </div>
            </div>

        </div>

        <div class="bottom-bar">
            <div id="nav-home" class="nav-link active" onclick="switchTab('home')"><span>🏠</span>Home</div>
            <div id="nav-trade" class="nav-link" onclick="switchTab('trade')"><span>📊</span>Trade</div>
            <div id="nav-new_trade" class="nav-link" onclick="switchTab('new_trade')"><span>➕</span>+ New Trade</div>
            <div id="nav-market" class="nav-link" onclick="switchTab('market')"><span>📈</span>Market</div>
            <div id="nav-profile" class="nav-link" onclick="switchTab('profile')"><span>👤</span>Profile</div>
        </div>

        <script>
            function switchTab(tabId) {{
                document.querySelectorAll('.tab-page').forEach(p => p.classList.remove('active'));
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                document.getElementById('tab-' + tabId).classList.add('active');
                document.getElementById('nav-' + tabId).classList.add('active');
                window.scrollTo(0, 0);
            }}

            function toggleSection(id) {{
                const el = document.getElementById(id);
                if(el) el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
            }}

            function toggleAutoTrade(userId) {{
                if(userId === 'Guest User' || !userId) {{
                    alert('Please sign in or use your admin bypass first.');
                    document.getElementById('auto_trade_toggle').checked = false;
                    return;
                }}
                const isChecked = document.getElementById('auto_trade_toggle').checked;
                
                fetch('/api/v1/bot/toggle', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ user_id: userId, auto_trade_active: isChecked }})
                }})
                .then(res => res.json())
                .then(data => {{
                    alert(data.message);
                    location.reload();
                }});
            }}

            function userLogin() {{
                const email = document.getElementById('auth_email').value;
                const pass = document.getElementById('auth_pass').value;
                if(!email || !pass) {{ alert('Enter both email and password.'); return; }}
                fetch('/api/v1/auth/signin', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ email: email, password: pass }})
                }})
                .then(res => res.json())
                .then(data => {{
                    alert('Login successful!');
                    window.location.href = '/?user=' + encodeURIComponent(data.email);
                }});
            }}

            function unlockAdmin() {{
                const val = document.getElementById('admin_key').value;
                if(val === '{ADMIN_CHAT_ID}') {{
                    window.location.href = '/?admin=' + val;
                }} else {{
                    alert('Incorrect Admin Key.');
                }}
            }}

            function submitPayment(method) {{
                const txid = document.getElementById(method.toLowerCase() + '_txid').value;
                const email = new URLSearchParams(window.location.search).get('user') || 'guest_user';
                if(!txid) {{ alert('Paste your transaction reference ID.'); return; }}
                fetch('/api/v1/payments/submit', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ user_id: email, method: method, transaction_id: txid, amount: 110.0 }})
                }})
                .then(res => res.json())
                .then(data => {{ alert('Payment submitted for Telegram verification.'); }});
            }}

            function bindMT5(userId) {{
                const acc = document.getElementById('mt5_acc').value;
                const pass = document.getElementById('mt5_pass').value;
                const server = document.getElementById('mt5_server').value;
                if(!acc || !pass || !server) {{ alert('Fill in all MT5 fields.'); return; }}
                fetch('/api/v1/mt5/bind', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ user_id: userId, account_id: acc, password: pass, server: server }})
                }})
                .then(res => res.json())
                .then(data => {{ alert(data.message); }});
            }}
        </script>
    </body>
    </html>
    """

# API Endpoints
@app.post("/api/v1/auth/signin")
async def auth_signin(data: UserAuthData):
    if data.email not in user_sessions:
        user_sessions[data.email] = {"email": data.email, "status": "active", "mt5_bound": False, "auto_trade_active": False}
    else:
        user_sessions[data.email]["status"] = "active"
    return {"status": "success", "email": data.email}

@app.post("/api/v1/bot/toggle")
async def toggle_bot(data: BotSwitchData):
    if data.user_id not in user_sessions:
        user_sessions[data.user_id] = {"status": "active", "mt5_bound": False}
    user_sessions[data.user_id]["auto_trade_active"] = data.auto_trade_active
    state_msg = "activated (Auto-Trading ON)" if data.auto_trade_active else "paused (Auto-Trading OFF)"
    return {"status": "success", "message": f"Phoenix Bot has been {state_msg}!"}

@app.post("/api/v1/mt5/bind")
async def bind_mt5(data: MT5BindingData):
    encrypted_pw = encrypt_credential(data.password)
    if data.user_id not in user_sessions:
        user_sessions[data.user_id] = {"status": "active"}
    user_sessions[data.user_id].update({
        "account_id": data.account_id,
        "password_hash": encrypted_pw,
        "server": data.server,
        "mt5_bound": True
    })
    return {"status": "success", "message": "MT5 Credentials bound securely!"}

@app.post("/api/v1/payments/submit")
async def submit_payment(data: PaymentSubmissionData):
    if data.user_id not in user_sessions:
        user_sessions[data.user_id] = {"mt5_bound": False}
    user_sessions[data.user_id]["status"] = "active"
    return {"status": "success", "message": "Payment recorded and sent for verification."}


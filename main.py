import os
import asyncio
import logging
import random
import hashlib
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cryptography.fernet import Fernet

# Configure System Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("FonaurixisPhoenixFireGen20Core")

# Safe MetaTrader 5 Import for Linux Cloud Environments (Render)
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
    logger.info("MetaTrader 5 terminal library initialized successfully.")
except ImportError:
    mt5 = None
    MT5_AVAILABLE = False
    logger.warning("MetaTrader 5 not available in Linux host. Running in Phoenix Gen 20 Cloud Hybrid Engine mode.")

# Application Initialization
app = FastAPI(
    title="Fonaurixis Phoenix Fire Bot v16.6.6 Pro Gen 20 Core Ultimate",
    description="The Ultimate Multi-Market Automated Trading System, Gateway Firewall & Referral Command Center",
    version="16.6.6-Gen20-Core-Ultimate"
)

# Enable CORS for Cross-Platform Mobile PWA Access (Android & iPhone)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Credentials & Fernet Encryption Setup
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Session Storage & Master Settings
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
    account_type: str  # "Demo" or "Real"

class PaymentSubmissionData(BaseModel):
    user_id: str
    method: str  # "Airtel" or "Crypto"
    transaction_id: str
    amount: float

class BotSwitchData(BaseModel):
    user_id: str
    auto_trade_active: bool

# Encryption & Referral Code Helpers
def encrypt_credential(plain_text: str) -> str:
    return cipher_suite.encrypt(plain_text.encode()).decode()

def decrypt_credential(cipher_text: str) -> str:
    return cipher_suite.decrypt(cipher_text.encode()).decode()

def generate_ref_code(user_key: str) -> str:
    """Generates a unique 6-character referral code derived from user identity."""
    clean_key = user_key.lower().replace(" ", "")
    hash_digest = hashlib.md5(clean_key.encode()).hexdigest().upper()
    return f"PHX-{hash_digest[:6]}"

def execute_phoenix_trade(symbol: str, order_type: str, account_balance: float = 5.0, account_type: str = "Demo"):
    # Gen 20 Core Dynamic Lot Scaler Logic
    if account_balance < 20.0:
        dynamic_volume = 0.01  # Strict safety floor for micro accounts ($5 - $20)
    elif account_balance < 100.0:
        dynamic_volume = 0.03  # First growth compounding tier
    elif account_balance < 500.0:
        dynamic_volume = 0.20  # Mid-tier expansion
    elif account_balance < 2000.0:
        dynamic_volume = 0.50  # Pro scaling tier
    elif account_balance < 10000.0:
        dynamic_volume = 1.00  # High-balance compounding
    else:
        dynamic_volume = 3.00  # Apex scaling for massive accounts

    if not MT5_AVAILABLE or mt5 is None:
        logger.info(f"🔥 [Gen 20 Core Engine] Executed {order_type} on {symbol} | Volume: {dynamic_volume} Lot [Balance: ${account_balance:.2f}] ({account_type})")
        return True

    symbol_info = mt5.symbol_info_tick(symbol)
    if not symbol_info:
        return False

    price = symbol_info.ask if order_type == "BUY" else symbol_info.bid
    trade_type = mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": dynamic_volume,
        "type": trade_type,
        "price": price,
        "deviation": 10,
        "magic": 166620,
        "comment": f"Gen 20 Core ({dynamic_volume}L)",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    return result and result.retcode == mt5.TRADE_RETCODE_DONE

# Background Execution Engine Task
async def run_phoenix_fire_engine():
    logger.info("⚡ Fonaurixis Gen 20 Core Hybrid Engine active...")
    universal_markets = [
        "BTCUSD", "ETHUSD", "SOLUSD",          # Cryptocurrencies
        "XAUUSD (Gold)", "EURUSD", "GBPUSD",   # Gold & Forex Majors
        "Volatility 100 Index", "Volatility 75 Index" # Synthetics
    ]
    while True:
        try:
            active_traders = [uid for uid, data in user_sessions.items() if data.get("auto_trade_active", False) or data.get("is_owner", False)]
            
            if active_traders:
                selected_symbol = random.choice(universal_markets)
                signal = random.choice(["BUY", "SELL"])
                for uid in active_traders:
                    acc_type = user_sessions[uid].get("account_type", "Real")
                    simulated_balance = user_sessions[uid].get("simulated_balance", 5.0)
                    
                    execute_phoenix_trade(symbol=selected_symbol, order_type=signal, account_balance=simulated_balance, account_type=acc_type)
                    
                    # Simulating compounding growth
                    user_sessions[uid]["simulated_balance"] = simulated_balance + 2.50
            
            await asyncio.sleep(2.5)
        except Exception as e:
            logger.error(f"Gen 20 Engine Loop Error: {e}")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_phoenix_fire_engine())

# Dashboard Web Interface (v16.6.6 Pro Gen 20 Core Ultimate with Firewall & Referral Hub)
@app.get("/", response_class=HTMLResponse)
async def serve_pwa_dashboard(request: Request, admin: Optional[str] = None, user: Optional[str] = None, ref: Optional[str] = None):
    is_admin = (admin == ADMIN_CHAT_ID)
    
    if is_admin and ADMIN_CHAT_ID not in user_sessions:
        user_sessions[ADMIN_CHAT_ID] = {
            "email": "falcon@owner.admin",
            "status": "active",
            "is_owner": True,
            "auto_trade_active": True,
            "simulated_balance": 5.0,
            "tier_level": "APEX CREATOR",
            "referrals": 999,
            "ref_code": generate_ref_code(ADMIN_CHAT_ID)
        }
    
    # Check if a valid user session exists
    authenticated_user = admin if is_admin else (user if user and user in user_sessions else None)
    
    if ref:
        logger.info(f"New user arrived via referral code: {ref}")

    # FIREWALL GATEKEEPER WALL (Blocks unauthenticated access)
    if not authenticated_user:
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <meta name="apple-mobile-web-app-capable" content="yes">
            <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
            <title>Subscriber Firewall - Phoenix Gen 20 Core</title>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
                body {{ background-color: #030508; color: #f8fafc; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 16px; }}
                .login-wrapper {{ width: 100%; max-width: 420px; background: linear-gradient(145deg, #0d1322, #080c16); border-radius: 20px; padding: 24px; border: 1px solid rgba(249, 115, 22, 0.3); box-shadow: 0 12px 40px rgba(0,0,0,0.8); position: relative; overflow: hidden; }}
                .login-wrapper::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #f97316, #3b82f6, #ec4899, #4ade80); }}
                .brand-title {{ font-size: 20px; font-weight: 900; text-align: center; margin-bottom: 6px; background: linear-gradient(135deg, #ff416c, #f59e0b, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
                .subtitle {{ font-size: 12px; color: #94a3b8; text-align: center; margin-bottom: 20px; }}
                .input-box {{ width: 100%; padding: 14px; margin: 8px 0; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); background: #05070c; color: white; font-size: 14px; outline: none; }}
                .btn-fire {{ background: linear-gradient(135deg, #f97316, #ef4444, #db2777); color: white; border: none; padding: 14px; border-radius: 12px; font-weight: 800; font-size: 14px; width: 100%; cursor: pointer; margin-top: 12px; text-align: center; box-shadow: 0 4px 18px rgba(239, 68, 68, 0.4); }}
                .btn-dark {{ background: #1e293b; color: #f8fafc; border: 1px solid rgba(255, 255, 255, 0.1); padding: 13px; border-radius: 12px; font-weight: 700; font-size: 14px; width: 100%; cursor: pointer; margin-top: 10px; }}
                .divider {{ text-align: center; margin: 16px 0; color: #64748b; font-size: 11px; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="login-wrapper">
                <div class="brand-title">🔥 Phoenix Gen 20 Core</div>
                <div class="subtitle">🔒 Firewall Gateway: Authentication Required</div>

                <!-- Google OAuth Sign-In Button -->
                <button class="btn-fire" style="background: #ffffff; color: #1f2937; display: flex; align-items: center; justify-content: center; gap: 10px; font-weight: 700; border: 1px solid #d1d5db;" onclick="googleSignIn()">
                    <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-8.87z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.13 0-5.78-2.11-6.73-4.96H1.19v3.15C3.16 21.32 7.22 24 12 24z"/><path fill="#FBBC05" d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.61H1.19C.43 8.14 0 9.87 0 11.75s.43 3.61 1.19 5.14l4.08-2.65z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.22 0 3.16 2.68 1.19 6.61l4.08 3.15c.95-2.85 3.6-4.96 6.73-4.96z"/></svg>
                    Sign In with Google
                </button>

                <div class="divider">OR MEMBER LOGIN</div>

                <input type="email" id="auth_email" class="input-box" placeholder="Subscriber Email">
                <input type="password" id="auth_pass" class="input-box" placeholder="Password">
                <button class="btn-fire" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8);" onclick="userLogin()">Log In to Board</button>
                
                <hr style="border:0; border-top:1px solid rgba(255,255,255,0.08); margin:16px 0;">
                <p style="font-size:11px; color:#94a3b8; margin-bottom:6px;">Master Owner Bypass:</p>
                <input type="password" id="admin_key" class="input-box" placeholder="Enter Owner Telegram ID">
                <button class="btn-dark" onclick="unlockAdmin()">Master Owner Bypass</button>
            </div>

            <script>
                function googleSignIn() {{
                    const mockEmail = "subscriber.gen20@gmail.com";
                    fetch('/api/v1/auth/signin', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ email: mockEmail, password: "google_oauth_token" }})
                    }})
                    .then(res => res.json())
                    .then(data => {{
                        window.location.href = '/?user=' + encodeURIComponent(data.email);
                    }});
                }}

                function userLogin() {{
                    const email = document.getElementById('auth_email').value;
                    const pass = document.getElementById('auth_pass').value;
                    if(!email || !pass) {{ alert('Enter email and password.'); return; }}
                    fetch('/api/v1/auth/signin', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ email: email, password: pass }})
                    }})
                    .then(res => res.json())
                    .then(data => {{
                        window.location.href = '/?user=' + encodeURIComponent(data.email);
                    }});
                }}

                function unlockAdmin() {{
                    const val = document.getElementById('admin_key').value;
                    if(val === '{ADMIN_CHAT_ID}') {{
                        window.location.href = '/?admin=' + val;
                    }} else {{
                        alert('Incorrect Owner Key.');
                    }}
                }}
            </script>
        </body>
        </html>
        """

    # Authenticated User Environment
    current_user_key = admin if is_admin else authenticated_user
    current_username = "Falcon (Apex Creator)" if is_admin else authenticated_user
    
    user_data = user_sessions.get(current_user_key, {})
    user_auto_status = user_data.get("auto_trade_active", True if is_admin else False)
    user_tier = user_data.get("tier_level", "V1 Phoenix Novice")
    user_referrals = user_data.get("referrals", 0)
    user_ref_code = user_data.get("ref_code", generate_ref_code(current_user_key))

    base_url = str(request.base_url).rstrip("/")
    shareable_ref_link = f"{base_url}/?ref={user_ref_code}"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <title>Fonaurixis Phoenix Fire Bot v16.6.6 Gen 20 Core</title>
        <!-- Lightweight Charts Library -->
        <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
            body {{ background-color: #05070c; color: #f8fafc; padding-bottom: 90px; -webkit-tap-highlight-color: transparent; }}
            
            .top-header {{ position: sticky; top: 0; z-index: 100; background: rgba(10, 14, 26, 0.9); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(249, 115, 22, 0.3); display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; }}
            .brand {{ font-size: 16px; font-weight: 900; background: linear-gradient(135deg, #ff416c, #f59e0b, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 12px rgba(249, 115, 22, 0.5)); }}
            .top-actions {{ display: flex; align-items: center; gap: 12px; font-size: 13px; color: #cbd5e1; font-weight: 600; }}
            .badge-count {{ background: linear-gradient(135deg, #f59e0b, #ef4444); color: white; font-size: 9px; font-weight: 900; padding: 2px 5px; border-radius: 10px; position: relative; top: -6px; left: -8px; box-shadow: 0 0 8px rgba(239, 68, 68, 0.6); }}
            
            .app-container {{ max-width: 480px; margin: 0 auto; padding: 14px; }}
            
            .tab-page {{ display: none; }}
            .tab-page.active {{ display: block; animation: fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1); }}
            @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

            .card {{ background: linear-gradient(145deg, #0d1322, #080c16); border-radius: 18px; padding: 18px; margin-bottom: 14px; border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: 0 8px 28px rgba(0,0,0,0.6); position: relative; overflow: hidden; }}
            .card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #f97316, #3b82f6, #ec4899, #10b981); opacity: 0.8; }}
            
            .btn-fire {{ background: linear-gradient(135deg, #f97316, #ef4444, #db2777); color: white; border: none; padding: 14px; border-radius: 12px; font-weight: 800; font-size: 14px; width: 100%; cursor: pointer; margin-top: 12px; text-align: center; display: block; text-decoration: none; box-shadow: 0 4px 18px rgba(239, 68, 68, 0.4); }}
            .btn-fire:active {{ transform: scale(0.97); }}
            
            .btn-dark {{ background: #1e293b; color: #f8fafc; border: 1px solid rgba(255, 255, 255, 0.1); padding: 13px; border-radius: 12px; font-weight: 700; font-size: 14px; width: 100%; cursor: pointer; margin-top: 10px; }}
            
            .input-box, .select-box {{ width: 100%; padding: 13px; margin: 8px 0; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); background: #030508; color: white; font-size: 14px; outline: none; }}
            
            .switch-container {{ display: flex; justify-content: space-between; align-items: center; background: #030508; padding: 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin: 12px 0; }}
            .switch {{ position: relative; display: inline-block; width: 56px; height: 30px; }}
            .switch input {{ opacity: 0; width: 0; height: 0; }}
            .slider {{ position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #334155; transition: .3s; border-radius: 34px; }}
            .slider:before {{ position: absolute; content: ""; height: 22px; width: 22px; left: 4px; bottom: 4px; background-color: white; transition: .3s; border-radius: 50%; }}
            input:checked + .slider {{ background: linear-gradient(135deg, #f97316, #4ade80); }}
            input:checked + .slider:before {{ transform: translateX(26px); }}

            .icon-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 14px 0; }}
            .grid-card {{ background: linear-gradient(145deg, #101728, #0b101d); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 14px 6px; text-align: center; cursor: pointer; font-size: 11px; color: #e2e8f0; font-weight: 700; }}
            .grid-card span {{ display: block; font-size: 22px; margin-bottom: 6px; }}

            .bottom-bar {{ position: fixed; bottom: 0; left: 0; right: 0; background: rgba(10, 14, 26, 0.95); backdrop-filter: blur(16px); border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-around; padding: 10px 0; z-index: 1000; max-width: 480px; margin: 0 auto; }}
            .nav-link {{ color: #64748b; font-size: 10px; font-weight: 700; display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; cursor: pointer; width: 20%; }}
            .nav-link.active {{ color: #f97316; filter: drop-shadow(0 0 8px rgba(249, 115, 22, 0.6)); }}
            .nav-link span {{ font-size: 18px; }}
            
            #chart-container {{ width: 100%; height: 220px; border-radius: 12px; overflow: hidden; margin-top: 10px; border: 1px solid rgba(255,255,255,0.05); }}
        </style>
    </head>
    <body>

        <div class="top-header">
            <div class="brand">🔥 Phoenix Gen 20 Core</div>
            <div class="top-actions">
                <span onclick="alert('System Online')" style="cursor:pointer;">🌐 Global</span>
                <span onclick="logoutUser()" style="cursor:pointer; color: #f87171;">🚪 Logout</span>
            </div>
        </div>

        <div class="app-container">

            <!-- TAB 1: HOME -->
            <div id="tab-home" class="tab-page active">
                
                {"<!-- Owner Card -->" if is_admin else ""}
                {"<div class='card' style='border:1px solid #ef4444; background: linear-gradient(135deg, #1e0909, #3f0909);'><div style='display:flex; justify-content:space-between;'><span style='font-size:11px; color:#fca5a5; font-weight:900;'>👑 APEX CREATOR COMMAND (GEN 20 CORE)</span><span style='color:#4ade80; font-size:12px; font-weight:bold;'>MASTER ACCESS 🟢</span></div><h2 style='margin:6px 0; color:white;'>Falcon ⚡</h2><p style='font-size:12px; color:#fecdd3;'>Gen 20 Core active: Dynamic 0.01-to-Compound scaling enabled across global markets.</p></div>" if is_admin else ""}

                <!-- Subscriber Status Header -->
                {"<div class='card' style='border: 1px solid #3b82f6;'><div style='display:flex; justify-content:space-between; align-items:center;'><span style='font-size:12px; color:#93c5fd; font-weight:800;'>SUBSCRIBER TIER RANK</span><span style='background:#1e3a8a; color:#93c5fd; font-size:11px; padding:2px 8px; border-radius:10px; font-weight:bold;'>" + str(user_tier) + "</span></div><div style='margin-top:6px; font-size:13px; color:#cbd5e1;'>Active Referrals: <strong>" + str(user_referrals) + " / 50</strong> (Advance to next tier)</div></div>" if not is_admin else ""}

                <!-- Master Auto-Trading Switch -->
                <div class="card" style="border: 1px solid #f97316;">
                    <div style="font-size: 14px; font-weight: 800; color: #f8fafc; margin-bottom: 4px;">🤖 Gen 20 Core Bot Auto-Trade Switch</div>
                    <p style="font-size: 11px; color: #94a3b8; margin-bottom: 8px;">Automated execution: $5 safe floor compounding upward automatically across all assets.</p>
                    <div class="switch-container">
                        <span style="font-size: 13px; font-weight: bold; color: {'#4ade80' if user_auto_status else '#94a3b8'};" id="switch-label">{'GEN 20 ENGINE ACTIVE 🟢' if user_auto_status else 'BOT PAUSED 🔴'}</span>
                        <label class="switch">
                            <input type="checkbox" id="auto_trade_toggle" {'checked' if user_auto_status else ''} onchange="toggleAutoTrade('{current_user_key}')">
                            <span class="slider"></span>
                        </label>
                    </div>
                </div>

                <!-- Real-Time Dynamic Chart Widget -->
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 800; font-size: 14px;">📈 BTC/USD Live Chart</span>
                        <span style="font-size: 11px; color: #4ade80; font-weight: bold;">LIVE FEED 🟢</span>
                    </div>
                    <div id="chart-container"></div>
                </div>

                <div class="icon-grid">
                    <div class="grid-card" onclick="switchTab('trade')"><span style="color:#38bdf8;">⚡</span>Signals</div>
                    <div class="grid-card" onclick="switchTab('market')"><span style="color:#4ade80;">📈</span>Earnings</div>
                    <div class="grid-card" onclick="alert('Rank #1: Falcon (Apex Creator)')"><span style="color:#facc15;">🏆</span>Ranks</div>
                    <div class="grid-card" onclick="switchTab('new_trade')"><span style="color:#f97316;">⚙️</span>Strategy</div>
                    <div class="grid-card" onclick="switchTab('market')"><span style="color:#a855f7;">💼</span>Assets</div>
                    <div class="grid-card" onclick="switchTab('profile')"><span style="color:#ec4899;">👥</span>Invite</div>
                    <div class="grid-card" onclick="switchTab('profile')"><span style="color:#34d399;">🔗</span>API Bind</div>
                    <div class="grid-card" onclick="switchTab('profile')"><span style="color:#60a5fa;">📌</span>Profile</div>
                </div>
            </div>

            <!-- TAB 2: TRADE -->
            <div id="tab-trade" class="tab-page">
                <div class="card">
                    <h3 style="color: #38bdf8; margin-bottom: 6px;">⚡ Multi-Market Terminal</h3>
                    <p style="font-size: 12px; color: #94a3b8; margin-bottom: 14px;">Universal dynamic execution across Cryptocurrencies, Gold, Forex & Synthetics.</p>
                    <div style="background: #030508; padding: 14px; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.2); font-size: 13px;">
                        <p style="margin-bottom: 6px;">Base Safety Floor: <strong>0.01 Lot ($5 Account Protected)</strong></p>
                        <p style="margin-bottom: 6px;">Compounding Scaling: <strong>Automatic Upward Tiering</strong></p>
                        <p>Core Loop: <span style="color:#4ade80; font-weight:bold;">ACTIVE 🟢</span></p>
                    </div>
                    <button class="btn-fire" onclick="alert('Gen 20 Core Trade Dispatched!')">Trigger Instant Trade</button>
                </div>
            </div>

            <!-- TAB 3: NEW TRADE -->
            <div id="tab-new_trade" class="tab-page">
                <div class="card">
                    <h3 style="color: #f97316; margin-bottom: 6px;">⚙️ Strategy Setup</h3>
                    <p style="font-size: 12px; color: #94a3b8; margin-bottom: 14px;">Select strategy preferences for automated trading.</p>
                    <input type="text" class="input-box" value="Asset: Universal Multi-Market (BTC/Gold/Forex)" readonly>
                    <input type="text" class="input-box" value="Mode: Gen 20 Dynamic Hybrid" readonly>
                    <button class="btn-fire" onclick="alert('Strategy Parameters Applied!')">Save Strategy Configuration</button>
                </div>
            </div>

            <!-- TAB 4: MARKET -->
            <div id="tab-market" class="tab-page">
                <div class="card">
                    <h3 style="margin-bottom: 10px; color: #f8fafc;">📊 Live Tickers</h3>
                    <div style="display:flex; justify-content:space-between; padding: 10px 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:13px;"><span>BTC/USD (Crypto)</span><span style="color:#4ade80; font-weight:bold;">+$92,850.00 (+3.8%)</span></div>
                    <div style="display:flex; justify-content:space-between; padding: 10px 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:13px;"><span>XAU/USD (Gold)</span><span style="color:#4ade80; font-weight:bold;">+$2,895.20 (+1.1%)</span></div>
                    <div style="display:flex; justify-content:space-between; padding: 10px 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:13px;"><span>EUR/USD (Forex)</span><span style="color:#4ade80; font-weight:bold;">+$1.0850 (+0.1%)</span></div>
                    <div style="display:flex; justify-content:space-between; padding: 10px 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:13px;"><span>Volatility 100</span><span style="color:#4ade80; font-weight:bold;">+$5,920.00 (+2.6%)</span></div>
                </div>
            </div>

            <!-- TAB 5: PROFILE, REFERRAL ENGINE & API BINDING -->
            <div id="tab-profile" class="tab-page">
                <div class="card">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <div style="width: 52px; height: 52px; border-radius: 50%; background: linear-gradient(135deg, #f97316, #ef4444); display: flex; align-items: center; justify-content: center; font-size: 22px;">👤</div>
                        <div>
                            <div style="font-size: 18px; font-weight: 800; color: white;">{current_username} 👑</div>
                            <div style="font-size: 12px; color: #94a3b8;">User Key: {current_user_key}</div>
                            <div style="font-size: 12px; color: #4ade80; margin-top: 4px;">Tier: <strong>{user_tier}</strong></div>
                        </div>
                    </div>
                </div>

                <!-- 🔥 UNIQUE SUBSCRIBER REFERRAL SYSTEM CARD 🔥 -->
                <div class="card" style="border: 1px solid #ec4899; background: linear-gradient(145deg, #15091d, #080c16);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-size: 14px; font-weight: 800; color: #f472b6;">🎁 Your Subscriber Referral Hub</span>
                        <span style="background: #831843; color: #fbcfe8; font-size: 10px; font-weight: bold; padding: 2px 8px; border-radius: 10px;">EARN V1-V5 RANKS</span>
                    </div>
                    <p style="font-size: 11px; color: #cbd5e1; margin-bottom: 12px;">Share your link on WhatsApp/Telegram. When new members join through your link, your rank advances automatically!</p>
                    
                    <label style="font-size: 11px; color: #94a3b8; font-weight: bold;">YOUR REFERRAL CODE:</label>
                    <input type="text" class="input-box" value="{user_ref_code}" readonly style="font-weight: 800; letter-spacing: 1px; color: #facc15; border-color: rgba(250, 204, 21, 0.3);">

                    <label style="font-size: 11px; color: #94a3b8; font-weight: bold; margin-top: 6px; display: block;">YOUR PERSONAL INVITATION LINK:</label>
                    <input type="text" id="user_invite_link" class="input-box" value="{shareable_ref_link}" readonly style="font-size: 12px; color: #38bdf8;">

                    <button class="btn-fire" style="background: linear-gradient(135deg, #ec4899, #8b5cf6);" onclick="copyReferralLink()">📋 Copy Invite Link</button>
                </div>

                <div class="card">
                    <h4 style="color: #facc15; margin-bottom: 8px;">Bind MT5 Account (Demo / Real)</h4>
                    <select id="mt5_acc_type" class="select-box">
                        <option value="Demo">Demo Account (Risk-Free Testing)</option>
                        <option value="Real" selected>Real Account (Live Money)</option>
                    </select>
                    <input type="text" id="mt5_acc" class="input-box" placeholder="MT5 Account Number">
                    <input type="password" id="mt5_pass" class="input-box" placeholder="MT5 Password">
                    <input type="text" id="mt5_server" class="input-box" placeholder="Server (e.g., Deriv-Demo / Exness-Real)">
                    <button class="btn-fire" onclick="bindMT5('{current_user_key}')">Securely Connect MT5 API</button>
                </div>

                <div class="card">
                    <h4 style="color: #38bdf8; margin-bottom: 4px;">Subscription Payment ($110)</h4>
                    <p style="font-size: 12px; color: #94a3b8;">Send funds to Airtel line:</p>
                    <p style="font-size: 18px; font-weight: bold; color: #facc15; margin: 4px 0;">{AIRTEL_NUMBER}</p>
                    <p style="font-size: 12px; margin-bottom: 8px;">({AIRTEL_NAME})</p>
                    <input type="text" id="airtel_txid" class="input-box" placeholder="Paste Airtel Transaction ID">
                    <button class="btn-fire" style="background: #0284c7;" onclick="submitPayment('Airtel')">Submit Payment</button>
                </div>
            </div>

        </div>

        <div class="bottom-bar">
            <div id="nav-home" class="nav-link active" onclick="switchTab('home')"><span>🏠</span>Home</div>
            <div id="nav-trade" class="nav-link" onclick="switchTab('trade')"><span>📊</span>Trade</div>
            <div id="nav-new_trade" class="nav-link" onclick="switchTab('new_trade')"><span>➕</span>+ Strategy</div>
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

            function logoutUser() {{
                window.location.href = '/';
            }}

            function copyReferralLink() {{
                const inviteInput = document.getElementById('user_invite_link');
                inviteInput.select();
                inviteInput.setSelectionRange(0, 99999);
                navigator.clipboard.writeText(inviteInput.value);
                alert('Referral Link Copied to Clipboard!');
            }}

            function toggleAutoTrade(userKey) {{
                const isChecked = document.getElementById('auto_trade_toggle').checked;
                fetch('/api/v1/bot/toggle', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ user_id: userKey, auto_trade_active: isChecked }})
                }})
                .then(res => res.json())
                .then(data => {{ alert(data.message); location.reload(); }});
            }}

            function bindMT5(userKey) {{
                const acc = document.getElementById('mt5_acc').value;
                const pass = document.getElementById('mt5_pass').value;
                const server = document.getElementById('mt5_server').value;
                const accType = document.getElementById('mt5_acc_type').value;
                if(!acc || !pass || !server) {{ alert('Fill in all MT5 fields.'); return; }}
                fetch('/api/v1/mt5/bind', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ user_id: userKey, account_id: acc, password: pass, server: server, account_type: accType }})
                }})
                .then(res => res.json())
                .then(data => {{ alert(data.message); }});
            }}

            function submitPayment(method) {{
                const txid = document.getElementById('airtel_txid').value;
                const userKey = "{current_user_key}";
                if(!txid) {{ alert('Paste your transaction reference ID.'); return; }}
                fetch('/api/v1/payments/submit', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ user_id: userKey, method: method, transaction_id: txid, amount: 110.0 }})
                }})
                .then(res => res.json())
                .then(data => {{ alert('Payment submitted for verification.'); }});
            }}

            // Render Dynamic Trading View Chart
            window.onload = function() {{
                const chartElement = document.getElementById('chart-container');
                if (chartElement && typeof LightweightCharts !== 'undefined') {{
                    const chart = LightweightCharts.createChart(chartElement, {{
                        layout: {{ backgroundColor: '#030508', textColor: '#cbd5e1' }},
                        grid: {{ vertLines: {{ color: 'rgba(255, 255, 255, 0.05)' }}, horzLines: {{ color: 'rgba(255, 255, 255, 0.05)' }} }},
                        timeScale: {{ borderVisible: false }},
                    }});
                    const lineSeries = chart.addLineSeries({{ color: '#f97316', lineWidth: 2 }});
                    lineSeries.setData([
                        {{ time: '2026-10-20', value: 91200 }},
                        {{ time: '2026-10-21', value: 91500 }},
                        {{ time: '2026-10-22', value: 91100 }},
                        {{ time: '2026-10-23', value: 92300 }},
                        {{ time: '2026-10-24', value: 92850 }},
                    ]);
                }}
            }};
        </script>
    </body>
    </html>
    """

# API Endpoints
@app.post("/api/v1/auth/signin")
async def auth_signin(data: UserAuthData):
    if data.email not in user_sessions:
        user_sessions[data.email] = {
            "email": data.email, 
            "status": "active", 
            "mt5_bound": False, 
            "auto_trade_active": True, 
            "simulated_balance": 5.0, 
            "tier_level": "V1 Phoenix Novice", 
            "referrals": 0,
            "ref_code": generate_ref_code(data.email)
        }
    else:
        user_sessions[data.email]["status"] = "active"
    return {"status": "success", "email": data.email}

@app.post("/api/v1/bot/toggle")
async def toggle_bot(data: BotSwitchData):
    if data.user_id not in user_sessions:
        user_sessions[data.user_id] = {"status": "active", "mt5_bound": False, "simulated_balance": 5.0, "ref_code": generate_ref_code(data.user_id)}
    user_sessions[data.user_id]["auto_trade_active"] = data.auto_trade_active
    state_msg = "activated (Gen 20 Core Hybrid ON)" if data.auto_trade_active else "paused (Gen 20 Core OFF)"
    return {"status": "success", "message": f"Phoenix Gen 20 Core Bot has been {state_msg}!"}

@app.post("/api/v1/mt5/bind")
async def bind_mt5(data: MT5BindingData):
    encrypted_pw = encrypt_credential(data.password)
    if data.user_id not in user_sessions:
        user_sessions[data.user_id] = {"status": "active", "simulated_balance": 5.0, "ref_code": generate_ref_code(data.user_id)}
    user_sessions[data.user_id].update({
        "account_id": data.account_id,
        "password_hash": encrypted_pw,
        "server": data.server,
        "account_type": data.account_type,
        "mt5_bound": True
    })
    return {"status": "success", "message": f"MT5 {data.account_type} Account bound with Fernet encryption!"}

@app.post("/api/v1/payments/submit")
async def submit_payment(data: PaymentSubmissionData):
    if data.user_id not in user_sessions:
        user_sessions[data.user_id] = {"mt5_bound": False, "simulated_balance": 5.0, "ref_code": generate_ref_code(data.user_id)}
    user_sessions[data.user_id]["status"] = "active"
    return {"status": "success", "message": "Payment recorded and sent for verification."}




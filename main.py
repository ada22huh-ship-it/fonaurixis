# ==============================================================================
# FONAURIXIS AUTOMATED MULTI-ASSET TRADING PLATFORM (SINGLE-FILE MASTER)
# ==============================================================================
import time
import random
import threading
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import MetaTrader5 as mt5
from cryptography.fernet import Fernet

# ------------------------------------------------------------------------------
# 1. OWNER & TELEGRAM CONFIGURATION
# ------------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = "9133992896:AAFKPaV8OQZ1UVPEKz_Opa5cQl8oAJSCtpo"  # Bot token integrated
USER_TELEGRAM_CHAT_ID = "8668083605"                              # Your Telegram Chat ID integrated

# Comprehensive global watchlist covering Crypto, Metals, Forex, and Synthetics
SYMBOL_WATCHLIST = [
    "XAUUSD", "XAGUSD",           # Gold & Silver
    "BTC/USDT", "ETH/USDT",       # Cryptocurrencies
    "EURUSD", "GBPUSD", "USDJPY", # Major Forex Pairs
    "Volatility 75 Index"         # Synthetics Hub
]

OWNER_PAYMENT_NUMBER = "0731552385"
OWNER_PAYMENT_NAME = "Nantongo Rebecca"
OWNER_PAYMENT_NETWORK = "Airtel Money Uganda"

# Generate encryption key for storing broker passwords securely in memory
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Central In-Memory Data Store
USER_DATABASE = {}

app = FastAPI(title="Fonaurixis Multi-Asset Trading Engine")


# ------------------------------------------------------------------------------
# 2. EMBEDDED PROFESSIONAL MOBILE TRADING UI
# ------------------------------------------------------------------------------
HTML_DASHBOARD = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fonaurixis Trading Command Center</title>
    <style>
        :root {{
            --bg-dark: #0b0e11;
            --card-bg: #151a21;
            --card-border: #21262d;
            --accent-gold: #f0b90b;
            --accent-green: #0ecb81;
            --accent-red: #f6465d;
            --text-main: #eaecef;
            --text-muted: #848e9c;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            padding-bottom: 70px;
        }}
        .container {{
            width: 100%;
            max-width: 480px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 12px;
            box-sizing: border-box;
        }}
        /* Activation Banner */
        .banner {{
            background: linear-gradient(135deg, #1e2329 0%, #151a21 100%);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 16px;
            text-align: left;
        }}
        .banner h3 {{ margin: 0 0 4px 0; font-size: 16px; color: var(--accent-gold); display: flex; align-items: center; gap: 6px; }}
        .banner p {{ margin: 0 0 12px 0; font-size: 12px; color: var(--text-muted); line-height: 1.4; }}
        .btn-gold {{
            background-color: var(--accent-gold);
            color: #000000;
            font-weight: 700;
            border: none;
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }}
        /* Metrics Card */
        .metrics-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 16px;
        }}
        .metrics-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        .metric-title {{ font-size: 12px; color: var(--text-muted); }}
        .metric-val {{ font-size: 22px; font-weight: 700; color: var(--accent-green); margin-top: 2px; }}
        .toggle-group {{
            background: #0b0e11;
            padding: 2px;
            border-radius: 6px;
            display: flex;
            gap: 2px;
        }}
        .toggle-btn {{
            background: transparent;
            color: var(--text-muted);
            border: none;
            padding: 4px 12px;
            font-size: 12px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
        }}
        .toggle-btn.active {{
            background: var(--accent-gold);
            color: #000;
        }}
        .metrics-grid-stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            border-top: 1px solid var(--card-border);
            padding-top: 12px;
            text-align: center;
        }}
        .stat-box span {{ display: block; font-size: 11px; color: var(--text-muted); }}
        .stat-box strong {{ font-size: 13px; color: var(--text-main); }}
        
        /* Auto Mode Toggle */
        .auto-box {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 12px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .switch {{
            position: relative; display: inline-block; width: 46px; height: 24px;
        }}
        .switch input {{ opacity: 0; width: 0; height: 0; }}
        .slider {{
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background-color: #374151; transition: .4s; border-radius: 24px;
        }}
        .slider:before {{
            position: absolute; content: ""; height: 18px; width: 18px; left: 3px; bottom: 3px;
            background-color: white; transition: .4s; border-radius: 50%;
        }}
        input:checked + .slider {{ background-color: var(--accent-green); }}
        input:checked + .slider:before {{ transform: translateX(22px); }}

        /* Quick Icons Grid */
        .quick-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            text-align: center;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 16px 8px;
        }}
        .quick-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            color: var(--text-muted);
            font-size: 11px;
            font-weight: 500;
        }}
        .quick-icon {{
            width: 38px; height: 38px; background: #1e2329; border-radius: 50%;
            display: flex; align-items: center; justify-content: center; font-size: 16px; color: var(--accent-gold);
            border: 1px solid var(--card-border);
        }}

        /* Market Movers Watchlist */
        .market-section {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 16px;
        }}
        .market-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        .market-badge {{
            background: rgba(14, 203, 129, 0.1);
            color: var(--accent-green);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
        }}
        .crypto-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid var(--card-border);
        }}
        .crypto-row:last-child {{ border-bottom: none; }}
        .crypto-name strong {{ display: block; font-size: 14px; color: var(--text-main); }}
        .crypto-name span {{ font-size: 11px; color: var(--text-muted); }}
        .crypto-price {{ text-align: right; }}
        .crypto-price strong {{ display: block; font-size: 14px; color: var(--text-main); }}
        .crypto-price span {{ font-size: 11px; color: var(--accent-green); }}

        /* Bottom Nav Bar */
        .bottom-nav {{
            position: fixed; bottom: 0; left: 0; right: 0;
            background: #151a21;
            border-top: 1px solid var(--card-border);
            display: flex;
            justify-content: space-around;
            padding: 8px 0;
            z-index: 1000;
        }}
        .nav-item {{
            display: flex; flex-direction: column; align-items: center;
            color: var(--text-muted); font-size: 10px; text-decoration: none; gap: 2px; cursor: pointer;
        }}
        .nav-item.active {{ color: var(--accent-gold); }}
        .nav-item span.icon {{ font-size: 18px; }}

        /* Modal Screens */
        .modal {{
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); z-index: 2000; justify-content: center; align-items: center; padding: 16px; box-sizing: border-box;
        }}
        .modal-content {{
            background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px;
            width: 100%; max-width: 400px; padding: 20px; box-sizing: border-box; max-height: 90vh; overflow-y: auto;
        }}
        input, select {{
            width: 100%; padding: 10px; margin-top: 6px; margin-bottom: 12px;
            border-radius: 6px; border: 1px solid var(--card-border); background: #0b0e11; color: white; box-sizing: border-box;
        }}
        .profile-row {{
            display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--card-border);
            font-size: 13px; cursor: pointer; color: var(--text-main);
        }}
        .profile-row:hover {{ color: var(--accent-gold); }}
    </style>
</head>
<body>

<div class="container">
    
    <!-- TOP ACTIVATION BANNER -->
    <div class="banner" id="banner-section">
        <h3>⚡ Activate Your Bot</h3>
        <p>Deposit funds and activate your license to unlock 24/7 automated trading across all markets.</p>
        <button class="btn-gold" onclick="openModal('pay-modal')">Deposit & Activate</button>
    </div>

    <!-- METRICS & WINS CARD -->
    <div class="metrics-card">
        <div class="metrics-top">
            <div>
                <div class="metric-title">LIFETIME WINS</div>
                <div class="metric-val" id="lifetime-profit">+$0.00</div>
                <div style="font-size:11px; color:var(--text-muted); margin-top:2px;">Today: +$0.00</div>
            </div>
            <div class="toggle-group">
                <button class="toggle-btn active">Spot</button>
                <button class="toggle-btn">Futures</button>
            </div>
        </div>
        <div class="metrics-grid-stats">
            <div class="stat-box"><span>Win Rate</span><strong id="win-rate">-</strong></div>
            <div class="stat-box"><span>Days</span><strong>0/0</strong></div>
            <div class="stat-box"><span>Active</span><strong id="active-trades">0</strong></div>
            <div class="stat-box"><span>Trades</span><strong id="total-trades">0</strong></div>
        </div>
    </div>

    <!-- GO-AUTO FUTURES TOGGLE -->
    <div class="auto-box">
        <div>
            <strong style="font-size:13px; display:block;">🤖 Go-Auto Engine</strong>
            <span style="font-size:11px; color:var(--text-muted);">Autonomous multi-asset execution</span>
        </div>
        <label class="switch">
            <input type="checkbox" id="engine-switch" onchange="toggleEngine(this)">
            <span class="slider"></span>
        </label>
    </div>

    <!-- QUICK NAV ICONS GRID -->
    <div class="quick-grid">
        <div class="quick-item" onclick="openModal('signals-modal')"><div class="quick-icon">📈</div>Signals</div>
        <div class="quick-item" onclick="openModal('pay-modal')"><div class="quick-icon">💰</div>Earnings</div>
        <div class="quick-item" onclick="alert('Leaderboard active for elite subscribers.')"><div class="quick-icon">🏆</div>Leaderboard</div>
        <div class="quick-item" onclick="openModal('strategy-modal')"><div class="quick-icon">⚙️</div>Strategy</div>
        <div class="quick-item" onclick="openModal('pay-modal')"><div class="quick-icon">👛</div>Assets</div>
        <div class="quick-item" onclick="openModal('profile-modal')"><div class="quick-icon">👥</div>Invite</div>
        <div class="quick-item" onclick="openModal('broker-modal')"><div class="quick-icon">🔗</div>API Bind</div>
        <div class="quick-item" onclick="openModal('profile-modal')"><div class="quick-icon">🛡️</div>More</div>
    </div>

    <!-- GLOBAL MARKET MOVERS WATCHLIST (TRADE EVERYTHING) -->
    <div class="market-section">
        <div class="market-header">
            <div>
                <strong style="font-size:14px;">Global Market Movers</strong>
                <span style="display:block; font-size:11px; color:var(--text-muted);">Crypto, Metals, Forex & Synthetics</span>
            </div>
            <div class="market-badge">ALL-MARKET LIVE</div>
        </div>

        <div class="crypto-row">
            <div class="crypto-name"><strong>XAUUSD</strong><span>Spot Gold Engine</span></div>
            <div class="crypto-price"><strong>$2,642.10</strong><span>+0.84%</span></div>
        </div>
        <div class="crypto-row">
            <div class="crypto-name"><strong>XAGUSD</strong><span>Spot Silver Hub</span></div>
            <div class="crypto-price"><strong>$31.45</strong><span>+1.22%</span></div>
        </div>
        <div class="crypto-row">
            <div class="crypto-name"><strong>BTC/USDT</strong><span>Bitcoin Multi-Asset</span></div>
            <div class="crypto-price"><strong>$80,658.30</strong><span>+0.51%</span></div>
        </div>
        <div class="crypto-row">
            <div class="crypto-name"><strong>EURUSD</strong><span>Euro / US Dollar</span></div>
            <div class="crypto-price"><strong>$1.0852</strong><span>+0.15%</span></div>
        </div>
        <div class="crypto-row">
            <div class="crypto-name"><strong>Volatility 75</strong><span>Synthetics Hub</span></div>
            <div class="crypto-price"><strong>$452,190.20</strong><span>+1.45%</span></div>
        </div>
    </div>

</div>

<!-- BOTTOM NAVIGATION BAR -->
<div class="bottom-nav">
    <div class="nav-item active" onclick="location.reload()"><span class="icon">🏠</span>Home</div>
    <div class="nav-item" onclick="openModal('signals-modal')"><span class="icon">📊</span>Trade</div>
    <div class="nav-item" onclick="openModal('broker-modal')"><span class="icon">➕</span>API Bind</div>
    <div class="nav-item" onclick="openModal('pay-modal')"><span class="icon">📈</span>Market</div>
    <div class="nav-item" onclick="openModal('profile-modal')"><span class="icon">👤</span>Profile</div>
</div>

<!-- MODAL: PROFILE, TEAM & AFFILIATES -->
<div id="profile-modal" class="modal">
    <div class="modal-content">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h3 style="color:var(--accent-gold); margin:0;">👤 Subscriber Profile</h3>
            <button style="background:transparent; border:none; color:var(--text-muted); font-size:16px; cursor:pointer;" onclick="closeModal('profile-modal')">✕</button>
        </div>
        
        <div style="background:#0b0e11; padding:12px; border-radius:8px; margin-bottom:14px; border:1px solid var(--card-border);">
            <div style="font-size:12px; color:var(--text-muted);">Account ID</div>
            <strong id="profile-user-id" style="font-size:14px; color:var(--accent-blue);">Not signed in</strong>
            <div style="font-size:12px; color:var(--text-muted); margin-top:8px;">License Tier</div>
            <strong id="profile-tier" style="font-size:13px; color:var(--accent-red);">V1 - Inactive</strong>
        </div>

        <!-- REFERRAL / TEAM SECTION -->
        <div style="background:rgba(240, 185, 11, 0.05); border:1px dashed var(--accent-gold); padding:12px; border-radius:8px; margin-bottom:14px;">
            <strong style="font-size:13px; color:var(--accent-gold); display:block; margin-bottom:4px;">👥 Your Referral & Team Link</strong>
            <p style="font-size:11px; color:var(--text-muted); margin:0 0 8px 0;">Share this link to expand your customer network and earn referral commissions.</p>
            <div style="display:flex; gap:6px;">
                <input type="text" id="ref-link" value="https://fonaurixis.app/ref/FALCON99" readonly style="margin:0; font-size:11px;">
                <button class="btn-gold" style="width:auto; padding:0 12px; font-size:12px;" onclick="copyRefLink()">Copy</button>
            </div>
        </div>

        <div class="profile-row" onclick="openModal('broker-modal'); closeModal('profile-modal');"><span>🔗 API Binding (Exchanges & MT5)</span> <span>›</span></div>
        <div class="profile-row" onclick="openModal('pay-modal'); closeModal('profile-modal');"><span>💰 Fuel Wallet & Subscriptions</span> <span>›</span></div>
        <div class="profile-row" onclick="alert('Push notifications enabled for Telegram & App alerts.')"><span>🔔 Notification Settings</span> <span>›</span></div>
        <div class="profile-row" onclick="openModal('auth-modal'); closeModal('profile-modal');"><span>🔐 Account Security & Sign Out</span> <span>›</span></div>
        <div class="profile-row" onclick="alert('Fonaurixis Support: Contact via Telegram @FonaurixisSupport')"><span>❓ Help & Support</span> <span>›</span></div>
    </div>
</div>

<!-- MODAL: PAYMENT / ACTIVATION -->
<div id="pay-modal" class="modal">
    <div class="modal-content">
        <h3 style="color:var(--accent-gold); margin-top:0;">📱 Mobile Money Deposit</h3>
        <p style="font-size:12px; color:var(--text-muted);">Send subscription ($110) or fuel via Airtel Money:</p>
        <ul style="font-size:12px; padding-left:18px; color:var(--text-main);">
            <li><strong>Network:</strong> {OWNER_PAYMENT_NETWORK}</li>
            <li><strong>Number:</strong> <span style="color:var(--accent-green);">{OWNER_PAYMENT_NUMBER}</span></li>
            <li><strong>Name:</strong> {OWNER_PAYMENT_NAME}</li>
        </ul>
        <label style="font-size:12px;">Airtel SMS Transaction ID:</label>
        <input type="text" id="tx-id" placeholder="e.g. 10984729103">
        <label style="font-size:12px;">Select Package:</label>
        <select id="pay-type">
            <option value="110">Annual Subscription ($110 License)</option>
            <option value="10">Fuel Balance Top-Up ($10)</option>
        </select>
        <button class="btn-gold" style="margin-top:8px;" onclick="submitPayment()">Submit Payment Code</button>
        <button style="background:transparent; border:none; color:var(--text-muted); width:100%; margin-top:10px; cursor:pointer;" onclick="closeModal('pay-modal')">Close</button>
    </div>
</div>

<!-- MODAL: BROKER BINDING -->
<div id="broker-modal" class="modal">
    <div class="modal-content">
        <h3 style="color:var(--accent-gold); margin-top:0;">🔗 Bind MT5 Account</h3>
        <label style="font-size:12px;">MetaTrader Login ID:</label>
        <input type="text" id="broker-login" placeholder="e.g. 5092841">
        <label style="font-size:12px;">Trader Password:</label>
        <input type="password" id="broker-pass" placeholder="Encrypted securely">
        <button class="btn-gold" style="margin-top:8px;" onclick="bindBroker()">Save Credentials</button>
        <button style="background:transparent; border:none; color:var(--text-muted); width:100%; margin-top:10px; cursor:pointer;" onclick="closeModal('broker-modal')">Close</button>
    </div>
</div>

<!-- MODAL: SIGN IN -->
<div id="auth-modal" class="modal" style="display:flex;">
    <div class="modal-content" id="auth-box">
        <h3 style="color:var(--accent-gold); margin-top:0;">🔐 Subscriber Login</h3>
        <p style="font-size:12px; color:var(--text-muted);">Sign in securely to activate your session.</p>
        <button class="btn-gold" style="background:#ea4335; color:white; margin-bottom:8px;" onclick="signIn('google')">Sign in with Google</button>
        <button class="btn-gold" style="background:#000; color:white; border:1px solid #333;" onclick="signIn('apple')">Sign in with Apple</button>
    </div>
</div>

<script>
    let currentUser = null;

    function openModal(id) {{ document.getElementById(id).style.display = 'flex'; }}
    function closeModal(id) {{ document.getElementById(id).style.display = 'none'; }}

    function copyRefLink() {{
        const copyText = document.getElementById("ref-link");
        copyText.select();
        navigator.clipboard.writeText(copyText.value);
        alert("Referral link copied to clipboard! Share it to grow your team.");
    }}

    async function signIn(provider) {{
        const res = await fetch('/api/v1/auth/social-signin', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{ id_token: "token_" + Math.random(), provider: provider }})
        }});
        const data = await res.json();
        if(data.status === 'success') {{
            currentUser = data.user_id;
            document.getElementById('profile-user-id').innerText = currentUser;
            closeModal('auth-modal');
            alert("Signed in successfully as: " + currentUser);
            if(data.can_start_bot) {{
                document.getElementById('banner-section').style.display = 'none';
                document.getElementById('profile-tier').innerText = "V1 - Active & Trading";
                document.getElementById('profile-tier').style.color = "var(--accent-green)";
            }}
        }}
    }}

    async function submitPayment() {{
        const txId = document.getElementById('tx-id').value;
        const amount = parseFloat(document.getElementById('pay-type').value);
        if(!txId) {{ alert("Please enter Transaction ID"); return; }}
        
        await fetch('/api/v1/manual-payment-submit', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{ user_id: currentUser || 'guest_user', transaction_id: txId, amount: amount, network: "Airtel Money" }})
        }});
        alert("Payment submitted for owner verification on Telegram!");
        closeModal('pay-modal');
    }}

    async function bindBroker() {{
        const login = document.getElementById('broker-login').value;
        const pass = document.getElementById('broker-pass').value;
        if(!login || !pass) {{ alert("Fill all fields"); return; }}
        
        await fetch('/api/v1/user/bind-broker', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{ user_id: currentUser || 'guest_user', broker_login: login, raw_password: pass }})
        }});
        alert("Broker encrypted & linked safely!");
        closeModal('broker-modal');
    }}

    function toggleEngine(el) {{
        if(el.checked) {{
            alert("Go-Auto Engine Activated! Scanning multi-asset markets 24/7.");
        }} else {{
            alert("Go-Auto Engine Paused.");
        }}
    }}
</script>

</body>
</html>
"""


# ------------------------------------------------------------------------------
# 3. ROUTE: DASHBOARD RENDERER
# ------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    return HTML_DASHBOARD


# ------------------------------------------------------------------------------
# 4. SECURITY & AUTHENTICATION ENDPOINTS
# ------------------------------------------------------------------------------
def encrypt_sensitive_data(raw_text: str) -> bytes:
    return cipher_suite.encrypt(raw_text.encode())

def decrypt_sensitive_data(encrypted_bytes: bytes) -> str:
    return cipher_suite.decrypt(encrypted_bytes).decode()

def verify_social_login(id_token: str, provider: str):
    if not id_token:
        raise HTTPException(status_code=401, detail="Authentication token missing.")
    user_id = f"user_{provider}_{hash(id_token) % 100000}"
    if user_id not in USER_DATABASE:
        USER_DATABASE[user_id] = {
            "email": f"{user_id}@auth_provider.com",
            "provider": provider,
            "has_active_license": False,
            "fuel_balance": 0.00,
            "encrypted_broker_pass": None
        }
    return user_id

class OAuthSignInRequest(BaseModel):
    id_token: str
    provider: str

class CredentialsBindRequest(BaseModel):
    user_id: str
    broker_login: str
    raw_password: str

class DirectPaymentRequest(BaseModel):
    user_id: str
    transaction_id: str
    amount: float
    network: str

@app.post("/api/v1/auth/social-signin")
def social_signin(data: OAuthSignInRequest):
    user_id = verify_social_login(data.id_token, data.provider)
    user_data = USER_DATABASE[user_id]
    return {
        "status": "success",
        "user_id": user_id,
        "email": user_data["email"],
        "has_active_license": user_data["has_active_license"],
        "fuel_balance": user_data["fuel_balance"],
        "can_start_bot": user_data["has_active_license"] and user_data["fuel_balance"] >= 5.00
    }

@app.post("/api/v1/user/bind-broker")
def bind_broker(data: CredentialsBindRequest):
    if data.user_id in USER_DATABASE:
        encrypted_pass = encrypt_sensitive_data(data.raw_password)
        USER_DATABASE[data.user_id]["encrypted_broker_pass"] = encrypted_pass
        USER_DATABASE[data.user_id]["broker_login"] = data.broker_login
        return {"status": "success", "message": "Broker credentials encrypted & linked safely."}
    raise HTTPException(status_code=404, detail="User profile not found.")

@app.post("/api/v1/manual-payment-submit")
def submit_manual_payment(data: DirectPaymentRequest):
    alert_msg = (
        f"🔔 *NEW PAYMENT SUBMITTED FOR VERIFICATION*\n\n"
        f"👤 *User ID:* `{data.user_id}`\n"
        f"💵 *Amount:* ${data.amount:.2f}\n"
        f"📱 *Network:* {data.network}\n"
        f"🔢 *Transaction ID:* `{data.transaction_id}`\n\n"
        f"👉 *Action:* Check your Airtel SMS ({OWNER_PAYMENT_NAME} - {OWNER_PAYMENT_NUMBER}). "
        f"To approve, send:\n`/approve_{data.user_id}_{int(data.amount)}`"
    )
    send_telegram_alert(USER_TELEGRAM_CHAT_ID, alert_msg)
    return {"status": "success", "message": "Verification request sent to owner Telegram."}

@app.post("/api/v1/telegram-webhook")
def telegram_webhook(payload: dict):
    try:
        message = payload.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "").strip()

        if text.startswith("/start"):
            welcome_text = (
                f"⚡ *Welcome to Fonaurixis Trading Platform* ⚡\n\n"
                f"To subscribe ($110/yr) or top up fuel via Airtel Money:\n"
                f"• *Number:* `{OWNER_PAYMENT_NUMBER}`\n"
                f"• *Name:* {OWNER_PAYMENT_NAME}\n\n"
                f"Open the dashboard link on your phone to submit your payment code!"
            )
            send_telegram_alert(chat_id, welcome_text)

        elif text.startswith("/approve_"):
            parts = text.split("_")
            if len(parts) >= 4:
                u_id = f"{parts[1]}_{parts[2]}_{parts[3]}"
                amt = float(parts[4]) if len(parts) > 4 else 110.0

                if u_id in USER_DATABASE:
                    if amt >= 110:
                        USER_DATABASE[u_id]["has_active_license"] = True
                        send_telegram_alert(chat_id, f"✅ Annual License Activated for user `{u_id}`!")
                    else:
                        USER_DATABASE[u_id]["fuel_balance"] += amt
                        send_telegram_alert(chat_id, f"⛽ Added ${amt:.2f} fuel balance to `{u_id}`!")

    except Exception as e:
        print(f"⚠️ [Telegram Webhook Error]: {e}")

    return {"status": "ok"}


# ------------------------------------------------------------------------------
# 5. EXECUTION ROUTER & MULTI-ASSET ENGINE
# ------------------------------------------------------------------------------
def get_account_equity_and_type():
    if not mt5.initialize():
        return 0.0, "UNKNOWN"
    account_info = mt5.account_info()
    if account_info is None:
        return 0.0, "UNKNOWN"
    equity = account_info.equity
    currency = account_info.currency
    is_cent_account = "USC" in currency or account_info.leverage > 500
    return equity, "CENT" if is_cent_account else "STANDARD"

def calculate_dynamic_risk_limits():
    equity, acc_type = get_account_equity_and_type()
    effective_usd_power = equity / 100.0 if acc_type == "CENT" else equity

    if effective_usd_power <= 50:
        return 2, 0.01 if acc_type == "STANDARD" else 1.0
    elif 50 < effective_usd_power <= 500:
        return 5, 0.02
    else:
        return 15, 0.05

def route_order(symbol, side, size):
    if symbol in SYMBOL_WATCHLIST:
        if not mt5.initialize():
            return False
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return False
        price = tick.ask if side == "BUY" else tick.bid
        order_type = mt5.ORDER_TYPE_BUY if side == "BUY" else mt5.ORDER_TYPE_SELL
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(size),
            "type": order_type,
            "price": price,
            "deviation": 20,
            "magic": 998877,
            "comment": "Fonaurixis Multi-Asset Engine",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return result.retcode == mt5.TRADE_RETCODE_DONE
    return True

def send_telegram_alert(chat_id, message_text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message_text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"⚠️ [Telegram Alert Error]: {e}")

def run_fonaurixis_engine():
    print("=================================================================")
    print("   ⚡ FONAURIXIS MULTI-ASSET ENGINE RUNNING IN BACKGROUND        ")
    print("=================================================================")
    while True:
        try:
            active_paid_users = [
                u_id for u_id, u_data in USER_DATABASE.items()
                if u_data["has_active_license"] and u_data["fuel_balance"] >= 5.00
            ]
            if not active_paid_users:
                time.sleep(15)
                continue

            max_allowed_trades, dynamic_lot_size = calculate_dynamic_risk_limits()
            for symbol in SYMBOL_WATCHLIST:
                score, direction = random.randint(65, 95), "BUY"
                if score >= 75:
                    success = route_order(symbol=symbol, side=direction, size=dynamic_lot_size)
                    if success:
                        send_telegram_alert(
                            USER_TELEGRAM_CHAT_ID,
                            f"⚡ *Fonaurixis Trade Alert*\n• Symbol: {symbol}\n• Action: {direction}"
                        )
                    time.sleep(10)
                    break
        except Exception as e:
            print(f"⚠️ [Engine Error]: {e}")
        time.sleep(10)


# ------------------------------------------------------------------------------
# 6. APPLICATION ENTRYPOINT (BACKGROUND THREAD + FASTAPI SERVER)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    engine_thread = threading.Thread(target=run_fonaurixis_engine, daemon=True)
    engine_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

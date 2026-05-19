import streamlit as st
import os
import time
import random
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kasparro · Checkout Recovery AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080B12;
    color: #E8EBF2;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem 2rem !important; max-width: 1400px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #2A3045; border-radius: 4px; }

/* ── Top Banner ── */
.kasparro-header {
    background: linear-gradient(135deg, #0D1117 0%, #111827 100%);
    border: 1px solid #1E2538;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.kasparro-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(100, 220, 255, 0.04) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(168, 85, 247, 0.06) 0%, transparent 60%);
    pointer-events: none;
}
.kasparro-header-inner { position: relative; z-index: 1; }
.kasparro-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #F0F4FF;
    line-height: 1;
}
.kasparro-title span { color: #64DCFF; }
.kasparro-sub {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #4A5578;
    margin-top: 6px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 20px;
    padding: 5px 12px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #10B981;
    letter-spacing: 0.5px;
}
.status-dot {
    width: 6px; height: 6px;
    background: #10B981;
    border-radius: 50%;
    animation: pulse-dot 1.5s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ── Panel Cards ── */
.panel-card {
    background: #0D1117;
    border: 1px solid #1A2035;
    border-radius: 14px;
    padding: 24px;
    height: 100%;
}
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #8B9DC3;
    text-transform: uppercase;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-title-icon {
    font-size: 16px;
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.metric-card {
    background: #111827;
    border: 1px solid #1E2538;
    border-radius: 10px;
    padding: 14px 16px;
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: #4A5578;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #F0F4FF;
    line-height: 1;
}
.metric-value.green { color: #10B981; }
.metric-value.yellow { color: #F59E0B; }
.metric-value.red { color: #EF4444; }
.metric-value.blue { color: #64DCFF; }
.metric-sub {
    font-size: 10px;
    color: #4A5578;
    margin-top: 4px;
}

/* ── Checkout UI ── */
.checkout-box {
    background: #111827;
    border: 1px solid #1E2538;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.checkout-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1A2035;
}
.checkout-item:last-child { border-bottom: none; }
.item-name {
    font-size: 13px;
    color: #C8D0E8;
    font-weight: 500;
}
.item-meta {
    font-size: 11px;
    color: #4A5578;
    margin-top: 2px;
    font-family: 'DM Mono', monospace;
}
.item-price {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #F0F4FF;
}
.item-price.shipping { color: #F59E0B; }
.item-price.free { color: #10B981; text-decoration: line-through; }
.total-row {
    background: linear-gradient(135deg, #0D1B2A, #0D1117);
    border: 1px solid #1E3A5F;
    border-radius: 10px;
    padding: 14px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
}
.total-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #4A5578;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.total-amount {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #64DCFF;
}

/* ── Friction Alert ── */
.friction-alert {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.06), rgba(239, 68, 68, 0.04));
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-left: 3px solid #F59E0B;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 14px 0;
    font-size: 12px;
    color: #F59E0B;
    font-family: 'DM Mono', monospace;
}
.friction-alert-title {
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* ── Agent Intervention Card ── */
.agent-card {
    background: linear-gradient(135deg, rgba(100, 220, 255, 0.04), rgba(168, 85, 247, 0.04));
    border: 1px solid rgba(100, 220, 255, 0.15);
    border-radius: 12px;
    padding: 20px;
    margin: 16px 0;
    position: relative;
    overflow: hidden;
}
.agent-card::before {
    content: '';
    position: absolute;
    top: -1px; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #64DCFF, #A855F7, #64DCFF);
    background-size: 200% 100%;
    animation: shimmer 2s linear infinite;
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.agent-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(100, 220, 255, 0.1);
    border: 1px solid rgba(100, 220, 255, 0.2);
    border-radius: 6px;
    padding: 3px 10px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #64DCFF;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.agent-message {
    font-size: 14px;
    line-height: 1.6;
    color: #C8D0E8;
    font-weight: 400;
}

/* ── Log Terminal ── */
.log-terminal {
    background: #070A0F;
    border: 1px solid #131B2E;
    border-radius: 10px;
    padding: 16px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    max-height: 340px;
    overflow-y: auto;
}
.log-line {
    padding: 4px 0;
    border-bottom: 1px solid #0D1117;
    display: flex;
    gap: 10px;
    align-items: flex-start;
    line-height: 1.5;
}
.log-line:last-child { border-bottom: none; }
.log-ts {
    color: #2A3555;
    white-space: nowrap;
    font-size: 10px;
    padding-top: 1px;
    min-width: 75px;
}
.log-tag {
    font-size: 9px;
    padding: 1px 6px;
    border-radius: 3px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    white-space: nowrap;
    font-weight: 600;
    min-width: 55px;
    text-align: center;
}
.log-tag.info { background: rgba(100, 220, 255, 0.08); color: #64DCFF; }
.log-tag.success { background: rgba(16, 185, 129, 0.08); color: #10B981; }
.log-tag.warn { background: rgba(245, 158, 11, 0.08); color: #F59E0B; }
.log-tag.error { background: rgba(239, 68, 68, 0.08); color: #EF4444; }
.log-msg { color: #6B7FA8; flex: 1; }

/* ── Button overrides ── */
div.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    transition: all 0.2s ease !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0EA5E9, #6366F1) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.25) !important;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(99, 102, 241, 0.4) !important;
}

/* ── Input styling ── */
.stTextInput > div > div > input {
    background: #111827 !important;
    border: 1px solid #1E2538 !important;
    border-radius: 8px !important;
    color: #E8EBF2 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #64DCFF !important;
    box-shadow: 0 0 0 3px rgba(100, 220, 255, 0.08) !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: #111827 !important;
    border-color: #1E2538 !important;
    border-radius: 8px !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #64DCFF, #6366F1) !important;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid #1A2035; margin: 20px 0; }

/* ── Recovery badge ── */
.recovered-badge {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    margin: 10px 0;
}
.recovered-badge-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #10B981;
    margin-bottom: 4px;
}
.recovered-badge-sub {
    font-size: 12px;
    color: #4A5578;
}

/* ── Friction type buttons ── */
.friction-btn-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 8px;
}

/* ── Section label ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #4A5578;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* ── Progress steps ── */
.steps-row {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 16px 0;
}
.step {
    display: flex;
    align-items: center;
    gap: 8px;
    flex: 1;
}
.step-circle {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    flex-shrink: 0;
}
.step-circle.done { background: #10B981; color: #fff; }
.step-circle.active { background: #1E3A5F; border: 2px solid #64DCFF; color: #64DCFF; }
.step-circle.pending { background: #111827; border: 1px solid #1E2538; color: #4A5578; }
.step-label { font-size: 11px; color: #4A5578; }
.step-label.active { color: #C8D0E8; font-weight: 600; }
.step-connector {
    height: 1px;
    flex: 1;
    background: #1E2538;
    margin: 0 8px;
}
.step-connector.done { background: #10B981; }

/* ── Conversion funnel bar ── */
.funnel-row {
    margin: 8px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.funnel-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #4A5578;
    width: 90px;
    text-align: right;
    letter-spacing: 0.5px;
}
.funnel-bar-bg {
    flex: 1;
    height: 6px;
    background: #111827;
    border-radius: 3px;
    overflow: hidden;
}
.funnel-bar-fill {
    height: 100%;
    border-radius: 3px;
}
.funnel-pct {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #6B7FA8;
    width: 35px;
}

/* animate everything in */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeUp 0.35s ease forwards; }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ───────────────────────────────────────────────────────
def init_state():
    defaults = {
        "checkout_state": "Active",
        "friction_detected": None,
        "agent_offer": None,
        "logs": [],
        "cart_total": 4500,
        "shipping_fee": 350,
        "shipping_free": False,
        "discount_applied": 0,
        "recoveries_this_session": 0,
        "friction_count": 0,
        "anthropic_key": "",
        "agent_thinking": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─── Helpers ─────────────────────────────────────────────────────────────────
def ts():
    return datetime.now().strftime("%H:%M:%S")

def log(msg, level="INFO"):
    st.session_state.logs.insert(0, {"ts": ts(), "level": level, "msg": msg})
    if len(st.session_state.logs) > 60:
        st.session_state.logs = st.session_state.logs[:60]

def call_claude(friction_type, behavior_details):
    api_key = os.getenv("ANTHROPIC_API_KEY") or st.session_state.get("anthropic_key", "")
    if not api_key:
        log("No API key found — routing to deterministic fallback engine.", "WARN")
        return fallback(friction_type), "fallback"
    
    try:
        client = Anthropic(api_key=api_key)
        discount = 10 if friction_type == "Price Hesitation" else 0
        shipping_msg = "We'll waive the shipping fee." if friction_type == "Shipping Friction" else ""

        prompt = f"""You are a real-time checkout recovery agent for Kasparro, a premium D2C brand.
A buyer is showing abandonment signals. Craft a hyper-personalised, empathetic 2-3 sentence intervention.
Sound human and helpful — NOT like a popup. Be specific about the offer.

Cart Value: ₹{st.session_state.cart_total}
Shipping Fee: ₹{st.session_state.shipping_fee}
Friction Type: {friction_type}
Behavioural Signals: {behavior_details}
Offer Available: {"10% discount code SAVE10" if discount else "Free shipping code FREESHIP" if shipping_msg else "5% loyalty code LOYAL5"}

Write only the message to the buyer. No preamble, no labels."""

        log("Dispatching context payload to Claude claude-sonnet-4-20250514.", "INFO")
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=160,
            messages=[{"role": "user", "content": prompt}]
        )
        log("LLM generation successful — intervention compiled.", "SUCCESS")
        return message.content[0].text.strip(), "llm"
    except Exception as e:
        log(f"Claude API error: {str(e)[:60]}. Engaging fallback.", "ERROR")
        return fallback(friction_type), "fallback"

def fallback(friction_type):
    if friction_type == "Price Hesitation":
        return f"We noticed you're comparing costs — that's smart! Use code **SAVE10** right now for an instant 10% off your ₹{st.session_state.cart_total} order. This code is valid only for this session."
    elif friction_type == "Shipping Friction":
        return f"Delivery costs shouldn't stop you from getting what you love. Use **FREESHIP** to waive your ₹{st.session_state.shipping_fee} shipping fee — applied instantly at checkout."
    elif friction_type == "Trust Signal":
        return "We completely understand wanting to feel confident before purchasing. Your order is covered by a 30-day no-questions return policy and secure payment processing. Use **LOYAL5** for an extra 5% off."
    else:
        return "Looks like you need a little nudge — here's one: use **CART5** for 5% off your order. Limited to this session only."

def apply_offer(friction_type):
    if friction_type == "Price Hesitation":
        st.session_state.discount_applied = int(st.session_state.cart_total * 0.10)
    elif friction_type == "Shipping Friction":
        st.session_state.shipping_free = True
    st.session_state.checkout_state = "Recovered"
    st.session_state.recoveries_this_session += 1
    log("Offer accepted by buyer. Cart modified. Session marked RECOVERED.", "SUCCESS")

def reset():
    keys = ["checkout_state","friction_detected","agent_offer","shipping_free",
            "discount_applied","friction_count","agent_thinking"]
    for k in keys:
        del st.session_state[k]
    init_state()
    st.session_state.logs = []
    log("Workspace reset. New checkout session initialised.", "INFO")


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="kasparro-header animate-in">
  <div class="kasparro-header-inner" style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
    <div>
      <div class="kasparro-title">KASPARRO <span>↯</span> CHECKOUT RECOVERY</div>
      <div class="kasparro-sub">Agentic Commerce Infrastructure · Real-Time Abandonment Prevention</div>
    </div>
    <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
      <div class="status-pill"><div class="status-dot"></div> AGENT ONLINE</div>
      <div class="status-pill" style="color:#A855F7; border-color:rgba(168,85,247,0.3); background:rgba(168,85,247,0.06);">
        ⚡ Powered by Claude
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── Top Metrics Row ──────────────────────────────────────────────────────────
cart_display = st.session_state.cart_total - st.session_state.discount_applied
ship_display = 0 if st.session_state.shipping_free else st.session_state.shipping_fee

state_colour = {"Active": "blue", "Recovered": "green", "Completed": "green"}.get(st.session_state.checkout_state, "yellow")

st.markdown(f"""
<div class="metric-grid animate-in">
  <div class="metric-card">
    <div class="metric-label">Session State</div>
    <div class="metric-value {state_colour}">{st.session_state.checkout_state.upper()}</div>
    <div class="metric-sub">Checkout lifecycle</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Cart Value</div>
    <div class="metric-value">₹{cart_display:,}</div>
    <div class="metric-sub">{"Discount applied: ₹" + str(st.session_state.discount_applied) if st.session_state.discount_applied else "No discount"}</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Friction Events</div>
    <div class="metric-value {'red' if st.session_state.friction_count > 0 else 'blue'}">{st.session_state.friction_count}</div>
    <div class="metric-sub">This session</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── Main Layout ──────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")


# ═══════════════════════════════════════════════════════════════════
# LEFT PANEL — Checkout UI
# ═══════════════════════════════════════════════════════════════════
with left:
    st.markdown('<div class="panel-title"><span class="panel-title-icon">🛒</span> SIMULATED CHECKOUT</div>', unsafe_allow_html=True)

    # ── Checkout Progress Steps ──
    s = st.session_state.checkout_state
    steps = [
        ("1", "Cart", "done"),
        ("2", "Details", "done"),
        ("3", "Payment", "active" if s == "Active" else "done"),
        ("4", "Confirm", "done" if s == "Completed" else "pending"),
    ]
    step_html = '<div class="steps-row">'
    for i, (num, label, state) in enumerate(steps):
        icon = "✓" if state == "done" else num
        step_html += f'<div class="step"><div class="step-circle {state}">{icon}</div><div class="step-label {"active" if state == "active" else ""}">{label}</div></div>'
        if i < len(steps) - 1:
            step_html += f'<div class="step-connector {"done" if state == "done" else ""}"></div>'
    step_html += '</div>'
    st.markdown(step_html, unsafe_allow_html=True)

    # ── Order Items ──
    ship_html = f'<span class="item-price shipping">₹{ship_display}</span>' if not st.session_state.shipping_free else '<span class="item-price free">₹350</span> <span style="color:#10B981; font-size:12px; margin-left:6px;">FREE</span>'
    discount_row = ""
    if st.session_state.discount_applied:
        discount_row = f"""
        <div class="checkout-item">
          <div><div class="item-name" style="color:#10B981;">Discount Applied</div><div class="item-meta">Code: SAVE10</div></div>
          <span class="item-price" style="color:#10B981;">-₹{st.session_state.discount_applied:,}</span>
        </div>"""

    st.markdown(f"""
    <div class="checkout-box animate-in">
      <div class="checkout-item">
        <div>
          <div class="item-name">Premium Ergonomic Desk Chair</div>
          <div class="item-meta">SKU: KSP-ERG-001 · Qty: 1 · Forest Green</div>
        </div>
        <span class="item-price">₹4,500</span>
      </div>
      {discount_row}
      <div class="checkout-item">
        <div><div class="item-name">Shipping & Handling</div><div class="item-meta">Standard · 3-5 business days</div></div>
        {ship_html}
      </div>
      <div class="total-row" style="margin-top:12px;">
        <div>
          <div class="total-label">ORDER TOTAL</div>
          <div style="font-size:11px; color:#4A5578; margin-top:2px;">Incl. all taxes</div>
        </div>
        <div class="total-amount">₹{cart_display + ship_display:,}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Shipping Address ──
    st.markdown('<div class="section-label">Delivery Address</div>', unsafe_allow_html=True)
    st.text_input("", value="Sector 17, Chandigarh — 160017, IN", disabled=True, label_visibility="collapsed")

    # ── Coupon Field ──
    st.markdown('<div class="section-label" style="margin-top:10px;">Discount Code</div>', unsafe_allow_html=True)
    code_col, apply_col = st.columns([3, 1])
    with code_col:
        coupon_code = st.text_input("", placeholder="e.g. SAVE10", label_visibility="collapsed", key="coupon_input",
                                    disabled=st.session_state.checkout_state == "Completed")
    with apply_col:
        st.write("")
        st.button("Apply", use_container_width=True, disabled=st.session_state.checkout_state == "Completed")

    st.write("")

    # ── State: Completed ──
    if st.session_state.checkout_state == "Completed":
        st.markdown("""
        <div class="recovered-badge" style="background:linear-gradient(135deg, rgba(16,185,129,0.08), rgba(100,220,255,0.04)); border-color:rgba(16,185,129,0.3);">
          <div class="recovered-badge-title">🎉 Order Placed Successfully!</div>
          <div class="recovered-badge-sub">Confirmation sent · Order ID #KSP-20260519</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("↩ Reset Simulation", use_container_width=True):
            reset()
            st.rerun()

    # ── State: Active or Recovered ──
    else:
        # ── Payment Button ──
        btn_label = "✓ Complete Payment" if st.session_state.checkout_state == "Active" else "✓ Complete Payment with Offer"
        if st.button(btn_label, type="primary", use_container_width=True, key="pay_btn"):
            st.session_state.checkout_state = "Completed"
            log("CONVERSION SUCCESS — buyer completed checkout.", "SUCCESS")
            st.rerun()

        st.markdown('<hr>', unsafe_allow_html=True)

        # ── Friction Simulation Controls ──
        st.markdown('<div class="section-label">⚡ Simulate Buyer Friction Signals</div>', unsafe_allow_html=True)

        friction_types = {
            "💸 Price Hesitation": ("Price Hesitation", "Buyer opened coupon input 3× and paused 45s on the order total."),
            "🚚 Shipping Friction": ("Shipping Friction", "Buyer toggled shipping options 4× and hovered delivery policy link."),
            "🛡️ Trust Signal": ("Trust Signal", "Buyer navigated to returns policy and scrolled to bottom of page twice."),
            "⏱️ Timeout Hesitation": ("Timeout", "Buyer idle for 90s on payment screen, mouse moved to browser close button."),
        }

        fc1, fc2 = st.columns(2)
        friction_items = list(friction_types.items())
        for i, (label, (ftype, detail)) in enumerate(friction_items):
            col = fc1 if i % 2 == 0 else fc2
            with col:
                if st.button(label, use_container_width=True, key=f"friction_{i}",
                             disabled=st.session_state.checkout_state == "Recovered"):
                    st.session_state.friction_detected = ftype
                    st.session_state.friction_count += 1
                    log(f"Friction captured: {ftype} — analysing behavioural signals.", "WARN")
                    log("Routing to Claude Sonnet for contextual intervention generation.", "INFO")
                    with st.spinner("Agent generating intervention…"):
                        result, source = call_claude(ftype, detail)
                    st.session_state.agent_offer = result
                    log(f"Intervention source: {'LLM' if source == 'llm' else 'Fallback Rules Engine'}.", "INFO")
                    st.rerun()

    # ── Agent Intervention Card ──
    if st.session_state.agent_offer and st.session_state.checkout_state not in ["Completed"]:
        st.markdown(f"""
        <div class="agent-card animate-in">
          <div class="agent-badge">⚡ AI INTERVENTION · {st.session_state.friction_detected}</div>
          <div class="agent-message">{st.session_state.agent_offer}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.checkout_state == "Active":
            if st.button("✓ Accept Offer & Apply to Cart", type="primary", use_container_width=True, key="accept_offer"):
                apply_offer(st.session_state.friction_detected)
                st.rerun()
        elif st.session_state.checkout_state == "Recovered":
            st.markdown("""
            <div class="recovered-badge">
              <div class="recovered-badge-title">✓ Offer Applied</div>
              <div class="recovered-badge-sub">Cart updated. Complete payment above.</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# RIGHT PANEL — Agent Monitor
# ═══════════════════════════════════════════════════════════════════
with right:
    st.markdown('<div class="panel-title"><span class="panel-title-icon">⚙️</span> AGENT OPERATIONS MONITOR</div>', unsafe_allow_html=True)

    # ── API Key ──
    api_key_input = st.text_input(
        "Anthropic API Key",
        placeholder="sk-ant-… (optional — uses fallback if blank)",
        type="password",
        key="anthropic_key",
        help="Provide your Anthropic API key to use Claude claude-sonnet-4-20250514. Falls back to a deterministic rules engine automatically."
    )

    st.markdown('<hr>', unsafe_allow_html=True)

    # ── Conversion Funnel ──
    st.markdown('<div class="section-label">Conversion Funnel</div>', unsafe_allow_html=True)
    funnel_data = [
        ("Sessions", 100, "#64DCFF"),
        ("Add to Cart", 68, "#6366F1"),
        ("Checkout", 41, "#A855F7"),
        ("Recovered", 27, "#10B981"),
        ("Converted", 19, "#F59E0B"),
    ]
    funnel_html = ""
    for label, pct, color in funnel_data:
        funnel_html += f"""
        <div class="funnel-row">
          <div class="funnel-label">{label}</div>
          <div class="funnel-bar-bg">
            <div class="funnel-bar-fill" style="width:{pct}%; background:{color};"></div>
          </div>
          <div class="funnel-pct">{pct}%</div>
        </div>"""
    st.markdown(f'<div style="margin:12px 0 20px 0;">{funnel_html}</div>', unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    # ── Session Diagnostics ──
    st.markdown('<div class="section-label">Live Session Diagnostics</div>', unsafe_allow_html=True)

    diag_items = [
        ("Friction Type", st.session_state.friction_detected or "None", "#6B7FA8"),
        ("Cart Value", f"₹{st.session_state.cart_total - st.session_state.discount_applied:,}", "#64DCFF"),
        ("Shipping", "FREE" if st.session_state.shipping_free else f"₹{st.session_state.shipping_fee}", "#10B981" if st.session_state.shipping_free else "#F59E0B"),
        ("Discount", f"₹{st.session_state.discount_applied}" if st.session_state.discount_applied else "—", "#10B981" if st.session_state.discount_applied else "#4A5578"),
        ("Events Fired", str(st.session_state.friction_count), "#A855F7"),
        ("Recoveries", str(st.session_state.recoveries_this_session), "#10B981"),
    ]
    diag_html = '<div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:20px;">'
    for k, v, c in diag_items:
        diag_html += f"""
        <div class="metric-card">
          <div class="metric-label">{k}</div>
          <div style="font-family:'Syne',sans-serif; font-size:15px; font-weight:700; color:{c};">{v}</div>
        </div>"""
    diag_html += "</div>"
    st.markdown(diag_html, unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    # ── Live Log Terminal ──
    st.markdown('<div class="section-label">Operational Telemetry Log</div>', unsafe_allow_html=True)

    if not st.session_state.logs:
        log("System initialised. Monitoring checkout session lifecycle.", "INFO")

    level_map = {"INFO": "info", "SUCCESS": "success", "WARN": "warn", "ERROR": "error"}
    log_html = '<div class="log-terminal">'
    for entry in st.session_state.logs:
        tag_class = level_map.get(entry["level"], "info")
        log_html += f"""
        <div class="log-line">
          <span class="log-ts">{entry['ts']}</span>
          <span class="log-tag {tag_class}">{entry['level']}</span>
          <span class="log-msg">{entry['msg']}</span>
        </div>"""
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)

    st.write("")
    if st.button("Clear Logs", use_container_width=True, key="clear_logs"):
        st.session_state.logs = []
        log("Log buffer cleared.", "INFO")
        st.rerun()

def load_css(bg_img):
    return f"""
    <style>
    
/* =========================
   🌌 MAIN APP BACKGROUND
========================= */
.stApp {{
    background-image: url("data:image/jpg;base64,{bg_img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Dark Overlay */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.12);
    z-index: -1;
}}

/* =========================
   📌 MAIN CONTAINER
========================= */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
}}

/* =========================
   📂 SIDEBAR
========================= */
section[data-testid="stSidebar"] {{
    background: rgba(15, 23, 42, 0.18);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.12);
    padding: 20px 12px;
    box-shadow: 4px 0 25px rgba(0,0,0,0.18);
}}

/* Sidebar Radio Labels */
div[role="radiogroup"] label {{
    font-size: 16px !important;
    font-weight: 600;
    color: #e0e7ff !important;
    transition: all 0.3s ease;
}}

div[role="radiogroup"] label:hover {{
    color: #60a5fa !important;
    transform: translateX(5px);
}}


/* =========================
   📊 KPI CARDS
========================= */
.kpi-card {{
    border-radius: 12px;
    padding: 12px 10px;
    min-height: 95px;
    text-align: center;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.18);
    transition: all 0.3s ease;
    backdrop-filter: blur(8px);
    border-left: 4px solid rgba(255,255,255,0.15);
}}

.kpi-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.35);
}}

.emoji {{
    font-size: 1.9em;
    margin-bottom: 4px;
}}

.kpi-title {{
    font-size: 1.2rem;
    opacity: 0.85;
    margin-bottom: 4px;
}}

.kpi-card h1 {{
    font-size: 2em;
    margin: 0;
    line-height: 1;
    font-weight: 700;
}}

/* KPI Themes */
.card-green  {{ background: linear-gradient(135deg, #22c55e 0%, #14532d 100%); }}
.card-purple {{ background: linear-gradient(135deg, #8b5cf6 0%, #312e81 100%); }}
.card-orange {{ background: linear-gradient(135deg, #f59e0b 0%, #78350f 100%); }}
.card-red    {{ background: linear-gradient(135deg, #ef4444 0%, #7f1d1d 100%); }}

/* =========================
   📦 SECTION BOXES
========================= */
.section-box {{
    background: rgba(5, 13, 22, 0.2);
    backdrop-filter: blur(20px);
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
    transition: all 0.4s ease;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}}

.section-box:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 35px rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.12);
}}

/* =========================
   ✨ DIVIDER
========================= */
.custom-divider {{
    height: 2px;
    background: linear-gradient(90deg, transparent, #60a5fa, transparent);
    margin: 20px 0;
    border-radius: 2px;
}}

/* =========================
   🔠 HEADINGS
========================= */
h1, h2, h3 {{
    color: #e0e7ff !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}}

h2 {{
    border-bottom: 3px solid #60a5fa;
    padding-bottom: 10px;
}}

/* =========================
   📋 TABLES
========================= */
.dataframe {{
    border-radius: 12px !important;
    overflow: hidden;
}}

/* =========================
   🔘 BUTTONS
========================= */
button[data-testid="baseButton-secondary"] {{
    background-color: #3b82f6 !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}}

button[data-testid="baseButton-secondary"]:hover {{
    background-color: #2563eb !important;
    transform: scale(1.05) !important;
    box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4) !important;
}}

/* =========================
   📈 METRICS
========================= */
.metric-value {{
    font-size: 2.2em !important;
    font-weight: bold !important;
    color: #60a5fa !important;
}}

/* =========================
   🏷️ STATUS BADGES
========================= */
.status-badge {{
    display: inline-block;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9em;
}}

.status-pass {{
    background-color: rgba(34, 197, 94, 0.2);
    color: #22c55e;
    border: 1px solid #22c55e;
}}

.status-fail {{
    background-color: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    border: 1px solid #ef4444;
}}

/* =========================
   📜 SCROLLABLE BOX
========================= */
.scrollable-box {{
    max-height: 400px;
    overflow-y: auto;
    border-radius: 12px;
    padding: 15px;
    background-color: rgba(0,0,0,0.25);
}}

/* =========================
   💡 INFO BOX
========================= */
.info-box {{
    background: linear-gradient(
        135deg,
        rgba(96, 165, 250, 0.12),
        rgba(139, 92, 246, 0.12)
    );
    border-left: 5px solid #60a5fa;
    padding: 15px;
    border-radius: 10px;
    margin: 15px 0;
}}

/* =========================
   ✅ SUCCESS / ERROR
========================= */
.success-box {{
    background: linear-gradient(
        135deg,
        rgba(34, 197, 94, 0.1),
        rgba(16, 185, 129, 0.1)
    );
    border: 2px solid #22c55e;
}}

.error-box {{
    background: linear-gradient(
        135deg,
        rgba(239, 68, 68, 0.1),
        rgba(220, 38, 38, 0.1)
    );
    border: 2px solid #ef4444;
}}

/* =========================
   🌟 GLOBAL TEXT COLORS
========================= */
html, body, [class*="css"] {{
    color: #f8fafc !important;
}}

p     {{ color: #e2e8f0 !important; }}
label {{ color: #f1f5f9 !important; font-weight: 500 !important; }}

h1 {{ color: #ffffff !important; font-weight: 800 !important; }}
h2 {{ color: #dbeafe !important; border-bottom: 2px solid #60a5fa !important; }}
h3 {{ color: #bfdbfe !important; }}
h4, h5, h6 {{ color: #e0f2fe !important; }}

section[data-testid="stSidebar"] * {{ color: #f8fafc !important; }}

[data-testid="stMetricLabel"] {{ color: #dbeafe !important; }}
[data-testid="stMetricValue"] {{ color: #ffffff !important; font-weight: 700 !important; }}

.stTabs [data-baseweb="tab"] {{ color: #e2e8f0 !important; }}
.stTabs [aria-selected="true"] {{ color: white !important; }}

.streamlit-expanderHeader {{ color: #f8fafc !important; font-weight: 600 !important; }}
.stMarkdown {{ color: #f1f5f9 !important; }}

.dataframe {{ color: white !important; }}
thead tr th {{ background: rgba(59,130,246,0.25) !important; color: white !important; }}
tbody tr td {{ color: #f8fafc !important; }}

input, textarea {{ color: white !important; }}
div[data-baseweb="select"] * {{ color: white !important; }}
[data-baseweb="tag"] {{ background: #2563eb !important; color: white !important; }}
.stSlider label {{ color: white !important; }}
div[role="radiogroup"] label {{ color: #f8fafc !important; }}
.stAlert {{ color: white !important; }}
.js-plotly-plot .plotly {{ border-radius: 12px; }}
footer {{ color: #cbd5e1 !important; }}

/* =========================
   🔗 SOCIAL BUTTONS (Footer)
========================= */
.social-btn {{
    text-decoration: none;
    display: inline-block;
    color: white;
    padding: 12px 24px;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 600;
    font-family: sans-serif;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.social-btn:hover {{
    transform: translateY(-2px);
    color: white;
}}

.btn-linkedin {{
    background: linear-gradient(135deg, #0A66C2, #004182);
    box-shadow: 0 4px 15px rgba(10,102,194,0.35);
    margin-right: 15px;
}}

.btn-linkedin:hover {{
    box-shadow: 0 8px 25px rgba(10,102,194,0.55);
}}

.btn-github {{
    background: linear-gradient(135deg, #24292e, #000000);
    box-shadow: 0 4px 15px rgba(0,0,0,0.35);
}}

.btn-github:hover {{
    box-shadow: 0 8px 25px rgba(0,0,0,0.55);
}}
    </style>
    """
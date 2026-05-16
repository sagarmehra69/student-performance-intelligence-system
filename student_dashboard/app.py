"""
Student Performance Intelligence System (SPIS)
A comprehensive dashboard for analyzing and predicting student performance.
"""

# =====================================================
# 📦 IMPORTS
# =====================================================
import os
import base64

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.styles import load_css
from modules.loader import load_data
from modules.filters import apply_filters
from modules.database import (
    login_user,
    register_user
)
from modules.visualization import (
    marks_distribution, subject_bar, pass_fail_pie, student_trend, forecast_plot
)
from modules.prediction import (
    train_model, predict_marks, risk_level
)
from modules.report import generate_pdf
from modules.recommendation import generate_detailed_feedback, teacher_comment


# =====================================================
# ⚙️ PAGE CONFIGURATION
# =====================================================
st.set_page_config(page_title="SPIS Dashboard", layout="wide", initial_sidebar_state="expanded")

# =====================================================
# 📁 BASE DIRECTORY 
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64(file_path: str) -> str:
    """Encode a file to base64 string for embedding in HTML/CSS."""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    bg_img = get_base64(os.path.join(BASE_DIR, "assets/background.jpg"))
except FileNotFoundError:
    bg_img = ""  # Fallback if image not found

st.markdown(load_css(bg_img), unsafe_allow_html=True)


# =====================================================
# 🎛️ SIDEBAR CONTROLS
# =====================================================
st.sidebar.header("🎛️ Control Panel")
st.sidebar.markdown("---")

# Sidebar logo — rendered correctly inside the column context

def get_logo_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ✅ Sidebar logo 

logo_base64 = get_base64(os.path.join(BASE_DIR, "assets/logo.png"))

st.sidebar.markdown(
    f"""
    <div style="
        text-align:center;
        padding:12px;
        background: rgba(15,23,42,0.6);
        border-radius: 12px;
        margin-bottom: 10px;
    ">
        <img src="data:image/png;base64,{logo_base64}"
            style="
                width:140px;
                height:auto;
                object-fit:contain;
                display:block;
                margin:auto;
            ">
        <div style="color:white; font-weight:600; margin-top:6px;">
            SPIS
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None
    
    
# =====================================================
# 🔐 AUTHENTICATION SYSTEM
# =====================================================

st.sidebar.header("🔐 Authentication")

auth_mode = st.sidebar.radio(
    "Choose Option",
    ["Login", "Register"]
)


# =====================================================
# LOGIN
# =====================================================

if auth_mode == "Login":

    if not st.session_state.logged_in:

        username = st.sidebar.text_input("👤 Username")

        password = st.sidebar.text_input(
            "🔑 Password",
            type="password"
        )

        login_btn = st.sidebar.button("🚀 Login")

        if login_btn:

            user = login_user(username, password)

            if user:

                st.session_state.logged_in = True
                st.session_state.role = user[3]
                st.session_state.username = user[1]

                st.rerun()

            else:
                st.sidebar.error(
                    "❌ Invalid Username or Password"
                )

    else:

        st.sidebar.success(
            f"✅ Logged in as {st.session_state.role}"
        )

        st.sidebar.markdown(
            f"👤 {st.session_state.username}"
        )

        logout_btn = st.sidebar.button("🚪 Logout")

        if logout_btn:

            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.username = None

            st.rerun()


# =====================================================
# REGISTER
# =====================================================

else:

    st.sidebar.subheader("📝 Create Account")

    new_user = st.sidebar.text_input(
        "👤 Create Username"
    )

    new_pass = st.sidebar.text_input(
        "🔑 Create Password",
        type="password"
    )

    new_role = st.sidebar.selectbox(
        "🎓 Select Role",
        ["Student", "Admin"]
    )

    register_btn = st.sidebar.button(
        "✅ Register"
    )

    if register_btn:

        if len(new_user) < 3:
            st.sidebar.warning(
                "Username too short"
            )
            
        elif len(new_pass) < 6:
            st.sidebar.warning(
        "Password must be at least 6 characters"
    )

        else:

            success = register_user(
                new_user,
                new_pass,
                new_role
            )

            if success:

                st.sidebar.success(
                    "🎉 Registration Successful!"
                )

            else:

                st.sidebar.error(
                    "⚠️ Username already exists"
                )
       
# =====================================================
# 🌟 PUBLIC INTRO SCREEN
# =====================================================

if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align:center; padding: 40px 20px 20px 20px;">
        <h1 style="
            font-size: 3.5rem;
            font-weight: 900;
            color: white;
            margin-bottom: 15px;
            text-shadow: 0 0 30px rgba(59,130,246,0.9);
            letter-spacing: -2px;
            line-height: 1.1;
        ">
            🎓 Student Performance Intelligence System
        </h1>
        <p style="
            font-size: 1.35rem;
            color: #cbd5e1;
            max-width: 950px;
            margin: auto;
            line-height: 1.9;
            margin-bottom: 35px;
        ">
            AI-powered academic analytics platform designed to analyze,
            predict, and improve student performance using
            Machine Learning, Data Visualization, and Intelligent Recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ✅ Style the image container via CSS class, not wrapping div
    st.markdown("""
    <style>
    [data-testid="stImage"] {
        background: rgba(15,23,42,0.72);
        backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 28px;
        padding: 22px;
        margin-top: 10px;
        box-shadow: 0 10px 45px rgba(0,0,0,0.45);
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

    st.image(
        os.path.join(BASE_DIR, "assets/hero.png"),
        use_container_width=True
    )

    st.markdown("""
    <div style="
        margin-top: 35px;
        background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(139,92,246,0.18));
        border: 1px solid rgba(96,165,250,0.25);
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        font-size: 1.15rem;
        color: #f8fafc;
        font-weight: 600;
        box-shadow: 0 5px 25px rgba(0,0,0,0.25);
    ">
        🔐 Please login or register from the sidebar to continue
    </div>
    """, unsafe_allow_html=True)

    st.stop()
# =====================================================
# 📂 DATASET SOURCE SELECTION
# =====================================================

dataset_mode = st.sidebar.radio(
    "📊 Choose Dataset Source",
    [
        "Use Default Dataset",
        "Upload Custom Dataset"
    ]
)

# =====================================================
# � DATASET UPLOAD (if custom mode selected)
# =====================================================

uploaded_students = None
uploaded_marks = None

if dataset_mode == "Upload Custom Dataset":
    st.sidebar.header("📂 Upload Dataset")

    uploaded_students = st.sidebar.file_uploader(
        "Upload Students CSV",
        type=["csv"],
        key="students_file"
    )

    uploaded_marks = st.sidebar.file_uploader(
        "Upload Marks CSV",
        type=["csv"],
        key="marks_file"
    )

    st.sidebar.markdown("""
    <div style="
    background: rgba(59,130,246,0.12);
    padding: 12px;
    border-radius: 10px;
    border-left: 4px solid #3b82f6;
    margin-top: 10px;
    ">
    📘 <b>Required Files:</b><br>
    • students.csv<br>
    • marks.csv
    </div>
    """, unsafe_allow_html=True)

    # 📥 SAMPLE TEMPLATE DOWNLOADS
    sample_students = pd.DataFrame({
        "student_id": [101],
        "name": ["Rahul"],
        "branch": ["CSE"],
        "year": [2]
    })

    sample_marks = pd.DataFrame({
        "student_id": [101],
        "subject": ["Mathematics"],
        "marks": [85]
    })

    st.sidebar.download_button(
        "📥 Download Students Template",
        sample_students.to_csv(index=False),
        "students_template.csv",
        "text/csv"
    )

    st.sidebar.download_button(
        "📥 Download Marks Template",
        sample_marks.to_csv(index=False),
        "marks_template.csv",
        "text/csv"
    )

    # Check if files are uploaded
    if uploaded_students is None or uploaded_marks is None:
        st.warning("⚠️ Please upload both CSV files.")
        st.stop()

# =====================================================
# �📥 LOAD DATA
# =====================================================
df = load_data(uploaded_students, uploaded_marks)
   
# =====================================================
# 🤖 CACHED MODEL TRAINING 
# =====================================================

@st.cache_resource
def get_trained_model(data: pd.DataFrame):
    """Train and cache the ML model for performance predictions."""
    return train_model(data)

# =====================================================
# 🖼️ HEADER
# =====================================================
st.image(
    os.path.join(BASE_DIR, "assets/hero.png"),
    use_container_width=True,
    caption="📊 Empowering Student Success with Data-Driven Insights"
)

st.markdown("""
<div style="text-align: center; margin: 35px 0;">
    <h1 style="font-size: 3.2em; color: white; font-weight: 900; 
    margin: 0; text-shadow: 0 4px 20px rgba(255,255,255,0.25); letter-spacing: -1px;">
        🎓 Student Performance Intelligence System
    </h1>
    <p style="font-size: 1.2em; color: #e2e8f0; margin-top: 12px; font-weight: 500;
        text-shadow: 0 2px 10px rgba(0,0,0,0.4);">
        📊 Analyze • 🔮 Predict • 📈 Improve
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# 🎛️ SIDEBAR FILTERS
# =====================================================
st.sidebar.subheader("🔍 Filter Dashboard")

search = st.sidebar.text_input(
    "🔎 Search Student",
    placeholder="Enter student name..."
)

student_ids = df["student_id"].unique()
branches    = df["branch"].unique()
subjects    = df["subject"].unique()
years       = sorted(df["year"].unique())

with st.sidebar.expander("👤 Student Selection", expanded=True):
    selected_student = st.selectbox("Select Student", student_ids, help="Choose a student to analyze")

with st.sidebar.expander("📂 Department & Year", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        selected_branch = st.multiselect("🏫 Branch", branches, help="Filter by branch")
    with col2:
        selected_year = st.multiselect("📅 Year", years, help="Filter by year")

with st.sidebar.expander("📚 Subjects", expanded=False):
    selected_subject = st.multiselect("📖 Subject", subjects, help="Filter by subject")

with st.sidebar.expander("⚙️ Advanced Settings", expanded=False):
    st.write("**📊 Mark Range**")
    marks_range   = st.slider("Select range:", 0, 100, (0, 100), help="Filter marks by range")
    st.write("**🏆 Admin Settings**")
    top_n         = st.slider("Top Students to Show", 1, 20, 5, help="Number of top performers")
    status_filter = st.radio("🎯 Status Filter", ["All", "Pass", "Fail"], help="Filter by pass/fail status")

st.sidebar.markdown("---")
st.sidebar.write("💡 **Tip:** Use filters to customize your view and discover insights!")


filtered_df = apply_filters(
    data=df,
    role_key=(
    st.session_state.role.lower()
    if st.session_state.role
    else "guest"
),
    selected_student=selected_student,
    selected_branch=selected_branch,
    selected_year=selected_year,
    selected_subject=selected_subject,
    marks_range=marks_range,
    status_filter=status_filter,
    search=search
)

# =====================================================
# 📊 KPI METRICS
# =====================================================
def calculate_kpi_metrics(data: pd.DataFrame) -> dict:
    """Calculate key performance indicators from filtered data."""
    if data.empty:
        return {"total_students": 0, "avg_marks": 0, "top_score": 0, "pass_percent": 0, "fail_count": 0}

    total_students = data["student_id"].nunique()
    avg_marks      = round(data["marks"].mean(), 2)
    top_score      = int(data["marks"].max())

    student_status = data.groupby("student_id")["marks"].apply(
        lambda x: "Pass" if (x >= 40).all() else "Fail"
    )
    pass_students = (student_status == "Pass").sum()
    fail_students = (student_status == "Fail").sum()
    pass_percent  = round((pass_students / total_students) * 100, 2) if total_students > 0 else 0

    return {
        "total_students": total_students,
        "avg_marks":      avg_marks,
        "top_score":      top_score,
        "pass_percent":   pass_percent,
        "fail_count":     fail_students,
    }

kpi = calculate_kpi_metrics(filtered_df)

# =====================================================
# 📊 KPI CARDS
# =====================================================
st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown(f"""
    <div class="kpi-card card-purple">
        <div class="emoji">🎓</div>
        <div class="kpi-title">Total Students</div>
        <h1>{kpi["total_students"]}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card card-green">
        <div class="emoji">📊</div>
        <div class="kpi-title">Average Marks</div>
        <h1>{kpi["avg_marks"]}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card card-orange">
        <div class="emoji">🏆</div>
        <div class="kpi-title">Top Score</div>
        <h1>{kpi["top_score"]}</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if kpi["pass_percent"] >= 70:
        color_class, emoji = "card-green", "✅"
    elif kpi["pass_percent"] >= 50:
        color_class, emoji = "card-orange", "⚠️"
    else:
        color_class, emoji = "card-red", "❌"

    st.markdown(f"""
    <div class="kpi-card {color_class}">
        <div class="emoji">{emoji}</div>
        <div class="kpi-title">Pass Rate</div>
        <h1>{kpi["pass_percent"]}%</h1>
    </div>
    """, unsafe_allow_html=True)



# =====================================================
# 📂 NAVIGATION TABS
# =====================================================
st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] { gap: 10px; }

.stTabs [data-baseweb="tab"] {
    background-color: rgba(100,100,100,0.1);
    border-radius: 12px 12px 0 0;
    padding: 15px 25px !important;
    font-weight: 600;
    border: 2px solid rgba(100,100,100,0.2);
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    border: 2px solid #60a5fa !important;
    color: white !important;
}

.stTabs [aria-selected="false"]:hover {
    background-color: rgba(100,100,100,0.2);
}
</style>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "📊 Overview",
    "👤 Student Analysis",
    "🤖 AI Insights",
    "📄 Student Feedback"
])

# =====================================================
# 📊 TAB 0 — OVERVIEW
# =====================================================
with tabs[0]:
    st.markdown("""
    <div class="section-box">
        <h2>📊 Performance Overview</h2>
        <p style="color: #94a3b8; margin: 10px 0 0 0;">Real-time analytics dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("📈 Loading visualizations..."):
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.markdown("<h3 style='text-align: center;'>📊 Marks Distribution</h3>", unsafe_allow_html=True)
            st.plotly_chart(marks_distribution(filtered_df), use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center;'>📚 Subject Performance</h3>", unsafe_allow_html=True)
            st.plotly_chart(subject_bar(filtered_df), use_container_width=True)

        with col3:
            st.markdown("<h3 style='text-align: center;'>📌 Pass vs Fail</h3>", unsafe_allow_html=True)
            st.plotly_chart(pass_fail_pie(filtered_df), use_container_width=True)

    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(16, 185, 129, 0.1)); 
                border-left: 5px solid #22c55e; padding: 15px; border-radius: 10px; margin: 20px 0;">
        <strong>✅ Insights Status:</strong>
        <span style="color: #22c55e;">Dynamically updated based on active filters</span>
    </div>
    """, unsafe_allow_html=True)

    # 🔐 ADMIN-ONLY SECTION
    if st.session_state.role.lower() == "admin":
        st.markdown("""
        <div class="custom-divider"></div>
        <h2 style="color: #ef4444;">🔐 Admin Dashboard</h2>
        """, unsafe_allow_html=True)

        with st.expander("🏆 Top Performers", expanded=True):
            top_students = (
                filtered_df.groupby(["student_id", "name"])["marks"]
                .mean()
                .reset_index()
                .sort_values(by="marks", ascending=False)
                .head(top_n)
            )
            for idx, (_, row) in enumerate(top_students.iterrows(), 1):
                emoji = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "⭐"
                st.markdown(f"""
                <div style="background: rgba(34, 197, 94, 0.1); padding: 12px; border-radius: 8px;
                            margin: 8px 0; border-left: 4px solid #22c55e;">
                    <strong>{emoji} #{idx}. {row['name']} (ID: {row['student_id']})</strong>
                    <span style="float: right; color: #22c55e; font-weight: bold;">📊 {row['marks']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("⚠️ At-Risk Students", expanded=False):
            weak_students = filtered_df[filtered_df["marks"] < 40]
            if not weak_students.empty:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(220,38,38,0.1));
                            border: 2px solid #ef4444; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <strong style="color: #ef4444;">❌ Alert: Students below passing marks detected</strong>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(weak_students, use_container_width=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(16,185,129,0.1));
                            border: 2px solid #22c55e; padding: 15px; border-radius: 10px;">
                    <strong style="color: #22c55e;">✅ No at-risk students detected 🎉</strong>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("📊 Subject Analysis", expanded=False):
            fig = px.box(
                filtered_df, x="subject", y="marks", color="subject",
                template="plotly_dark", title="Distribution of Marks by Subject"
            )
            st.plotly_chart(fig, use_container_width=True)

    # 📋 DATA TABLE
    st.markdown("""
    <div class="custom-divider"></div>
    <h2>📋 Student Data</h2>
    """, unsafe_allow_html=True)

    with st.expander("📊 View Full Dataset", expanded=True):
        
        filtered_df = filtered_df.copy()
        filtered_df["marks"] = filtered_df["marks"].round(1)
        numeric_cols = filtered_df.select_dtypes(include=["number"]).columns
        st.dataframe(
            filtered_df.style
            .background_gradient(cmap="viridis", subset=["marks"])
            .map(lambda x: "color: red" if isinstance(x, (int, float)) and x < 40 else "", subset=["marks"])
            .format({
                "marks": "{:.1f}",
                "attendance": "{}%"
            }),
            use_container_width=True,
            height=400
        )

# =====================================================
# 👤 TAB 1 — STUDENT ANALYSIS
# =====================================================
with tabs[1]:
    st.image(
        os.path.join(BASE_DIR, "assets/students.png"),
        use_container_width=True,
        caption="👤 In-depth Student Analysis"
    )

    student_df = df[df["student_id"] == selected_student]

    if student_df.empty:
        st.warning("⚠️ No data available for selected student")
    else:
        student_info = student_df.iloc[0]

        st.markdown(f"""
        <div class="section-box">
            <h2>👤 Student Profile: {student_info['name']}</h2>
            <div style="margin-top: 10px; display: flex; gap: 20px; flex-wrap: wrap;">
                <span style="background: rgba(59,130,246,0.2); padding: 8px 16px; border-radius: 20px;
                             color: #60a5fa;"><strong>ID:</strong> {selected_student}</span>
                <span style="background: rgba(139,92,246,0.2); padding: 8px 16px; border-radius: 20px;
                             color: #8b5cf6;"><strong>📚 Subjects:</strong> {len(student_df)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown("<h3>📄 Subject-wise Performance</h3>", unsafe_allow_html=True)
            display_df = student_df[["subject", "marks", "branch", "year"]].copy()
            display_df["Status"] = display_df["marks"].apply(
                lambda x: "✅ Pass" if x >= 40 else "❌ Fail"
            )
            st.dataframe(
                display_df.style
                .background_gradient(cmap="RdYlGn", subset=display_df.select_dtypes(include=["number"]).columns)
                .map(lambda x: "color: green" if "Pass" in str(x) else "color: red" if "Fail" in str(x) else ""),
                use_container_width=True
            )

        with col2:
            avg = student_df["marks"].mean()
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); padding: 25px;
                        border-radius: 15px; text-align: center; color: white;">
                <h4 style="margin: 0 0 10px 0;">Overall Average</h4>
                <div style="font-size: 2.5em; font-weight: bold; margin: 10px 0;">{round(avg, 2)}</div>
                <div style="font-size: 0.9em; opacity: 0.8;">out of 100</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(avg / 100, 1.0))

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("<h3>📈 Performance Trend</h3>", unsafe_allow_html=True)
        st.plotly_chart(student_trend(df, selected_student), use_container_width=True)

# =====================================================
# 🤖 TAB 2 — AI INSIGHTS
# =====================================================
with tabs[2]:
    with st.spinner("🤖 Training advanced ML model..."):
       model, features, metrics = get_trained_model(df)

    predicted = predict_marks(model, features, selected_student)
    risk = risk_level(predicted, features)
    feedback  = generate_detailed_feedback(df, selected_student, features)
    rec       = feedback[0] if feedback else "No recommendation available"

    st.markdown("<h2>🤖 AI-Powered Analytics</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(f"""
        <div class="kpi-card card-purple">
            <div style="font-size: 2em;">🔮</div>
            <div style="font-size: 0.9em; opacity: 0.8; margin: 5px 0;">Predicted Total</div>
            <h1>{round(predicted, 2)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card card-orange">
            <div style="font-size: 2em;">⚠️</div>
            <div style="font-size: 0.9em; opacity: 0.8; margin: 5px 0;">Risk Level</div>
            <h1 style="font-size: 1.8em; margin: 5px 0 0 0;">{risk}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        subject_count = len(df[df["student_id"] == selected_student])
        st.markdown(f"""
        <div class="kpi-card card-green">
            <div style="font-size: 2em;">📚</div>
            <div style="font-size: 0.9em; opacity: 0.8; margin: 5px 0;">Total Subjects</div>
            <h1>{subject_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    with st.expander("📈 Future Performance Forecast", expanded=True):
        forecast = forecast_plot(df, selected_student)
        if forecast:
            st.plotly_chart(forecast, use_container_width=True)
        else:
            st.info("📊 Not enough historical data for forecast generation")

    with st.expander("💡 AI Recommendation", expanded=True):
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(16,185,129,0.1));
                    border-left: 5px solid #22c55e; padding: 15px; border-radius: 10px;">
            <strong style="color: #22c55e;">✨ Recommendation:</strong>
            <p style="margin: 10px 0 0 0; color: white;">{rec}</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📊 Model Features & Metrics", expanded=False):
        model_features_df = features[features["student_id"] == selected_student].copy()
        if not model_features_df.empty:
            cols_display = st.columns(2)
            for idx, col in enumerate(model_features_df.columns[1:]):  # Skip student_id
                with cols_display[idx % 2]:
                    val = model_features_df[col].values[0]
                    st.metric(
                        f"📊 {col.replace('_', ' ').title()}",
                        f"{round(val, 2) if isinstance(val, float) else val}"
                    )

# =====================================================
# 📄 TAB 3 — STUDENT FEEDBACK
# =====================================================
with tabs[3]:
    st.markdown("""
    <div class="section-box">
        <h2>📄 Comprehensive Student Report</h2>
        <p style="color: #94a3b8;">AI-generated academic performance analysis & insights</p>
    </div>
    """, unsafe_allow_html=True)

    # Reuse the already-trained model (no redundant call)
    model, features, metrics = get_trained_model(df)
    student_in_features = not features[features["student_id"] == selected_student].empty

    if not student_in_features:
        st.warning("⚠️ Student not found in model features")
    else:
        predicted = predict_marks(model, features, selected_student)
        risk      = risk_level(predicted, features)
        feedback  = generate_detailed_feedback(df, selected_student, features)

        student_marks = df[df["student_id"] == selected_student]["marks"]
        avg = student_marks.mean() if len(student_marks) > 0 else 0

        trend = 0
        if "trend" in features.columns:
            trend_val = features[features["student_id"] == selected_student]["trend"]
            if len(trend_val) > 0:
                trend = trend_val.values[0]

        comment = teacher_comment(avg, trend)

        # Quick Stats
        st.markdown("<h3>📊 Quick Stats</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.markdown(f"""
            <div style="background: rgba(59,130,246,0.35); padding: 20px; border-radius: 12px;
                        border-left: 5px solid #3b82f6; text-align: center;">
                <div style="font-size: 2em; color: #ffffff; font-weight: bold;">{round(avg, 2)}</div>
                <div style="color: #f8fafc; margin-top: 5px;">📊 Average Marks</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background: rgba(139,92,246,0.35); padding: 20px; border-radius: 12px;
                        border-left: 5px solid #8b5cf6; text-align: center;">
                <div style="font-size: 2em; color: #f8fafc; font-weight: bold;">{round(predicted, 2)}</div>
                <div style="color: #f8fafc; margin-top: 5px;">🔮 Predicted Total</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            risk_emoji = "🟢" if "Safe" in risk else "🟡" if "Watchlist" in risk else "🔴"
            st.markdown(f"""
            <div style="background: rgba(245,158,11,0.35); padding: 20px; border-radius: 12px;
                        border-left: 5px solid #f59e0b; text-align: center;">
                <div style="font-size: 1.8em; margin-bottom: 5px;">{risk_emoji}</div>
                <div style="color: #f8fafc;">⚠️ {risk}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # AI Feedback
        st.markdown("<h3>🧠 AI-Generated Feedback</h3>", unsafe_allow_html=True)
        feedback_icons = ["💡", "📈", "⭐", "🎯", "📚", "🚀", "✅", "🔥"]

        for i, line in enumerate(feedback, 1):
            icon = feedback_icons[(i - 1) % len(feedback_icons)]
            st.markdown(f"""
            <div style="background: rgba(59,130,246,0.35); padding: 12px 15px; border-radius: 8px;
                        margin-bottom: 8px; border-left: 5px solid #3b82f6; display: flex; gap: 10px;">
                <span style="font-size: 1.2em;">{icon}</span>
                <span>{line}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Teacher Comment
        st.markdown("<h3>👨‍🏫 Teacher's Commentary</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(139,92,246,0.35), rgba(96,165,250,0.35));
                    border-left: 5px solid #8b5cf6; padding: 20px; border-radius: 12px; font-style: italic;">
            <span style="font-size: 1.05em; color: #e0e7ff;">{comment}</span>
        </div>
        """, unsafe_allow_html=True)

        # PDF Export
        st.markdown("""
        <div class="custom-divider"></div>
        <h3>📥 Export & Share</h3>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📥 📄 Download Full Report as PDF", use_container_width=True, key="pdf_download"):
                with st.spinner("📄 Generating professional PDF report..."):
                    # Refresh student_df for this tab
                    student_df   = df[df["student_id"] == selected_student]
                    student_info = student_df.iloc[0]

                    # NOTE: Replace `attendance=87` with a real column when available
                    file_path = generate_pdf(
                        student_info=student_info,
                        marks_df=student_df,
                        feedback=feedback,
                        predicted=predicted,
                        risk=risk,
                        attendance = student_info.get("attendance", 87)  # TODO: pull from attendance data when available
                    )

                    if file_path:
                        with open(file_path, "rb") as pdf_file:
                            st.download_button(
                                label="✅ PDF Ready - Click to Download",
                                data=pdf_file.read(),
                                file_name=f"Student_Report_{selected_student}_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        st.success("✅ PDF generated successfully! Ready for download.")


# =====================================================
# 📌 FOOTER — 
# =====================================================

st.markdown("""
<div style="margin-top: 50px; padding: 20px; text-align: center; color: #94a3b8;
            border-top: 2px solid rgba(96, 165, 250, 0.2);">
    <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-bottom: 15px;">
        <span>✨ <strong>SPIS v2.0</strong></span>
        <span>•</span>
        <span>🎓 <strong>Student Performance Intelligence System</strong></span>
        <span>•</span>
        <span>🚀 <strong>Powered by ML & Analytics</strong></span>
    </div>
    <p style="margin: 10px 0; font-size: 0.9em;">
        💡 Tips: Use filters to customize your analysis •
        📊 Charts update in real-time •
        📄 Export reports as PDF for sharing
    </p>
    <p style="margin-top: 15px; font-size: 0.85em; opacity: 0.7;">
        © 2026 Student Performance Intelligence System
        | Developed by Sagar Mehra | BCA 2023-2026 | All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)
 
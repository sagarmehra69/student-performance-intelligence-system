# """
# Student Performance Intelligence System (SPIS)
# A comprehensive dashboard for analyzing and predicting student performance.
# """

# # =====================================================
# # 📦 IMPORTS
# # =====================================================
# import os
# import base64
# import streamlit as st
# import pandas as pd

# from modules.styles import load_css
# from modules.loader import load_data
# from modules.auth_ui import authentication_ui
# from modules.sidebar import sidebar_filters

# from modules.kpi import (
#     calculate_kpi_metrics,
#     show_kpi_cards
# )

# from modules.student_tab import show_student_tab
# from modules.overview_tab import show_overview_tab
# from modules.ai_tab import show_ai_tab
# from modules.feedback_tab import show_feedback_tab
# from modules.prediction import train_model

# # =====================================================
# # ⚙️ PAGE CONFIGURATION
# # =====================================================
# st.set_page_config(page_title="SPIS Dashboard", layout="wide", initial_sidebar_state="expanded")

# # =====================================================
# # 📁 BASE DIRECTORY 
# # =====================================================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# def get_base64(file_path: str) -> str:
#     """Encode a file to base64 string for embedding in HTML/CSS."""
#     with open(file_path, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# try:
#     bg_img = get_base64(os.path.join(BASE_DIR, "assets/background.jpg"))
# except FileNotFoundError:
#     bg_img = ""  # Fallback if image not found

# # =====================================================
# # 🎨 LOAD CUSTOM STYLES
# # =====================================================

# st.markdown(load_css(bg_img), unsafe_allow_html=True)

# # =====================================================
# # 🎛️ SIDEBAR CONTROLS
# # =====================================================
# st.sidebar.header("🎛️ Control Panel")
# st.sidebar.markdown("---")

# # Sidebar logo and title 

# try:
#     logo_base64 = get_base64(os.path.join(BASE_DIR, "assets/logo.png"))
# except:
#     logo_base64 = ""

# st.sidebar.markdown(
#     f"""
#     <div style="
#         text-align:center;
#         padding:12px;
#         background: rgba(15,23,42,0.6);
#         border-radius: 12px;
#         margin-bottom: 10px;
#     ">
#         <img src="data:image/png;base64,{logo_base64}"
#             style="
#                 width:140px;
#                 height:auto;
#                 object-fit:contain;
#                 display:block;
#                 margin:auto;
#             ">
#         <div style="color:white; font-weight:600; margin-top:6px;">
#             SPIS
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if "role" not in st.session_state:
#     st.session_state.role = "student"
    
# if not st.session_state.logged_in:
#     authentication_ui(BASE_DIR)
#     st.stop()

# # =====================================================
# # 📂 DATASET SOURCE SELECTION
# # =====================================================

# dataset_mode = st.sidebar.radio(
#     "📊 Choose Dataset Source",
#     [
#         "Use Default Dataset",
#         "Upload Custom Dataset"
#     ]
# )

# # =====================================================
# #  DATASET UPLOAD (if custom mode selected)
# # =====================================================

# uploaded_students = None
# uploaded_marks = None

# if dataset_mode == "Upload Custom Dataset":
#     st.sidebar.header("📂 Upload Dataset")

#     uploaded_students = st.sidebar.file_uploader(
#         "Upload Students CSV",
#         type=["csv"],
#         key="students_file"
#     )

#     uploaded_marks = st.sidebar.file_uploader(
#         "Upload Marks CSV",
#         type=["csv"],
#         key="marks_file"
#     )

#     st.sidebar.markdown("""
#     <div style="
#     background: rgba(59,130,246,0.2);
#     padding: 12px;
#     border-radius: 10px;
#     border-left: 4px solid #3b82f6;
#     margin-top: 10px;
#     color: #ffffff;
#     ">
#     📘 <b style="color: #60a5fa;">Required Files:</b><br>
#     <span style="color: #e2e8f0;">• students.csv<br>
#     • marks.csv</span>
#     </div>
#     """, unsafe_allow_html=True)

#     # 📥 SAMPLE TEMPLATE DOWNLOADS
#     sample_students = pd.DataFrame({
#         "student_id": [101],
#         "name": ["Rahul"],
#         "branch": ["CSE"],
#         "year": [2]
#     })

#     sample_marks = pd.DataFrame({
#         "student_id": [101],
#         "subject": ["Mathematics"],
#         "marks": [85]
#     })

#     st.sidebar.download_button(
#         "📥 Download Students Template",
#         sample_students.to_csv(index=False),
#         "students_template.csv",
#         "text/csv"
#     )

#     st.sidebar.download_button(
#         "📥 Download Marks Template",
#         sample_marks.to_csv(index=False),
#         "marks_template.csv",
#         "text/csv"
#     )

#     required_students = ["student_id", "name", "branch", "year"]
#     required_marks = ["student_id", "subject", "marks"]
#     # Check if files are uploaded
#     if uploaded_students is None or uploaded_marks is None:
#         st.warning("⚠️ Please upload both CSV files.")
#         st.stop()

# # =====================================================
# # �📥 LOAD DATA
# # =====================================================

# try:
#     df = load_data(uploaded_students, uploaded_marks)
# except Exception as e:
#     st.error(f"Dataset loading failed: {e}")
#     st.stop()
   
# # =====================================================
# # 🤖 CACHED MODEL TRAINING 
# # =====================================================

# @st.cache_resource
# def get_trained_model(data: pd.DataFrame):
#     """Train and cache the ML model for performance predictions."""
#     return train_model(data)

# # =====================================================
# # 🖼️ HEADER
# # =====================================================
# hero_path = os.path.join(BASE_DIR, "assets/hero.png")

# if os.path.exists(hero_path):
#     st.image(hero_path, use_container_width=True,
#     caption="📊 Empowering Student Success with Data-Driven Insights"
# )

# st.markdown("""
# <div style="text-align: center; margin: 35px 0;">
#     <h1 style="font-size: 3.2em; color: #ffffff; font-weight: 900; 
#     margin: 0; text-shadow: 0 4px 20px rgba(255,255,255,0.3); letter-spacing: -1px;">
#         🎓 Student Performance Intelligence System
#     </h1>
#     <p style="font-size: 1.2em; color: #e2e8f0; margin-top: 12px; font-weight: 600;
#         text-shadow: 0 2px 10px rgba(0,0,0,0.4);">
#         📊 Analyze • 🔮 Predict • 📈 Improve
#     </p>
# </div>
# """, unsafe_allow_html=True)

# # =====================================================
# # 🎛️ SIDEBAR FILTERS
# # =====================================================

# filtered_df, selected_student, top_n = sidebar_filters(df)

# # =====================================================
# # 📊 KPI CALCULATIONS
# # =====================================================

# kpi = calculate_kpi_metrics(filtered_df)
# show_kpi_cards(kpi)

# # =====================================================
# # 📂 NAVIGATION TABS
# # =====================================================
# st.markdown("""
# <style>
# .stTabs [data-baseweb="tab-list"] { gap: 10px; }
# .stTabs [data-baseweb="tab"] {
#     background-color: rgba(100,100,100,0.1);
#     border-radius: 12px 12px 0 0;
#     padding: 15px 25px !important;
#     font-weight: 600;
#     border: 2px solid rgba(100,100,100,0.2);
#     transition: all 0.3s ease;
# }
# .stTabs [aria-selected="true"] {
#     background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
#     border: 2px solid #60a5fa !important;
#     color: white !important;
# }
# .stTabs [aria-selected="false"]:hover {
#     background-color: rgba(100,100,100,0.2);
# }
# </style>
# """, unsafe_allow_html=True)

# tabs = st.tabs([
#     "📊 Overview",
#     "👤 Student Analysis",
#     "🤖 AI Insights",
#     "📄 Student Feedback"
# ])

# # =====================================================
# # 📊 TAB 0 — OVERVIEW
# # =====================================================
# with tabs[0]:
#     show_overview_tab(filtered_df, top_n)

# # =====================================================
# # 👤 TAB 1 — STUDENT ANALYSIS
# # =====================================================
# with tabs[1]:
#     show_student_tab(df, selected_student, BASE_DIR)
    
# # =====================================================
# # 🤖 TAB 2 — AI INSIGHTS
# # =====================================================

# with tabs[2]:
#     show_ai_tab(df, selected_student, get_trained_model)
    
# # =====================================================
# # 📄 TAB 3 — STUDENT FEEDBACK
# # =====================================================

# # with tabs[3]:
# #     show_feedback_tab(df, selected_student, get_trained_model)
    
# # =====================================================
# # 📌 FOOTER — 
# # =====================================================

# st.markdown("""
# <div style="margin-top: 50px; padding: 20px; text-align: center; color: #cbd5e1;
#             border-top: 2px solid rgba(96, 165, 250, 0.3);">
#     <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-bottom: 15px;">
#         <span style="color: #e2e8f0; font-weight: 600;">✨ <strong>SPIS v2.0</strong></span>
#         <span style="color: #64748b;">•</span>
#         <span style="color: #e2e8f0; font-weight: 600;">🎓 <strong>Student Performance Intelligence System</strong></span>
#         <span style="color: #64748b;">•</span>
#         <span style="color: #e2e8f0; font-weight: 600;">🚀 <strong>Powered by ML & Analytics</strong></span>
#     </div>
#     <p style="margin: 10px 0; font-size: 0.9em; color: #cbd5e1; font-weight: 500;">
#         💡 Tips: Use filters to customize your analysis •
#         📊 Charts update in real-time •
#         📄 Export reports as PDF for sharing
#     </p>
#     <p style="margin-top: 15px; font-size: 0.85em; opacity: 0.8; color: #94a3b8;">
#         © 2026 Student Performance Intelligence System
#         | Developed by Sagar Mehra | BCA 2023-2026 | All rights reserved
#     </p>
# </div>
# """, unsafe_allow_html=True)
 
"""
Student Performance Intelligence System (SPIS)
PDF Report Generator — report.py
"""

import os
import tempfile

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# =====================================================
# 🎓 GRADE CALCULATOR
# =====================================================
def calculate_grade(avg: float) -> str:
    """Return letter grade based on average marks."""
    if avg >= 90:   return "A+"
    elif avg >= 80: return "A"
    elif avg >= 70: return "B"
    elif avg >= 60: return "C"
    elif avg >= 50: return "D"
    else:           return "F"


# =====================================================
# 📄 PDF GENERATOR
# =====================================================
def generate_pdf(
    student_info,
    marks_df,
    feedback: list,
    predicted: float,
    risk: str,
    attendance: int = 85
) -> str:
    """
    Generate a student performance report PDF.

    Returns the file path of the generated PDF,
    or None if generation fails.
    """

    student_id = student_info["student_id"]

    # ✅ Save to temp dir — works in any environment
    file_name = os.path.join(
        tempfile.gettempdir(),
        f"student_{student_id}_report.pdf"
    )

    try:
        doc = SimpleDocTemplate(
            file_name,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )

        content = []

        # ── Metrics ──────────────────────────────────
        avg_marks = marks_df["marks"].mean()
        grade     = calculate_grade(avg_marks)

        # ── Pull attendance from data if available ───
        if "attendance" in marks_df.columns:
            attendance = int(marks_df["attendance"].iloc[0])

        # =====================================================
        # 🎨 CUSTOM STYLES
        # =====================================================
        title_style = ParagraphStyle(
            "title",
            fontSize=22,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1F2937"),
            alignment=TA_CENTER,
            spaceAfter=4,
        )

        subtitle_style = ParagraphStyle(
            "subtitle",
            fontSize=10,
            fontName="Helvetica",
            textColor=colors.HexColor("#6B7280"),
            alignment=TA_CENTER,
            spaceAfter=14,
        )

        section_title_style = ParagraphStyle(
            "section_title",
            fontSize=12,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=8,
        )

        label_style = ParagraphStyle(
            "label",
            fontSize=10,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1E40AF"),
        )

        value_style = ParagraphStyle(
            "value",
            fontSize=10,
            fontName="Helvetica",
            textColor=colors.HexColor("#111827"),
        )

        # =====================================================
        # 🏷️ HEADER
        # =====================================================

        content.append(
            Paragraph(
                "STUDENT PERFORMANCE REPORT CARD",
                 ParagraphStyle(
                  "main_title",
                   parent=title_style,
                   leading=30,
                   spaceAfter=10,
               )
           )
  )

        # spacing between title & subtitle
        content.append(Spacer(1, 8))

        content.append(
            Paragraph(
                 "AI-Powered Academic Intelligence System — SPIS v2.0",
                  ParagraphStyle(
                    "sub_title",
                     parent=subtitle_style,
                     leading=18,
                     spaceAfter=20,
               )
            )
       )

       # divider line
        divider = Table(
           [[""]],
           colWidths=[540],
           rowHeights=[2]
       )

        divider.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#3B82F6")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))

        content.append(divider)
        content.append(Spacer(1, 18))       
       


        # =====================================================
        # 👤 STUDENT INFO — 2 COLUMN LAYOUT
        # =====================================================
        # Shared cell padding helper
        cell_pad = [
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ]

        info_style_base = [
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#DBEAFE")),
            ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F0F9FF")),
            ("GRID",       (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
            ("ALIGN",      (0, 0), (-1, -1), "LEFT"),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ] + cell_pad

        left_info = [
            [Paragraph("<b>Student ID</b>", label_style), Paragraph(str(student_info["student_id"]), value_style)],
            [Paragraph("<b>Name</b>",       label_style), Paragraph(str(student_info["name"]),       value_style)],
            [Paragraph("<b>Branch</b>",     label_style), Paragraph(str(student_info["branch"]),     value_style)],
        ]

        right_info = [
            [Paragraph("<b>Year</b>",          label_style), Paragraph(str(student_info["year"]),        value_style)],
            [Paragraph("<b>Attendance</b>",    label_style), Paragraph(f"{attendance}%",                 value_style)],
            [Paragraph("<b>Average Marks</b>", label_style), Paragraph(str(round(avg_marks, 1)),          value_style)],
        ]

        left_table  = Table(left_info,  colWidths=[120, 150])
        right_table = Table(right_info, colWidths=[120, 150])

        left_table.setStyle(TableStyle(info_style_base))
        right_table.setStyle(TableStyle(info_style_base))

        info_container = Table([[left_table, right_table]], colWidths=[270, 270])
        info_container.setStyle(TableStyle([
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("TOPPADDING",    (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))

        content.append(info_container)
        content.append(Spacer(1, 15))

        # =====================================================
        # 🎓 GRADE BANNER
        # =====================================================
        grade_color_map = {
            "A+": "#10B981",
            "A":  "#3B82F6",
            "B":  "#F59E0B",
            "C":  "#EF4444",
            "D":  "#EC4899",
            "F":  "#6B7280",
        }
        grade_color = grade_color_map.get(grade, "#6B7280")

        grade_style = ParagraphStyle(
                "grade",
                alignment=TA_CENTER,
                textColor=colors.white,
                fontName="Helvetica-Bold",
                leading=65,
            )
        
        grade_para = Paragraph(
            f"<font size='58'><b>{grade}</b></font>",
            grade_style
        )
        
        grade_table = Table([[grade_para]], colWidths=[540], rowHeights=[80])
        grade_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor(grade_color)),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("ROWHEIGHTS",    (0, 0), (-1, -1), 10),
            
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor(grade_color)),
        ]))

        content.append(grade_table)
        content.append(Spacer(1, 15))

        # =====================================================
        # 📊 SUBJECT PERFORMANCE TABLE
        # =====================================================
        content.append(Paragraph("Subject-wise Performance", section_title_style))

        table_data = [["Subject", "Marks", "Grade", "Status"]]

        for _, row in marks_df.iterrows():
            marks         = float(row["marks"])
            status        = "Pass" if marks >= 40 else "Fail"
            subject_grade = calculate_grade(marks)
            table_data.append([
                str(row["subject"]),
                str(round(marks, 1)),   # ✅ rounded — no more 46.000000
                subject_grade,
                status,
            ])

        marks_table = Table(table_data, colWidths=[200, 80, 70, 90])
        marks_table.setStyle(TableStyle([
            # Header row
            ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#1E40AF")),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, 0),  11),
            ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
            ("TOPPADDING",    (0, 0), (-1, 0),  10),
            ("BOTTOMPADDING", (0, 0), (-1, 0),  10),
            ("LEFTPADDING",   (0, 0), (-1, 0),  10),
            ("RIGHTPADDING",  (0, 0), (-1, 0),  10),
            # Data rows
            ("BACKGROUND",    (0, 1), (-1, -1), colors.HexColor("#F0F9FF")),
            ("FONTSIZE",      (0, 1), (-1, -1), 10),
            ("ALIGN",         (1, 1), (-1, -1), "CENTER"),
            ("TOPPADDING",    (0, 1), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ("LEFTPADDING",   (0, 1), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 1), (-1, -1), 10),
            # Grid
            ("GRID",          (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))

        # Color-code Pass/Fail status column
        for i in range(1, len(table_data)):
            mark_val = float(table_data[i][1])
            if mark_val >= 40:
                marks_table.setStyle(TableStyle([
                    ("TEXTCOLOR", (3, i), (3, i), colors.HexColor("#059669")),
                    ("FONTNAME",  (3, i), (3, i), "Helvetica-Bold"),
                ]))
            else:
                marks_table.setStyle(TableStyle([
                    ("TEXTCOLOR", (3, i), (3, i), colors.HexColor("#DC2626")),
                    ("FONTNAME",  (3, i), (3, i), "Helvetica-Bold"),
                ]))

        content.append(marks_table)
        content.append(Spacer(1, 15))

        # =====================================================
        # 🤖 AI ANALYTICS & RECOMMENDATIONS
        # =====================================================
        content.append(Paragraph("AI Analytics & Key Recommendations", section_title_style))

        analytics_para = Paragraph(
            f"<b>Predicted Score:</b> {round(predicted, 1)}<br/>"
            f"<b>Risk Level:</b> {risk}<br/>"
            f"<b>Grade:</b> {grade}<br/>"
            f"<b>Avg Marks:</b> {round(avg_marks, 1)}",
            ParagraphStyle(
                "analytics",
                fontSize=10,
                leading=16,
                textColor=colors.white,
                alignment=TA_CENTER,
            )
        )

        analytics_box = Table([[analytics_para]], colWidths=[200])
        analytics_box.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (0, 0), colors.HexColor("#7C3AED")),
            ("TOPPADDING",    (0, 0), (0, 0), 14),
            ("BOTTOMPADDING", (0, 0), (0, 0), 14),
            ("LEFTPADDING",   (0, 0), (0, 0), 12),
            ("RIGHTPADDING",  (0, 0), (0, 0), 12),
            ("VALIGN",        (0, 0), (0, 0), "MIDDLE"),
        ]))

        # Recommendations — up to 4 points
        rec_lines  = feedback[:4] if feedback else ["No recommendations available."]
        rec_text   = "<br/>".join([f"• {line}" for line in rec_lines])
        rec_para   = Paragraph(
            rec_text,
            ParagraphStyle(
                "rec",
                fontSize=9,
                leading=14,
                textColor=colors.HexColor("#374151"),
            )
        )

        rec_box = Table([[rec_para]], colWidths=[300])
        rec_box.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (0, 0), colors.HexColor("#E0F2FE")),
            ("TOPPADDING",    (0, 0), (0, 0), 12),
            ("BOTTOMPADDING", (0, 0), (0, 0), 12),
            ("LEFTPADDING",   (0, 0), (0, 0), 12),
            ("RIGHTPADDING",  (0, 0), (0, 0), 12),
            ("VALIGN",        (0, 0), (0, 0), "TOP"),
        ]))

        insights_container = Table([[analytics_box, rec_box]], colWidths=[230, 310])
        insights_container.setStyle(TableStyle([
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("TOPPADDING",    (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))

        content.append(insights_container)
        content.append(Spacer(1, 20))

        # =====================================================
        # 📌 FOOTER
        # =====================================================
        footer_style = ParagraphStyle(
            "footer",
            alignment=TA_CENTER,
            fontSize=8,
            textColor=colors.HexColor("#9CA3AF"),
        )
        content.append(Paragraph(
            "Generated by Student Performance Intelligence System (SPIS) v2.0  |  "
            "AI-Powered Academic Analytics  |  © 2026 Sagar Mehra",
            footer_style
        ))

        # ── Build ─────────────────────────────────────────
        doc.build(content)
        return file_name

    except Exception as e:
        print(f"[report.py] PDF generation error: {e}")
        return None
# modules/filters.py

import pandas as pd


def apply_filters(
    data: pd.DataFrame,
    role_key,
    selected_student,
    selected_branch,
    selected_year,
    selected_subject,
    marks_range,
    status_filter,
    search
) -> pd.DataFrame:
    """
    Apply dashboard filters to dataset.
    """

    filtered = data.copy()

    # =====================================================
    # 👨‍🎓 STUDENT ROLE FILTER
    # =====================================================
    if role_key == "student":
        filtered = filtered[
            filtered["student_id"] == selected_student
        ]

    # =====================================================
    # 🏫 BRANCH FILTER
    # =====================================================
    if selected_branch:
        filtered = filtered[
            filtered["branch"].isin(selected_branch)
        ]

    # =====================================================
    # 📅 YEAR FILTER
    # =====================================================
    if selected_year:
        filtered = filtered[
            filtered["year"].isin(selected_year)
        ]

    # =====================================================
    # 📚 SUBJECT FILTER
    # =====================================================
    if selected_subject:
        filtered = filtered[
            filtered["subject"].isin(selected_subject)
        ]

    # =====================================================
    # 📊 MARKS RANGE FILTER
    # =====================================================
    filtered = filtered[
        (filtered["marks"] >= marks_range[0]) &
        (filtered["marks"] <= marks_range[1])
    ]

    # =====================================================
    # 🎯 PASS / FAIL FILTER
    # =====================================================
    if status_filter != "All":

        student_status = filtered.groupby("student_id")[
            "marks"
        ].apply(
            lambda x: "Pass" if (x >= 40).all() else "Fail"
        )

        valid_students = student_status[
            student_status == status_filter
        ].index

        filtered = filtered[
            filtered["student_id"].isin(valid_students)
        ]

    # =====================================================
    # 🔎 SEARCH FILTER
    # =====================================================
    if search:
        filtered = filtered[
            filtered["name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    return filtered
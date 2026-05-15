import pandas as pd
import os
import streamlit as st


# =====================================================
# BASE DIRECTORY
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(ttl=3600)
def load_data(students_file=None, marks_file=None) -> pd.DataFrame:
    """
    Load uploaded datasets or fallback to default datasets.
    """

    try:

        # ==========================================
        # LOAD UPLOADED FILES
        # ==========================================
        if students_file is not None and marks_file is not None:

            students = pd.read_csv(students_file)
            marks = pd.read_csv(marks_file)

        # ==========================================
        # LOAD DEFAULT FILES
        # ==========================================
        else:

            students_path = os.path.join(
                BASE_DIR,
                "data",
                "students.csv"
            )

            marks_path = os.path.join(
                BASE_DIR,
                "data",
                "marks.csv"
            )

            students = pd.read_csv(students_path)
            marks = pd.read_csv(marks_path)

        # ==========================================
        # VALIDATION
        # ==========================================

        required_students = [
            "student_id",
            "name",
            "branch",
            "year"
        ]

        required_marks = [
            "student_id",
            "subject",
            "marks"
        ]

        missing_students = [
            col for col in required_students
            if col not in students.columns
        ]

        missing_marks = [
            col for col in required_marks
            if col not in marks.columns
        ]

        # ==========================================
        # ERROR HANDLING
        # ==========================================

        if missing_students:

            st.error(
                f"❌ Students CSV missing columns: {missing_students}"
            )

            st.stop()

        if missing_marks:

            st.error(
                f"❌ Marks CSV missing columns: {missing_marks}"
            )

            st.stop()

        # ==========================================
        # MERGE DATA
        # ==========================================

        df = pd.merge(
            students,
            marks,
            on="student_id",
            how="left"
        )

        # ==========================================
        # CLEAN DATA
        # ==========================================

        df.drop_duplicates(inplace=True)

        df["marks"] = pd.to_numeric(
            df["marks"],
            errors="coerce"
        )

        df.dropna(subset=["marks"], inplace=True)

        return df

    except FileNotFoundError:

        st.error(
            "❌ Default dataset files not found."
        )

        st.stop()

    except Exception as e:

        st.error(
            f"❌ Error loading dataset: {e}"
        )

        st.stop()
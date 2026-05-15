def generate_detailed_feedback(df, student_id, features=None):
    student = df[df["student_id"] == student_id]

    if student.empty:
        return ["No data available"]

    avg = student["marks"].mean()
    total = student["marks"].sum()
    subjects = student["subject"].tolist()
    weak = student[student["marks"] < 50]["subject"].tolist()

    feedback = []

    feedback.append(f"Student ID {student_id} has been evaluated based on academic performance data.")
    feedback.append(f"The overall average score is {avg:.2f}, indicating current performance level.")
    feedback.append(f"The total marks obtained across all subjects is {total}.")
    feedback.append(f"The student has appeared in {len(subjects)} subjects.")

    if avg >= 75:
        feedback.append("The student is performing at an excellent level and shows strong academic consistency.")
        feedback.append("Advanced problem-solving and deeper conceptual learning are recommended.")
    elif avg >= 50:
        feedback.append("The student shows average performance with room for improvement.")
        feedback.append("Consistency and regular revision can significantly boost performance.")
    else:
        feedback.append("The student is currently underperforming and requires immediate attention.")
        feedback.append("Focus should be on building strong fundamentals and daily practice.")

    if weak:
        feedback.append(f"The following subjects need improvement: {', '.join(weak)}.")
        feedback.append("Extra practice and targeted revision are strongly recommended for these subjects.")
    else:
        feedback.append("No major weak subjects identified, maintain the current momentum.")

    if features is not None:
        trend = features[features["student_id"] == student_id]["trend"].values
        if len(trend) > 0:
            if trend[0] > 0:
                feedback.append("The performance trend is improving over time, which is a positive sign.")
            else:
                feedback.append("The performance trend is declining and needs immediate corrective action.")

    feedback.append("Time management and structured study planning can further enhance results.")
    feedback.append("Regular self-assessment and mock tests are recommended.")
    feedback.append("Maintaining consistency is key to long-term academic success.")

    return feedback

def teacher_comment(avg, trend=0):
    if avg >= 75:
        comment = "The student demonstrates excellent academic performance and strong conceptual clarity."
    elif avg >= 50:
        comment = "The student shows satisfactory progress but needs more consistency."
    else:
        comment = "The student requires significant improvement and focused academic effort."

    if trend > 0:
        comment += " Positive growth trend observed, which is encouraging."
    else:
        comment += " Performance trend needs improvement."

    comment += " Regular revision and disciplined study habits are recommended."

    return comment
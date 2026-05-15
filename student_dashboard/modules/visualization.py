from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def student_trend(df, student_id):

    data = df[df["student_id"] == student_id].copy()

    fig = px.line(
        data,
        x="subject",
        y="marks",
        markers=True,
        title="Student Performance Trend"
    )

    # Premium Line Styling
    fig.update_traces(
        line=dict(
            color="#C80D0D",
            width=5,
            shape="spline",
           
        ),
        
        marker=dict(
            size=12,
            color="#68EC04",
            line=dict(
                color="white",
                width=2
            )
        ),
        
    


        mode="lines+markers+text",
        text=data["marks"],
        textposition="top center",
        fill='tozeroy',
        fillcolor='rgba(150, 13, 13, 0.10)'
    )

    # Layout Styling
    fig.update_layout(
        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            size=14
        ),

        title=dict(
            x=0.5,
            font=dict(size=24)
        ),

        xaxis=dict(
            title="Subjects",
            showgrid=False,
            tickangle=-15
        ),

        yaxis=dict(
            title="Marks",
            range=[0, 100],
            gridcolor="rgba(255,255,255,0.08)"
        ),

        hovermode="x unified",

        height=500
    )
    
    return fig


def cluster_plot(segmented_df):
    fig = px.scatter(
        segmented_df,
        x="mean",
        y="sum",
        color="cluster",
        title="Student Segmentation"
    )
    fig.update_layout(
      template="plotly_dark",
      paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",
      font=dict(color="white")
)
    
    return fig


def forecast_plot(df, student_id):

    data = df[df["student_id"] == student_id]

    y = data["marks"].values
    x = list(range(len(y)))

    if len(y) < 2:
        return None

    # Linear Forecast
    coef = np.polyfit(x, y, 1)

    future_x = list(range(len(y) + 3))
    future_y = np.polyval(coef, future_x)

    fig = px.line(
        x=future_x,
        y=future_y,
        markers=True,
        title="Future Performance Forecast"
    )

    # Premium Forecast Styling
    fig.update_traces(

        line=dict(
            color="#48E201",
            width=5,
            shape="spline"
        ),

        marker=dict(
            size=11,
            color="#F59E0B",
            line=dict(
                color="white",
                width=2
            )
        ),

        mode="lines+markers+text",

        text=[round(v, 1) for v in future_y],
        textposition="top center",

        fill="tozeroy",
        fillcolor="rgba(34,197,94,0.15)"
    )

    # Layout
    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            size=14
        ),

        title=dict(
            x=0.5,
            font=dict(size=24)
        ),

        xaxis=dict(
            title="Future Exams",
            showgrid=False
        ),

        yaxis=dict(
            title="Predicted Marks",
            range=[0, 100],
            gridcolor="rgba(255,255,255,0.08)"
        ),

        hovermode="x unified",

        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=14,
            font_color="white"
        ),

        height=500
    )

    return fig

def marks_distribution(df):

    fig = px.histogram(
        df,
        x="marks",
        nbins=20,
        color_discrete_sequence=["#2390D0"],
        title="Marks Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        bargap=0.08
    )

    fig.update_traces(
        marker_line_width=1,
        marker_line_color="white"
    )

    return fig

def subject_bar(df):

    # Calculate average marks per subject
    subject_avg = (
        df.groupby("subject")["marks"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        subject_avg,
        x="subject",
        y="marks",
        color="subject",
        title="Average Subject Performance",
        color_discrete_sequence=[
            "#60A5FA",
            "#8B5CF6",
            "#22C55E",
            "#F59E0B",
            "#EF4444",
            "#14B8A6"
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis_title="Subjects",
        yaxis_title="Average Marks",
        yaxis=dict(range=[0,100]),
        showlegend=False
    )

    fig.update_traces(
        marker_line_width=0
    )

    return fig

def pass_fail_pie(df):

    df = df.copy()

    df["result"] = df["marks"].apply(
        lambda x: "Pass" if x >= 40 else "Fail"
    )

    summary = df["result"].value_counts().reset_index()
    summary.columns = ["Result", "Count"]

    fig = px.pie(
        summary,
        names="Result",
        values="Count",
        color="Result",
        color_discrete_map={
            "Pass": "#22C55E",
            "Fail": "#EF4444"
        },
        hole=0.45,
        title="Pass vs Fail"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    fig.update_traces(
        textinfo="percent+label",
        pull=[0.03, 0]
    )

    return fig

def forecast_plot(df, student_id):

    student = df[df["student_id"] == student_id]

    if len(student) < 2:
        return None

    marks = student["marks"].values

    # X-axis
    x = np.arange(len(marks)).reshape(-1, 1)

    # Train regression model
    model = LinearRegression()
    model.fit(x, marks)

    # Predict future points
    future_x = np.arange(len(marks) + 3).reshape(-1, 1)

    predictions = model.predict(future_x)

    # Labels
    labels = [
        f"Test {i+1}"
        for i in range(len(predictions))
    ]

    # Create graph
    fig = go.Figure()

    # Actual Marks
    fig.add_trace(
        go.Scatter(
            x=labels[:len(marks)],
            y=marks,
            mode="lines+markers",
            name="Actual Performance"
        )
    )

    # Forecast
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=predictions,
            mode="lines+markers",
            name="Forecast Prediction",
            line=dict(dash="dash")
        )
    )

    fig.update_layout(
        title="📈 AI Forecasted Academic Trend",
        template="plotly_dark",
        height=500,
        xaxis_title="Assessments",
        yaxis_title="Marks",
        legend_title="Analysis"
    )

    return fig
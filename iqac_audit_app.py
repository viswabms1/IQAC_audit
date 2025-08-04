import streamlit as st
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import base64
import os

# ------------------- LOGIN -------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.set_page_config(page_title="IQAC Login", layout="centered")
    st.title("🔒 IQAC Report Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "iqac" and password == "dsu2025":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password")
    st.stop()

# ------------------- PAGE SETUP -------------------
st.set_page_config(page_title="IQAC Audit Report", layout="wide")
st.markdown("### INTERNAL QUALITY ASSURANCE CELL (IQAC)")
st.markdown("## Academic Preparedness Audit")
st.image("logo.png", width=100)

# ------------------- BASIC INFO -------------------
school_name = st.text_input("School Name")
department_name = st.text_input("Department Name")
academic_year = st.text_input("Academic Year (e.g., 2024–25)")

# ------------------- CHECKLIST -------------------
checklist = {
    "1. Curriculum and Academic Planning": [
        ("1a", "Approved Department-level academic calendar aligned with university calendar."),
        ("1b", "Course allocation sheet available and faculty assigned as per expertise."),
        ("1c", "Approved Lesson plans prepared with CO-PO mapping, teaching materials, and references."),
        ("1d", "Approved Finalized timetable for theory/lab/tutorials."),
        ("1e", "Approved List of electives and value added/NPTEL courses.")
    ],
    "2. Faculty Readiness": [
        ("2a", "Approved Faculty workload."),
        ("2b", "Updated faculty profiles"),
        ("2c", "Orientation/training sessions conducted and documented with feedback")
    ],
    "3. Student Preparedness and Support": [
        ("3a", "Plan for Bridge/induction courses for lateral entries."),
        ("3b", "Approved Mentor-mentee allocation list"),
        ("3c", "Plan for supporting slow and advanced learners")
    ],
    "4. Infrastructure and Lab readiness": [
        ("4a", "Lab equipment verified for functionality and calibration done"),
        ("4b", "All required software/tools installed and verified."),
        ("4c", "Lab manuals updated, CO-mapped, and accessible to students")
    ],
    "5. Assessment and Evaluation": [
        ("5a", "Approved Rubrics for practicals, projects, and seminars")
    ],
    "6. Academic documentation": [
        ("6a", "Previous semester result analysis with comparative trends and action points."),
        ("6b", "Report on Action taken on previous audit/feedback")
    ],
    "7. Quality Assurance and Compliance": [
        ("7a", "List and status of active industry-academia MoUs with utilization report"),
        ("7b", "Plan/calendar for guest lectures, workshops, and FDPs.")
    ],
    "8. Research and Innovation": [
        ("8a", "Innovation/Entrepreneurship activities planned")
    ],
    "9. Student Activities and Outreach": [
        ("9a", "Activity list of Cocurricular and Extracurricular"),
        ("9b", "Alumni interaction plans")
    ]
}

form_data = []
for section, items in checklist.items():
    st.subheader(section)
    for code, text in items:
        col1, col2 = st.columns([1, 4])
        with col1:
            response = st.radio(f"{code}_resp", ["Yes", "No", "N.A."], key=f"resp_{code}", horizontal=True)
        with col2:
            remark = st.text_input(f"{code}_remark", placeholder="Remarks", key=f"rem_{code}")
        form_data.append({
            "section": section,
            "code": code,
            "text": text,
            "response": response,
            "remark": remark
        })

# ------------------- GENERATE REPORT -------------------
if st.button("Generate Report"):
    grouped = {}
    for entry in form_data:
        grouped.setdefault(entry['section'], []).append({
            "code": entry["code"],
            "text": entry["text"],
            "response": entry["response"],
            "remark": entry["remark"]
        })
    report = [{"title": sec, "items": grouped[sec]} for sec in grouped]

    with open("logo.png", "rb") as img:
        logo_base64 = base64.b64encode(img.read()).decode("utf-8")

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")

    html_output = template.render(
        report=report,
        date=datetime.now().strftime("%d-%m-%Y"),
        time=datetime.now().strftime("%I:%M %p"),
        school_name=school_name,
        department_name=department_name,
        academic_year=academic_year,
        logo_base64=logo_base64
    )

    with open("IQAC_Audit_Report.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    with open("IQAC_Audit_Report.html", "rb") as f:
        st.download_button(
            label="📄 Download HTML Report (Open & Print)",
            data=f,
            file_name="IQAC_Audit_Report.html",
            mime="text/html"
        )

    st.markdown("💡 Open the downloaded HTML in your browser and press **Ctrl+P → Save as PDF**.")

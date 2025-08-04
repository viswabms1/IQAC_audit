import streamlit as st
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
now = datetime.utcnow() + timedelta(hours=5, minutes=30)


import base64
import os

st.set_page_config(layout="wide")

# Auth
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
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

st.title("📋 Academic Preparedness Audit Form")

school_name = st.text_input("School Name")
department_name = st.text_input("Department Name")
academic_year = st.text_input("Academic Year")

questions = {
    "1. Curriculum and Academic Planning": [
        ("1a", "Department-level academic calendar aligned with university calendar"),
        ("1b", "Course allocation sheet available and faculty assigned as per expertise"),
        ("1c", "Approved Lesson plans with CO-PO mapping and references"),
        ("1d", "Finalized timetable for theory/lab/tutorials"),
        ("1e", "List of electives and value-added/NPTEL courses approved")
    ],
    "2. Faculty Readiness": [
        ("2a", "Approved Faculty workload"),
        ("2b", "Updated faculty profiles"),
        ("2c", "Orientation/training sessions documented")
    ],
    "3. Student Preparedness and Support": [
        ("3a", "Bridge/induction course plan for lateral entries"),
        ("3b", "Mentor-mentee allocation list"),
        ("3c", "Support plans for slow and advanced learners")
    ],
    "4. Infrastructure and Lab Readiness": [
        ("4a", "Lab equipment verified and calibrated"),
        ("4b", "Required software/tools installed"),
        ("4c", "Lab manuals updated and CO-mapped")
    ],
    "5. Assessment and Evaluation": [
        ("5a", "Rubrics for practicals, projects, and seminars approved")
    ],
    "6. Academic Documentation": [
        ("6a", "Previous semester result analysis and action points"),
        ("6b", "Action taken report on previous audit/feedback")
    ],
    "7. Quality Assurance and Compliance": [
        ("7a", "List of active industry-academia MoUs and utilization report"),
        ("7b", "Calendar for guest lectures, workshops, and FDPs")
    ],
    "8. Research and Innovation": [
        ("8a", "Innovation/Entrepreneurship activities planned")
    ],
    "9. Student Activities and Outreach": [
        ("9a", "Cocurricular and Extracurricular activity list"),
        ("9b", "Alumni interaction plans")
    ]
}

with st.form("audit_form"):
    responses = {}
    for section, items in questions.items():
        st.subheader(section)
        for code, text in items:
            resp = st.radio(f"{code}) {text}", ["Yes", "No", "N.A."], key=f"{code}_resp")
            remark = st.text_input(f"Remarks for {code}", key=f"{code}_remark")
            responses[code] = {"text": text, "response": resp, "remark": remark}
    submitted = st.form_submit_button("✅ Generate Report")

if submitted:
    report = []
    for section, items in questions.items():
        section_items = []
        for code, _ in items:
            entry = responses[code]
            section_items.append({
                "code": code,
                "text": entry["text"],
                "response": entry["response"],
                "remark": entry["remark"]
            })
        report.append({"title": section, "items": section_items})

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("report_template.html")

    def get_base64_logo(path="logo.png"):
        if not os.path.exists(path):
            return ""
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    logo_base64 = get_base64_logo()

    html = template.render(
    academic_year=academic_year,
    school_name=school_name,
    department_name=department_name,
    date=now.strftime("%d-%m-%Y"),
    time=now.strftime("%I:%M %p"),
    report=report,
    logo_base64=logo_base64
)

    st.download_button("📄 Download Report as HTML", data=html, file_name="iqac_audit_report.html", mime="text/html")
    st.components.v1.html(html, height=800, scrolling=True)



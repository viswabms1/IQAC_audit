# IQAC Audit Report App

This Streamlit app allows department coordinators to complete an IQAC Academic Preparedness Audit form and generate a downloadable, printable HTML report.

## Features
- Login protected (username: `iqac`, password: `dsu2025`)
- Academic year, school, department details
- Structured checklist (Yes/No/NA with remarks)
- Generates printable HTML report
- Save report as PDF using browser (Ctrl+P → Save as PDF)

## How to Run

```bash
pip install -r requirements.txt
streamlit run iqac_audit_app.py
```

## Files
- `iqac_audit_app.py` — main Streamlit app (not included in this ZIP, paste your code)
- `templates/report_template.html` — Jinja2 template for the report
- `logo.png` — Place your institutional logo with this name in the same folder

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import datetime

BASE_DIR = os.path.dirname(__file__)

def generate_report(task_id, url, test_type, findings):

    reports_dir = os.path.join(BASE_DIR, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    file_path = os.path.join(reports_dir, f"report_{task_id}.pdf")

    c = canvas.Canvas(file_path, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "RAPID API Security Assessment Report")

    y -= 40

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Target API: {url}")
    y -= 20

    c.drawString(50, y, f"Test Type: {test_type}")
    y -= 20

    c.drawString(50, y, f"Generated: {datetime.datetime.now()}")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Findings")

    y -= 20
    c.setFont("Helvetica", 11)

    if not findings:
        c.drawString(60, y, "No vulnerabilities detected during testing.")
        y -= 20

    for v in findings:

        description = v.get("description", "")
        mitigation = v.get("mitigation", "")
        severity = v.get("severity", "")
        cvss = v.get("cvss", "")

        c.drawString(60, y, f"Vulnerability: {description}")
        y -= 15

        c.drawString(80, y, f"Severity Level: {severity}")
        y -= 15

        c.drawString(80, y, f"CVSS Score: {cvss}")
        y -= 15

        c.drawString(80, y, f"Mitigation: {mitigation}")
        y -= 25

        if y < 100:
            c.showPage()
            y = 750

    c.save()

    return file_path
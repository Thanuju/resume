from flask import Flask, render_template, request, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_resume():
    # Collect form data
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    linkedin = request.form.get("linkedin")
    github = request.form.get("github")
    skills = request.form.get("skills")
    education = request.form.get("education")
    experience = request.form.get("experience")
    projects = request.form.get("projects")
    certificates = request.form.get("certificates")

    # PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Header
    header_style = styles['Heading1']
    header_style.textColor = colors.HexColor("#2E86C1")
    elements.append(Paragraph(f"{name}", header_style))
    elements.append(Paragraph(f"📧 {email} | 📱 {phone}", styles['Normal']))
    elements.append(Paragraph(f"🔗 LinkedIn: {linkedin}", styles['Normal']))
    elements.append(Paragraph(f"💻 GitHub: {github}", styles['Normal']))
    elements.append(Spacer(1, 15))

    # Section function
    def add_section(title, content):
        section_title = Paragraph(f"<b>{title}</b>", styles['Heading2'])
        elements.append(section_title)
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(content.replace("\n", "<br/>"), styles['Normal']))
        elements.append(Spacer(1, 12))

    # Add formatted sections
    add_section("Skills", skills if skills else "N/A")
    add_section("Education", education if education else "N/A")
    add_section("Experience", experience if experience else "N/A")
    add_section("Projects", projects if projects else "N/A")
    add_section("Certificates", certificates if certificates else "N/A")

    # Build PDF
    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="resume.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)

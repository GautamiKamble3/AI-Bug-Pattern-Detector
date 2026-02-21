from flask import Flask, render_template, request, session, redirect, url_for, send_file
from detector.bug_detector import analyze_code
from database import (
    init_db, save_bug_report, get_all_reports,
    init_user_table, create_user, validate_user
)

import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "secret123"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if validate_user(username, password):
            session["user"] = username
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if create_user(username, password):
            return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    bugs = None

    if request.method == "POST":
        file = request.files["codefile"]
        code = file.read().decode("utf-8")

        bugs = analyze_code(code)
        save_bug_report(session["user"], file.filename, bugs)

    reports = get_all_reports(session["user"])


    bug_counts = [len(r[1].split(",")) if r[1] != "No bugs" else 0 for r in reports]

    return render_template("index.html", bugs=bugs, reports=reports, bug_counts=bug_counts)


@app.route("/download/<filename>")
def download_pdf(filename):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph(f"Bug Report for {filename}", styles["Title"]))
    elements.append(Spacer(1, 20))

    reports = get_all_reports()
    for r in reports:
        if r[0] == filename:
            elements.append(Paragraph(f"Bugs: {r[1]}", styles["Normal"]))
            elements.append(Paragraph(f"Time: {r[2]}", styles["Normal"]))

    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="bug_report.pdf", mimetype="application/pdf")


if __name__ == "__main__":
    init_db()
    init_user_table()
    app.run(debug=True)

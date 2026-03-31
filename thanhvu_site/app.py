from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from thanhvu_site.translations import TRANSLATIONS
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

@app.context_processor
def inject_translations():
    lang = session.get('lang', 'en')
    return {'t': TRANSLATIONS[lang], 'lang': lang}

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "ngntram04@gmail.com"
app.config["MAIL_PASSWORD"] = "wvcgpyycojlggdbk"
app.config["MAIL_DEFAULT_SENDER"] = "ngntram04@gmail.com"

mail = Mail(app)


# ─────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────

@app.route("/set-lang/<code>")
def set_lang(code):
    if code in ('en', 'vi'):
        session['lang'] = code
    return redirect(request.referrer or url_for('home'))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name  = request.form.get("last_name",  "").strip()
        email      = request.form.get("email",      "").strip()
        phone      = request.form.get("phone",      "").strip()
        business   = request.form.get("business",   "").strip()
        service    = request.form.get("service",    "").strip()
        message    = request.form.get("message",    "").strip()

        try:
            msg = Message(
                subject=f"New Contact Form Enquiry from {first_name} {last_name}",
                recipients=["ngntram04@gmail.com"],
            )
            msg.body = f"""New contact form submission

First name: {first_name}
Last name:  {last_name}
Email:      {email}
Phone:      {phone}
Business:   {business}
Service:    {service}

Message:
{message}
"""
            mail.send(msg)
            flash("Your message has been sent successfully.", "success")
        except Exception as e:
            print(e)
            flash("Sorry, something went wrong. Please try again.", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "GET":
        return redirect(url_for("contact"))
    if request.method == "POST":
        name    = request.form.get("name",    "").strip()
        email   = request.form.get("email",   "").strip()
        phone   = request.form.get("phone",   "").strip()
        service = request.form.get("service", "").strip()
        date    = request.form.get("date",    "").strip()
        time    = request.form.get("time",    "").strip()
        notes   = request.form.get("notes",   "").strip()

        try:
            msg = Message(
                subject=f"New Appointment Request from {name}",
                recipients=["ngntram04@gmail.com"],
            )
            msg.body = f"""New appointment booking request

Name:     {name}
Email:    {email}
Phone:    {phone}
Service:  {service}
Date:     {date}
Time:     {time}

Notes:
{notes}
"""
            mail.send(msg)
            flash("Your appointment request has been sent! We will confirm shortly.", "success")
        except Exception as e:
            print(e)
            flash("Sorry, something went wrong. Please try again.", "danger")

        return redirect(url_for("book"))

    return render_template("book.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard/spreadsheet")
def dashboard_spreadsheet():
    return render_template("dashboard-spreadsheet.html")


@app.route("/dashboard/calculator")
def dashboard_calculator():
    return render_template("dashboard-web-calculator.html")


# ─────────────────────────────────────────────
#  Error handlers
# ─────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("home.html"), 404


@app.errorhandler(500)
def server_error(e):
    return "<h2>500 — Something went wrong.</h2>", 500

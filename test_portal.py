#!/usr/bin/env python3
"""
Local test portal for browser automation testing.

A simple Flask app with:
  - Login page (username/password)
  - Dashboard with date picker
  - CSV report generation and download

Run:  python test_portal.py
Then: open http://localhost:5050

Credentials: testuser / testpass123
"""

import csv
import io
import random
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session, make_response, flash
)

app = Flask(__name__)
app.secret_key = "test-portal-secret-key-for-automation"

# --- Test credentials ---
TEST_USER = "testuser"
TEST_PASS = "testpass123"

# --- HTML Templates ---

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Test Portal - Login</title>
<style>
  body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex;
         justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
  .login-box { background: white; padding: 40px; border-radius: 8px;
               box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 350px; }
  h2 { text-align: center; color: #333; margin-bottom: 24px; }
  label { display: block; margin-bottom: 4px; font-weight: bold; color: #555; }
  input[type=text], input[type=password] {
    width: 100%; padding: 10px; margin-bottom: 16px; border: 1px solid #ddd;
    border-radius: 4px; box-sizing: border-box; font-size: 14px; }
  button { width: 100%; padding: 12px; background: #4a90d9; color: white;
           border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
  button:hover { background: #357abd; }
  .error { color: red; text-align: center; margin-bottom: 12px; }
  .info { color: #666; text-align: center; font-size: 12px; margin-top: 16px; }
</style>
</head>
<body>
  <div class="login-box">
    <h2>Test Portal Login</h2>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    <form method="POST" action="/login">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" placeholder="Enter username" required>
      <label for="password">Password</label>
      <input type="password" id="password" name="password" placeholder="Enter password" required>
      <button type="submit" id="login-btn">Login</button>
    </form>
    <p class="info">Test credentials: testuser / testpass123</p>
  </div>
</body>
</html>
"""

DASHBOARD_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Test Portal - Reports Dashboard</title>
<style>
  body { font-family: Arial, sans-serif; background: #f0f2f5; margin: 0; }
  .navbar { background: #4a90d9; color: white; padding: 12px 24px;
            display: flex; justify-content: space-between; align-items: center; }
  .navbar a { color: white; text-decoration: none; }
  .container { max-width: 800px; margin: 30px auto; padding: 0 20px; }
  .card { background: white; border-radius: 8px; padding: 30px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
  h2 { color: #333; margin-top: 0; }
  label { display: block; margin-bottom: 4px; font-weight: bold; color: #555; }
  input[type=date] { padding: 10px; border: 1px solid #ddd; border-radius: 4px;
                     font-size: 14px; width: 200px; }
  select { padding: 10px; border: 1px solid #ddd; border-radius: 4px;
           font-size: 14px; width: 220px; }
  .form-row { display: flex; gap: 20px; align-items: flex-end; margin-bottom: 16px; }
  .form-group { display: flex; flex-direction: column; }
  .btn { padding: 12px 24px; background: #4a90d9; color: white; border: none;
         border-radius: 4px; font-size: 14px; cursor: pointer; text-decoration: none;
         display: inline-block; }
  .btn:hover { background: #357abd; }
  .btn-green { background: #5cb85c; }
  .btn-green:hover { background: #4cae4c; }
  .success { color: green; font-weight: bold; margin: 12px 0; }
  table { width: 100%; border-collapse: collapse; margin-top: 16px; }
  th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
  th { background: #f5f5f5; }
  .welcome { font-size: 18px; margin-bottom: 8px; }
</style>
</head>
<body>
  <div class="navbar">
    <span><strong>Test Portal</strong> - Reports Dashboard</span>
    <a href="/logout">Logout</a>
  </div>
  <div class="container">
    <div class="card">
      <p class="welcome">Welcome, <strong>{{ username }}</strong>!</p>
      <p>Generate and download usage reports by selecting a date range and report type below.</p>
    </div>

    <div class="card">
      <h2>Generate Report</h2>
      <form method="POST" action="/generate-report">
        <div class="form-row">
          <div class="form-group">
            <label for="report_type">Report Type</label>
            <select id="report_type" name="report_type">
              <option value="usage">Usage Summary</option>
              <option value="billing">Billing Report</option>
              <option value="activity">Activity Log</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="start_date">Start Date</label>
            <input type="date" id="start_date" name="start_date" value="{{ default_start }}" required>
          </div>
          <div class="form-group">
            <label for="end_date">End Date</label>
            <input type="date" id="end_date" name="end_date" value="{{ default_end }}" required>
          </div>
          <div class="form-group">
            <button type="submit" class="btn" id="generate-btn">Generate Report</button>
          </div>
        </div>
      </form>

      {% if report_data %}
      <hr>
      <h3>Report Results: {{ report_title }}</h3>
      <p>Period: {{ period }}</p>
      <table>
        <thead>
          <tr>{% for col in columns %}<th>{{ col }}</th>{% endfor %}</tr>
        </thead>
        <tbody>
          {% for row in report_data %}
          <tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>
          {% endfor %}
        </tbody>
      </table>
      <br>
      <a href="/download-report?type={{ report_type }}&start={{ start_date }}&end={{ end_date }}"
         class="btn btn-green" id="download-btn">Download CSV</a>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def generate_report_data(report_type, start_date, end_date):
    """Generate fake report data for the given date range."""
    rows = []
    current = start_date
    while current <= end_date:
        if report_type == "usage":
            rows.append([
                current.strftime("%Y-%m-%d"),
                f"{random.randint(50, 500)} kWh",
                f"${random.randint(5, 80):.2f}",
                random.choice(["Normal", "Peak", "Off-Peak"]),
            ])
        elif report_type == "billing":
            rows.append([
                current.strftime("%Y-%m-%d"),
                f"INV-{random.randint(10000, 99999)}",
                f"${random.randint(20, 300):.2f}",
                random.choice(["Paid", "Pending", "Overdue"]),
            ])
        elif report_type == "activity":
            rows.append([
                current.strftime("%Y-%m-%d"),
                random.choice(["Login", "Report Generated", "Settings Changed", "Export", "Profile Updated"]),
                f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                random.choice(["Admin", "User", "System"]),
            ])
        current += timedelta(days=1)
    return rows


REPORT_COLUMNS = {
    "usage": ["Date", "Consumption", "Cost", "Rate Type"],
    "billing": ["Date", "Invoice #", "Amount", "Status"],
    "activity": ["Date", "Action", "Time", "Performed By"],
}

REPORT_TITLES = {
    "usage": "Usage Summary",
    "billing": "Billing Report",
    "activity": "Activity Log",
}


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == TEST_USER and password == TEST_PASS:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"
    return render_template_string(LOGIN_PAGE, error=error)


@app.route("/dashboard")
@login_required
def dashboard():
    today = datetime.now()
    default_start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    default_end = today.strftime("%Y-%m-%d")
    return render_template_string(
        DASHBOARD_PAGE,
        username=session["user"],
        default_start=default_start,
        default_end=default_end,
        report_data=None,
        columns=[],
        report_title="",
        period="",
        report_type="",
        start_date="",
        end_date="",
    )


@app.route("/generate-report", methods=["POST"])
@login_required
def generate_report():
    report_type = request.form.get("report_type", "usage")
    start_str = request.form.get("start_date", "")
    end_str = request.form.get("end_date", "")

    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
    except ValueError:
        return redirect(url_for("dashboard"))

    report_data = generate_report_data(report_type, start_date, end_date)
    columns = REPORT_COLUMNS.get(report_type, [])
    title = REPORT_TITLES.get(report_type, "Report")

    today = datetime.now()
    default_start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    default_end = today.strftime("%Y-%m-%d")

    return render_template_string(
        DASHBOARD_PAGE,
        username=session["user"],
        default_start=default_start,
        default_end=default_end,
        report_data=report_data,
        columns=columns,
        report_title=title,
        period=f"{start_str} to {end_str}",
        report_type=report_type,
        start_date=start_str,
        end_date=end_str,
    )


@app.route("/download-report")
@login_required
def download_report():
    report_type = request.args.get("type", "usage")
    start_str = request.args.get("start", "")
    end_str = request.args.get("end", "")

    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
    except ValueError:
        return redirect(url_for("dashboard"))

    columns = REPORT_COLUMNS.get(report_type, [])
    rows = generate_report_data(report_type, start_date, end_date)

    # Build CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)

    response = make_response(output.getvalue())
    filename = f"{report_type}_report_{start_str}_to_{end_str}.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    return response


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    print("=" * 50)
    print("  TEST PORTAL RUNNING")
    print("  URL:  http://localhost:5050")
    print("  User: testuser")
    print("  Pass: testpass123")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5050, debug=False)

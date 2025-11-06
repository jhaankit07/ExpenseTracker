from flask import Flask, render_template, request, redirect, send_file
import csv, os
from datetime import datetime

app = Flask(__name__)
FILE = "expenses.csv"
MONTHLY_LIMIT = 2000

# Create CSV if not exists
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Amount", "Description"])

@app.route("/")
def index():
    expenses = []
    total = 0
    with open(FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(row)
            total += float(row["Amount"])

    # Smart spending message
    if total > MONTHLY_LIMIT:
        message = f"⚠️ You crossed your monthly limit of ₹{MONTHLY_LIMIT}!"
    elif total > 1000:
        message = "You're spending a lot, try to control it!"
    else:
        message = "Good job! You're managing your expenses well!"

    # Greeting based on time
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        greet = "Good Morning ☀️"
    elif hour < 18:
        greet = "Good Afternoon 🌞"
    else:
        greet = "Good Evening 🌙"

    return render_template("index.html", expenses=expenses, total=total, message=message, greet=greet)

@app.route("/add", methods=["POST"])
def add():
    date = request.form["date"]
    category = request.form["category"]
    amount = request.form["amount"]
    desc = request.form["description"]

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount, desc])

    return redirect("/")

@app.route("/download")
def download():
    return send_file(FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

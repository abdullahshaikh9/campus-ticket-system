import os
import secrets

from flask import Flask, render_template, request, redirect, session, flash
from db import init_db, authenticate, create_ticket, get_student_tickets, get_all_tickets, update_ticket_status

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = authenticate(request.form["username"], request.form["password"])
        if user:
            session["user_id"] = user["user_id"]
            session["role"] = user["role"]
            session["username"] = user["username"]
            return redirect("/dashboard")
        flash("Invalid credentials", "error")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    
    if session["role"] == "student":
        tickets = get_student_tickets(session["user_id"])
        return render_template("student_dashboard.html", tickets=tickets)
    else:
        tickets = get_all_tickets()
        return render_template("admin_dashboard.html", tickets=tickets)

@app.route("/submit_ticket", methods=["POST"])
def submit_ticket():
    if session.get("role") != "student":
        return redirect("/")
    title = request.form["title"]
    category = request.form["category"]
    create_ticket(session["user_id"], title, category)
    flash("Ticket submitted successfully!", "success")
    return redirect("/dashboard")

@app.route("/update_status", methods=["POST"])
def update_status():
    if session.get("role") != "admin":
        return redirect("/")
    ticket_id = request.form["ticket_id"]
    new_status = request.form["new_status"]
    success, msg = update_ticket_status(ticket_id, new_status)
    flash(msg, "success" if success else "error")
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

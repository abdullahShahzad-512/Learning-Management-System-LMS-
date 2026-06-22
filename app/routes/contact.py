from flask import render_template, request, flash, redirect, url_for
from . import main

@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Example action (you can replace with DB/email logic)
        print(name, email, message)

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html")
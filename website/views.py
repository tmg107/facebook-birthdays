from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
# Anything not related to authetication, show pages to website here

views = Blueprint('views', __name__)

# Add decorator to require login
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)











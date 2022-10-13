from app_config import app
from flask import render_template


@app.route('/')
def index():
  return render_template('pages/home.html')

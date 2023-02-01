import os
from flask import Flask, render_template, request, redirect, url_for, flash, g, abort
from datetime import datetime

# Import database models and utility functions
from models import ShortURL, Click, init_db, get_db_connection, close_db_connection
from utils import generate_unique_short_code, is_valid_url, is_valid_custom_code

# --- Flask App Initialization ---
app = Flask(__name__, instance_relative_config=True)

# Load configuration from config.py
# This includes SECRET_KEY and DATABASE path
app.config.from_object('config')

# Ensure the instance folder exists for the database
try:
    os.makedirs(app.instance_path)
except OSError:
    pass # Folder already exists

# --- Database Setup and Teardown ---

def get_db():
    """
    Establishes a database connection if one is not already present in the global
    `g` object for the current request. The connection
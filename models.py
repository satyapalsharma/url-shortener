from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy. This object will be initialized with the Flask app
# in app.py using db.init_app(app). This allows models to be defined before
# the app object is fully created.
db = SQLAlchemy()

class URL(db.Model):
    """
    Represents a shortened URL entry in the database.
    Each entry stores the original long URL, its unique short code,
    creation details, and basic analytics.
    """
    __tablename__ = 'urls' # Explicitly define table name for clarity

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False, index=True)
    # Max URL length can be very long, 2048 characters is a common practical limit.
    # Indexing improves lookup performance for original URLs.

    short_code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    # The unique short identifier for the URL.
    # Max length 16 allows for a large number of unique codes (e.g., base62).
    # Unique constraint ensures no two short codes are the same.
    # Indexing improves lookup performance for short codes.

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Timestamp when the short URL was created.
    # Using datetime.utcnow ensures timezone-agnostic storage, which is a best practice.

    expires_at = db.Column(db.DateTime, nullable=True)
    # Optional expiration date for the short URL. If null, it never expires.

    clicks = db.Column(db.Integer, default=0, nullable=False)
    # Counter for the total number of times this short URL has been clicked.

    last_clicked_at = db.Column(db.DateTime, nullable=True)
    # Timestamp of the most recent click.

    custom_code = db.Column(db.Boolean, default=False, nullable=False)
    # Flag to indicate if the short_code was user-defined (True) or system-generated (False).

    creator_ip = db.Column(db.String(45), nullable=True)
    # IP address of the user who created the short URL.
    # Max length 45 accommodates IPv6 addresses. Useful for basic abuse prevention or analytics.

    # Define a relationship to the Click model for analytics.
    # 'clicks_data' will be a list of Click objects associated with this URL.
    # backref='short_url' allows accessing the parent URL from a Click object (e.g., click.short_url).
    # lazy=True means related objects are loaded only when accessed.
    # cascade="all, delete-orphan" ensures that if a URL is deleted, all its associated
    # click records are also deleted from the database.
    clicks_data = db.relationship('Click', backref='short_url', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        """
        Provides a more readable representation of the URL object for debugging.
        """
        return f"<URL {self.short_code}: {self.original_url[:50]}...>"


class Click(db.Model):
    """
    Represents a single click event for a shortened URL, storing detailed analytics.
    """
    __tablename__ = 'clicks' # Explicitly define table name

    id = db.Column(db.Integer, primary_key=True)

    short_url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=False)
    # Foreign key linking this click event to a specific URL entry.
    # 'urls.id' refers to the 'id' column in the 'urls' table.

    clicked_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Timestamp when the click occurred (UTC).

    referrer = db.Column(db.String(2048), nullable=True)
    # The HTTP Referer header, indicating where the click originated from.

    user_agent = db.Column(db.String(512), nullable=True)
    # The User-Agent header, providing information about the client's browser and OS.

    ip_address = db.Column(db.String(45), nullable=True)
    # IP address of the user who clicked the short URL.

    country = db.Column(db.String(64), nullable=True)
    # Country derived from the IP address (e.g., using a GeoIP service).
    # This would typically be populated by a background task or a utility function.

    city = db.Column(db.String(64), nullable=True)
    # City derived from the IP address.

    def __repr__(self):
        """
        Provides a more readable representation of the Click object for debugging.
        """
        return f"<Click {self.id} for URL_ID {self.short_url_id} at {self.clicked_at}>"


def create_tables(app):
    """
    Utility function to create all database tables defined in models.py.
    This should be called once during application setup, typically within
    an application context.

    Args:
        app: The Flask application instance.
    """
    with app.app_context():
        db.create_all()
        print("Database tables created or already exist.")
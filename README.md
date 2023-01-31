# URL Shortener

A robust URL shortening service built with Flask, offering efficient URL management, detailed click analytics, and the flexibility to create custom short codes. This project demonstrates a full-stack web application with a focus on clean architecture, database interaction, and user experience.

## Features

*   **Shorten URLs:** Convert long URLs into concise, shareable short links.
*   **Custom Short Codes:** Users can define their own memorable short codes instead of randomly generated ones.
*   **Click Analytics:** Track the number of clicks for each shortened URL.
*   **Redirects:** Seamlessly redirect users from the short URL to the original long URL.
*   **Database Persistence:** Store URLs and their associated data using SQLite.
*   **Responsive UI:** Simple and intuitive user interface built with HTML/CSS.
*   **Error Handling:** Graceful handling for invalid URLs or non-existent short codes.

## Tech Stack

*   **Backend:** Python, Flask
*   **Database:** SQLite
*   **Frontend:** HTML, CSS, JavaScript (minimal)

## Installation

To get this project up and running on your local machine, follow these steps:

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

### 2. Set up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Database Initialization

The project uses SQLite. The database file `shortener.db` will be created inside the `instance/` directory. You need to initialize the database schema.

```bash
flask --app app init-db
```
*Note: Ensure `FLASK_APP=app.py` is set in your environment or use `python -m flask --app app init-db` if the above command fails.*

### 5. Configuration

The `config.py` file contains default configuration. For production, it's best to use environment variables for sensitive data like `SECRET_KEY`.

You can set environment variables like this (example for Linux/macOS):

```bash
export FLASK_APP=app.py
export FLASK_ENV=development # or production
export SECRET_KEY='your_super_secret_key_here' # Generate a strong, random key
```
On Windows (Command Prompt):
```bash
set FLASK_APP=app.py
set FLASK_ENV=development
set SECRET_KEY=your_super_secret_key_here
```
On Windows (PowerShell):
```powershell
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
$env:SECRET_KEY="your_super_secret_key_here"
```

### 6. Run the Application

Once everything is set up, you can run the Flask development server:

```bash
flask run
```

The application will typically be available at `http://127.0.0.1:5000/`.

## Usage

### Shortening a URL

1.  Navigate to the homepage (`/`).
2.  Enter a long URL into the input field.
3.  (Optional) Enter a desired custom short code. If left blank, a random one will be generated.
4.  Click "Shorten".
5.  You will be redirected to a page showing your new short URL.

### Accessing a Shortened URL

Simply navigate to `http://127.0.0.1:5000/<your-short-code>`. The application will redirect you to the original long URL and increment the click count.

### Viewing Analytics

After shortening a URL, the shortened URL page will display the current click count for that specific short code.

## Project Structure

```
.
├── .gitignore              # Specifies intentionally untracked files to ignore
├── README.md               # This file
├── app.py                  # Main Flask application file, defines routes and core logic
├── config.py               # Configuration settings for the Flask app
├── models.py               # Defines the database schema and ORM models
├── requirements.txt        # Lists all Python dependencies
├── utils.py                # Utility functions (e.g., for generating short codes)
├── instance/               # Contains instance-specific files, like the SQLite database
│   └── shortener.db        # The SQLite database file
├── static/                 # Static assets (CSS, JS, images)
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── main.js         # Client-side JavaScript (if any)
└── templates/              # HTML templates for rendering pages
    ├── analytics.html      # Template for displaying URL analytics
    ├── base.html           # Base template for consistent page structure
    ├── index.html          # Homepage template for URL input
    └── shortened.html      # Template for displaying the shortened URL
```

## Configuration

The `config.py` file holds application-wide settings. Key settings include:

*   `SECRET_KEY`: Essential for session management and security. **MUST be a strong, random value in production.**
*   `DATABASE`: Path to the SQLite database file.

It's recommended to use environment variables for `SECRET_KEY` in production environments to keep sensitive information out of the codebase.

## Database Schema

The `shortener.db` database contains a single table: `urls`.

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_code TEXT UNIQUE NOT NULL,
    clicks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

*   `id`: Primary key, auto-incrementing integer.
*   `original_url`: The full URL provided by the user.
*   `short_code`: The unique, shortened code (e.g., `abcde`).
*   `clicks`: Counter for how many times the short URL has been accessed.
*   `created_at`: Timestamp when the URL was shortened.

## Future Enhancements

*   **User Authentication:** Allow users to register, log in, and manage their own shortened URLs.
*   **Link Expiration:** Set an expiration date for short URLs.
*   **QR Code Generation:** Generate QR codes for shortened URLs.
*   **API Endpoints:** Provide a RESTful API for programmatic URL shortening.
*   **Dockerization:** Containerize the application for easier deployment.
*   **More Advanced Analytics:** Track referrer, browser, OS, etc.
*   **Rate Limiting:** Prevent abuse of the shortening service.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
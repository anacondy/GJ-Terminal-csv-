# app.py
# Government Jobs Dashboard - Flask Application

from flask import Flask, render_template, abort
import sqlite3
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'jobs.db')

app = Flask(__name__)

# Security configurations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False

# Disable debug mode in production
DEBUG_MODE = os.environ.get('FLASK_ENV') == 'development'

# Database connection with security improvements
def get_db_connection():
    """Create and return a database connection with row factory."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            "Database not found. Please run 'python database_setup.py' first."
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Routes ---

# Main page route
@app.route('/')
def index():
    """Display all government jobs in a table format."""
    try:
        conn = get_db_connection()
        jobs = conn.execute('SELECT * FROM jobs ORDER BY id').fetchall()
        conn.close()
        return render_template('index.html', jobs=jobs)
    except Exception as e:
        app.logger.error(f"Error loading jobs: {e}")
        abort(500)

# Job details route with validation
@app.route('/details/<int:job_id>')
def details(job_id):
    """Display detailed information for a specific job."""
    try:
        conn = get_db_connection()
        
        # Fetch job with validation
        job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
        if not job:
            conn.close()
            abort(404)
        
        # Fetch related details and cutoffs
        job_details = conn.execute(
            'SELECT * FROM job_details WHERE job_id = ? ORDER BY id', 
            (job_id,)
        ).fetchall()
        
        job_cutoffs = conn.execute(
            'SELECT * FROM job_cutoffs WHERE job_id = ? ORDER BY category', 
            (job_id,)
        ).fetchall()
        
        conn.close()
        return render_template('details.html', job=job, details=job_details, cutoffs=job_cutoffs)
    except Exception as e:
        app.logger.error(f"Error loading job details for ID {job_id}: {e}")
        abort(500)

# Error handlers
@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return "Job not found", 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return "Internal server error", 500

# Application entry point
if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print("❌ Database not found!")
        print("Please run: python database_setup.py")
        exit(1)
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(
        debug=DEBUG_MODE,
        host='0.0.0.0',
        port=port
    )

# database_setup.py
# FINAL, ROBUST version that uses full paths to find CSV files.

import sqlite3
import csv
import os  # Import the 'os' library to find file paths

# --- This is the "find things" part ---
# It gets the exact "street address" of your project folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

# --- Drop & Recreate tables (unchanged) ---
cursor.execute('DROP TABLE IF EXISTS job_details')
cursor.execute('DROP TABLE IF EXISTS job_cutoffs')
cursor.execute('DROP TABLE IF EXISTS jobs')
cursor.execute(
    '''CREATE TABLE jobs (id INTEGER PRIMARY KEY, post_name TEXT, exam_name TEXT, conducting_body TEXT, "group" TEXT, gazetted_status TEXT, pay_level INTEGER, salary TEXT, eligibility TEXT, age_limit TEXT, pet_status TEXT);''')
cursor.execute(
    '''CREATE TABLE job_details (id INTEGER PRIMARY KEY, job_id INTEGER, category TEXT, title TEXT, description TEXT, FOREIGN KEY (job_id) REFERENCES jobs (id));''')
cursor.execute(
    '''CREATE TABLE job_cutoffs (id INTEGER PRIMARY KEY, job_id INTEGER, category TEXT, cutoff_score TEXT, year INTEGER, FOREIGN KEY (job_id) REFERENCES jobs (id));''')


# --- This function now uses the full path to read the CSV ---
def populate_table(csv_file_name, table_name):
    # Create the full, exact path to the CSV file.
    full_path = os.path.join(BASE_DIR, csv_file_name)

    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            # Use the correct INSERT query for each table
            if table_name == 'jobs':
                query = 'INSERT INTO jobs VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            elif table_name == 'job_details':
                query = 'INSERT INTO job_details VALUES (NULL, ?, ?, ?, ?)'
            elif table_name == 'job_cutoffs':
                query = 'INSERT INTO job_cutoffs VALUES (NULL, ?, ?, ?, ?)'

            for row in reader:
                cursor.execute(query, row)
            print(f"✅ Successfully populated '{table_name}' from '{csv_file_name}'.")
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find '{csv_file_name}'. Make sure it's in the same folder as your Python files.")


# --- Populate each table from its CSV ---
populate_table('jobs.csv', 'jobs')
populate_table('details.csv', 'job_details')
populate_table('cutoffs.csv', 'job_cutoffs')

conn.commit()
conn.close()

print("\nDatabase 'jobs.db' has been successfully built from your CSV files! 🚀")

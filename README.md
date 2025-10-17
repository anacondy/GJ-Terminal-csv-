# GJ Terminal - Government Jobs Dashboard 🚀

A modern, terminal-inspired web application for browsing and exploring government job opportunities in India. Built with Flask and SQLite, featuring a sleek dark theme UI with advanced search, sorting, and detailed job information.

![GJ Terminal Homepage](https://github.com/user-attachments/assets/7f7045ec-27cb-459a-911a-b360fa955f67)

## ✨ Features

- **📊 Comprehensive Job Listings**: Browse 80+ government job positions with complete details
- **🔍 Advanced Search**: Press `Ctrl+K` to open the search overlay and filter jobs instantly
- **⚡ Column Sorting**: Click on any column header to sort jobs by that field
- **🎯 Job Details**: Click on any job to view detailed information including:
  - Eligibility criteria
  - Exam pattern
  - Key roles and responsibilities
  - Salary and benefits
  - Category-wise cutoff scores
- **⌨️ Keyboard Navigation**: Use arrow keys to navigate through the table
- **🎨 Modern UI**: Dark theme with smooth animations and hover effects
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🖼️ Screenshots

### Main Dashboard
![Main Dashboard](https://github.com/user-attachments/assets/7f7045ec-27cb-459a-911a-b360fa955f67)

### Search Functionality
![Search Overlay](https://github.com/user-attachments/assets/acf89c96-70a1-4418-a91a-e4703a2473f7)

### Job Details Page
![Job Details](https://github.com/user-attachments/assets/fe4d0b08-62b2-4fa2-aec9-d6056d0104af)

## 📁 Project Structure

```
GJ-Terminal-csv-/
├── app.py                  # Main Flask application
├── database_setup.py       # Database initialization script
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
├── jobs.csv               # Main jobs data
├── details.csv            # Detailed job information
├── cutoffs.csv            # Cutoff scores by category
├── templates/             # HTML templates
│   ├── index.html         # Main dashboard
│   └── details.html       # Job details page
└── jobs.db                # SQLite database (auto-generated)
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/anacondy/GJ-Terminal-csv-.git
   cd GJ-Terminal-csv-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python database_setup.py
   ```
   
   You should see:
   ```
   ✅ Successfully populated 'jobs' from 'jobs.csv'.
   ✅ Successfully populated 'job_details' from 'details.csv'.
   ✅ Successfully populated 'job_cutoffs' from 'cutoffs.csv'.
   
   Database 'jobs.db' has been successfully built from your CSV files! 🚀
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   
   Navigate to: `http://localhost:5000`

## 🎮 Usage Guide

### Keyboard Shortcuts

- **Ctrl + K**: Open search overlay
- **Escape**: Close search overlay
- **Arrow Keys**: Navigate the table
  - ← → : Scroll horizontally
  - ↑ ↓ : Scroll vertically

### Features

1. **Search**: Press `Ctrl+K` and type to filter jobs in real-time
2. **Sort**: Click on any column header to sort (click again to reverse)
3. **View Details**: Click on any row to see complete job information
4. **Navigate**: Use the back arrow (←) on the details page to return to the dashboard

## 🗄️ Database Schema

### Jobs Table
- `id`: Primary key
- `post_name`: Job position name
- `exam_name`: Examination name
- `conducting_body`: Organization conducting the exam
- `group`: Job group (A, B, C, D)
- `gazetted_status`: Gazetted/Non-Gazetted
- `pay_level`: Government pay scale level
- `salary`: Approximate salary range
- `eligibility`: Education requirements
- `age_limit`: Age criteria
- `pet_status`: Physical test requirement

### Job Details Table
- `id`: Primary key
- `job_id`: Foreign key to jobs table
- `category`: Information category
- `title`: Detail title
- `description`: Detailed information

### Job Cutoffs Table
- `id`: Primary key
- `job_id`: Foreign key to jobs table
- `category`: Reservation category
- `cutoff_score`: Required score
- `year`: Examination year

## 🔒 Security Considerations

### Current Implementation
- ✅ SQL injection protection via parameterized queries
- ✅ Input sanitization through Flask's templating
- ✅ No sensitive data storage
- ✅ Debug mode disabled in production

### Recommendations for Production

1. **Environment Variables**: Store sensitive configuration in environment variables
2. **HTTPS**: Always use HTTPS in production
3. **WSGI Server**: Use production WSGI server like Gunicorn
4. **Database**: Consider PostgreSQL for production
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **CORS**: Configure CORS policies if needed
7. **Content Security Policy**: Add CSP headers

## 🚢 Deployment

### Using Gunicorn (Recommended for Production)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Using Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python database_setup.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t gj-terminal .
docker run -p 5000:5000 gj-terminal
```

### Deployment Platforms

The application can be deployed on:
- **Heroku**: Use Procfile with Gunicorn
- **AWS EC2**: Traditional VM deployment
- **Google Cloud Run**: Containerized deployment
- **Azure App Service**: Web app deployment
- **Railway/Render**: Modern PaaS platforms

## 🔧 Configuration

### Development Mode
```python
app.run(debug=True)  # In app.py
```

### Production Mode
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

Or use environment variables:
```python
import os
app.run(
    debug=os.getenv('DEBUG', 'False') == 'True',
    host=os.getenv('HOST', '0.0.0.0'),
    port=int(os.getenv('PORT', 5000))
)
```

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **Database**: SQLite3 (File-based database)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with Google Fonts (Manrope)
- **Data Format**: CSV files

## 📊 Data Management

### Adding New Jobs

1. Edit `jobs.csv` with the new job information
2. Edit `details.csv` with job details (use the same job_id)
3. Edit `cutoffs.csv` with cutoff scores
4. Re-run `python database_setup.py` to update the database

### CSV Format

**jobs.csv**: POST NAME, EXAM NAME, CONDUCTING BODY, GROUP, GAZETTED STATUS, PAY LEVEL, SALARY, ELIGIBILITY, AGE LIMIT, PET STATUS

**details.csv**: job_id, category, title, description

**cutoffs.csv**: job_id, category, cutoff_score, year

## 🐛 Troubleshooting

### Database not found
```bash
python database_setup.py
```

### Port already in use
Change the port in app.py or:
```bash
python app.py --port 8000
```

### CSV file not found
Ensure CSV files are in the same directory as app.py

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created with ❤️ by the GJ Terminal team - Anuj Meena (GitHub Copilot)

## 🙏 Acknowledgments

- Government job data compiled from various official sources
- Icons and fonts from Google Fonts
- Inspired by modern terminal UI designs

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Your contact information]

---

**Note**: This application is for informational purposes only. Always verify job information from official government sources before applying.

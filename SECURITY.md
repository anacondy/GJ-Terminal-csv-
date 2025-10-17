# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Features

### Current Implementation

✅ **SQL Injection Protection**
- All database queries use parameterized statements
- No raw SQL string concatenation

✅ **Input Validation**
- Flask's built-in input sanitization
- Type checking on route parameters (e.g., `<int:job_id>`)
- Database query validation with error handling

✅ **Template Security**
- Jinja2 auto-escaping enabled by default
- Prevents XSS attacks in rendered HTML

✅ **Error Handling**
- Custom error pages for 404 and 500 errors
- No sensitive information leaked in error messages
- Proper logging without exposing stack traces to users

✅ **Static File Security**
- No user uploads (read-only application)
- All data loaded from trusted CSV files

## Security Recommendations for Production

### 1. Environment Variables
Store sensitive configuration in environment variables:

```bash
export SECRET_KEY='your-random-secret-key-here'
export FLASK_ENV='production'
export DATABASE_URL='your-database-url'
```

### 2. HTTPS/SSL
Always use HTTPS in production:
- Use Let's Encrypt for free SSL certificates
- Configure your reverse proxy (Nginx/Apache) for SSL
- Set `secure` flag on cookies

### 3. WSGI Server
Never use Flask's built-in server in production:

```bash
# Use Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or uWSGI
uwsgi --http :5000 --wsgi-file app.py --callable app
```

### 4. Database Security
For production environments:
- Migrate from SQLite to PostgreSQL/MySQL
- Use database connection pooling
- Implement regular backups
- Use read-only database user for the application

### 5. Rate Limiting
Implement rate limiting to prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### 6. Content Security Policy (CSP)
Add CSP headers to prevent XSS:

```python
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com;"
    )
    return response
```

### 7. Security Headers
Add security headers:

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### 8. CORS Configuration
If building an API, configure CORS properly:

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET"],
        "allow_headers": ["Content-Type"]
    }
})
```

### 9. Logging and Monitoring
- Set up centralized logging (e.g., ELK stack, CloudWatch)
- Monitor for suspicious activity
- Set up alerts for repeated 404s or 500s
- Log all authentication attempts (if implemented)

### 10. Dependency Management
- Regularly update dependencies: `pip list --outdated`
- Use `pip-audit` to check for known vulnerabilities
- Pin exact versions in requirements.txt

```bash
pip install pip-audit
pip-audit
```

## Known Limitations

### Current Security Limitations

⚠️ **No Authentication/Authorization**
- Application is publicly accessible
- No user accounts or access control
- Consider adding authentication if needed

⚠️ **SQLite Database**
- Not recommended for high-traffic production
- No built-in replication
- Limited concurrent write performance

⚠️ **No Rate Limiting**
- Vulnerable to DoS attacks
- No request throttling implemented

⚠️ **Debug Mode**
- Ensure DEBUG=False in production
- Debug mode exposes sensitive information

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email the maintainer directly at: [security@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

You will receive a response within 48 hours. We appreciate responsible disclosure.

## Security Checklist for Deployment

Before deploying to production, ensure:

- [ ] DEBUG mode is disabled
- [ ] SECRET_KEY is changed from default
- [ ] HTTPS/SSL is configured
- [ ] Using production WSGI server (not Flask dev server)
- [ ] Database credentials are in environment variables
- [ ] Security headers are configured
- [ ] Rate limiting is implemented (if needed)
- [ ] Error pages don't expose sensitive info
- [ ] All dependencies are up to date
- [ ] Database backups are configured
- [ ] Logging and monitoring are set up
- [ ] Firewall rules are configured
- [ ] Application runs as non-root user

## Security Updates

We monitor security advisories for:
- Flask and Werkzeug
- Python standard library
- All project dependencies

Updates are applied promptly when security issues are discovered.

## License

This security policy is part of the GJ Terminal project and follows the same MIT License.

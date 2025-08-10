# LibraryProject

This is a simple Django project for managing books and users.

## Features
- Custom User model
- Book management
- User API (create, update, delete, get)

## Setup
1. Clone the repo
2. Install requirements
3. Run migrations
4. Start the server

Security measures in this project
--------------------------------
- DEBUG=False in production.
- AUTH_COOKIE_SECURE and CSRF_COOKIE_SECURE set to True.
- SECURE_SSL_REDIRECT enabled (production).
- HSTS enabled (SECURE_HSTS_SECONDS=31536000).
- X_FRAME_OPTIONS='DENY', SECURE_CONTENT_TYPE_NOSNIFF=True, SECURE_BROWSER_XSS_FILTER=True.
- All forms include {% csrf_token %}. Use Django forms for validation.
- Use ORM queries to avoid SQL injection; raw SQL only with parameterization.
- Content Security Policy set via middleware (or django-csp recommended).
- Use HTTPS/TLS in production (certificate via Let's Encrypt). Set SECURE_PROXY_SSL_HEADER if behind proxy.


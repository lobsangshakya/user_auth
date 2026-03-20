# Quick Reference - Minimal Django OTP Auth

## Run Server
```bash
source venv/bin/activate
python manage.py runserver
```

## URLs
- Signup: http://127.0.0.1:8000/signup/
- Verify: http://127.0.0.1:8000/verify/1/
- Login: http://127.0.0.1:8000/login/
- Dashboard: http://127.0.0.1:8000/dashboard/
- Logout: http://127.0.0.1:8000/logout/

## Flow
1. Signup with email/password → User created (inactive)
2. Check terminal for OTP (printed automatically)
3. Visit /verify/<user_id>/ and enter OTP
4. User activated and verified
5. Login with email/password
6. Access dashboard (protected)

## Key Files
- `minimal/models.py` - User & OTP models
- `minimal/views.py` - 5 view functions
- `minimal/urls.py` - URL routing
- `templates/*.html` - 4 simple templates

## Settings Changes
```python
INSTALLED_APPS += ['minimal']
AUTH_USER_MODEL = 'minimal.User'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

That's it! No complexity, just Django auth basics.

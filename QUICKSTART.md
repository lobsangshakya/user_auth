# Quick Start Guide

## 1. Update Email Settings (config/settings.py)

Replace these lines with your actual email credentials:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 2. Run the Server

```bash
source venv/bin/activate
python manage.py runserver
```

## 3. Test URLs

- Signup: http://127.0.0.1:8000/signup/
- Login: http://127.0.0.1:8000/login/
- Dashboard: http://127.0.0.1:8000/dashboard/

## 4. Testing Without Email

To test without sending real emails, change this in `config/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

The OTP will be printed in the terminal instead of emailed.

## 5. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Access admin panel at: http://127.0.0.1:8000/admin/

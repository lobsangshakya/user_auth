# Django Email OTP Authentication

A minimal Django project demonstrating email-based authentication with OTP verification.

## Project Structure

```
User_auth/
├── accounts/                    # Main authentication app
│   ├── models.py               # User & OTP models
│   ├── views.py                # Signup, OTP, Login views
│   ├── urls.py                 # URL routing
│   └── migrations/             # Database migrations
├── config/                      # Django project settings
│   ├── settings.py             # Configuration (email, DB, etc.)
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py
├── templates/                   # HTML templates
│   ├── signup.html
│   ├── verify_otp.html
│   ├── login.html
│   └── dashboard.html
├── manage.py
└── db.sqlite3                   # SQLite database
```

## Setup Instructions

### 1. Configure Email Settings

Edit `config/settings.py` and update these lines with your email credentials:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

**For Gmail:**
- Use an App Password (not your regular password)
- Generate it at: https://myaccount.google.com/apppasswords

### 2. Run the Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations (already done)
python manage.py migrate

# Start server
python manage.py runserver
```

### 3. Test the Application

1. **Sign Up**: Go to `http://127.0.0.1:8000/signup/`
   - Enter username, email, and password
   - User is created but inactive

2. **Verify OTP**: Check your email for the 6-digit code
   - Go to `http://127.0.0.1:8000/verify-otp/<user_id>/`
   - Enter the OTP code
   - Account becomes active and verified

3. **Login**: Go to `http://127.0.0.1:8000/login/`
   - Use your email and password
   - Only verified users can login

4. **Dashboard**: `http://127.0.0.1:8000/dashboard/`
   - Protected page (requires login)

## How It Works

### Flow Diagram

```
Signup → Generate OTP → Send Email → Store OTP in DB
   ↓
User enters OTP → Verify against DB
   ↓
Valid? → Activate User → Delete OTP
   ↓
Login with email/password → Check if verified
   ↓
Verified? → Grant access to dashboard
```

### Key Components

**1. Models (`accounts/models.py`)**
- `User`: Custom user model using email instead of username
- `OTP`: Stores OTP codes with 5-minute expiry

**2. Views (`accounts/views.py`)**
- `signup_view`: Creates user, generates OTP, sends email
- `verify_otp_view`: Validates OTP, activates user
- `login_view`: Authenticates and checks verification status
- `dashboard_view`: Protected page for verified users

**3. URLs (`accounts/urls.py`)**
- `/signup/` - User registration
- `/verify-otp/<user_id>/` - OTP verification
- `/login/` - User login
- `/dashboard/` - Protected page
- `/logout/` - User logout

## Features

✅ Email-based authentication (no username required for login)
✅ 6-digit OTP generation and email sending
✅ OTP stored in database with 5-minute expiry
✅ User account activation only after OTP verification
✅ Login restricted to verified users only
✅ Simple SMTP email configuration
✅ Clean, minimal code with comments
✅ SQLite database (no setup required)

## Testing Without Real Email

For testing, you can use Django's console email backend. Add this to `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This prints emails to the terminal instead of sending them.

## Security Notes

- This is a learning project - add rate limiting for production
- Use HTTPS in production
- Store email credentials in environment variables
- Add CSRF protection (already included)
- Implement password reset functionality

## Database Schema

**User Table:**
- email (unique)
- password (hashed)
- is_verified (boolean)
- is_active (boolean)

**OTP Table:**
- user (foreign key)
- otp_code (6 digits)
- created_at (timestamp)
- expires_at (5 minutes from creation)
# user_auth

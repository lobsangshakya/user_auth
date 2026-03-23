# Bugfix Requirements Document

## Introduction

The Django project has several interconnected issues preventing it from running cleanly: conflicting migration state, incorrect SMTP/SSL email configuration, a signup flow that crashes the server on email failure, misconfigured templates settings, a fragile two-write user creation pattern, broken URL routing that causes a 404 at the root path, URLs with trailing slashes instead of clean paths, and an unused `base.html` removal request that is actually blocked because all templates extend it. Together these prevent `python manage.py runserver` from working correctly and break the signup-OTP-verification flow.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN migrations are applied THEN the system fails due to conflicting or missing migration files, preventing table creation for `auth_user` and related Django tables.

1.2 WHEN the server starts with a stale `db.sqlite3` THEN the system references an inconsistent database state that does not match the current migration history.

1.3 WHEN a user submits the signup form THEN the system crashes or raises an `SMTPException` because `EMAIL_SSL_KEYFILE` and `EMAIL_SSL_CERTFILE` are set to invalid values alongside `EMAIL_USE_TLS=True` on port 587.

1.4 WHEN `send_mail` raises an exception during signup THEN the system returns a 500 error instead of continuing, because the call is not wrapped in a try/except block.

1.5 WHEN Django renders templates THEN the system cannot locate them because `TEMPLATES[0]['DIRS']` is set to `[]` inside the `TEMPLATES` list definition and then overridden via a separate `TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']` line later in the file, which is fragile and order-dependent.

1.6 WHEN a new user signs up THEN the system creates the user with `is_active=True` by default via `create_user()` and then sets `user.is_active = False` and calls `user.save()` as a second database write, leaving the user transiently active between the two writes.

1.7 WHEN a browser visits `http://127.0.0.1:8000/` THEN the system returns a 404 because `config/urls.py` delegates to `include('minimal.urls')` and `minimal/urls.py` only defines `path('signup/', ...)`, so the root path `""` has no matching route.

1.8 WHEN a browser visits any app URL THEN the system requires trailing slashes (e.g. `/signup/`, `/login/`, `/dashboard/`) because all paths in `minimal/urls.py` are defined with trailing slashes, producing 404s for clean URLs without slashes.

1.9 WHEN `base.html` is evaluated for removal THEN the system cannot remove it because all four templates (`signup.html`, `login.html`, `verify.html`, `dashboard.html`) extend `base.html` via `{% extends "base.html" %}`.

### Expected Behavior (Correct)

2.1 WHEN migrations are run on a clean state THEN the system SHALL create all required tables including `auth_user`, `minimal_otp`, sessions, and all other Django built-in tables without errors.

2.2 WHEN the database is reset THEN the system SHALL allow `makemigrations` and `migrate` to complete successfully from a clean `db.sqlite3`.

2.3 WHEN a user submits the signup form THEN the system SHALL connect to Gmail SMTP on port 587 using `EMAIL_USE_TLS=True` only, with no `EMAIL_SSL_KEYFILE` or `EMAIL_SSL_CERTFILE` settings present.

2.4 WHEN `send_mail` raises any exception during signup THEN the system SHALL catch the error, print a debug log, and continue to redirect the user to the verification page without a 500 crash.

2.5 WHEN Django starts THEN the system SHALL locate templates correctly because `TEMPLATES[0]['DIRS']` SHALL be set to `[BASE_DIR / 'templates']` inline inside the `TEMPLATES` list definition, not via a separate post-definition assignment.

2.6 WHEN a new user is created during signup THEN the system SHALL pass `is_active=False` directly to `create_user()` so the user is created inactive in a single atomic database write.

2.7 WHEN a browser visits `http://127.0.0.1:8000/` THEN the system SHALL directly render the signup page without a redirect, by mapping the root path `""` directly to the signup view in `config/urls.py` (not via `include`).

2.8 WHEN a browser visits any app URL THEN the system SHALL serve clean URLs without trailing slashes: `/signup`, `/login`, `/verify/<int:user_id>`, `/dashboard`, `/logout`, by removing trailing slashes from all path definitions in `minimal/urls.py`.

2.9 WHEN `base.html` removal is requested THEN the system SHALL retain `base.html` because it is actively used as the base template extended by all four page templates.

### Unchanged Behavior (Regression Prevention)

3.1 WHEN a user submits a valid OTP THEN the system SHALL CONTINUE TO activate the account, delete the OTP record, and redirect to the login page.

3.2 WHEN a user submits an invalid OTP THEN the system SHALL CONTINUE TO display an error message and re-render the verify page.

3.3 WHEN a registered email is used to sign up again THEN the system SHALL CONTINUE TO show an "already registered" error and re-render the signup page.

3.4 WHEN a verified user logs in with correct credentials THEN the system SHALL CONTINUE TO authenticate and redirect to the dashboard.

3.5 WHEN an unverified or inactive user attempts to log in THEN the system SHALL CONTINUE TO reject the login with an appropriate error message.

3.6 WHEN a logged-in user visits the logout URL THEN the system SHALL CONTINUE TO end the session and redirect to the login page.

3.7 WHEN the admin URL is accessed THEN the system SHALL CONTINUE TO serve the Django admin interface.

3.8 WHEN any page template is rendered THEN the system SHALL CONTINUE TO extend `base.html` for shared layout, styles, and message display.

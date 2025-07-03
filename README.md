1. Introduction
The AI Communication Assistant is a web-based application that facilitates user authentication, data management, and communication features. It integrates email-based OTP verification, password reset mechanisms, and automated data processing from a text file.

2. Project Structure
The project follows a modular structure with the following key components:

models.py - Defines the User model.
routes.py - Manages user authentication, dashboard, and admin functionalities.
utils.py - Implements email notifications, OTP verification, text file parsing, and database updates.
run.py - The main entry point for the application, which starts the web server and monitors file updates.
3. Models (models.py)
User Model
The User class represents the user entity. It extends UserMixin from Flask-Login for session handling.

Attributes:
id (str) - Unique identifier for the user.
username (str) - User’s email address (validated during sign-up).
password (str) - Hashed password for authentication.
user_type (str) - Defines the role (admin, user, maintenance).
4. Routes (routes.py)
Authentication Routes
Login (/login) - Validates user credentials and starts a session.
Signup (/signup) - Registers a new user with OTP verification.
Logout (/logout) - Ends the session.
Password Management
Forgot Password (/forgot-password) - Sends a password reset email with a time-sensitive token.
Reset Password (/reset-password/<token>) - Allows users to reset their password using the token.
User Dashboard
Dashboard (/dashboard) - Displays processed data from the database.
Machines Data (/machines_data) - Returns machine-related data in JSON format.
Admin Panel
Admin Dashboard (/admin-panel) - Restricted to admin users, providing an interface for managing system data.
5. Utility Functions (utils.py)
Email Handling
send_reset_email(email, reset_url) - Sends password reset links via Mailjet API.
send_otp(email, otp) - Sends a one-time password for email verification.
Data Processing
parse_text_file(file_path) - Reads and structures data from a text file.
update_database(file_path) - Updates the database with parsed data.
File Monitoring
monitor_file(file_path) - Uses Watchdog to detect changes in a data file and update the database accordingly.
6. Application Execution (run.py)
Starts the Flask server (app.run(debug=True)).
Runs monitor_file(file_path) in a separate thread to track data file updates.
7. Dependencies
Backend: Flask, Flask-Login, MongoDB (via pymongo), Werkzeug for password hashing.
Email & Security: Mailjet API, itsdangerous for token management.
File Handling: Watchdog for real-time file monitoring.

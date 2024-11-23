Overview
This project is a file management system built with Flask, a Python web framework. It allows users to upload, download, and manage files. Administrators can grant or revoke access to files for specific users and view logs of file downloads.

Features
- User Authentication: Users can register and log in to the system.
- File Upload: Authenticated users can upload files.
- File Download: Authenticated users can download files they have access to.
- Access Management: Administrators can grant or revoke access to files for specific users.
- Logging: The system logs file uploads and downloads.
- Admin Dashboard: Administrators can view logs and download statistics.

Prerequisites
- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Werkzeug

Usage

User
1. Register/Login: Users need to register or log in to access the system.
2. Upload Files: After logging in, users can upload files.
3. Download Files: Users can download files they have access to.

Admin
1. Access Management: Administrators can grant or revoke access to files for specific users.
2. View Logs: Administrators can view logs of file uploads and downloads.
3. View Statistics: Administrators can view download statistics for each user.

File Structure

file-management-system/
├── database/
│   ├── site.db             # SQLite database file
├── static/
│   ├── style.css           # CSS file for styling
├── templates/
│   ├── index.html          # Home page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── logs.html           # Logs of file downloads
│   ├── edit.html           # Edit file access permissions
│   ├── upload.html         # Upload file
├── venv/                   # Virtual environment directory
│   ├── Scripts/
│   ├── Lib/
│   ├── ...
├── config.py               # Configuration settings
├── dbmodels.py             # Database models
├── forms.py                # Forms for user input
├── main.py                 # Main application file
├── routes.py               # Routes and views
├── auth.py                 # User authentication
├── README.md               # Project documentation
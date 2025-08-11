ADK EduHub
Project Overview

ADK EduHub is a role-based educational platform designed to facilitate online learning and campus communication. It provides distinct dashboards and functionalities for admins, teachers, and students, including course management, announcements, schedules, messaging, and profile settings. The platform aims to enhance collaboration and transparency within educational institutions.
Features

    Role-based dashboards for Admin, Teacher, and Student

    CRUD operations for Courses, Students, Teachers, Schedules, and Messages

    Announcement system with role-specific visibility and admin announcements

    User profile management and customizable settings

    Real-time notifications for students on announcements

    Secure authentication and role-based permissions

    Responsive and user-friendly interface using Bootstrap

Tech Stack

    Backend: Django 4.x, Python 3.12

    Frontend: HTML5, CSS3, Bootstrap 5

    Database: SQLite (default, can be changed)

    Authentication: Django’s built-in user model extended with custom roles

    Version Control: Git, GitHub

Installation Instructions

    Clone the repository:

git clone https://github.com/asubash017/Adk_EduHub.git
cd Adk_EduHub

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate    # Linux/macOS
# venv\Scripts\activate     # Windows

Install dependencies:

pip install -r requirements.txt

Apply database migrations:

python manage.py migrate

Create a superuser (admin):

python manage.py createsuperuser

Run the development server:

    python manage.py runserver

    Access the app:

    Open your browser and navigate to http://127.0.0.1:8000/

Usage

    Login: Use your created superuser or user credentials to login.

    Dashboard: Access role-based dashboards tailored for Admin, Teacher, or Student.

    Manage Content: Create, update, or delete courses, announcements, schedules, etc.

    Notifications: Students receive announcements relevant to their role directly on their dashboard.

    Settings: Update your profile and preferences.

Screenshots can be added here for clarity.
Contributing

Contributions are welcome! To contribute:

    Fork the repository.

    Create a new branch: git checkout -b feature/your-feature-name

    Make your changes and commit: git commit -m "Add your message"

    Push to your branch: git push origin feature/your-feature-name

    Open a pull request describing your changes.

Please ensure your code follows the project's coding conventions and includes relevant tests.
License

This project is licensed under the MIT License. See the LICENSE file for details.
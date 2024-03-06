# Task Manager Application

## Overview

This Task Manager application is a Flask-based web app designed to help users manage their daily tasks efficiently. With features like user authentication, task addition, and deletion, it offers a comprehensive platform for personal or team task management. The application emphasizes simplicity, usability, and effectiveness in task organization.

## Features

- **User Authentication**: Secure signup, login, and logout functionalities.
- **Task Management**: Users can add, view, update, and delete tasks.
- **User-Specific Tasks**: Tasks are user-specific, ensuring that users can only see and manage their tasks.
- **Change Password**: Users can change their password through a simple process.
- **Delete Account**: Users have the option to delete their account, which also removes all associated tasks.
- **Responsive Design**: The application is built with a mobile-first approach, ensuring usability across devices.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework.
- **Flask-Login**: For handling user authentication sessions.
- **Flask-SQLAlchemy**: For ORM and database operations.
- **SQLite**: A lightweight disk-based database to store user and task data.
- **Werkzeug**: For password hashing and security.
- **HTML & CSS**: For structuring and styling the web interface.

## Setup and Installation

1. **Clone the Repository**
    ```sh
    git clone ...
    ```
2. **Create a Virtual Environment**
   - For Windows:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
    - For macOS and Linux:
      ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the Application**
   ```sh
    python app.py
    ```
Visit `http://127.0.0.1:5000/` in your browser to access the application.

## Usage
- *Register a New User*: Navigate to the registration page from the homepage and fill in your username and password.
- *Log In*: Use your credentials to log in and start managing your tasks.
- *Add a Task*: Enter a task description in the provided field and submit.
- *Edit/Delete Tasks*: Each task has an option to edit or delete, allowing for easy task management.
- *Change Password/Delete Account*: Access these options through links in the navigation bar.

## Contributing

Want to contribute? Great! To fix a bug or enhance the application, follow these steps:

- Fork the repo
- Create a new branch (`git checkout -b improve-feature`)
- Make the appropriate changes in the files
- Add changes to reflect the changes made
- Commit your changes (`git commit -am 'Improve feature'`)
- Push to the branch (`git push origin improve-feature`)
- Create a Pull Request
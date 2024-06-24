# Marist Task Management System

## Overview

The Marist Task Management System is a robust task management application designed to enhance productivity and organization. It features multi-level user authentication, a dynamic calendar display, personalized task management, advanced search functionality, and more. This README provides an overview of the project, instructions for setting up the application, and details on how to use it.

## Features

1. **Multi-Level User Authentication**: Supports both admin and standard user roles with unique permissions for each.
2. **Dynamic Calendar Display**: Offers daily, weekly, monthly, and yearly views for tasks.
3. **Personalized Task Management**: Users can add, edit, and remove tasks with detailed information.
4. **Advanced Search Functionality**: Users can search for tasks using various parameters like duration, title, and time.
5. **User-Friendly Interface**: Intuitive and easy-to-use interface with clear navigation.
6. **Data Reporting**: Generates tabular reports and well-organized calendars.
7. **Alerts and Warnings**: Notifies users of overlapping tasks or duplicate entries.
8. **Graceful Exit**: Provides a thank you message upon exit and records logout time.

## Project Structure

The project consists of several components, each responsible for different aspects of the task management system:

- **User Authentication**: Separate login systems for users and admins with session tracking.
- **Task Management**: Users can add, edit, and delete tasks, and view tasks in various calendar formats.
- **User Settings**: Users can customize their notification settings and other preferences.
- **Admin Settings**: Admins have additional privileges to manage user information and system settings.
- **Database**: MySQL database to store user data, tasks, alerts, and settings.

## Setup Instructions

### Prerequisites

- Python 3.x
- MySQL Server
- Required Python libraries (listed in `requirements.txt`)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/YourUsername/MaristTaskManager.git
   cd MaristTaskManager
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Set Up the Database

Start MySQL Server.
Create a database named MaristTask.
Execute the SQL scripts provided in Phase5.1(DataInsert).sql and Phase5.2 Tables(Normalized).sql to create and populate the necessary tables.
Configure Database Connection

Update the database connection settings in the config.py file:

python
Copy code
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'your_password'
DB_NAME = 'MaristTask'
Running the Application
Start the Application

bash
Copy code
python main.py
Access the Application

Open your web browser and navigate to http://localhost:5000.

Usage Instructions
Admin Access
Username: admin_user
Password: admin_pass
Normal User Access
Username: normal_user
Password: normal_pass
Logging In
Open the login page.
Enter the provided username and password.
Click the "Login" button.
Main Menu
After logging in, you will be presented with the main menu. The options available will depend on your role (admin or normal user).

Admin Functions
Admins have additional functionalities such as managing users, viewing login records, and adjusting system settings.

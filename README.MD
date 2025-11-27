CPS510 – Online Movie Store

This project is a Python-based Online Movie Store application that supports multiple user roles, including Customer, Customer Service, Content Manager, and Developer. The application uses an Oracle database and runs locally through the terminal.

Repository link:
https://github.com/ayeshaq27/cps510-online-movie-store.git

⚠️ Note: This application must be downloaded and run locally. It cannot be run directly from GitHub.

Prerequisites

Before running the application, ensure you have:

Python 3.8 or later

pip installed

Access to an Oracle database

Your Oracle username and password

Installation Instructions
macOS (MacBook)

Go to the GitHub repository:
https://github.com/ayeshaq27/cps510-online-movie-store

Click Code → Download ZIP.

Double-click the downloaded ZIP file to extract it.

Open Visual Studio Code and select File → Open Folder, then open the extracted project folder.

Open the terminal (VS Code: View → Terminal or macOS Terminal).

Install the required dependency:

pip3 install oracledb


Navigate to the project directory if needed:

cd path/to/extracted/folder


Run the application:

python3 landing_page.py


You will be redirected to the login screen.

Linux (Ubuntu / Debian / similar)

Download the ZIP file from the GitHub repository.

Extract the files:

unzip cps510-online-movie-store.zip


Open the extracted folder in Visual Studio Code or your preferred editor.

Install the required package:

pip3 install oracledb


Navigate to the project folder:

cd cps510-online-movie-store


Run the application:

python3 landing_page.py


The login screen will appear.

Windows

Go to the GitHub repository and click Code → Download ZIP.

Right-click the ZIP file and select Extract All.

Open the extracted folder in Visual Studio Code.

Open the terminal (Ctrl + ) or use Command Prompt.

Install the dependency:

pip install oracledb


Ensure you are in the correct directory and run:

python landing_page.py


You will be taken to the login screen.

User Guide – Login Instructions

After running landing_page.py, choose the appropriate login option from the GUI.

Customer Service Login

Click the “Customer Service Login” button.

Enter the following credentials:

Employee ID: 60001

Password: Josh123

Content Manager Login

Click the “Content Manager Login” button.

Enter the following credentials:

Employee ID: 51090

Password: charlie123

Developer Login

Click the “Developer Login” button.

Enter the following credentials:

Employee ID: 70001

Password: Python123

Customer Login

Existing customer:

Username: Alice

Password: passAlice

New customer:

You may register your own account using the Register option on the login screen.

Oracle Database Credentials

✅ Important:
When logging in or registering (for any role), you will be prompted in the terminal to enter your Oracle database username and password.

These credentials are required for the application to connect to the database successfully.

Notes

The application must be run locally.

Ensure all Oracle credentials are entered correctly.

If connection issues occur, verify Oracle client setup and network access.

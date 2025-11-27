# CPS510 – Online Movie Store

This project is a Python-based Online Movie Store application that supports multiple user roles, including **Customer**, **Customer Service**, **Content Manager**, and **Developer**. The application connects to an **Oracle database** and runs locally via the terminal.

GitHub Repository:  
https://github.com/ayeshaq27/cps510-online-movie-store.git

> ⚠️ **Important:** This project must be downloaded and run locally. It cannot be run directly from GitHub.

---

## Prerequisites

Make sure you have the following installed:
- Python **3.8 or later**
- `pip`
- An Oracle Database account
- Oracle username and password

---

## Installation & Setup

### macOS (MacBook)

1. Go to the GitHub repository.
2. Click **Code → Download ZIP**.
3. Double-click the ZIP file to extract it.
4. Open **Visual Studio Code** and open the extracted folder.
5. Open the terminal (`View → Terminal`).
6. Install the required dependency:
   ```bash
   pip3 install oracledb
7. Navigate to the project directory if needed:
    cd path/to/extracted/folder
8. Run the application:
    python3 landing_page.py

Linux (Ubuntu / Debian)

Download the ZIP from GitHub.

Extract the files:

unzip cps510-online-movie-store.zip


Open the project folder in VS Code or another editor.

Install the dependency:

pip3 install oracledb


Navigate to the folder:

cd cps510-online-movie-store


Run the application:

python3 landing_page.py

Windows

Download the ZIP from GitHub and extract it.

Open the folder in Visual Studio Code.

Open the terminal (Ctrl + ).

Install the dependency:

pip install oracledb


Run the application:

python landing_page.py

User Guide – Login Instructions

Select the appropriate login option from the application’s login screen.

Customer Service Login

Click Customer Service Login

Enter:

Employee ID: 60001

Password: Josh123

Content Manager Login

Click Content Manager Login

Enter:

Employee ID: 51090

Password: charlie123

Developer Login

Click Developer Login

Enter:

Employee ID: 70001

Password: Python123

Customer Login

Existing Customer

Username: Alice

Password: passAlice

New Customer

You may create your own account using the Register option.

Oracle Database Credentials

When logging in or registering, you will be prompted in the terminal to enter your Oracle username and password.

✅ These credentials are required for the application to function properly.

Notes

This application must be run locally.

Ensure Oracle credentials are entered correctly.

If database connection issues occur, verify Oracle client setup and access permissions.

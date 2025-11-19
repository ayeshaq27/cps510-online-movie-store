# login_gui.py
import tkinter as tk
from tkinter import messagebox
from connect import get_connection
import oracledb

_result = {"code": None, "username": None}


def on_login(root, entry_username, entry_password):
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not (username and password):
        messagebox.showerror("Error", "All fields are required.")
        return

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT PASSWORD FROM CUSTOMER WHERE USERNAME = :u", {"u": username})
        row = cur.fetchone()

        if row is None:
            messagebox.showwarning("User does not exist", f"Username '{username}' does not exist.")
            _result["code"] = 0
            _result["username"] = None
            root.destroy()
            return

        stored_password = row[0]

        if stored_password != password:
            messagebox.showwarning("Incorrect Password", "The password you entered is incorrect.")
            return  # Keep window open to re-try

        messagebox.showinfo("Success", f"User '{username}' logged in successfully!")

        # Basic role distinction: numeric usernames -> employee, else customer
        if username.isdigit():
            _result["code"] = 2  # employee
        else:
            _result["code"] = 1  # customer

        _result["username"] = username
        root.destroy()

    except oracledb.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if cur is not None:
            try:
                cur.close()
            except:
                pass
        if conn is not None:
            try:
                conn.close()
            except:
                pass


def login_user():
    """
    Open the Login GUI and return dict:
      {
        "code": 0/1/2/None,
        "username": "alice" or None
      }
    """
    _result["code"] = None
    _result["username"] = None

    root = tk.Tk()
    root.title("Movie123 - Login")
    root.geometry("300x200")

    tk.Label(root, text="Welcome back to Movie123!", font=("Arial", 12)).pack(pady=10)

    tk.Label(root, text="Username").pack()
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)

    tk.Label(root, text="Password").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)

    tk.Button(root, text="Login",
              command=lambda: on_login(root, entry_username, entry_password)).pack(pady=15)

    root.mainloop()
    return _result


if __name__ == "__main__":
    print("Login result:", login_user())

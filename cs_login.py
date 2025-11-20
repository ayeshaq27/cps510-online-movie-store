#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
from connect import get_connection
import oracledb

_result = {"code": None, "employee_id": None}


def on_login(root, entry_empid, entry_password):
    empid = entry_empid.get().strip()
    password = entry_password.get().strip()

    if not (empid and password):
        messagebox.showerror("Error", "All fields are required.")
        return

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()


        cur.execute("SELECT PASSWORD FROM CUSTOMER_SERVICE WHERE EMPLOYEE_ID = :e", {"e": empid})
        row = cur.fetchone()

        if row is None:
            messagebox.showwarning("User does not exist", f"Employee ID '{empid}' does not exist.")
            _result["code"] = 0
            _result["employee_id"] = None
            root.destroy()
            return

        stored_password = row[0]

        if stored_password != password:
            messagebox.showwarning("Incorrect Password", "The password you entered is incorrect.")
            return  # keep window open to retry

        messagebox.showinfo("Success", f"Employee '{empid}' logged in successfully!")
        _result["code"] = 2
        _result["employee_id"] = empid
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


def cs_login_user():
    """Open a simple CM login GUI and return dict:

      {"code": 2/0/None, "employee_id": "51090"|None}
    """
    _result["code"] = None
    _result["employee_id"] = None

    root = tk.Tk()
    root.title("Customer Service Login")
    root.geometry("320x200")

    tk.Label(root, text="Customer Service Login", font=("Arial", 12)).pack(pady=10)

    tk.Label(root, text="Employee ID").pack()
    entry_empid = tk.Entry(root)
    entry_empid.pack(pady=5)

    tk.Label(root, text="Password").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)

    tk.Button(root, text="Login", command=lambda: on_login(root, entry_empid, entry_password)).pack(pady=15)

    root.mainloop()
    return _result


if __name__ == "__main__":
    print("CS login result:", cs_login_user())

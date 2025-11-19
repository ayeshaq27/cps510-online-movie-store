# register_gui.py
import tkinter as tk
from tkinter import messagebox
from connect import get_connection 
import oracledb

# We use a small dict so nested functions can modify it
_result = {"code": 0}


def on_register(root, entries):
    username = entries["username"].get().strip()
    password = entries["password"].get().strip()
    first_name = entries["first_name"].get().strip()
    last_name = entries["last_name"].get().strip()
    age_text = entries["age"].get().strip()
    email = entries["email"].get().strip()
    phone = entries["phone"].get().strip()

    if not (username and password and first_name and last_name and age_text and email and phone):
        messagebox.showerror("Error", "All fields are required.")
        return

    try:
        age = int(age_text)
        if age <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Age must be a positive integer.")
        return

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Check if username exists
        cur.execute("SELECT COUNT(*) FROM CUSTOMER WHERE USERNAME = :u", {"u": username})
        count = cur.fetchone()[0]

        if count > 0:
            messagebox.showwarning("User Exists", f"Username '{username}' already exists.")
            _result["code"] = 2
            root.destroy()
            return

        # Insert new user
        cur.execute("""
            INSERT INTO CUSTOMER (
                USERNAME, BALANCE, PASSWORD, FIRST_NAME, LAST_NAME, AGE, EMAIL, PHONE
            ) VALUES (
                :username, :balance, :password, :first_name, :last_name, :age, :email, :phone
            )
        """, {
            "username": username,
            "balance": 0.0,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "email": email,
            "phone": phone,
        })

        conn.commit()
        messagebox.showinfo("Success", f"User '{username}' registered successfully!")
        _result["code"] = 1
        root.destroy()

    except oracledb.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        try:
            conn.close()
        except:
            pass


def on_go_to_login(root):
    _result["code"] = 3
    root.destroy()


def register_user():
    """
    Open the Register GUI and return:
      0 = closed / cancelled
      1 = registered successfully
      2 = username already exists
      3 = user clicked 'Login' button
    """
    _result["code"] = 0

    root = tk.Tk()
    root.title("Movie123 - Register")
    root.geometry("350x420")

    tk.Label(root, text="Register New Customer", font=("Arial", 16)).pack(pady=10)

    entries = {}

    def make_field(label_text, is_password=False):
        tk.Label(root, text=label_text).pack()
        e = tk.Entry(root, show="*" if is_password else "")
        e.pack()
        return e

    entries["username"] = make_field("Username")
    entries["password"] = make_field("Password", is_password=True)
    entries["first_name"] = make_field("First Name")
    entries["last_name"] = make_field("Last Name")
    entries["age"] = make_field("Age")
    entries["email"] = make_field("Email")
    entries["phone"] = make_field("Phone")

    tk.Button(root, text="Register",
              command=lambda: on_register(root, entries)).pack(pady=10)

    tk.Button(root, text="Already have an account? Login",
              command=lambda: on_go_to_login(root)).pack()

    root.mainloop()
    return _result["code"]


if __name__ == "__main__":
    print("Result code:", register_user())

#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import oracledb
from connect import get_connection


def fetch_customer(username: str):
    """
    Fetch a single customer row by username.
    Returns a dict or None if not found.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT USERNAME, BALANCE, PASSWORD, FIRST_NAME, LAST_NAME,
                   AGE, EMAIL, PHONE
            FROM CUSTOMER
            WHERE USERNAME = :u
        """, {"u": username})
        row = cur.fetchone()
        if not row:
            return None
        cols = [d[0] for d in cur.description]
        return dict(zip(cols, row))
    except oracledb.Error as e:
        messagebox.showerror("Database Error", str(e))
        return None
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass


def show_edit_customer_gui(username: str):
    """
    Show an edit form for the given username.

    Returns:
        {"code": 1}  -> successfully updated
        {"code": 0}  -> cancelled/closed or failed
    """
    result = {"code": 0}

    customer = fetch_customer(username)
    if customer is None:
        messagebox.showerror("Error", f"Customer '{username}' not found.")
        return result

    root = tk.Tk()
    root.title(f"Edit Customer - {username}")
    root.geometry("400x420")

    tk.Label(root, text=f"Edit Customer: {username}", font=("Arial", 16)).pack(pady=10)

    form = tk.Frame(root)
    form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Helper to create label + entry
    def make_field(row, label_text, initial_value="", is_readonly=False):
        tk.Label(form, text=label_text).grid(row=row, column=0, sticky="w", pady=4)
        e = tk.Entry(form)
        e.grid(row=row, column=1, sticky="ew", pady=4)
        e.insert(0, "" if initial_value is None else str(initial_value))
        if is_readonly:
            e.config(state="readonly")
        return e

    form.columnconfigure(1, weight=1)

    # USERNAME read-only
    entry_username = make_field(0, "Username", customer["USERNAME"], is_readonly=True)
    entry_balance = make_field(1, "Balance", customer["BALANCE"])
    entry_password = make_field(2, "Password", customer["PASSWORD"])
    entry_first = make_field(3, "First Name", customer["FIRST_NAME"])
    entry_last = make_field(4, "Last Name", customer["LAST_NAME"])
    entry_age = make_field(5, "Age", customer["AGE"])
    entry_email = make_field(6, "Email", customer["EMAIL"])
    entry_phone = make_field(7, "Phone", customer["PHONE"])

    def on_save():
        # Read values
        balance_text = entry_balance.get().strip()
        password = entry_password.get().strip()
        first_name = entry_first.get().strip()
        last_name = entry_last.get().strip()
        age_text = entry_age.get().strip()
        email = entry_email.get().strip()
        phone = entry_phone.get().strip()

        # Basic validation
        if not (balance_text and password and first_name and last_name and age_text and email and phone):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            balance = float(balance_text)
        except ValueError:
            messagebox.showerror("Error", "Balance must be a number.")
            return

        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Age must be a positive integer.")
            return

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE CUSTOMER
                SET BALANCE = :bal,
                    PASSWORD = :pwd,
                    FIRST_NAME = :fn,
                    LAST_NAME = :ln,
                    AGE = :age,
                    EMAIL = :em,
                    PHONE = :ph
                WHERE USERNAME = :u
            """, {
                "bal": balance,
                "pwd": password,
                "fn": first_name,
                "ln": last_name,
                "age": age,
                "em": email,
                "ph": phone,
                "u": username,
            })
            conn.commit()
            messagebox.showinfo("Success", f"Customer '{username}' updated successfully.")
            result["code"] = 1
            root.destroy()
        except oracledb.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def on_cancel():
        result["code"] = 0
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Save", width=10, command=on_save).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)

    root.protocol("WM_DELETE_WINDOW", on_cancel)
    root.mainloop()
    return result


if __name__ == "__main__":
    # quick manual test
    u = input("Username to edit: ").strip()
    if u:
        print(show_edit_customer_gui(u))

# customer_list.py
#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import oracledb
from connect import get_connection


def fetch_customers():
    """Fetch all customers from the CUSTOMER table."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT USERNAME, FIRST_NAME, LAST_NAME, EMAIL, PHONE, BALANCE FROM CUSTOMER ORDER BY USERNAME")
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        return cols, rows
    except oracledb.Error as e:
        messagebox.showerror("Database Error", str(e))
        return [], []
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass


def show_customer_list_gui():
    """
    Display a window listing all customers.
    
    Returns:
        {"code": 1, "username": "alice"}  → selected a customer
        {"code": 0, "username": None}    → closed window / no selection
    """
    result = {"code": 0, "username": None}

    root = tk.Tk()
    root.title("Movie123 - Customer List")
    root.geometry("900x450")

    tk.Label(root, text="Registered Customers", font=("Arial", 18)).pack(pady=10)

    # === Table Frame ===
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    cols, rows = fetch_customers()
    if not cols:
        cols = ["USERNAME", "FIRST_NAME", "LAST_NAME", "EMAIL", "PHONE", "BALANCE"]

    tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")

    # Scrollbars
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    # Column configuration
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor="center")

    # Insert rows
    for row in rows:
        clean_row = ["" if v is None else str(v) for v in row]
        tree.insert("", tk.END, values=clean_row)

    # === Buttons ===
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    def on_select():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a customer.")
            return

        values = tree.item(sel[0], "values")
        username = values[0]  # USERNAME is column 0

        result["code"] = 1
        result["username"] = username
        root.destroy()

    def on_close():
        result["code"] = 0
        result["username"] = None
        root.destroy()

    select_btn = tk.Button(btn_frame, text="Select Customer", width=18, command=on_select)
    close_btn = tk.Button(btn_frame, text="Close", width=12, command=on_close)
    select_btn.pack(side=tk.LEFT, padx=6)
    close_btn.pack(side=tk.LEFT, padx=6)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

    return result


if __name__ == "__main__":
    print("Result:", show_customer_list_gui())

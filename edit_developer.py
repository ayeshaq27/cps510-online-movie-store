# edit_developer.py
#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import oracledb
from connect import get_connection


def fetch_developers():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT EMPLOYEE_ID, EMAIL, PASSWORD, SPECIALTY, GITHUB
            FROM DEVELOPER
            ORDER BY EMPLOYEE_ID
        """)
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


def _open_dev_form(parent, title, initial=None):
    win = tk.Toplevel(parent)
    win.title(title)
    win.geometry("420x280")
    win.grab_set()

    form = tk.Frame(win)
    form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def field(row, label):
        tk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=4)
        e = tk.Entry(form)
        e.grid(row=row, column=1, sticky="ew", pady=4)
        return e

    form.columnconfigure(1, weight=1)

    e_id = field(0, "Employee ID")
    e_email = field(1, "Email")
    e_pass = field(2, "Password")
    e_spec = field(3, "Specialty")
    e_git = field(4, "GitHub URL")

    if initial:
        e_id.insert(0, str(initial["EMPLOYEE_ID"]))
        e_email.insert(0, initial["EMAIL"])
        e_pass.insert(0, initial["PASSWORD"])
        e_spec.insert(0, initial["SPECIALTY"])
        e_git.insert(0, initial["GITHUB"])
        e_id.config(state="readonly")

    result = {"data": None}

    def on_save():
        emp_id_text = e_id.get().strip()
        email = e_email.get().strip()
        pwd = e_pass.get().strip()
        spec = e_spec.get().strip()
        git = e_git.get().strip()

        if not (emp_id_text and email and pwd and spec and git):
            messagebox.showerror("Error", "All fields are required.", parent=win)
            return
        try:
            emp_id = int(emp_id_text)
        except ValueError:
            messagebox.showerror("Error", "Employee ID must be an integer.", parent=win)
            return

        result["data"] = {
            "EMPLOYEE_ID": emp_id,
            "EMAIL": email,
            "PASSWORD": pwd,
            "SPECIALTY": spec,
            "GITHUB": git,
        }
        win.destroy()

    def on_cancel():
        result["data"] = None
        win.destroy()

    btn_f = tk.Frame(win)
    btn_f.pack(pady=10)
    tk.Button(btn_f, text="Save", width=10, command=on_save).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_f, text="Cancel", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)

    win.protocol("WM_DELETE_WINDOW", on_cancel)
    win.wait_window()
    return result["data"]


def manage_developer_gui():
    root = tk.Tk()
    root.title("Manage Developers")
    root.geometry("800x350")

    tk.Label(root, text="Developers", font=("Arial", 16)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    cols, rows = fetch_developers()
    if not cols:
        cols = ["EMPLOYEE_ID", "EMAIL", "PASSWORD", "SPECIALTY", "GITHUB"]

    tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=150, anchor="center")

    for r in rows:
        tree.insert("", tk.END, values=[str(x) if x is not None else "" for x in r])

    def refresh():
        for item in tree.get_children():
            tree.delete(item)
        c2, r2 = fetch_developers()
        for r in r2:
            tree.insert("", tk.END, values=[str(x) if x is not None else "" for x in r])

    def on_add():
        data = _open_dev_form(root, "Add Developer")
        if not data:
            return
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO DEVELOPER (EMPLOYEE_ID, EMAIL, PASSWORD, SPECIALTY, GITHUB)
                VALUES (:id, :em, :pw, :sp, :gh)
            """, {
                "id": data["EMPLOYEE_ID"],
                "em": data["EMAIL"],
                "pw": data["PASSWORD"],
                "sp": data["SPECIALTY"],
                "gh": data["GITHUB"],
            })
            conn.commit()
            refresh()
        except oracledb.Error as e:
            messagebox.showerror("Database Error", str(e), parent=root)
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def on_edit():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a row to edit.", parent=root)
            return
        vals = tree.item(sel[0], "values")
        initial = {
            "EMPLOYEE_ID": int(vals[0]),
            "EMAIL": vals[1],
            "PASSWORD": vals[2],
            "SPECIALTY": vals[3],
            "GITHUB": vals[4],
        }
        data = _open_dev_form(root, "Edit Developer", initial=initial)
        if not data:
            return
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE DEVELOPER
                SET EMAIL     = :em,
                    PASSWORD  = :pw,
                    SPECIALTY = :sp,
                    GITHUB    = :gh
                WHERE EMPLOYEE_ID = :id
            """, {
                "id": data["EMPLOYEE_ID"],
                "em": data["EMAIL"],
                "pw": data["PASSWORD"],
                "sp": data["SPECIALTY"],
                "gh": data["GITHUB"],
            })
            conn.commit()
            refresh()
        except oracledb.Error as e:
            messagebox.showerror("Database Error", str(e), parent=root)
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def on_delete():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a row to delete.", parent=root)
            return
        vals = tree.item(sel[0], "values")
        emp_id = int(vals[0])
        if not messagebox.askyesno("Confirm", f"Delete developer {emp_id}?", parent=root):
            return
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM DEVELOPER WHERE EMPLOYEE_ID = :id", {"id": emp_id})
            conn.commit()
            refresh()
        except oracledb.Error as e:
            messagebox.showerror("Database Error", str(e), parent=root)
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    btn_f = tk.Frame(root)
    btn_f.pack(pady=10)

    tk.Button(btn_f, text="Add", width=10, command=on_add).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_f, text="Edit", width=10, command=on_edit).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_f, text="Delete", width=10, command=on_delete).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_f, text="Close", width=10, command=root.destroy).pack(side=tk.LEFT, padx=5)

    root.mainloop()


if __name__ == "__main__":
    manage_developer_gui()

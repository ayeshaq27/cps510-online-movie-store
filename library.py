#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import oracledb
from connect import get_connection


def fetch_library_for_user(username: str):
    """
    Fetch all library records for a given username.
    Joins MOVIES to show MOVIE_NAME as well.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                l.USERNAME,
                l.MOVIE_ID,
                m.MOVIE_NAME,
                l.COPY_ID,
                l.START_DATE,
                l.DUE_DATE,
                l.RETURNED_ON
            FROM LIBRARY l
            JOIN MOVIES m ON l.MOVIE_ID = m.ID
            WHERE l.USERNAME = :u
            ORDER BY l.START_DATE DESC
            """,
            {"u": username},
        )

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


def show_library_gui(username: str):
    """
    Open a window showing all library entries for the given username.
    """
    cols, rows = fetch_library_for_user(username)

    root = tk.Tk()
    root.title(f"Movie123 - Library for {username}")
    root.geometry("900x350")

    tk.Label(
        root,
        text=f"Library Records for '{username}'",
        font=("Arial", 16)
    ).pack(pady=10)

    if not rows:
        messagebox.showinfo("No Records", f"No library records found for user '{username}'.")
        if not cols:
            cols = [
                "USERNAME", "MOVIE_ID", "MOVIE_NAME", "COPY_ID",
                "START_DATE", "DUE_DATE", "RETURNED_ON"
            ]

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=cols, show="headings")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    for row in rows:
        display_row = ["" if cell is None else str(cell) for cell in row]
        tree.insert("", tk.END, values=display_row)

    # Button frame: Back (to movies) and Close
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)

    result = {"code": 0}  # 0=closed, 1=done/ok, 2=back to movies

    def on_back():
        result["code"] = 2
        root.destroy()

    def on_close():
        result["code"] = 0
        root.destroy()

    back_btn = tk.Button(btn_frame, text="Back", width=12, command=on_back)
    close_btn = tk.Button(btn_frame, text="Close", width=12, command=on_close)
    back_btn.pack(side=tk.LEFT, padx=6)
    close_btn.pack(side=tk.LEFT, padx=6)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
    return result["code"]


if __name__ == "__main__":
    u = input("Enter username to view library: ").strip()
    if u:
        show_library_gui(u)

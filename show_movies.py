# show_movies.py
#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import oracledb
from connect import get_connection


def fetch_movies(search: str = None):
    """Fetch movies from the MOVIES table.

    If `search` is provided (substring), return movies whose MOVIE_NAME
    contains the search text (case-insensitive).
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        if search and search.strip():
            # Use case-insensitive search on MOVIE_NAME
            q = "SELECT * FROM MOVIES WHERE UPPER(MOVIE_NAME) LIKE :p ORDER BY ID"
            param = {"p": f"%{search.strip().upper()}%"}
            cur.execute(q, param)
        else:
            cur.execute("SELECT * FROM MOVIES ORDER BY ID")

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


def show_movies_gui():
    """
    Show the movies screen and return a dict:
      {
        "code": 0 | 1 | 2,
        "movie_id": "M001" or None
      }

      code:
        0 = closed / no special action
        1 = user clicked 'Library'
        2 = user clicked 'Checkout' with a selected movie
    """
    result = {"code": 0, "movie_id": None}

    root = tk.Tk()
    root.title("Movie123 - Movies")
    root.geometry("1000x400")

    title_label = tk.Label(root, text="Available Movies", font=("Arial", 16))
    title_label.pack(pady=10)

    # Search area
    search_frame = tk.Frame(root)
    search_frame.pack(padx=10, pady=(0, 6), fill=tk.X)

    tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
    entry_search = tk.Entry(search_frame)
    entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 6))
    btn_search = tk.Button(search_frame, text="Find")
    btn_search.pack(side=tk.LEFT)

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    cols, rows = fetch_movies()
    if not cols:
        cols = ["ID", "MOVIE_NAME", "PRICE", "GENRE", "COPIES", "AVG_RATING",
                "RELEASE_DATE", "RUNTIME_MIN", "AGE_RATING", "LANGUAGE_CODE"]

    tree = ttk.Treeview(frame, columns=cols, show="headings")
    tree.config(selectmode="browse")

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
        tree.column(col, width=120, anchor="center")

    for row in rows:
        display_row = ["" if cell is None else str(cell) for cell in row]
        tree.insert("", tk.END, values=display_row)

    def refresh_tree(search_text: str = None):
        for i in tree.get_children():
            tree.delete(i)
        c, r = fetch_movies(search_text)
        for row in r:
            display_row = ["" if cell is None else str(cell) for cell in row]
            tree.insert("", tk.END, values=display_row)

    def do_search(event=None):
        txt = entry_search.get().strip()
        if not txt:
            refresh_tree(None)
        else:
            refresh_tree(txt)

    btn_search.config(command=do_search)
    entry_search.bind("<Return>", do_search)

    # Button frame
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)

    def on_checkout():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a movie first.")
            return
        values = tree.item(sel[0], "values")
        movie_id = values[0]  # assuming first column is ID
        result["code"] = 2
        result["movie_id"] = movie_id
        root.destroy()

    def on_library():
        result["code"] = 1
        root.destroy()

    def on_close():
        # leave code=0, movie_id=None
        root.destroy()

    checkout_btn = tk.Button(btn_frame, text="Checkout", width=12, command=on_checkout)
    library_btn = tk.Button(btn_frame, text="Library", width=12, command=on_library)
    checkout_btn.pack(side=tk.LEFT, padx=6)
    library_btn.pack(side=tk.LEFT, padx=6)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
    return result


if __name__ == "__main__":
    print("Movies result:", show_movies_gui())

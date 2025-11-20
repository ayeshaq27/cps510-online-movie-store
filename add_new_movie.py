# add_new_movie.py
#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import oracledb
from connect import get_connection


def generate_new_copy_ids(conn, movie_id: str, how_many: int):
    """
    Generate new COPY_ID values for INVENTORY for this movie.

    Pattern: MOVIE_ID_C001, MOVIE_ID_C002, ...
    """
    cur = conn.cursor()
    prefix = f"{movie_id}_C"

    cur.execute("""
        SELECT COPY_ID
        FROM INVENTORY
        WHERE MOVIE_ID = :mid AND COPY_ID LIKE :pref || '%'
    """, {"mid": movie_id, "pref": prefix})

    max_num = 0
    for (copy_id,) in cur:
        suffix = copy_id.replace(prefix, "")
        if suffix.isdigit():
            n = int(suffix)
            if n > max_num:
                max_num = n

    new_ids = []
    for i in range(1, how_many + 1):
        num = max_num + i
        new_ids.append(f"{prefix}{num:03d}")
    return new_ids


def show_add_movie_gui():
    """
    Open a window to add a brand new movie.

    Inserts into MOVIES and INVENTORY (for copies).
    AUTO-GENERATES copy IDs.

    Returns:
      {"code": 1, "movie_id": "M007"} -> success
      {"code": 0, "movie_id": None}   -> cancelled/failed
    """
    result = {"code": 0, "movie_id": None}

    root = tk.Tk()
    root.title("Add New Movie")
    root.geometry("400x260")

    tk.Label(root, text="Add New Movie", font=("Arial", 16)).pack(pady=10)

    form = tk.Frame(root)
    form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def make_field(row, label_text):
        tk.Label(form, text=label_text).grid(row=row, column=0, sticky="w", pady=4)
        e = tk.Entry(form)
        e.grid(row=row, column=1, sticky="ew", pady=4)
        return e

    form.columnconfigure(1, weight=1)

    entry_id = make_field(0, "ID (e.g., M007)")
    entry_name = make_field(1, "Name")
    entry_price = make_field(2, "Price")
    entry_genre = make_field(3, "Genre")
    entry_copies = make_field(4, "Copies")

    def on_save():
        movie_id = entry_id.get().strip()
        name = entry_name.get().strip()
        price_text = entry_price.get().strip()
        genre = entry_genre.get().strip()
        copies_text = entry_copies.get().strip()

        if not (movie_id and name and price_text and genre and copies_text):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            price = float(price_text)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
            return

        try:
            copies = int(copies_text)
            if copies <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Copies must be a positive integer.")
            return

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            # Check if ID already exists
            cur.execute("SELECT COUNT(*) FROM MOVIES WHERE ID = :mid", {"mid": movie_id})
            (cnt,) = cur.fetchone()
            if cnt > 0:
                messagebox.showerror("Error", f"Movie ID '{movie_id}' already exists.")
                return

            # Insert into MOVIES (minimal fields)
            cur.execute("""
                INSERT INTO MOVIES (ID, MOVIE_NAME, PRICE, GENRE, COPIES)
                VALUES (:mid, :nm, :pr, :gn, :cp)
            """, {
                "mid": movie_id,
                "nm": name,
                "pr": price,
                "gn": genre,
                "cp": copies,
            })

            # Create INVENTORY rows
            new_ids = generate_new_copy_ids(conn, movie_id, copies)
            for cid in new_ids:
                cur.execute("""
                    INSERT INTO INVENTORY (COPY_ID, MOVIE_ID, QUALITY, STATUS)
                    VALUES (:cid, :mid, '1080P', 'AVAILABLE')
                """, {"cid": cid, "mid": movie_id})

            conn.commit()
            messagebox.showinfo("Success", f"Movie '{movie_id}' added.")
            result["code"] = 1
            result["movie_id"] = movie_id
            root.destroy()

        except oracledb.Error as e:
            messagebox.showerror("Database Error", str(e))
            if conn:
                conn.rollback()
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def on_cancel():
        result["code"] = 0
        result["movie_id"] = None
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Save", width=10, command=on_save).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)

    root.protocol("WM_DELETE_WINDOW", on_cancel)
    root.mainloop()
    return result


if __name__ == "__main__":
    print(show_add_movie_gui())

# update_movie_base.py
#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import oracledb
from connect import get_connection


# ---------- DB HELPERS ----------

def fetch_movie_basic(movie_id: str):
    """
    Fetch minimal movie info for editing.
    Returns dict or None.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, MOVIE_NAME, PRICE, GENRE, COPIES
            FROM MOVIES
            WHERE ID = :mid
        """, {"mid": movie_id})
        row = cur.fetchone()
        if not row:
            return None
        cols = [d[0] for d in cur.description]
        return dict(zip(cols, row))
    except oracledb.Error as e:
        print("DB error in fetch_movie_basic:", e)
        return None
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass


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


def sync_inventory_copies(conn, movie_id: str, old_copies: int, new_copies: int):
    """
    Adjust INVENTORY rows when COPIES changes:
      - If new > old: add AVAILABLE copies with auto-generated COPY_IDs.
      - If new < old: delete AVAILABLE copies first; error if not enough available.
    """
    cur = conn.cursor()

    if new_copies > old_copies:
        delta = new_copies - old_copies
        new_ids = generate_new_copy_ids(conn, movie_id, delta)
        for cid in new_ids:
            cur.execute("""
                INSERT INTO INVENTORY (COPY_ID, MOVIE_ID, QUALITY, STATUS)
                VALUES (:cid, :mid, '1080P', 'AVAILABLE')
            """, {"cid": cid, "mid": movie_id})

    elif new_copies < old_copies:
        delta = old_copies - new_copies

        cur.execute("""
            SELECT COPY_ID
            FROM INVENTORY
            WHERE MOVIE_ID = :mid AND STATUS = 'AVAILABLE'
            ORDER BY COPY_ID
        """, {"mid": movie_id})

        available = [row[0] for row in cur]
        if len(available) < delta:
            raise ValueError(
                f"Cannot reduce copies to {new_copies}: "
                f"only {len(available)} AVAILABLE copies to delete."
            )

        to_delete = available[:delta]
        for cid in to_delete:
            cur.execute("""
                DELETE FROM INVENTORY
                WHERE COPY_ID = :cid AND MOVIE_ID = :mid
            """, {"cid": cid, "mid": movie_id})


# ---------- GUI: EDIT EXISTING MOVIE ----------

def edit_movie_gui(movie_id: str):
    """
    Open a window to update an existing movie's basic fields.
    Also updates INVENTORY if COPIES changes.

    Returns:
      {"code": 1} -> updated successfully
      {"code": 0} -> cancelled/closed or failed
    """
    result = {"code": 0}

    movie = fetch_movie_basic(movie_id)
    if movie is None:
        messagebox.showerror("Error", f"Movie '{movie_id}' not found.")
        return result

    root = tk.Tk()
    root.title(f"Edit Movie - {movie_id}")
    root.geometry("400x260")

    tk.Label(root, text=f"Edit Movie: {movie_id}", font=("Arial", 16)).pack(pady=10)

    form = tk.Frame(root)
    form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def make_field(row, label_text, initial, readonly=False):
        tk.Label(form, text=label_text).grid(row=row, column=0, sticky="w", pady=4)
        e = tk.Entry(form)
        e.grid(row=row, column=1, sticky="ew", pady=4)
        e.insert(0, "" if initial is None else str(initial))
        if readonly:
            e.config(state="readonly")
        return e

    form.columnconfigure(1, weight=1)

    entry_id = make_field(0, "ID", movie["ID"], readonly=True)
    entry_name = make_field(1, "Name", movie["MOVIE_NAME"])
    entry_price = make_field(2, "Price", movie["PRICE"])
    entry_genre = make_field(3, "Genre", movie["GENRE"])
    entry_copies = make_field(4, "Copies", movie["COPIES"])

    old_copies = int(movie["COPIES"])

    def on_save():
        name = entry_name.get().strip()
        price_text = entry_price.get().strip()
        genre = entry_genre.get().strip()
        copies_text = entry_copies.get().strip()

        if not (name and price_text and genre and copies_text):
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

            # Update MOVIES
            cur.execute("""
                UPDATE MOVIES
                SET MOVIE_NAME = :nm,
                    PRICE      = :pr,
                    GENRE      = :gn,
                    COPIES     = :cp
                WHERE ID = :mid
            """, {
                "nm": name,
                "pr": price,
                "gn": genre,
                "cp": copies,
                "mid": movie_id,
            })

            # Sync INVENTORY if copy count changed
            if copies != old_copies:
                sync_inventory_copies(conn, movie_id, old_copies, copies)

            conn.commit()
            messagebox.showinfo("Success", f"Movie '{movie_id}' updated.")
            result["code"] = 1
            root.destroy()

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            if conn:
                conn.rollback()
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
    print(edit_movie_gui("M001"))

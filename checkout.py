#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import oracledb
from connect import get_connection


def get_movie_details(movie_id: str):
    """
    Fetch full movie details from MOVIES table for display.
    Returns dict or None if not found.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, MOVIE_NAME, PRICE, GENRE, COPIES,
                   AVG_RATING, RELEASE_DATE, RUNTIME_MIN,
                   AGE_RATING, LANGUAGE_CODE
            FROM MOVIES
            WHERE ID = :mid
        """, {"mid": movie_id})
        row = cur.fetchone()
        if not row:
            return None
        cols = [d[0] for d in cur.description]
        return dict(zip(cols, row))
    except oracledb.Error:
        return None
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass


def process_checkout(username: str, movie_id: str):
    """
    Perform the actual checkout:
      - Check user + balance
      - Check movie + price
      - Find AVAILABLE copy in INVENTORY
      - Update INVENTORY, CUSTOMER, LIBRARY
    Returns (success: bool, msg: str)
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Lock customer's balance row
        cur.execute(
            "SELECT BALANCE FROM CUSTOMER WHERE USERNAME = :u FOR UPDATE",
            {"u": username},
        )
        row = cur.fetchone()
        if not row:
            return False, f"User '{username}' not found."
        balance = float(row[0])

        # Get movie price and name
        cur.execute(
            "SELECT PRICE, MOVIE_NAME FROM MOVIES WHERE ID = :mid",
            {"mid": movie_id},
        )
        row = cur.fetchone()
        if not row:
            return False, f"Movie '{movie_id}' not found."
        price, movie_name = float(row[0]), row[1]

        # Check balance
        if balance < price:
            return False, (
                f"Insufficient balance.\n"
                f"Current balance: {balance:.2f}, price: {price:.2f}"
            )

        # Find an AVAILABLE copy and lock it
        cur.execute(
            """
            SELECT COPY_ID
            FROM INVENTORY
            WHERE MOVIE_ID = :mid AND STATUS = 'AVAILABLE'
              AND ROWNUM = 1
            FOR UPDATE
            """,
            {"mid": movie_id},
        )
        row = cur.fetchone()
        if not row:
            return False, f"No AVAILABLE copies for movie '{movie_name}' ({movie_id})."
        copy_id = row[0]

        # Update INVENTORY: mark copy as RENTED
        cur.execute(
            "UPDATE INVENTORY SET STATUS = 'RENTED' WHERE COPY_ID = :cid",
            {"cid": copy_id},
        )

        # Update CUSTOMER: subtract price from balance
        cur.execute(
            "UPDATE CUSTOMER SET BALANCE = BALANCE - :p WHERE USERNAME = :u",
            {"p": price, "u": username},
        )

        # Insert into LIBRARY: START_DATE = today, DUE_DATE = +7 days, RETURNED_ON = NULL
        cur.execute(
            """
            INSERT INTO LIBRARY (USERNAME, MOVIE_ID, COPY_ID)
            VALUES (:u, :mid, :cid)
            """,
            {"u": username, "mid": movie_id, "cid": copy_id},
        )

        conn.commit()
        new_balance = balance - price
        msg = (
            f"Checkout successful!\n\n"
            f"Movie: {movie_name} ({movie_id})\n"
            f"Copy: {copy_id}\n"
            f"Charged: {price:.2f}\n"
            f"New balance: {new_balance:.2f}\n"
            f"Due in 7 days."
        )
        return True, msg

    except oracledb.Error as e:
        if conn:
            try:
                conn.rollback()
            except:
                pass
        return False, f"Database error: {e}"
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass


def show_checkout_gui(username: str, movie_id: str):
    """
    Show movie details and a 'Checkout' button for the given user/movie.
    Returns:
      1 = checkout succeeded
      0 = window closed or failed
    """
    movie = get_movie_details(movie_id)
    if movie is None:
        messagebox.showerror("Error", f"Movie '{movie_id}' not found.")
        return 0

    result = {"code": 0}

    root = tk.Tk()
    root.title(f"Checkout - {movie['MOVIE_NAME']}")
    root.geometry("500x400")

    tk.Label(root, text="Movie Checkout", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text=f"User: {username}", font=("Arial", 11)).pack(pady=2)
    tk.Label(root, text=f"Movie ID: {movie['ID']}", font=("Arial", 11)).pack(pady=2)
    tk.Label(root, text=f"Title: {movie['MOVIE_NAME']}", font=("Arial", 11)).pack(pady=2)
    tk.Label(root, text=f"Price: ${movie['PRICE']:.2f}", font=("Arial", 11)).pack(pady=2)
    tk.Label(root, text=f"Genre: {movie['GENRE']}", font=("Arial", 11)).pack(pady=2)
    tk.Label(root, text=f"Runtime: {movie['RUNTIME_MIN']} min", font=("Arial", 11)).pack(pady=2)
    tk.Label(root, text=f"Age Rating: {movie['AGE_RATING']}", font=("Arial", 11)).pack(pady=2)
    tk.Label(root, text=f"Language: {movie['LANGUAGE_CODE']}", font=("Arial", 11)).pack(pady=2)

    tk.Label(
        root,
        text="When you checkout, an AVAILABLE copy will be assigned\n"
             "and your balance will be reduced by the movie price.",
        wraplength=450,
        justify="center"
    ).pack(pady=10)

    def on_checkout():
        success, msg = process_checkout(username, movie_id)
        if success:
            messagebox.showinfo("Checkout Successful", msg)
            result["code"] = 1
            root.destroy()
        else:
            messagebox.showerror("Checkout Failed", msg)

    def on_close():
        result["code"] = 0
        root.destroy()

    tk.Button(root, text="Checkout", width=15, command=on_checkout).pack(pady=10)
    tk.Button(root, text="Cancel", width=15, command=on_close).pack()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
    return result["code"]


if __name__ == "__main__":
    # Simple manual test: run from terminal
    u = input("Enter username: ").strip()
    m = input("Enter movie ID (e.g., M001): ").strip()
    if u and m:
        print("Result code:", show_checkout_gui(u, m))

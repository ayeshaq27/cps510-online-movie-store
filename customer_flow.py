# customer_flow.py
from register_gui import register_user
from login_gui import login_user
from show_movies import show_movies_gui
from library import show_library_gui
from checkout import show_checkout_gui   # <--- NEW


def customer_flow():
    # STEP 1: REGISTER (optional)
    reg = register_user()   # 0, 1, 2, or 3

    if reg == 0:
        print("Registration cancelled/closed.")
        return

    # For 1=registered, 2=user exists, 3=clicked Login
    if reg in (1, 2, 3):
        login_res = login_user()  # {"code": 0/1/2/None, "username": str|None}
        login_code = login_res.get("code")
        username = login_res.get("username")

        if login_code is None:
            print("Login cancelled/closed.")
            return

        if login_code == 0:
            print("User does not exist. You may want to register again.")
            return

        if login_code == 1:
            # Customer login
            movies_res = show_movies_gui()   # {"code": 0/1/2, "movie_id": ...}
            code = movies_res.get("code")
            movie_id = movies_res.get("movie_id")

            if code == 1:
                # user clicked "Library"
                if username:
                    show_library_gui(username)
                else:
                    print("No username found in login result.")

            elif code == 2:
                # user clicked "Checkout"
                if username and movie_id:
                    show_checkout_gui(username, movie_id)
                else:
                    print("Missing username or movie_id for checkout.")

            else:
                # code == 0
                print("Movies window closed without action.")
            return

        if login_code == 2:
            # Employee login placeholder
            print("Employee login not implemented yet.")
            return

        print("Unknown login code:", login_code)


if __name__ == "__main__":
    customer_flow()

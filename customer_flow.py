# customer_flow.py
from register_gui import register_user
from login_gui import login_user
from show_movies import show_movies_gui
from library import show_library_gui
from checkout import show_checkout_gui   # <--- NEW


def go_home():
    # Import here to avoid top-level circular import during landing page startup
    import landing_page
    landing_page.main()


def customer_flow():
    # STEP 1: REGISTER (optional)
    reg = register_user()   # 0, 1, 2, or 3

    if reg == 0:
        print("Registration cancelled/closed.")
        go_home()
        return

    # For 1=registered, 2=user exists, 3=clicked Login
    if reg in (1, 2, 3):
        login_res = login_user()  # {"code": 0/1/2/None, "username": str|None}
        login_code = login_res.get("code")
        username = login_res.get("username")

        if login_code is None:
            print("Login cancelled/closed.")
            go_home()
            return

        if login_code == 0:
            print("User does not exist. You may want to register again.")
            go_home()
            return

        if login_code == 1:
            # Customer login
            movies_res = show_movies_gui()   # {"code": 0/1/2, "movie_id": ...}
            code = movies_res.get("code")
            movie_id = movies_res.get("movie_id")

            if code == 1:
                # user clicked "Library"
                if username:
                    lib_res = show_library_gui(username)
                    # If the user clicked Back in the library, return to movies
                    if lib_res == 2:
                        movies_res = show_movies_gui()   # re-open movies screen
                        code = movies_res.get("code")
                        movie_id = movies_res.get("movie_id")

                        if code == 1:
                            # user clicked Library again
                            show_library_gui(username)

                        elif code == 2:
                            # user clicked Checkout
                            if username and movie_id:
                                show_checkout_gui(username, movie_id)
                            else:
                                print("Missing username or movie_id for checkout after returning from library.")

                        else:
                            print("Movies window closed without action after returning from library.")

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
                go_home()
                return

            # after handling movies/library/checkout, return to landing
            go_home()
            return

        if login_code == 2:
            # Employee login placeholder
            print("Employee login not implemented yet.")
            go_home()
            return

        print("Unknown login code:", login_code)
        go_home()
        return


if __name__ == "__main__":
    customer_flow()

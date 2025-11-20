# cm_flow.py
from update_movie_base import edit_movie_gui 
from add_new_movie import show_add_movie_gui
from show_movies import show_movies_gui
from cm_login import cm_login_user


def cm_flow():
    # Require content-manager login before entering CM flow
    login_res = cm_login_user()
    login_code = login_res.get("code")
    employee_id = login_res.get("employee_id")

    if login_code is None:
        print("CM login cancelled/closed.")
        return

    if login_code != 2:
        print("Content Manager login failed or not authorized.")
        return

    # Proceed with regular CM actions
    res = show_movies_gui()  # {"code": 0/1/2, "movie_id": ...}
    code = res.get("code")
    movie_id = res.get("movie_id")

    if code == 2 and movie_id:
        # "Checkout" in CM mode = edit existing movie
        edit_movie_gui(movie_id)

    elif code == 1:
        # "Library" in CM mode = add new movie
        show_add_movie_gui()

    else:
        print("CM flow cancelled/closed or no action.")


if __name__ == "__main__":
    cm_flow()

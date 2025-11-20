from customer_database_change import show_customer_list_gui
from edit_customer import show_edit_customer_gui
from cs_login import cs_login_user


def cs_flow():
    """
    Customer Service flow for changing customer database details.

    Steps:
      1. Require Customer Service employee login.
      2. Show all customers in a table.
      3. Let user pick one.
      4. Open edit form for the selected customer.
    """
    # Require CS login first
    def go_home():
        import landing_page
        landing_page.main()

    login_res = cs_login_user()
    login_code = login_res.get("code")
    employee_id = login_res.get("employee_id")

    if login_code is None:
        print("Customer Service login cancelled/closed.")
        go_home()
        return

    if login_code != 2:
        print("Customer Service login failed or not authorized.")
        go_home()
        return

    # This returns: {"code": 1/0, "username": "alice" OR None}
    result = show_customer_list_gui()
    code = result.get("code")
    if code == 1:
        username = result.get("username")
        if not username:
            print("No username returned from customer list.")
            go_home()
            return

        edit_result = show_edit_customer_gui(username)
        if edit_result.get("code") == 1:
            print(f"Customer '{username}' details updated successfully by employee {employee_id}.")
        else:
            print("Edit cancelled or failed.")
    else:
        print("Customer database change cancelled/closed.")
        go_home()
        return

    # end of cs_flow: return to landing
    go_home()


if __name__ == "__main__":
    cs_flow()
from customer_database_change import show_customer_list_gui
from edit_customer import show_edit_customer_gui


def cs_flow():
    """
    Customer Service flow for changing customer database details.

    Steps:
      1. Show all customers in a table.
      2. Let user pick one.
      3. Open edit form for the selected customer.
    """
    # This returns: {"code": 1/0, "username": "alice" OR None}
    result = show_customer_list_gui()
    code = result.get("code")

    if code == 1:
        username = result.get("username")
        if not username:
            print("No username returned from customer list.")
            return

        edit_result = show_edit_customer_gui(username)
        if edit_result.get("code") == 1:
            print(f"Customer '{username}' details updated successfully.")
        else:
            print("Edit cancelled or failed.")
    else:
        print("Customer database change cancelled/closed.")
if __name__ == "__main__":
    cs_flow()
# dev_flow.py
#!/usr/bin/env python3
import tkinter as tk

from edit_customer_service import manage_customer_service_gui
from edit_content_manager import manage_content_manager_gui
from edit_developer import manage_developer_gui
from dev_login import dev_login_user


def dev_flow():
    """Main dev admin panel with 3 buttons. Requires developer login."""

    def go_home():
        import landing_page
        landing_page.main()

    # Require developer login first
    login_res = dev_login_user()
    login_code = login_res.get("code")
    employee_id = login_res.get("employee_id")

    if login_code is None:
        print("Developer login cancelled/closed.")
        go_home()
        return

    if login_code != 2:
        print("Developer login failed or not authorized.")
        go_home()
        return

    root = tk.Tk()
    root.title("Developer Admin Panel")
    root.geometry("350x220")

    tk.Label(root, text="Developer Control Panel", font=("Arial", 16)).pack(pady=15)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame,
        text="Edit Customer Service",
        width=22,
        command=manage_customer_service_gui,
    ).pack(pady=5)

    tk.Button(
        btn_frame,
        text="Edit Content Manager",
        width=22,
        command=manage_content_manager_gui,
    ).pack(pady=5)

    tk.Button(
        btn_frame,
        text="Edit Developers",
        width=22,
        command=manage_developer_gui,
    ).pack(pady=5)

    def on_close():
        root.destroy()
        go_home()

    tk.Button(
        root,
        text="Close",
        width=10,
        command=on_close,
    ).pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    dev_flow()

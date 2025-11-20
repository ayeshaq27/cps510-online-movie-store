import tkinter as tk
from tkinter import messagebox


def _call_flow_and_exit(flow_module_name: str, flow_func_name: str = "") -> None:
	"""Destroy the landing window then import and call the requested flow.

	Args:
		flow_module_name: module to import (e.g. 'customer_flow')
		flow_func_name: optional function name inside module (defaults to module-level function with same base name + '_flow')
	"""
	root = tk._default_root
	if root is not None:
		try:
			root.destroy()
		except Exception:
			pass

	try:
		module = __import__(flow_module_name)
		func_name = flow_func_name or f"{flow_module_name.split('_')[0]}_flow"
		func = getattr(module, func_name)
		func()
	except Exception as e:
		# If flow import or execution fails, show an error and exit.
		messagebox.showerror("Flow Error", f"Failed to start {flow_module_name}: {e}")


def main():
	global root
	root = tk.Tk()
	root.title("Online Movie Store — Landing")
	root.geometry("360x360")
	root.resizable(False, False)

	frm = tk.Frame(root, padx=16, pady=16)
	frm.pack(expand=True, fill=tk.BOTH)

	tk.Label(frm, text="Welcome — Choose a login", font=(None, 14)).pack(pady=(0, 8))

	btn_customer = tk.Button(frm, text="Customer Login", width=28, command=lambda: _call_flow_and_exit("customer_flow", "customer_flow"))
	btn_customer.pack(pady=4)

	btn_cs = tk.Button(frm, text="Customer Service Login", width=28, command=lambda: _call_flow_and_exit("cs_flow", "cs_flow"))
	btn_cs.pack(pady=4)

	btn_cm = tk.Button(frm, text="Content Manager Login", width=28, command=lambda: _call_flow_and_exit("cm_flow", "cm_flow"))
	btn_cm.pack(pady=4)

	btn_dev = tk.Button(frm, text="Developer Login", width=28, command=lambda: _call_flow_and_exit("dev_flow", "dev_flow"))
	btn_dev.pack(pady=4)

	root.mainloop()


if __name__ == "__main__":
	main()


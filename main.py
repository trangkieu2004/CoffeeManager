import tkinter as tk
from database import init_db
import login

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    root.title("COFFEE SHOP")
    root.state("zoomed")
    login.show_login(root)
    root.mainloop()

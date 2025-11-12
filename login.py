
"""
login.py - Mẫu file đăng nhập GUI bằng Tkinter
- Hỗ trợ: Đăng ký người dùng mới, đăng nhập, lưu user vào users.json (mật khẩu băm SHA-256)
- Chạy: python login.py
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
import hashlib

USERS_FILE = "users.json"

def hash_password(password: str) -> str:
    """Băm mật khẩu bằng SHA-256 (không dùng salt trong ví dụ đơn giản này)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

class LoginApp:
    def __init__(self, root):
        self.root = root
        root.title("Đăng nhập - PetStation")
        root.geometry("360x260")
        root.resizable(False, False)

        # Frame chính
        frame = tk.Frame(root, padx=16, pady=12)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="ĐĂNG NHẬP", font=("Helvetica", 14, "bold")).pack(pady=(0,12))

        # Username
        tk.Label(frame, text="Tên đăng nhập:").pack(anchor="w")
        self.entry_user = tk.Entry(frame)
        self.entry_user.pack(fill="x", pady=(0,8))

        # Password
        tk.Label(frame, text="Mật khẩu:").pack(anchor="w")
        pw_frame = tk.Frame(frame)
        pw_frame.pack(fill="x", pady=(0,8))
        self.entry_pw = tk.Entry(pw_frame, show="*")
        self.entry_pw.pack(side="left", fill="x", expand=True)
        self.show_pw_var = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(pw_frame, text="Hiện", variable=self.show_pw_var, command=self.toggle_password)
        chk.pack(side="right")

        # Buttons
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", pady=(8,4))
        tk.Button(btn_frame, text="Đăng nhập", command=self.login).pack(side="left", expand=True, fill="x", padx=(0,6))
        tk.Button(btn_frame, text="Đăng ký", command=self.open_register).pack(side="right", expand=True, fill="x", padx=(6,0))

        # Status label
        self.status_label = tk.Label(frame, text="", fg="green")
        self.status_label.pack(pady=(8,0))

        # Load users
        self.users = load_users()

    def toggle_password(self):
        if self.show_pw_var.get():
            self.entry_pw.config(show="")
        else:
            self.entry_pw.config(show="*")

    def login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pw.get()
        if not username or not password:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        hashed = hash_password(password)
        user = self.users.get(username)
        if user and user.get("password") == hashed:
            self.status_label.config(text=f"Đăng nhập thành công. Xin chào, {username}!", fg="green")
            messagebox.showinfo("Thành công", f"Đăng nhập thành công. Xin chào, {username}!")
            # TODO: mở cửa sổ chính của ứng dụng tại đây
        else:
            self.status_label.config(text="Tên đăng nhập hoặc mật khẩu không đúng.", fg="red")
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def open_register(self):
        RegisterWindow(self.root, self)

class RegisterWindow:
    def __init__(self, master, app: LoginApp):
        self.app = app
        self.top = tk.Toplevel(master)
        self.top.title("Đăng ký tài khoản")
        self.top.geometry("360x300")
        self.top.resizable(False, False)

        frame = tk.Frame(self.top, padx=16, pady=12)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="ĐĂNG KÝ", font=("Helvetica", 14, "bold")).pack(pady=(0,12))

        tk.Label(frame, text="Tên đăng nhập:").pack(anchor="w")
        self.entry_user = tk.Entry(frame)
        self.entry_user.pack(fill="x", pady=(0,8))

        tk.Label(frame, text="Mật khẩu:").pack(anchor="w")
        self.entry_pw = tk.Entry(frame, show="*")
        self.entry_pw.pack(fill="x", pady=(0,8))

        tk.Label(frame, text="Nhập lại mật khẩu:").pack(anchor="w")
        self.entry_pw2 = tk.Entry(frame, show="*")
        self.entry_pw2.pack(fill="x", pady=(0,8))

        tk.Label(frame, text="Email (tùy chọn):").pack(anchor="w")
        self.entry_email = tk.Entry(frame)
        self.entry_email.pack(fill="x", pady=(0,8))

        tk.Button(frame, text="Tạo tài khoản", command=self.register).pack(pady=(8,0))

    def register(self):
        username = self.entry_user.get().strip()
        pw = self.entry_pw.get()
        pw2 = self.entry_pw2.get()
        email = self.entry_email.get().strip()

        if not username or not pw:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return
        if pw != pw2:
            messagebox.showwarning("Sai mật khẩu", "Mật khẩu nhập lại không khớp.")
            return
        if username in self.app.users:
            messagebox.showwarning("Trùng tên", "Tên đăng nhập đã tồn tại, vui lòng chọn tên khác.")
            return

        # Lưu user mới
        self.app.users[username] = {
            "password": hash_password(pw),
            "email": email
        }
        save_users(self.app.users)
        messagebox.showinfo("Thành công", f"Tạo tài khoản '{username}' thành công.")
        self.top.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

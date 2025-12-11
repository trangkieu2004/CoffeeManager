import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, hashlib
import re

DB_FILE = "users.db"

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_frame(master, on_success=None, show_login_callback=None):
    """Trả về Frame đăng ký, on_success gọi khi đăng ký thành công"""

    # ✅ Frame to hơn
    frame = tk.Frame(master, bg="white", width=450, height=500, bd=0, relief="flat")
    frame.pack_propagate(False)

    # ---------------- Tiêu đề ----------------
    tk.Label(
        frame, text="🐾 COFFEE SHOP",
        fg="#0078D7", bg="white",
        font=("Helvetica", 26, "bold")
    ).pack(pady=(30, 10))

    tk.Label(
        frame, text="TẠO TÀI KHOẢN",
        bg="white",
        font=("Helvetica", 16, "bold")
    ).pack(pady=(0, 20))

    # ---------------- Tên đăng nhập ----------------
    tk.Label(frame, text="Tên đăng nhập", bg="white", anchor="w").pack(fill='x', padx=50)
    entry_user = ttk.Entry(frame, width=40, font=("Arial", 12))
    entry_user.pack(pady=(0, 15), padx=50)

    # ---------------- Mật khẩu ----------------
    tk.Label(frame, text="Mật khẩu", bg="white", anchor="w").pack(fill='x', padx=50)

    pass_frame = tk.Frame(frame, bg="white")
    pass_frame.pack(pady=(0, 10), padx=50, fill="x")

    entry_pass = ttk.Entry(pass_frame, font=("Arial", 12), show="*")
    entry_pass.pack(side="left", fill="x", expand=True)

    btn_eye1 = ttk.Button(pass_frame, text="👁️", width=3)
    btn_eye1.pack(side="right", padx=5)

    # ---------------- Nhập lại mật khẩu ----------------
    tk.Label(frame, text="Nhập lại mật khẩu", bg="white", anchor="w").pack(fill='x', padx=50)

    repass_frame = tk.Frame(frame, bg="white")
    repass_frame.pack(pady=(0, 10), padx=50, fill="x")

    entry_repass = ttk.Entry(repass_frame, font=("Arial", 12), show="*")
    entry_repass.pack(side="left", fill="x", expand=True)

    btn_eye2 = ttk.Button(repass_frame, text="👁️", width=3)
    btn_eye2.pack(side="right", padx=5)

    # ---------------- Xử lý icon con mắt ----------------
    showing = False

    def toggle_password():
        nonlocal showing
        showing = not showing
        if showing:
            entry_pass.config(show="")
            entry_repass.config(show="")
        else:
            entry_pass.config(show="*")
            entry_repass.config(show="*")

    btn_eye1.config(command=toggle_password)
    btn_eye2.config(command=toggle_password)

    # ---------------- Email ----------------
    tk.Label(frame, text="Email", bg="white", anchor="w").pack(fill='x', padx=50)
    entry_email = ttk.Entry(frame, width=40, font=("Arial", 12))
    entry_email.pack(pady=(0, 25), padx=50)

    # ---------------- Xử lý đăng ký ----------------
    def handle_register():
        username = entry_user.get().strip()
        password = entry_pass.get()
        repassword = entry_repass.get()
        email = entry_email.get().strip()

        # ✅ Kiểm tra rỗng
        if not username or not password or not email:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # ✅ Kiểm tra mật khẩu khớp
        if password != repassword:
            messagebox.showerror("Lỗi", "Mật khẩu nhập lại không khớp!")
            return

        # ✅ Kiểm tra định dạng email
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Lỗi", "Email không đúng định dạng!")
            return

        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username,password,email,role) VALUES (?,?,?,?)",
                (username, hash_password(password), email, "employee")
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Tạo tài khoản thành công!")

            if on_success:
                on_success()  # Quay về login

        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại")

    # ---------------- Style nút ----------------
    style = ttk.Style()
    style.theme_use('clam')
    style.configure(
        "Reg.TButton",
        background="#b87333",
        foreground="white",
        font=("Helvetica", 10, "bold")
    )
    style.map("Reg.TButton", background=[('active', '#8b4513')])
    # ✅ Style cho ENTRY (ô nhập)
    style.configure(
        "Custom.TEntry",
        font=("Segoe UI", 14)
    )

    # ---------------- Nút bấm ----------------
    btn_frame = tk.Frame(frame, bg="white")
    btn_frame.pack(pady=(0, 20))

    ttk.Button(
        btn_frame, text="Đăng ký", width=15,
        style="Reg.TButton", command=handle_register
    ).grid(row=0, column=0, padx=5)

    if show_login_callback:
        ttk.Button(
            btn_frame, text="Cancel", width=15,
            style="Reg.TButton", command=show_login_callback
        ).grid(row=0, column=1, padx=5)

    return frame

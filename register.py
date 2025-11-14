import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, hashlib

DB_FILE = "users.db"

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_frame(master, on_success=None, show_login_callback=None):
    """Trả về Frame đăng ký, on_success gọi khi đăng ký thành công"""
    frame = tk.Frame(master, bg="white", bd=0, relief="flat")

    tk.Label(frame, text="🐾 COFFEE SHOP", fg="#0078D7", bg="white",
             font=("Helvetica",26,"bold")).pack(pady=(30,10))
    tk.Label(frame, text="TẠO TÀI KHOẢN", bg="white", font=("Helvetica",16,"bold")).pack(pady=(0,20))

    # ---------------- Form ----------------
    tk.Label(frame, text="Tên đăng nhập", bg="white", anchor="w").pack(fill='x', padx=50)
    entry_user = ttk.Entry(frame, width=40, font=("Helvetica", 14))
    entry_user.pack(pady=(0,15), padx=50)

    tk.Label(frame, text="Mật khẩu", bg="white", anchor="w").pack(fill='x', padx=50)
    entry_pass = ttk.Entry(frame, width=40, font=("Helvetica", 14), show="*")
    entry_pass.pack(pady=(0,15), padx=50)

    tk.Label(frame, text="Email (tuỳ chọn)", bg="white", anchor="w").pack(fill='x', padx=50)
    entry_email = ttk.Entry(frame, width=40, font=("Helvetica", 14))
    entry_email.pack(pady=(0,25), padx=50)

    def handle_register():
        username = entry_user.get()
        password = entry_pass.get()
        email = entry_email.get()
        if not username or not password:
            messagebox.showwarning("Lỗi", "Tên đăng nhập và mật khẩu không được để trống!")
            return
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username,password,email,role) VALUES (?,?,?,?)",
                           (username, hash_password(password), email, "employee"))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Tạo tài khoản thành công!")
            if on_success:
                on_success()  # Gọi callback quay về login
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi","Tên đăng nhập đã tồn tại")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Reg.TButton", background="#b87333", foreground="white",
                    font=("Helvetica", 12, "bold"))
    style.map("Reg.TButton", background=[('active', '#8b4513')])
    style.configure("Reg.TButton", background="#b87333", foreground="white",
                font=("Helvetica", 10, "bold"))

    btn_frame = tk.Frame(frame, bg="white")
    btn_frame.pack(pady=(0,20))

    ttk.Button(btn_frame, text="Đăng ký", width=15, style="Reg.TButton", command=handle_register).grid(row=0, column=0, padx=5)

    # ---------------- Nút quay về login ----------------
    if show_login_callback:
        ttk.Button(btn_frame, text="Cancel", width=15, style="Reg.TButton",
                   command=show_login_callback).grid(row=0, column=1, padx=5)

    return frame

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os, sqlite3
import register
from database import DB_FILE, hash_password

def login_user(username, password, login_frame, root):
    """Xử lý đăng nhập"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE username=? AND password=?",
                   (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    if user:
        user_id, username, role = user
        messagebox.showinfo("Thành công", f"Xin chào {username}! Role: {role}")
        login_frame.place_forget()  # Ẩn khung login
        if role == "admin":
            show_admin_panel(root, user_id)
    else:
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

def show_admin_panel(root, admin_id):
    """Hiển thị panel admin trên root"""
    panel_frame = tk.Frame(root, bg="#f0f4f8")
    panel_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400)
    tk.Label(panel_frame, text="Admin Panel", font=("Arial",16,"bold"), bg="#f0f4f8").pack(pady=20)

def show_login(root):
    """Hiển thị khung login"""
    # Lấy đường dẫn ảnh
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(BASE_DIR, "img", "taixuong.jpg")

    if not os.path.exists(img_path):
        messagebox.showerror("Lỗi", f"Không tìm thấy ảnh background:\n{img_path}")
    else:
        bg_image = Image.open(img_path)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height))
        bg_photo = ImageTk.PhotoImage(bg_image)
        root.bg_photo = bg_photo  # giữ reference
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    login_frame = tk.Frame(root, bg="white", bd=0, relief="flat")
    login_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=400)

    tk.Label(login_frame, text="🐾 COFFEE SHOP", fg="#0078D7", bg="white",
             font=("Helvetica",26,"bold")).pack(pady=(30,10))
    tk.Label(login_frame, text="ĐĂNG NHẬP", bg="white", font=("Helvetica",16,"bold")).pack(pady=(0,20))

    tk.Label(login_frame, text="Tên đăng nhập", bg="white", anchor="w").pack(fill='x', padx=50)
    entry_user = ttk.Entry(login_frame, width=40, font=("Helvetica", 14))
    entry_user.pack(pady=(0,15), padx=50)

    tk.Label(login_frame, text="Mật khẩu", bg="white", anchor="w").pack(fill='x', padx=50)
    entry_pass = ttk.Entry(login_frame, width=40,font=("Helvetica", 14), show="*")
    entry_pass.pack(pady=(0,25), padx=50)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Coffee.TButton",
                    background="#b87333",
                    foreground="white",
                    font=("Helvetica",12,"bold"))
    style.map("Coffee.TButton",
              background=[('active','#8b4513')])

    ttk.Button(
        login_frame,
        text="Đăng nhập",
        width=25,
        style="Coffee.TButton",
        command=lambda: login_user(entry_user.get(), entry_pass.get(), login_frame, root)
    ).pack(pady=(0, 10))

    # Dòng đăng ký
    register_link_frame = tk.Frame(login_frame, bg="white")
    register_link_frame.pack(pady=(5,0))

    tk.Label(register_link_frame, text="Bạn chưa có tài khoản?", bg="white", font=("Helvetica",10)).pack(side="left")

    lbl_register = tk.Label(
        register_link_frame,
        text="Đăng ký",
        bg="white",
        fg="#0078D7",
        cursor="hand2",
        font=("Helvetica",10,"underline")
    )
    lbl_register.pack(side="left", padx=(5,0))
    lbl_register.bind("<Button-1>", lambda e: show_register(root, login_frame))

def show_register(root, login_frame):
    """Hiển thị khung đăng ký"""
    login_frame.place_forget()
    reg_frame = register.register_frame(root, 
                                    on_success=lambda: show_login(root),
                                    show_login_callback=lambda: show_login(root))

    reg_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=430)

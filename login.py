import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, hashlib, json
from PIL import Image, ImageTk
import os


DB_FILE = "users.db"

# ================= Database =================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        role TEXT NOT NULL,
        permissions TEXT
    )
    """)
    # Tạo 1 admin mặc định nếu chưa có
    cursor.execute("SELECT * FROM users WHERE role='admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("admin", hashlib.sha256("admin123".encode()).hexdigest(), "admin"))
    conn.commit()
    conn.close()

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ================= Login =================
def login_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, permissions FROM users WHERE username=? AND password=?",
                   (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    if user:
        user_id, username, role, permissions = user
        messagebox.showinfo("Thành công", f"Xin chào {username}! Role: {role}")
        if role == "admin":
            show_admin_panel(user_id)
        else:
            show_employee_panel(user_id, permissions)
    else:
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

# ================= Admin Panel =================
def show_admin_panel(admin_id):
    panel = tk.Toplevel(root)
    panel.title("Admin Panel")
    panel.geometry("500x400")
    panel.configure(bg="#f0f4f8")

    
    tk.Label(panel, text="Quản lý nhân viên", font=("Arial",16,"bold"), bg="#f0f4f8").pack(pady=15)
    frame = tk.Frame(panel, bg="white", bd=1, relief="solid")
    frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Nhập thông tin nhân viên mới
    tk.Label(frame, text="Tên đăng nhập:", bg="white").pack(anchor="w", padx=10, pady=(10,0))
    emp_user = ttk.Entry(frame); emp_user.pack(padx=10, pady=5, fill="x")

    tk.Label(frame, text="Mật khẩu:", bg="white").pack(anchor="w", padx=10, pady=(10,0))
    emp_pass = ttk.Entry(frame, show="*"); emp_pass.pack(padx=10, pady=5, fill="x")

    tk.Label(frame, text="Email:", bg="white").pack(anchor="w", padx=10, pady=(10,0))
    emp_email = ttk.Entry(frame); emp_email.pack(padx=10, pady=5, fill="x")

    tk.Label(frame, text="Phân quyền (ví dụ: order,inventory):", bg="white").pack(anchor="w", padx=10, pady=(10,0))
    emp_perm = ttk.Entry(frame); emp_perm.pack(padx=10, pady=5, fill="x")

    def create_employee():
        username = emp_user.get()
        password = emp_pass.get()
        email = emp_email.get()
        permissions = emp_perm.get()
        if not username or not password:
            messagebox.showwarning("Lỗi","Điền đủ tên và mật khẩu!")
            return
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username,password,email,role,permissions) VALUES (?,?,?,?,?)",
                           (username, hash_password(password), email, "employee", permissions))
            conn.commit(); conn.close()
            messagebox.showinfo("Thành công", f"Tạo nhân viên {username} thành công!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")

    ttk.Button(panel, text="Tạo nhân viên", command=create_employee).pack(pady=15)

# ================= Employee Panel =================
def show_employee_panel(emp_id, permissions):
    panel = tk.Toplevel(root)
    panel.title("Employee Panel")
    panel.geometry("400x300")
    tk.Label(panel, text="Giao diện nhân viên", font=("Arial",14,"bold"), bg="#f0f4f8").pack(pady=10)
    tk.Label(panel, text=f"Quyền hạn: {permissions}", bg="#f0f4f8").pack(pady=10)

# ================= GUI Login =================
root = tk.Tk()
root.title("COFFE SHOP")
root.state('zoomed') #full màn hình
#root.configure(bg="#f0f4f8") #nền nhạt, dễ nhìn
img_path = os.path.join("img", "tải xuống.jpg")
bg_image = Image.open(img_path)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
bg_image = bg_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)
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
style.theme_use('clam')  # Theme cho phép đổi nền
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
    command=lambda: login_user(entry_user.get(), entry_pass.get())
).pack(pady=(0, 10))

    # ------------------- Phần dưới nút đăng nhập -------------------
# Tạo frame chứa dòng đăng ký
register_frame = tk.Frame(login_frame, bg="white")
register_frame.pack(pady=(5,0))

tk.Label(register_frame, text="Bạn chưa có tài khoản?", bg="white", font=("Helvetica",10)).pack(side="left")

lbl_register = tk.Label(
    register_frame,
    text="Đăng ký",
    bg="white",
    fg="#0078D7",
    cursor="hand2",
    font=("Helvetica",10,"underline")
)
lbl_register.pack(side="left", padx=(5,0))
lbl_register.bind("<Button-1>", lambda e: open_register(root))


# ================= Start =================
init_db()
root.mainloop()

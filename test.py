import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, hashlib, json
from PIL import Image, ImageTk
import os


DB_FILE = "users.db"
print("Current working directory:", os.getcwd())

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

    tk.Label(frame, text="Tên đăng nhập:", bg="white").pack(anchor="w", padx=10)
    emp_user = ttk.Entry(frame); emp_user.pack(padx=10, pady=5, fill="x")

    tk.Label(frame, text="Mật khẩu:", bg="white").pack(anchor="w", padx=10)
    emp_pass = ttk.Entry(frame, show="*"); emp_pass.pack(padx=10, pady=5, fill="x")

    tk.Label(frame, text="Email:", bg="white").pack(anchor="w", padx=10)
    emp_email = ttk.Entry(frame); emp_email.pack(padx=10, pady=5, fill="x")

    tk.Label(frame, text="Phân quyền (vd: order,inventory):", bg="white").pack(anchor="w", padx=10)
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
    tk.Label(panel, text="Giao diện nhân viên", font=("Arial",14,"bold")).pack(pady=10)
    tk.Label(panel, text=f"Quyền hạn: {permissions}").pack(pady=10)



# =====================================================
# ============= FORM ĐĂNG KÝ (REGISTER) ===============
# =====================================================

def open_register(event=None):
    login_frame.place_forget()   # Ẩn form login
    register_frame.place(relx=0.5, rely=0.5, anchor="center")

def back_to_login():
    register_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

def register_user():
    username = reg_user.get()
    password = reg_pass.get()
    email = reg_email.get()

    if username == "" or password == "":
        messagebox.showwarning("Lỗi", "Không được để trống!")
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(username, password, email, role) VALUES (?,?,?,?)",
                       (username, hash_password(password), email, "employee"))
        conn.commit()
        conn.close()

        messagebox.showinfo("Thành công", "Đăng ký thành công!")
        back_to_login()

    except sqlite3.IntegrityError:
        messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")



# ================= GUI Login =================
root = tk.Tk()
root.title("COFFE SHOP")
root.state('zoomed')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, "img", "taixuong.jpg")

print("Đường dẫn ảnh:", img_path)

if os.path.exists(img_path):
    bg_image = Image.open(img_path)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ---------------- LOGIN FRAME ----------------
login_frame = tk.Frame(root, bg="white")
login_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=400)

tk.Label(login_frame, text="🐾 COFFEE SHOP", fg="#0078D7", bg="white",
         font=("Helvetica",26,"bold")).pack(pady=(30,10))
tk.Label(login_frame, text="ĐĂNG NHẬP", bg="white", font=("Helvetica",16,"bold")).pack(pady=(0,20))

tk.Label(login_frame, text="Tên đăng nhập", bg="white").pack()
entry_user = ttk.Entry(login_frame, width=40)
entry_user.pack(pady=10)

tk.Label(login_frame, text="Mật khẩu", bg="white").pack()
entry_pass = ttk.Entry(login_frame, show="*", width=40)
entry_pass.pack(pady=10)

ttk.Button(login_frame, text="Đăng nhập",
           command=lambda: login_user(entry_user.get(), entry_pass.get())
           ).pack(pady=10)

# Link Đăng ký
reg_link = tk.Label(login_frame, text="Bạn chưa có tài khoản? Đăng ký",
                    bg="white", fg="blue", cursor="hand2")
reg_link.pack()
reg_link.bind("<Button-1>", open_register)


# ---------------- REGISTER FRAME ----------------
register_frame = tk.Frame(root, bg="white", width=450, height=450)

tk.Label(register_frame, text="ĐĂNG KÝ TÀI KHOẢN",
         bg="white", fg="#0078D7", font=("Helvetica",20,"bold")).pack(pady=20)

tk.Label(register_frame, text="Tên đăng nhập", bg="white").pack()
reg_user = ttk.Entry(register_frame, width=40)
reg_user.pack(pady=10)

tk.Label(register_frame, text="Mật khẩu", bg="white").pack()
reg_pass = ttk.Entry(register_frame, show="*", width=40)
reg_pass.pack(pady=10)

tk.Label(register_frame, text="Email", bg="white").pack()
reg_email = ttk.Entry(register_frame, width=40)
reg_email.pack(pady=10)

ttk.Button(register_frame, text="Đăng ký", command=register_user).pack(pady=20)
ttk.Button(register_frame, text="Quay lại đăng nhập", command=back_to_login).pack()

# ================= Start =================
init_db()
root.mainloop()


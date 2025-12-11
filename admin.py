import tkinter as tk
from tkinter import ttk, messagebox
import employee   # module quản lý nhân viên
from product import ProductManagerApp
# import revenue   # để sau làm tiếp

# ===================== GIAO DIỆN ADMIN =====================
def show_admin_panel(root, admin_id=None):

    # XÓA TOÀN BỘ GIAO DIỆN CŨ
    for widget in root.winfo_children():
        widget.destroy()

    root.title("ADMIN - COFFEE SHOP")
    root.geometry("1200x700")
    root.configure(bg="#f2f2f2")

    # ===================== SIDEBAR =====================
    sidebar = tk.Frame(root, bg="#2c3e50", width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(
        sidebar,
        text="ADMIN PANEL",
        fg="white",
        bg="#2c3e50",
        font=("Arial", 16, "bold")
    ).pack(pady=25)

    # ===================== CONTENT =====================
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(side="right", fill="both", expand=True)

    # ===================== CLEAR CONTENT =====================
    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    # ===================== DASHBOARD (TRANG CHỦ) =====================
    def show_dashboard():
        clear_content()

        tk.Label(
            content_frame,
            text="HỆ THỐNG QUẢN LÝ QUÁN CÀ PHÊ",
            font=("Arial", 20, "bold"),
            bg="white"
        ).pack(pady=30)

        tk.Label(
            content_frame,
            text="Chọn chức năng bên trái để quản lý",
            font=("Arial", 12),
            bg="white"
        ).pack(pady=10)

    # ===================== QUẢN LÝ NHÂN VIÊN =====================
    def open_employee_management():
        employee.show_employee_management(content_frame)

    # ===================== ĐĂNG XUẤT =====================
    def logout():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            root.destroy()
            import login
            login.main()

    # ===================== QUẢN LÝ SẢN PHẨM =====================
    def open_products():
        ProductManagerApp(content_frame)

    # ===================== BUTTON STYLE =====================
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Admin.TButton",
        background="#34495e",
        foreground="white",
        font=("Arial", 11),
        padding=10
    )
    style.map(
        "Admin.TButton",
        background=[("active", "#1abc9c")]
    )

    # ===================== MENU BUTTON =====================
    ttk.Button(
        sidebar,
        text="🏠 Trang chủ",
        style="Admin.TButton",
        command=show_dashboard
    ).pack(fill="x", padx=10, pady=5)

    ttk.Button(
        sidebar,
        text="👨‍💼 Quản lý nhân viên",
        style="Admin.TButton",
        command=open_employee_management
    ).pack(fill="x", padx=10, pady=5)

    ttk.Button(
        sidebar,
        text="📦 Quản lý sản phẩm",
        style="Admin.TButton",
        command=open_products
    ).pack(fill="x", padx=10, pady=5)

    ttk.Button(
        sidebar,
        text="📊 Doanh thu",
        style="Admin.TButton",
        command=lambda: messagebox.showinfo("Thông báo", "Sẽ làm sau")
    ).pack(fill="x", padx=10, pady=5)

    ttk.Button(
        sidebar,
        text="🚪 Đăng xuất",
        style="Admin.TButton",
        command=logout
    ).pack(fill="x", padx=10, pady=30)

    # ===================== LOAD MẶC ĐỊNH =====================
    show_dashboard()

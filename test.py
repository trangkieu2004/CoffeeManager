import tkinter as tk
from tkinter import ttk, messagebox


def show_admin_panel():
    root = tk.Tk()
    root.title("HỆ THỐNG QUẢN LÝ QUÁN CÀ PHÊ - ADMIN")
    root.geometry("1100x650")
    root.configure(bg="#f0f2f5")

    # ================== HEADER ==================
    header = tk.Frame(root, bg="#6f4e37", height=60)
    header.pack(fill="x")

    tk.Label(
        header,
        text="☕ ADMIN - QUẢN LÝ QUÁN CÀ PHÊ",
        bg="#6f4e37",
        fg="white",
        font=("Helvetica", 18, "bold")
    ).pack(side="left", padx=20)

    btn_logout = tk.Button(
        header,
        text="Đăng xuất",
        font=("Arial", 11, "bold"),
        bg="#c0392b",
        fg="white",
        cursor="hand2",
        command=lambda: root.destroy()
    )
    btn_logout.pack(side="right", padx=20)

    # ================== MAIN ==================
    main_frame = tk.Frame(root, bg="#f0f2f5")
    main_frame.pack(fill="both", expand=True)

    # ================== SIDEBAR ==================
    sidebar = tk.Frame(main_frame, bg="#2c3e50", width=220)
    sidebar.pack(side="left", fill="y")

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(side="right", fill="both", expand=True)

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    # ================== CÁC TRANG ==================

    def show_product():
        clear_content()
        tk.Label(content_frame, text="QUẢN LÝ SẢN PHẨM", font=("Arial", 18, "bold")).pack(pady=20)

        table = ttk.Treeview(content_frame, columns=("id", "name", "price", "category"), show="headings")
        table.pack(fill="both", expand=True, padx=20, pady=10)

        table.heading("id", text="Mã")
        table.heading("name", text="Tên sản phẩm")
        table.heading("price", text="Giá")
        table.heading("category", text="Loại")

        table.insert("", "end", values=("SP01", "Cà phê sữa", "25000", "Cafe"))
        table.insert("", "end", values=("SP02", "Trà đào", "30000", "Trà"))

    def show_staff():
        clear_content()
        tk.Label(content_frame, text="QUẢN LÝ NHÂN VIÊN", font=("Arial", 18, "bold")).pack(pady=20)

        table = ttk.Treeview(content_frame, columns=("id", "name", "phone", "role"), show="headings")
        table.pack(fill="both", expand=True, padx=20, pady=10)

        table.heading("id", text="Mã")
        table.heading("name", text="Họ tên")
        table.heading("phone", text="SĐT")
        table.heading("role", text="Chức vụ")

        table.insert("", "end", values=("NV01", "Nguyễn Văn A", "0988888888", "Thu ngân"))
        table.insert("", "end", values=("NV02", "Trần Thị B", "0977777777", "Phục vụ"))

    def show_customer():
        clear_content()
        tk.Label(content_frame, text="QUẢN LÝ KHÁCH HÀNG", font=("Arial", 18, "bold")).pack(pady=20)

        table = ttk.Treeview(content_frame, columns=("id", "name", "phone", "point"), show="headings")
        table.pack(fill="both", expand=True, padx=20, pady=10)

        table.heading("id", text="Mã")
        table.heading("name", text="Họ tên")
        table.heading("phone", text="SĐT")
        table.heading("point", text="Điểm")

        table.insert("", "end", values=("KH01", "Lê Văn C", "0909999999", "120"))
        table.insert("", "end", values=("KH02", "Phạm Thị D", "0911111111", "85"))

    def show_invoice():
        clear_content()
        tk.Label(content_frame, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 18, "bold")).pack(pady=20)

        table = ttk.Treeview(content_frame, columns=("id", "time", "total", "staff"), show="headings")
        table.pack(fill="both", expand=True, padx=20, pady=10)

        table.heading("id", text="Mã HĐ")
        table.heading("time", text="Thời gian")
        table.heading("total", text="Tổng tiền")
        table.heading("staff", text="Nhân viên")

        table.insert("", "end", values=("HD01", "10:20 12/12", "120000", "NV01"))
        table.insert("", "end", values=("HD02", "11:05 12/12", "98000", "NV02"))

    def show_revenue():
        clear_content()

        tk.Label(
            content_frame,
            text="THỐNG KÊ DOANH THU",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        # ================== KHỐI TỔNG QUAN ==================
        overview_frame = tk.Frame(content_frame, bg="white")
        overview_frame.pack(fill="x", padx=20)

        def info_box(parent, title, value, color):
            box = tk.Frame(parent, bg=color, height=90, width=200)
            box.pack(side="left", padx=10)
            box.pack_propagate(False)

            tk.Label(box, text=title, bg=color, fg="white", font=("Arial", 11)).pack(pady=(12, 2))
            tk.Label(box, text=value, bg=color, fg="white", font=("Arial", 18, "bold")).pack()

        info_box(overview_frame, "Hôm nay", "1.250.000 ₫", "#27ae60")
        info_box(overview_frame, "Tháng này", "32.800.000 ₫", "#2980b9")
        info_box(overview_frame, "Năm nay", "215.500.000 ₫", "#8e44ad")

        # ================== BẢNG TOP SẢN PHẨM ==================
        tk.Label(
            content_frame,
            text="TOP SẢN PHẨM BÁN CHẠY",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        product_table = ttk.Treeview(
            content_frame,
            columns=("name", "quantity", "revenue"),
            show="headings",
            height=5
        )
        product_table.pack(fill="x", padx=20)

        product_table.heading("name", text="Sản phẩm")
        product_table.heading("quantity", text="Số lượng")
        product_table.heading("revenue", text="Doanh thu")

        product_table.insert("", "end", values=("Cà phê sữa", "120", "3.000.000 ₫"))
        product_table.insert("", "end", values=("Trà đào", "95", "2.850.000 ₫"))
        product_table.insert("", "end", values=("Bạc xỉu", "70", "1.750.000 ₫"))

        # ================== BẢNG TOP NHÂN VIÊN ==================
        tk.Label(
            content_frame,
            text="TOP NHÂN VIÊN BÁN HÀNG",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        staff_table = ttk.Treeview(
            content_frame,
            columns=("name", "invoice", "revenue"),
            show="headings",
            height=5
        )
        staff_table.pack(fill="x", padx=20)

        staff_table.heading("name", text="Nhân viên")
        staff_table.heading("invoice", text="Số hóa đơn")
        staff_table.heading("revenue", text="Doanh thu")

        staff_table.insert("", "end", values=("Nguyễn Văn A", "45", "6.200.000 ₫"))
        staff_table.insert("", "end", values=("Trần Thị B", "32", "4.800.000 ₫"))



    # ================== SIDEBAR BUTTON ==================

    menu_buttons = [
        ("📦 Quản lý Sản phẩm", show_product),
        ("👨‍💼 Quản lý Nhân viên", show_staff),
        ("👥 Quản lý Khách hàng", show_customer),
        ("🧾 Quản lý Hóa đơn", show_invoice),
        ("📊 Thống kê Doanh thu", show_revenue),
    ]

    for text, cmd in menu_buttons:
        tk.Button(
            sidebar,
            text=text,
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white",
            relief="flat",
            height=2,
            cursor="hand2",
            command=cmd
        ).pack(fill="x", padx=10, pady=8)

    show_product()  # Mặc định mở sản phẩm khi chạy

    root.mainloop()


# ================== CHẠY TRỰC TIẾP ==================
if __name__ == "__main__":
    show_admin_panel()
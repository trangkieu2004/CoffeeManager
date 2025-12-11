# product.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import copy

# Try to use DB_FILE from database.py if exists
try:
    from database import DB_FILE
except:
    DB_FILE = "products.db"


# ---------------------- MODEL / PROTOTYPE ----------------------
class ProductPrototype:
    def clone(self):
        return copy.deepcopy(self)


class Product(ProductPrototype):
    def __init__(self, name, price, category, size):
        self.id = None
        self.name = name
        self.price = price
        self.category = category
        self.size = size


# ---------------------- DATABASE ----------------------
def ensure_table():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT,
            category TEXT,
            size TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_product(product: Product):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products(name, price, category, size)
        VALUES (?, ?, ?, ?)
    """, (product.name, product.price, product.category, product.size))
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def update_product(product: Product):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        UPDATE products
        SET name=?, price=?, category=?, size=?
        WHERE id=?
    """, (product.name, product.price, product.category, product.size, product.id))
    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


def fetch_all_products():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, category, size FROM products ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    products = []
    for r in rows:
        p = Product(r[1], r[2], r[3], r[4])
        p.id = r[0]
        products.append(p)
    return products


# ---------------------- UI INSIDE ADMIN ----------------------
class ProductManagerApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        ensure_table()

        # XÓA MÀN HÌNH CŨ CỦA ADMIN
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Tạo container cho toàn bộ giao diện
        self.root = ttk.Frame(self.parent)
        self.root.pack(fill="both", expand=True)

        self.products = fetch_all_products()
        self.setup_style()
        self.build_ui()
        self.load_products_into_tree()

    # ---------------------- STYLE ----------------------
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("Treeview", rowheight=35, font=("Segoe UI", 11))

    # ---------------------- UI ----------------------
    def build_ui(self):
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=14, pady=10)

        # LEFT PANEL — FORM
        left = ttk.Frame(container, width=280)
        left.pack(side="left", fill="y", padx=(0, 12))

        ttk.Label(left, text="☕ QUẢN LÝ SẢN PHẨM", font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.name_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.size_var = tk.StringVar(value="M")

        self._build_entry(left, "Tên sản phẩm", self.name_var)
        self._build_entry(left, "Giá", self.price_var)
        self._build_entry(left, "Loại", self.category_var)

        ttk.Label(left, text="Size").pack(anchor="w", pady=(6, 0))
        size_combo = ttk.Combobox(left, values=["S", "M", "L"], textvariable=self.size_var, state="readonly")
        size_combo.pack(fill="x", pady=6)
        size_combo.current(1)

        ttk.Separator(left).pack(fill="x", pady=10)

        ttk.Button(left, text="➕ Thêm sản phẩm", command=self.on_add).pack(fill="x", pady=6)
        ttk.Button(left, text="✏️ Sửa sản phẩm", command=self.on_edit).pack(fill="x", pady=6)
        ttk.Button(left, text="❌ Xóa sản phẩm", command=self.on_delete).pack(fill="x", pady=6)
        ttk.Button(left, text="📄 Nhân bản (Prototype)", command=self.on_clone).pack(fill="x", pady=12)

        # RIGHT PANEL — TREEVIEW
        right = ttk.Frame(container)
        right.pack(side="right", fill="both", expand=True)

        columns = ("name", "price", "category", "size")
        self.tree = ttk.Treeview(right, columns=columns, show="headings")
        self.tree.heading("name", text="Tên")
        self.tree.heading("price", text="Giá")
        self.tree.heading("category", text="Loại")
        self.tree.heading("size", text="Size")

        self.tree.column("name", width=300)
        self.tree.column("price", width=100, anchor="center")
        self.tree.column("category", width=150, anchor="center")
        self.tree.column("size", width=60, anchor="center")

        vsb = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self.on_edit())

    # Helper: create entry
    def _build_entry(self, parent, label, var):
        ttk.Label(parent, text=label).pack(anchor="w", pady=(6, 0))
        entry = ttk.Entry(parent, textvariable=var)
        entry.pack(fill="x", pady=6)
        return entry

    # ---------------------- LOAD TREE ----------------------
    def load_products_into_tree(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)

        for p in self.products:
            self.tree.insert("", "end", iid=str(p.id),
                             values=(p.name, p.price, p.category, p.size))

    # ---------------------- ACTIONS ----------------------
    def on_add(self):
        name = self.name_var.get().strip()
        price = self.price_var.get().strip()
        category = self.category_var.get().strip()
        size = self.size_var.get().strip()

        if not name or not price or not category:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        p = Product(name, price, category, size)
        pid = insert_product(p)
        p.id = pid
        self.products.append(p)

        self.tree.insert("", "end", iid=str(p.id),
                         values=(p.name, p.price, p.category, p.size))

        self._clear_form()

    def on_edit(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Chọn sản phẩm", "Hãy chọn sản phẩm để sửa!")

        product = self._get_selected_product()
        if product:
            self._open_edit_popup(product)

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Chọn sản phẩm", "Hãy chọn sản phẩm để xóa!")

        if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa?"):
            return

        pid = int(sel[0])
        delete_product(pid)

        self.products = [p for p in self.products if p.id != pid]
        self.tree.delete(sel[0])

    def on_clone(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Chọn sản phẩm", "Hãy chọn sản phẩm để nhân bản!")

        original = self._get_selected_product()
        cloned = original.clone()
        cloned.name += " (Copy)"

        pid = insert_product(cloned)
        cloned.id = pid
        self.products.append(cloned)

        self.tree.insert("", "end", iid=str(pid),
                         values=(cloned.name, cloned.price, cloned.category, cloned.size))

    # ---------------------- UTILS ----------------------
    def _get_selected_product(self):
        try:
            pid = int(self.tree.selection()[0])
        except:
            return None

        for p in self.products:
            if p.id == pid:
                return p
        return None

    def on_tree_select(self, event):
        p = self._get_selected_product()
        if p:
            self.name_var.set(p.name)
            self.price_var.set(p.price)
            self.category_var.set(p.category)
            self.size_var.set(p.size)

    def _clear_form(self):
        self.name_var.set("")
        self.price_var.set("")
        self.category_var.set("")
        self.size_var.set("M")

    # ---------------------- POPUP EDIT ----------------------
    def _open_edit_popup(self, product: Product):
        popup = tk.Toplevel(self.parent)
        popup.title("Chỉnh sửa sản phẩm")
        popup.geometry("350x320")
        popup.resizable(False, False)
        popup.grab_set()

        frame = ttk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Label(frame, text="Tên").pack(anchor="w")
        name_e = ttk.Entry(frame)
        name_e.pack(fill="x", pady=6)
        name_e.insert(0, product.name)

        ttk.Label(frame, text="Giá").pack(anchor="w")
        price_e = ttk.Entry(frame)
        price_e.pack(fill="x", pady=6)
        price_e.insert(0, product.price)

        ttk.Label(frame, text="Loại").pack(anchor="w")
        cat_e = ttk.Entry(frame)
        cat_e.pack(fill="x", pady=6)
        cat_e.insert(0, product.category)

        ttk.Label(frame, text="Size").pack(anchor="w")
        size_c = ttk.Combobox(frame, values=["S", "M", "L"], state="readonly")
        size_c.pack(fill="x", pady=6)
        size_c.set(product.size)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        def save():
            product.name = name_e.get().strip()
            product.price = price_e.get().strip()
            product.category = cat_e.get().strip()
            product.size = size_c.get().strip()

            update_product(product)
            self.load_products_into_tree()
            popup.destroy()

        ttk.Button(btn_frame, text="💾 Lưu", command=save).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Hủy", command=popup.destroy).pack(side="left", padx=10)

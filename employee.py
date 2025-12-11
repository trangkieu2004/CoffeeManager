import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_FILE

# ================= TẠO BẢNG =================
def create_employee_table():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            position TEXT,
            salary REAL
        )
    """)
    conn.commit()
    conn.close()


# ================= GIAO DIỆN QUẢN LÝ =================
def show_employee_management(parent_frame):
    create_employee_table()

    for w in parent_frame.winfo_children():
        w.destroy()

    tk.Label(parent_frame, text="QUẢN LÝ NHÂN VIÊN", font=("Arial", 20, "bold")).pack(pady=15)

    # ================= TÌM KIẾM =================
    search_frame = tk.Frame(parent_frame)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="🔍 Tìm kiếm:").pack(side="left")
    entry_search = ttk.Entry(search_frame, width=35)
    entry_search.pack(side="left", padx=10)

    ttk.Button(search_frame, text="Tìm", command=lambda: load_data(entry_search.get())).pack(side="left")

    # ================= BẢNG =================
    cols = ("id", "name", "phone", "position", "salary")
    tree = ttk.Treeview(parent_frame, columns=cols, show="headings", height=12)
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    tree.heading("id", text="ID")
    tree.heading("name", text="Tên")
    tree.heading("phone", text="SĐT")
    tree.heading("position", text="Chức vụ")
    tree.heading("salary", text="Lương")

    tree.column("id", width=50, anchor="center")
    tree.column("salary", width=120, anchor="center")

    # ================= LOAD DATA =================
    def load_data(keyword=""):
        tree.delete(*tree.get_children())

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        if keyword:
            cur.execute("""
                SELECT * FROM employees
                WHERE name LIKE ? OR phone LIKE ? OR position LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        else:
            cur.execute("SELECT * FROM employees")

        for row in cur.fetchall():
            tree.insert("", "end", values=row)

        conn.close()

    # ================= POPUP THÊM / SỬA =================
    def open_employee_popup(mode="add"):
      popup = tk.Toplevel()
      popup.title("Thêm nhân viên" if mode == "add" else "Sửa nhân viên")
      popup.geometry("380x260")
      popup.resizable(False, False)
      popup.transient()
      popup.grab_set()

      container = tk.Frame(popup)
      container.pack(pady=20, padx=20, fill="both", expand=True)

      # ====== FORM GRID ======
      tk.Label(container, text="Tên NV").grid(row=0, column=0, sticky="w", pady=5)
      tk.Label(container, text="SĐT").grid(row=1, column=0, sticky="w", pady=5)
      tk.Label(container, text="Chức vụ").grid(row=2, column=0, sticky="w", pady=5)
      tk.Label(container, text="Lương").grid(row=3, column=0, sticky="w", pady=5)

      entry_name = ttk.Entry(container, width=30)
      entry_phone = ttk.Entry(container, width=30)
      entry_position = ttk.Entry(container, width=30)
      entry_salary = ttk.Entry(container, width=30)

      entry_name.grid(row=0, column=1, pady=5, padx=10)
      entry_phone.grid(row=1, column=1, pady=5, padx=10)
      entry_position.grid(row=2, column=1, pady=5, padx=10)
      entry_salary.grid(row=3, column=1, pady=5, padx=10)

      selected = tree.focus()

      if mode == "edit":
          if not selected:
              messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên cần sửa")
              popup.destroy()
              return

          data = tree.item(selected, "values")
          entry_name.insert(0, data[1])
          entry_phone.insert(0, data[2])
          entry_position.insert(0, data[3])
          entry_salary.insert(0, data[4])

      # ====== LƯU ======
      def save_employee():
          name = entry_name.get()
          phone = entry_phone.get()
          position = entry_position.get()
          salary = entry_salary.get()

          if not name:
              messagebox.showerror("Lỗi", "Tên không được để trống")
              return

          conn = sqlite3.connect(DB_FILE)
          cur = conn.cursor()

          if mode == "add":
              cur.execute(
                  "INSERT INTO employees(name, phone, position, salary) VALUES (?,?,?,?)",
                  (name, phone, position, salary)
              )
              messagebox.showinfo("Thành công", "Thêm nhân viên thành công!")
          else:
              emp_id = tree.item(selected, "values")[0]
              cur.execute(
                  "UPDATE employees SET name=?, phone=?, position=?, salary=? WHERE id=?",
                  (name, phone, position, salary, emp_id)
              )
              messagebox.showinfo("Thành công", "Cập nhật nhân viên thành công!")

          conn.commit()
          conn.close()
          popup.destroy()
          load_data()

      # ====== NÚT ======
      btn_frame = tk.Frame(container)
      btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

      ttk.Button(btn_frame, text="💾 Lưu", width=12, command=save_employee).grid(row=0, column=0, padx=10)
      ttk.Button(btn_frame, text="❌ Hủy", width=12, command=popup.destroy).grid(row=0, column=1, padx=10)


    # ================= XÓA =================
    def delete_employee():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên cần xóa")
            return

        emp_id = tree.item(selected, "values")[0]

        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?"):
            return

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Thành công", "Xóa nhân viên thành công!")
        load_data()

    # ================= NÚT =================
    btn_frame = tk.Frame(parent_frame)
    btn_frame.pack(pady=15)

    ttk.Button(btn_frame, text="➕ Thêm", width=12, command=lambda: open_employee_popup("add")).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="✏️ Sửa", width=12, command=lambda: open_employee_popup("edit")).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="🗑 Xóa", width=12, command=delete_employee).grid(row=0, column=2, padx=10)

    load_data()

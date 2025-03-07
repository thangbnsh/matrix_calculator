import tkinter as tk
from tkinter import messagebox
import numpy as np

# Biến toàn cục lưu ma trận kết quả trung gian C
intermediate_matrix_C = None

def get_matrix(entry_widgets):
    """Lấy giá trị từ các ô nhập liệu và tạo ma trận 3x3"""
    try:
        matrix = np.array([[float(entry_widgets[i][j].get()) for j in range(3)] for i in range(3)])
        return matrix
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
        return None

def show_result(result, label_var):
    """Hiển thị kết quả (dạng chuỗi) vào nhãn được chỉ định"""
    label_var.set(result)

def show_result_middle(result):
    """Hiển thị kết quả vào ô kết quả trung gian (ma trận C)"""
    result_text_mid.set("Kết quả:\n" + result)

def update_matrix(entries, matrix):
    """Cập nhật ma trận vào ô nhập liệu.
       Nếu phần ảo của phần tử là rất nhỏ, chuyển về số thực."""
    for i in range(3):
        for j in range(3):
            val = matrix[i][j]
            # Nếu là số phức với phần ảo rất nhỏ, lấy phần thực
            if isinstance(val, complex) and abs(val.imag) < 1e-6:
                val = val.real
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(val))

def calculate_determinant(matrix, label_var):
    det = np.linalg.det(matrix)
    show_result(f"Định thức: {det:.2f}", label_var)
    # Không trả về kết quả dưới dạng ma trận

def calculate_inverse(matrix, label_var):
    try:
        inverse = np.linalg.inv(matrix)
        show_result(f"Nghịch đảo:\n{np.array_str(inverse)}", label_var)
        return inverse
    except np.linalg.LinAlgError:
        show_result("Ma trận không khả nghịch", label_var)
        return None

def calculate_transpose(matrix, label_var):
    transpose = matrix.T
    show_result(f"Chuyển vị:\n{np.array_str(transpose)}", label_var)
    return transpose

def calculate_power(matrix, label_var):
    power = np.linalg.matrix_power(matrix, 2)
    show_result(f"Lũy thừa bậc 2:\n{np.array_str(power)}", label_var)
    return power

def diagonalize_matrix(matrix, label_var):
    try:
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        diag_matrix = np.diag(eigenvalues)
        show_result(f"Chéo hóa:\n{np.array_str(diag_matrix)}", label_var)
        return diag_matrix
    except np.linalg.LinAlgError:
        show_result("Không thể chéo hóa", label_var)
        return None

# Các hàm cho phép toán giữa 2 ma trận (A và B)
def calc_add():
    global intermediate_matrix_C
    A = get_matrix(entries_a)
    B = get_matrix(entries_b)
    if A is not None and B is not None:
        intermediate_matrix_C = A + B
        show_result_middle(np.array_str(intermediate_matrix_C))
        
def calc_subtract():
    global intermediate_matrix_C
    A = get_matrix(entries_a)
    B = get_matrix(entries_b)
    if A is not None and B is not None:
        intermediate_matrix_C = A - B
        show_result_middle(np.array_str(intermediate_matrix_C))
        
def calc_multiply():
    global intermediate_matrix_C
    A = get_matrix(entries_a)
    B = get_matrix(entries_b)
    if A is not None and B is not None:
        intermediate_matrix_C = np.dot(A, B)
        show_result_middle(np.array_str(intermediate_matrix_C))

# Các hàm thao tác trên ma trận A và B riêng (các phép tính trả về ma trận)
def calc_inv(matrix_entries, calc_func, result_label):
    global intermediate_matrix_C
    m = get_matrix(matrix_entries)
    res = calc_func(m, result_label)
    if res is not None:
        intermediate_matrix_C = res
        show_result_middle(np.array_str(res))
        
def calc_trans(matrix_entries, calc_func, result_label):
    global intermediate_matrix_C
    m = get_matrix(matrix_entries)
    res = calc_func(m, result_label)
    if res is not None:
        intermediate_matrix_C = res
        show_result_middle(np.array_str(res))
        
def calc_power(matrix_entries, calc_func, result_label):
    global intermediate_matrix_C
    m = get_matrix(matrix_entries)
    res = calc_func(m, result_label)
    if res is not None:
        intermediate_matrix_C = res
        show_result_middle(np.array_str(res))
        
def calc_diag(matrix_entries, calc_func, result_label):
    global intermediate_matrix_C
    m = get_matrix(matrix_entries)
    res = calc_func(m, result_label)
    if res is not None:
        intermediate_matrix_C = res
        show_result_middle(np.array_str(res))

# Hàm lưu kết quả từ ma trận trung gian C vào ma trận A hoặc B
def save_result_to_matrix(matrix_entries):
    global intermediate_matrix_C
    if intermediate_matrix_C is not None:
        update_matrix(matrix_entries, intermediate_matrix_C)
    else:
        messagebox.showerror("Lỗi", "Không có ma trận kết quả để lưu!")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Matrix Calculator")
root.geometry("1400x600")

result_text_a = tk.StringVar()
result_text_b = tk.StringVar()
result_text_mid = tk.StringVar()

# Tạo lưới nhập liệu cho Ma trận A và B
entries_a = [[tk.Entry(root, width=5) for _ in range(3)] for _ in range(3)]
entries_b = [[tk.Entry(root, width=5) for _ in range(3)] for _ in range(3)]

# Sắp xếp ô nhập liệu ra màn hình 
# (Ma trận A ở cột 0-2, Ma trận B ở cột 30-32)
for i in range(3):
    for j in range(3):
        entries_a[i][j].grid(row=i, column=j, padx=3, pady=3)
        entries_b[i][j].grid(row=i, column=j+30, padx=3, pady=3)

# Khối nút tính toán cho Ma trận A
btn_det_a = tk.Button(root, text="Định thức A", 
                      command=lambda: calculate_determinant(get_matrix(entries_a), result_text_a))
btn_det_a.grid(row=3, column=0, columnspan=3)

btn_inv_a = tk.Button(root, text="Nghịch đảo A", 
                      command=lambda: calc_inv(entries_a, calculate_inverse, result_text_a))
btn_inv_a.grid(row=4, column=0, columnspan=3)

btn_trans_a = tk.Button(root, text="Chuyển vị A", 
                        command=lambda: calc_trans(entries_a, calculate_transpose, result_text_a))
btn_trans_a.grid(row=5, column=0, columnspan=3)

btn_power_a = tk.Button(root, text="Lũy thừa A²", 
                        command=lambda: calc_power(entries_a, calculate_power, result_text_a))
btn_power_a.grid(row=6, column=0, columnspan=3)

btn_diag_a = tk.Button(root, text="Chéo hóa A", 
                       command=lambda: calc_diag(entries_a, diagonalize_matrix, result_text_a))
btn_diag_a.grid(row=7, column=0, columnspan=3)

result_label_a = tk.Label(root, textvariable=result_text_a, justify="left")
result_label_a.grid(row=8, column=0, columnspan=3, pady=20)

btn_save_a = tk.Button(root, text="Lưu kết quả vào A", 
                       command=lambda: save_result_to_matrix(entries_a))
btn_save_a.grid(row=9, column=0, columnspan=3, pady=10)

# Khối nút tính toán cho Ma trận B
btn_det_b = tk.Button(root, text="Định thức B", 
                      command=lambda: calculate_determinant(get_matrix(entries_b), result_text_b))
btn_det_b.grid(row=3, column=30, columnspan=3)

btn_inv_b = tk.Button(root, text="Nghịch đảo B", 
                      command=lambda: calc_inv(entries_b, calculate_inverse, result_text_b))
btn_inv_b.grid(row=4, column=30, columnspan=3)

btn_trans_b = tk.Button(root, text="Chuyển vị B", 
                        command=lambda: calc_trans(entries_b, calculate_transpose, result_text_b))
btn_trans_b.grid(row=5, column=30, columnspan=3)

btn_power_b = tk.Button(root, text="Lũy thừa B²", 
                        command=lambda: calc_power(entries_b, calculate_power, result_text_b))
btn_power_b.grid(row=6, column=30, columnspan=3)

btn_diag_b = tk.Button(root, text="Chéo hóa B", 
                       command=lambda: calc_diag(entries_b, diagonalize_matrix, result_text_b))
btn_diag_b.grid(row=7, column=30, columnspan=3)

result_label_b = tk.Label(root, textvariable=result_text_b, justify="left")
result_label_b.grid(row=8, column=30, columnspan=3, pady=20)

btn_save_b = tk.Button(root, text="Lưu kết quả vào B", 
                       command=lambda: save_result_to_matrix(entries_b))
btn_save_b.grid(row=9, column=30, columnspan=3, pady=10)

# Khối giữa: Nút tính toán giữa 2 ma trận (Cộng, Trừ, Nhân)
middle_frame = tk.Frame(root, bd=2, relief="sunken")
middle_frame.grid(row=3, column=12, rowspan=6, padx=20, pady=20)

btn_add = tk.Button(middle_frame, text="Cộng", command=calc_add)
btn_add.grid(row=0, column=0, padx=5, pady=5)

btn_subtract = tk.Button(middle_frame, text="Trừ", command=calc_subtract)
btn_subtract.grid(row=1, column=0, padx=5, pady=5)

btn_multiply = tk.Button(middle_frame, text="Nhân", command=calc_multiply)
btn_multiply.grid(row=2, column=0, padx=5, pady=5)

result_label_mid = tk.Label(middle_frame, textvariable=result_text_mid, justify="left")
result_label_mid.grid(row=3, column=0, padx=5, pady=5)

# Chạy chương trình
root.mainloop()

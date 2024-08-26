import numpy as np

def to_binary_matrix(matrix):
    # 将矩阵转化为 NumPy 数组
    A = np.array(matrix, dtype=float)
    
    # 获取矩阵的行数和列数
    m, n = A.shape
    
    # 行变换：高斯消元法
    for i in range(min(m, n)):
        # 找到第 i 列中绝对值最大的元素所在的行
        max_row = np.argmax(np.abs(A[i:, i])) + i
        if A[max_row, i] == 0:
            continue
        
        # 交换行
        if max_row != i:
            A[[i, max_row]] = A[[max_row, i]]
        
        # 将主对角线上的元素变为 1
        A[i] = A[i] / A[i, i]
        
        # 使其他行对应列元素为 0
        for j in range(m):
            if i != j:
                A[j] = A[j] - A[j, i] * A[i]

    # 将矩阵中的元素变为 -1, 0, 1
    # B = np.round(A).astype(int)
    # B[B > 1] = 1
    # B[B < -1] = -1
    
    return A

# 示例矩阵
matrix = [
    [1, 0, -2],
    [0, 1, -1],
]

result = to_binary_matrix(matrix)
print(result)

# 代码生成时间: 2025-10-02 01:44:26
import numpy as np
a""
This module provides a set of functions to perform matrix operations.
"""

def matrix_addition(matrix_a, matrix_b):
    """
    Adds two matrices element-wise.
    
    Args:
        matrix_a (np.ndarray): The first matrix.
        matrix_b (np.ndarray): The second matrix.
    
    Returns:
        np.ndarray: The result of the addition.
    """
    if matrix_a.shape != matrix_b.shape:
        raise ValueError("Matrices must have the same dimensions for addition.")
    return np.add(matrix_a, matrix_b)

def matrix_subtraction(matrix_a, matrix_b):
    """
    Subtracts one matrix from another element-wise.
    
    Args:
        matrix_a (np.ndarray): The first matrix.
        matrix_b (np.ndarray): The second matrix.
    
    Returns:
        np.ndarray: The result of the subtraction.
    """
    if matrix_a.shape != matrix_b.shape:
        raise ValueError("Matrices must have the same dimensions for subtraction.")
    return np.subtract(matrix_a, matrix_b)

def matrix_multiplication(matrix_a, matrix_b):
    """
    Multiplies two matrices.
    
    Args:
        matrix_a (np.ndarray): The first matrix.
        matrix_b (np.ndarray): The second matrix.
    
    Returns:
        np.ndarray: The result of the multiplication.
    """
    if matrix_a.shape[1] != matrix_b.shape[0]:
        raise ValueError("The number of columns in the first matrix must equal the number of rows in the second matrix for multiplication.")
    return np.dot(matrix_a, matrix_b)

def matrix_transpose(matrix):
    """
    Transposes the given matrix.
    
    Args:
        matrix (np.ndarray): The matrix to transpose.
    
    Returns:
        np.ndarray: The transposed matrix.
    """
    return np.transpose(matrix)

def matrix_inverse(matrix):
    """
    Calculates the inverse of a square matrix.
    
    Args:
        matrix (np.ndarray): The square matrix to invert.
    
    Returns:
        np.ndarray: The inverse of the matrix, or None if the matrix is singular.
    """
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("The matrix must be square for inversion.")
    try:
        return np.linalg.inv(matrix)
    except np.linalg.LinAlgError:
        return None

def main():
    matrix1 = np.array([[1, 2], [3, 4]])
    matrix2 = np.array([[5, 6], [7, 8]])
    print("Matrix Addition:")
    print(matrix_addition(matrix1, matrix2))
    print("Matrix Subtraction:")
    print(matrix_subtraction(matrix1, matrix2))
    print("Matrix Multiplication:")
    print(matrix_multiplication(matrix1, matrix2))
    print("Matrix Transpose:")
    print(matrix_transpose(matrix1))
    print("Matrix Inverse:")
    print(matrix_inverse(matrix1))

def __starting_point():
    main()
if __name__ == "__main__":
    __starting_point()
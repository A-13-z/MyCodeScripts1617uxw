'''
Name: Aswitha Sriee
Roll No.: EE23B092
File: matmul.py
Assignment: Matrix Multiplication
Imports: List, Tuple from typing
Functions: is_valid_matrix(m) and matrix_multiply(m1, m2)
'''

from typing import List, Tuple

def is_valid_matrix(matrix: List[List]) -> Tuple[bool, int]:
    '''
    Check if a given matrix is valid, (i.e.) it can be multiplied with another valid matrix

    Parameters:
    matrix (List[List]): A nested list whose inner-list can be of type int, float, or complex

    Returns:
    Tuple[bool, int]: The validity of the matrix and the error it represents

    Things the function looks for:-
        + if the sub-lists are all of equal length :- ERROR CODE -> -1
        + if the data-type of the sub-list entries are valid (int, float or complex):- ERROR CODE -> -2
        + if the length is non-zero :- ERROR CODE -> -3

    If all the above conditions are fulfilled, the matrix is said to be valid and the function returns (True, 0)
    Else it returns (False, ERR_CODE)
    '''

    #length of the outer list; gives the number of rows
    l = len(matrix)

    #check if the list is non-empty (ERROR -3)
    if l != 0:
        #length of the sub-list; if ERROR -1 is occuring that would imply length of some sub-list is not equal to l1
        #this would imply that the matrix is not of uniform shape, that is, the columns are indiscernible
        l1 = len(matrix[0])

        #checking individual rows iteratively
        for i in matrix:
            #checks if ERROR -1 occurs
            if len(i) != l1:
                return (False, -1)
            
            #checks if ERROR -2 occurs
            if len([1 for j in i if (not(type(j) == int)) and (not(type(j) == float)) and (not(type(j) == complex))]) != 0:
                return (False, -2)
        #returns if it passes all conditions sucessfully
        return (True, 0)
    else:
        #returns if ERROR -3 occurs
        return (False, -3)

def matrix_multiply(matrix1: List[List], matrix2: List[List]) -> List[List]:
    '''
    Multiplies two valid matrices. The validity of the matrices are checked by is_valid_matrix(matrix) function

    Parameters:
    matrix1 (List[List]): A nested list whose inner-list can be of type int, float, or complex
    matrix2 (List[List]): A nested list whose inner-list can be of type int, float, or complex

    Returns:
    List[List]: The matrix multiplication result of matrix1 and matrix2

    The function checks if the matrices can be multiplied. If the shape of matrix1 is (m, n) and that if matrix2 is (p, q)
    then, the function checks if n = p before proceeding with the multiplication itself.
    '''

    #checks if the individual matrices are valid
    if is_valid_matrix(matrix1)[0] and is_valid_matrix(matrix2)[0]:
        #checks if the dimensions are appropriate for multiplication (as explained above)
        if len(matrix2) != len(matrix1[0]):
            #if not appropriate then ValueError is raise
            raise ValueError("Invalid Dimensions. Can't be multiplied")
        
        #the lengths of the matrices, that is the number of rows in each matrix
        l1 = len(matrix1)
        l2 = len(matrix2)

        #initializing the resultant matrix with zeroes
        final_result = [[0 for _ in range(len(matrix2[0]))] for _w in range(l1)]

        #iterates through the rows of matrix1
        for i in range(l1):
            #accessing the row of matrix1
            row = matrix1[i]
            
            #iterates through column of matrix2
            for j in range(len(matrix2[0])):
                #iterates through the rows to access the element from jth column
                for k in range(l2):
                    #adding the sum to the final result at the correct position
                    final_result[i][j] += row[k]*matrix2[k][j]
        
        #returns the resultant matrix
        return final_result
    else:
        #if the matrix/matrices are not valid

        #if the datatype of sub-list(s) contains datatypes other than int/float/complex
        if is_valid_matrix(matrix1)[1] == -2 or is_valid_matrix(matrix2)[1] == -2:
            raise TypeError("Invalid datatypes in the matrix")
        else:
            #if the length is zero/if the columns are not discernible
            #raise ValueError
            raise ValueError("Unable to multiply two matrices given")   
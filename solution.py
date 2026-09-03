def submat(mat:List[List[int]]) -> int:
    ##### DP solution
    width = len(mat)
    if width == 0:
        return 0
    height = len(mat[0])
    if height == 0:
        return 0
    #

if __name__ == "__main__":
    A = [[1, 0, 1],
         [1, 1, 0],
         [1, 1, 0]]
    B = [[1, 1, 0, 1],
         [1, 1, 1, 0],
         [0, 1, 0, 0]]
    a = submat(A)
    b = submat(B)
    print(f"Solution A: {a}")
    print(f"Soultion B: {b}")
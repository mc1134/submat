import tester as tester

class Solution:
    def sprint(self, s):
        if False: # CHANGE THIS TO TRUE FOR PRINTING LOGS
            print(s)

    def submat(self, mat:list[list[int]]) -> int:
        # choose self.bf or self.dp
        return self.dp(mat)

    def dp(self, mat):
        ##### DP solution
        height = len(mat)
        if height == 0:
            return 0
        width = len(mat[0])
        if width == 0:
            return 0
        dp = [[0 for _ in range(width)] for _ in range(height)]
        for h_idx in range(height):
            for w_idx in range(width):
                # use DP
                up, left, upleft = 0, 0, 0
                if h_idx > 0:
                    up = dp[h_idx-1][w_idx]
                if w_idx > 0:
                    left = dp[h_idx][w_idx-1]
                if up * left > 0:
                    upleft = dp[h_idx-1][w_idx-1]
                # calculate the number of all-1 submats that include this 1
                N = 0
                if mat[h_idx][w_idx] == 1:
                    i, lmax = h_idx, 0
                    while i >= 0 and mat[i][w_idx] != 0:
                        j = w_idx
                        while j >= 0 and j >= lmax:
                            if mat[i][j] == 1:
                                N += 1
                            else:
                                lmax = j+1
                            j -= 1
                        i -= 1
                if height*width < 50:
                    self.sprint("{} {} {} {}".format(up, left, upleft, N))
                dp[h_idx][w_idx] = left + up - upleft + N
                pass
        return dp[-1][-1]

    def bf(self, mat):
        ##### brute force solution
        # iterate through all possible submatrix dimensions, from smallest to largest
        # for each size, move the "sliding window" through and check if every element is a 1
        # if it is, increment sum
        if len(mat) == 0 or len(mat[0]) == 0:
            return 0
        s = 0
        for dim_height in range(1, len(mat) + 1):
            for dim_width in range(1, len(mat[0]) + 1):
                self.sprint("{} {}".format(dim_height, dim_width))
                for h_idx in range(len(mat) - dim_height + 1):
                    for w_idx in range(len(mat[0]) - dim_width + 1):
                        test = [row[w_idx:w_idx + dim_width] for row in mat][h_idx:h_idx + dim_height]
                        self.sprint("\t{} {}; {}".format(h_idx, w_idx, test))
                        self.sprint("\t\t{}".format([i == 1 for row in test for i in row]))
                        if all([i == 1 for row in test for i in row]):
                            s += 1
        return s

if __name__ == "__main__":
    solution = Solution()
    tester.run_tests(solution)
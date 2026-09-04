import tester as tester

class Solution:
    def sprint(self, s):
        if False: # CHANGE THIS TO TRUE FOR PRINTING LOGS
            print(s)

    def submat(self, mat:list[list[int]]) -> int:
        ##### DP solution
        # height = len(mat)
        # if height == 0:
        #     return 0
        # width = len(mat[0])
        # if width == 0:
        #     return 0
        # dp = [[0 for _ in range(width)] for _ in range(height)]
        # print(dp)
        # return -1
        ##### brute force solution
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
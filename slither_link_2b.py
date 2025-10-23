"""
简陋数回解题器
用一维列表
然后进一步优化

2025/8/26 - 2025/9/5
"""

class Slither_link():
    def __init__(self, size, puzzle):
        self.size = size
        self.puzzle = puzzle
        self._techniques = {7:self._last_line_around_num, 8:self._eliminate_line_around_num, 9:self._eliminate_line_around_dot, 10:self._no_branches, 11:self._no_end, \
                            12:self._no_other_loop}
    def load(self, size, loop_str):
        """加载谜题
        参数
        size：tuple，第一个元素表示一行有多少列，第二个元素表示有多少行
        loop_str：str，.表示空，0到4表示数字"""
        self.size = size
        self.width = self.size[0]
        self.height = self.size[1]
        if len(loop_str) > self.width * self.height:
            return "题目出错：不可能的尺寸"
        for x in loop_str:
            if x not in ['.', '0', '1', '2', '3', '4']:
                return "题目出错： 不可能的字符{}".format(x)
        loop = ([1, None] * self.width + [1] + [None] * (2 * self.width + 1)) * self.height + [1, None] * self.width + [1]
        for y in range(self.height):
            for x in range(self.width):
                c = loop_str[y*self.width+x]
                if c != '.':
                    loop[(2*y+1)*(2*self.width+1)+2*x+1] = int(c)
        self.loop = loop
    # width -> n
    # height -> height*2+1
    def print_loop(self, loop):
        for x in range(len(loop)):
            if loop[x] == None:
                print('.', end = ' ')
            else:
                print(loop[x], end = ' ')
            if (x + 1) % (2 * self.width + 1) == 0:
                print()
    def zeros(self, loop):
        """0周围没有线
        1 . 1      1 0 1
        . 0 .  ->  0 0 0
        1 . 1      1 0 1
        """
        n = self.width*2+1
        for x in range(n, self.height*2*n, 2*n):
            for y in range(1, n, 2):
                a = x + y
                if loop[x+y] == 0:
                    loop[x+y-n], loop[x+y+n], loop[x+y-1], loop[x+y+1] = 0, 0, 0, 0
    def corner3(self, loop):
        """角落3定式
        1 . 1 . 1      1 1 1 . 1
        . 3 . . .      1 3 . . .
        1 . 1 . 1  ->  1 . 1 . 1
        . . . . .      . . . . .
        1 . 1 . 1      1 . 1 . 1
        """
        n = self.width*2+1
        m = self.height*2*n
        if loop[n+1] == 3:
            loop[1] = 0
            loop[n] = 0
        if loop[2*n-2] == 3:
            loop[n-2] = 0
            loop[2*n-1] = 0
        if loop[m-n+1] == 3:
            loop[m-n] = 0
            loop[m+1] = 0
        if loop[m-2] == 3:
            loop[m-1] = 0
            loop[m+n-2] = 0
    def corner1(self, loop):
        """角落1定式
        1 . 1 . 1      1 0 1 . 1
        . 1 . . .      0 1 . . .
        1 . 1 . 1  ->  1 . 1 . 1
        . . . . .      . . . . .
        1 . 1 . 1      1 . 1 . 1
        """
        n = self.width*2+1
        m = self.height*2*n
        if loop[n+1] == 1:
            loop[1] = 0
            loop[n] = 0
        if loop[2*n-2] == 1:
            loop[n-2] = 0
            loop[2*n-1] = 0
        if loop[m-n+1] == 1:
            loop[m-n] = 0
            loop[m+1] = 0
        if loop[m-2] == 1:
            loop[m-1] = 0
            loop[m+n-2] = 0
    def adjacent3s(self, loop):
        """相邻3定式
        1 . 1 . 1 . 1      1 . 1 1 1 . 1
        . . . 3 . . .      . . . 3 . . .
        1 . 1 . 1 . 1  ->  1 0 1 1 1 0 1
        . . . 3 . . .      . . . 3 . . .
        1 . 1 . 1 . 1      1 . 1 1 1 . 1
        """
        n = self.width*2+1
        m = self.height*2*n
        for x in range(n, m, 2*n):  # 横向
            for y in range(1, n, 2):
                a = x + y
                if loop[a] == 3:
                    if y != n - 2:
                        if loop[a+2] == 3:
                            loop[a-1], loop[a+1], loop[a+3] = 1, 1, 1
                            if x != n:
                                loop[a-2*n+1] = 0
                            if x != m-n:
                                loop[a+2*n+1] = 0
                    if x != m - n:
                        if loop[a+2*n] == 3:
                            loop[a-n], loop[a+n], loop[a+3*n] = 1, 1, 1
                            if y != 1:
                                loop[a+n-2] = 0
                            if y != n-2:
                                loop[a+n+2] = 0
    def diagonal_3s(self, loop):
        """对角3定式，对角相邻的两个3，远离另外一个3的两边连线
        1 . 1 . 1      1 . 1 1 1
        . . . 3 .      . . . 3 1
        1 . 1 . 1  ->  1 . 1 . 1
        . 3 . . .      1 3 . . .
        1 . 1 . 1      1 1 1 . 1
        
        若
        1 . 1 . 1      1 . 1 . 1      1 . 1 . 1
        . . . 3 .      . . . 3 .      . . 0 3 .
        1 . 1 . 1  ->  1 1 1 . 1  ->  1 1 1 0 1
        0 3 . . .      0 3 1 . .      0 3 1 . . 
        1 . 1 . 1      1 1 1 . 1      1 1 1 . 1 剩下的3只剩两个位置可以连线，矛盾
        """
        n = self.width*2+1
        for x in range(n, self.height*2*n-n, 2*n):
            for y in range(1, n-1, 2):
                if loop[x+y] == 3:
                    a = x + y
                    if y != 1:
                        if loop[a+2*n-2] == 3:
                            loop[a+3*n-2], loop[a+2*n-3], loop[a-n], loop[a+1] = 1, 1, 1, 1
                    if y != n - 1:
                        if loop[a+2*n+2] == 3:
                            loop[a+3*n+2], loop[a+2*n+3], loop[a-n], loop[a-1] = 1, 1, 1, 1
    def extended_diagonal_3s(self, loop):
        """扩展版的对角3定式，在一条对角线上的两个3中间间隔任意数量的2，且这些2和3彼此对角相邻，两个3远离另外一个3和中间的2的两边连线
        1 . 1 . 1 . 1      1 . 1 . 1 1 1
        . . . . . 3 .      . . . . . 3 1
        1 . 1 . 1 . 1      1 . 1 . 1 . 1
        . . . 2 . . .  ->  . . . 2 . . .
        1 . 1 . 1 . 1      1 . 1 . 1 . 1
        . 3 . . . . .      1 3 . . . . .
        1 . 1 . 1 . 1      1 1 1 . 1 . 1

        若
        1 . 1 . 1 . 1      1 . 1 . 1 1 1      1 . 1 . 1 1 1      1 . 1 . 1 1 1      1 . 1 . 1 1 1
        . . . . . 3 0      . . . . 1 3 0      . . . . 1 3 0      . . . . 1 3 0      . . . . 1 3 0
        1 . 1 . 1 . 1      1 . 1 . 1 1 1      1 . 1 0 1 1 1      1 . 1 0 1 1 1      1 . 1 0 1 1 1
        . . . 2 . . .  ->  . . . 2 . . .  ->  . . . 2 0 . .  ->  . . 1 2 0 . .  ->  . . 1 2 0 . .
        1 . 1 . 1 . 1      1 . 1 . 1 . 1      1 . 1 . 1 . 1      1 . 1 1 1 . 1      1 0 1 1 1 . 1
        . 3 . . . . .      . 3 . . . . .      . 3 . . . . .      . 3 . . . . .      . 3 0 . . . .
        1 . 1 . 1 . 1      1 . 1 . 1 . 1      1 . 1 . 1 . 1      1 . 1 . 1 . 1      1 . 1 . 1 . 1 剩下的3周围只剩两个位置可以连线，矛盾

        1 . 1 . 1 . . . 1 . 1 . 1      1 . 1 . 1 . . . 1 . 1 1 1
        . . . . .       . . . 3 .      . . . . .       . . . 3 1
        1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1
        . . . . .       . 2 . . .      . . . . .       . 2 . . .
        1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1
        .             .         .      .             .         .
        .           .           .  ->  .           .           .
        .         .             .      .         .             .
        1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1
        . . . 2 .       . . . . .      . . . 2 .       . . . . .
        1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1
        . 3 . . .       . . . . .      . 3 . . .       . . . . .
        1 . 1 . 1 . . . 1 . 1 . 1      1 . 1 . 1 . . . 1 . 1 . 1

        若
        1 . 1 . 1 . . . 1 . 1 0 1      1 . 1 . 1 . . . 1 . 1 0 1      1 . 1 . 1 . . . 1 . 1 0 1      1 . 1 . 1 . . . 1 . 1 0 1               1 . 1 . 1 . . . 1 . 1 0 1      1 . 1 . 1 . . . 1 . 1 0 1
        . . . . .       . . . 3 .      . . . . .       . . 1 3 1      . . . . .       . . 1 3 1      . . . . .       . . 1 3 1               . . . . .       . . 1 3 1      . . . . .       . . 1 3 1
        1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 1 1      1 . 1 . 1       1 0 1 1 1      1 . 1 . 1       1 0 1 1 1               1 . 1 . 1       1 0 1 1 1      1 . 1 . 1       1 0 1 1 1
        . . . . .       . 2 . . .      . . . . .       . 2 . . .      . . . . .       . 2 0 . .      . . . . .       1 2 0 . .               . . . . .       1 2 0 . .      . . . . .       1 2 0 . .
        1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 1 1 . 1               1 . 1 . 1       1 1 1 . 1      1 . 1 . 1       1 1 1 . 1
        .             .         .      .             .         .      .             .         .      .             .         .               .             .         .      .             .         .
        .           .           .  ->  .           .           .  ->  .           .           .  ->  .           .           .  ->  ...  ->  .           .           .  ->  .           .           . 
        .         .             .      .         .             .      .         .             .      .         .             .               .         .             .      .         .             .
        1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1               1 . 1 0 1       1 . 1 . 1      1 . 1 0 1       1 . 1 . 1
        . . . 2 .       . . . . .      . . . 2 .       . . . . .      . . . 2 .       . . . . .      . . . 2 .       . . . . .               . . 1 2 0       . . . . .      . . 1 2 0       . . . . .
        1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1      1 . 1 . 1       1 . 1 . 1               1 . 1 1 1       1 . 1 . 1      1 0 1 1 1       1 . 1 . 1
        . 3 . . .       . . . . .      . 3 . . .       . . . . .      . 3 . . .       . . . . .      . 3 . . .       . . . . .               . 3 . . .       . . . . .      . 3 0 . .       . . . . .
        1 . 1 . 1 . . . 1 . 1 . 1      1 . 1 . 1 . . . 1 . 1 . 1      1 . 1 . 1 . . . 1 . 1 . 1      1 . 1 . 1 . . . 1 . 1 . 1               1 . 1 . 1 . . . 1 . 1 . 1      1 . 1 . 1 . . . 1 . 1 . 1 剩下的3周围只剩两个位置可以连线，矛盾
        """
        n = self.width*2+1
        m = self.height*2*n
        for x in range(n, m, 2*n):
            for y in range(1, n-1, 2):
                if loop[x+y] == 3:
                    search_3_x, search_3_y = x + 2 * n, y + 2
                    if search_3_x < m and search_3_y < n:
                        if loop[search_3_x+search_3_y] == 2:
                            while 1:
                                search_3_x += 2 * n
                                search_3_y += 2
                                if search_3_x < m and search_3_y < n:
                                    if loop[search_3_x+search_3_y] == 3:
                                        loop[x+y-n], loop[x+y-1], loop[search_3_x+search_3_y+1], loop[search_3_x+search_3_y+n] = 1, 1, 1, 1
                                        break
                                    elif loop[search_3_x+search_3_y] == 2:
                                        continue
                                    else:
                                        break
                                else:
                                    break
                    search_3_x, search_3_y = x + 2 * n, y - 2
                    if search_3_x < m and search_3_y > 0:
                        if loop[search_3_x+search_3_y] == 2:
                            while 1:
                                search_3_x += 2 * n
                                search_3_y -= 2
                                if search_3_x < m and search_3_y > 0:
                                    if loop[search_3_x+search_3_y] == 3:
                                        loop[x+y-n], loop[x+y+1], loop[search_3_x+search_3_y-1], loop[search_3_x+search_3_y+n] = 1, 1, 1, 1
                                        break
                                    elif loop[search_3_x+search_3_y] == 2:
                                        continue
                                    else:
                                        break
                                else:
                                    break
    def extended_diagonal_3s_2(self, loop):
        n = self.width*2+1
        m = self.height*2*n
        for x in range(n, m, 2*n):
            for y in range(1, n-1, 2):
                if loop[x+y] == 3:
                    search_3_x, search_3_y = x + 2 * n, y + 2
                    if search_3_x < m and search_3_y < n:
                        if loop[search_3_x+search_3_y] == 2:
                            while 1:
                                search_3_x += 2 * n
                                search_3_y += 2
                                if search_3_x < m and search_3_y < n:
                                    if loop[search_3_x+search_3_y] == 3:
                                        loop[x+y-n], loop[x+y-1], loop[search_3_x+search_3_y+1], loop[search_3_x+search_3_y+n] = 1, 1, 1, 1
                                        break
                                    elif loop[search_3_x+search_3_y] == 2:
                                        continue
                                    else:
                                        break
                                else:
                                    break
                    search_3_x, search_3_y = x + 2 * n, y - 2
                    if search_3_x < m and search_3_y > 0:
                        if loop[search_3_x+search_3_y] == 2:
                            while 1:
                                search_3_x += 2 * n
                                search_3_y -= 2
                                if search_3_x < m and search_3_y > 0:
                                    if loop[search_3_x+search_3_y] == 3:
                                        loop[x+y-n], loop[x+y+1], loop[search_3_x+search_3_y-1], loop[search_3_x+search_3_y+n] = 1, 1, 1, 1
                                        break
                                    elif loop[search_3_x+search_3_y] == 2:
                                        continue
                                    else:
                                        break
                                else:
                                    break
    def _last_line_around_num(self, loop):
        """数字x周围只剩x个位置->都连线
        例
        1 0 1      1 0 1
        0 1 0  ->  0 1 0
        1 . 1      1 1 1
        
        1 0 1      1 0 1
        0 2 .  ->  0 2 1
        1 . 1      1 1 1

        1 . 1      1 1 1
        . 3 .  ->  1 3 1
        1 0 1      1 0 1
        """
        n = self.width*2+1
        for x in range(n, self.height*2*n+n, 2*n):
            for y in range(1, n, 2):
                a = x + y
                if loop[a] != None and loop[a] != 0:  # python 版本：3.12.0  如果还用x作为内层循环的变量，这个x会覆盖掉外层循环变量x的值，在内层循环执行完成之后，外层这一次循环完成之前，x都是内层循环时最后一次循环的循环变量值，是一个元组，不是整数，从而在这里出错。
                    lines = [loop[a-1], loop[a+1], loop[a-n], loop[a+n]]
                    if lines.count(1) + lines.count(None) == loop[a]:
                        if loop[a-1] == None:  # 4个if比for加if稍快一些
                            loop[a-1] = 1
                        if loop[a+1] == None:
                            loop[a+1] = 1
                        if loop[a-n] == None:
                            loop[a-n] = 1
                        if loop[a+n] == None:
                            loop[a+n] = 1
    def _eliminate_line_around_num(self, loop):
        """如果一个数字x周围已有x个位置可以连线，那么其余位置都不能连线"""
        n = self.width*2+1
        for x in range(n, self.height*2*n+n, 2*n):
            for y in range(1, n, 2):
                a = x + y
                if loop[a] != None and loop[a] != 0:
                    if [loop[a-1], loop[a+1], loop[a-n], loop[a+n]].count(1) == loop[a]:
                        if loop[a-1] == None:
                            loop[a-1] = 0
                        if loop[a+1] == None:
                            loop[a+1] = 0
                        if loop[a-n] == None:
                            loop[a-n] = 0
                        if loop[a+n] == None:
                            loop[a+n] = 0
    def _eliminate_line_around_dot(self, loop):
        """如果一个没有连线的点只有一个可能位置能连线，则这个位置不能连线"""
        n = self.width*2+1
        m = self.height*2*n
        if loop[1] == 0:  #(0, 0)
            loop[n] = 0
        if loop[n] == 0:
            loop[1] = 0
        if loop[n-2] == 0:  #(0, n-1)
            loop[n*2-1] = 0
        if loop[n*2-1] == 0:
            loop[n-2] = 0
        if loop[m+1] == 0:  #(m, 0)
            loop[m-n] = 0
        if loop[m-n] == 0:
            loop[m+1] = 0
        if loop[m+n-2] == 0:  #(m, n-1)
            loop[m-1] = 0
        if loop[m-1] == 0:
            loop[m+n-2] = 0
        for y in range(2, n-1, 2):  #(0,1)-(0,n-2)
            if [loop[y+n], loop[y-1], loop[y+1]].count(0) == 2:
                if loop[y+n] == None:
                    loop[y+n] = 0
                if loop[y-1] == None:
                    loop[y-1] = 0
                if loop[y+1] == None:
                    loop[y+1] = 0
        for y in range(2, n-1, 2):  #(m,1)-(m,n-2)
            if [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(0) == 2:
                if loop[m+y-n] == None:
                    loop[m+y-n] = 0
                if loop[m+y-1] == None:
                    loop[m+y-1] = 0
                if loop[m+y+1] == None:
                    loop[m+y+1] = 0
        for x in range(2*n, m, 2*n):  #(n,0)-(m-1,0)
            if [loop[x+1], loop[x+n], loop[x-n]].count(0) == 2:
                if loop[x+1] == None:
                    loop[x+1] = 0
                if loop[x+n] == None:
                    loop[x+n] = 0
                if loop[x-n] == None:
                    loop[x-n] = 0
        for x in range(2*n, m, 2*n):  #(n,n-1)-(m-1,n-1)
            if [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(0) == 2:
                if loop[x+n-2] == None:
                    loop[x+n-2] = 0
                if loop[x-1] == None:
                    loop[x-1] = 0
                if loop[x+2*n-1] == None:
                    loop[x+2*n-1] = 0
        for x in range(2*n, m, 2*n):  #(n,1)-(m-1,n-2)
            for y in range(2, n-1, 2):
                a = x + y
                if [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(0) == 3:
                    if loop[a-n] == None:
                        loop[a-n] = 0
                    if loop[a+n] == None:
                        loop[a+n] = 0
                    if loop[a-1] == None:
                        loop[a-1] = 0
                    if loop[a+1] == None:
                        loop[a+1] = 0
    def _no_branches(self, loop):
        """没有分叉"""
        n = self.width*2+1
        m = self.height*2*n
        for y in range(2, n-1, 2):  #(0,1)-(0,n-2)
            if [loop[y+n], loop[y-1], loop[y+1]].count(1) == 2:
                if loop[y+n] == None:
                    loop[y+n] = 0
                if loop[y-1] == None:
                    loop[y-1] = 0
                if loop[y+1] == None:
                    loop[y+1] = 0
        for y in range(2, n-1, 2):  #(m,1)-(m,n-2)
            if [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(1) == 2:
                if loop[m+y-n] == None:
                    loop[m+y-n] = 0
                if loop[m+y-1] == None:
                    loop[m+y-1] = 0
                if loop[m+y+1] == None:
                    loop[m+y+1] = 0
        for x in range(2*n, m, 2*n):  #(n,0)-(m-1,0)
            if [loop[x+1], loop[x+n], loop[x-n]].count(1) == 2:
                if loop[x+1] == None:
                    loop[x+1] = 0
                if loop[x+n] == None:
                    loop[x+n] = 0
                if loop[x-n] == None:
                    loop[x-n] = 0
        for x in range(2*n, m, 2*n):  #(n,n-1)-(m-1,n-1)
            if [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(1) == 2:
                if loop[x+n-2] == None:
                    loop[x+n-2] = 0
                if loop[x-1] == None:
                    loop[x-1] = 0
                if loop[x+2*n-1] == None:
                    loop[x+2*n-1] = 0
        for x in range(2*n, m, 2*n):  #(n,1)-(m-1,n-2)
            for y in range(2, n-1, 2):
                a = x + y
                if [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(1) == 2:
                    if loop[a-n] == None:
                        loop[a-n] = 0
                    if loop[a+n] == None:
                        loop[a+n] = 0
                    if loop[a-1] == None:
                        loop[a-1] = 0
                    if loop[a+1] == None:
                        loop[a+1] = 0
    def _no_end(self, loop):
        """没有独立端点"""
        n = self.width*2+1
        m = self.height*2*n
        if loop[1] == 1 and loop[n] == None:  #(0, 0)
            loop[n] = 1
        if loop[n] == 1 and loop[1] == None:
            loop[1] = 1
        if loop[n-2] == 1 and loop[n*2-1] == None:  #(0, n-1)
            loop[n*2-1] = 1
        if loop[n*2-1] == 1 and loop[n-2] == None:
            loop[n-2] = 1
        if loop[m+1] == 1 and loop[m-n] == None:  #(m, 0)
            loop[m-n] = 1
        if loop[m-n] == 1 and loop[m+1] == None:
            loop[m+1] = 1
        if loop[m+n-2] == 1 and loop[m-1] == None:  #(m, n-1)
            loop[m-1] = 1
        if loop[m-1] == 1 and loop[m+n-2] == None:
            loop[m+n-2] = 1
        for y in range(2, n-1, 2):  #(0,1)-(0,n-2)
            if [loop[y+n], loop[y-1], loop[y+1]].count(0) == 1 and [loop[y+n], loop[y-1], loop[y+1]].count(1) == 1:
                if loop[y+n] == None:
                    loop[y+n] = 1
                if loop[y-1] == None:
                    loop[y-1] = 1
                if loop[y+1] == None:
                    loop[y+1] = 1
        for y in range(2, n-1, 2):  #(m,1)-(m,n-2)
            if [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(0) == 1 and [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(1) == 1:
                if loop[m+y-n] == None:
                    loop[m+y-n] = 1
                if loop[m+y-1] == None:
                    loop[m+y-1] = 1
                if loop[m+y+1] == None:
                    loop[m+y+1] = 1
        for x in range(2*n, m, 2*n):  #(n,0)-(m-1,0)
            if [loop[x+1], loop[x+n], loop[x-n]].count(0) == 1 and [loop[x+1], loop[x+n], loop[x-n]].count(1) == 1:
                if loop[x+1] == None:
                    loop[x+1] = 1
                if loop[x+n] == None:
                    loop[x+n] = 1
                if loop[x-n] == None:
                    loop[x-n] = 1
        for x in range(2*n, m, 2*n):  #(n,n-1)-(m-1,n-1)
            if [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(0) == 1 and [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(1) == 1:
                if loop[x+n-2] == None:
                    loop[x+n-2] = 1
                if loop[x-1] == None:
                    loop[x-1] = 1
                if loop[x+2*n-1] == None:
                    loop[x+2*n-1] = 1
        for x in range(2*n, m, 2*n):  #(n,1)-(m-1,n-2)
            for y in range(2, n-1, 2):
                a = x + y
                if [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(0) == 2 and [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(1) == 1:
                    if loop[a-n] == None:
                        loop[a-n] = 1
                    if loop[a+n] == None:
                        loop[a+n] = 1
                    if loop[a-1] == None:
                        loop[a-1] = 1
                    if loop[a+1] == None:
                        loop[a+1] = 1
    def _search_end(self, loop, pos):
        """给定线段，寻找所连折线的末端以及有没有连成环
        pos：整数，表示要找的位置

        返回
        长度，末端，是否环
        """
        if pos % 2 != 1:  # 不是连线
            raise ValueError("invalid value pos {} for loop".format(pos))
        if loop[pos] == None or loop[pos] == 0:  # 相应位置没有连线
            raise ValueError("invalid value pos {} for loop".format(pos))
        n = self.width*2+1
        m = self.height*2*n
        loop[pos] = 2  # 标记初始线段
        length = 1
        if (pos % n) % 2 == 1:
            dot_pos = pos - 1
            dot_pos_y = dot_pos % n
            dot_pos_x = dot_pos - dot_pos_y
            while 1:
                if dot_pos_x != 0:
                    if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                        length += 1
                        loop[dot_pos-n] = 2
                        dot_pos = dot_pos - 2 * n
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_x != m:
                    if loop[dot_pos+n] == 1:
                        length += 1
                        loop[dot_pos+n] = 2
                        dot_pos = dot_pos + 2 * n
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_y != 0:
                    if loop[dot_pos-1] == 1:
                        length += 1
                        loop[dot_pos-1] = 2
                        dot_pos = dot_pos - 2
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_y != n-1:
                    if loop[dot_pos+1] == 1:
                        length += 1
                        loop[dot_pos+1] = 2
                        dot_pos = dot_pos + 2
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos == pos + 1:
                    return 1
                end_pos1 = dot_pos
                break
            dot_pos = pos + 1
            dot_pos_y = dot_pos % n
            dot_pos_x = dot_pos - dot_pos_y
            while 1:
                if dot_pos_x != 0:
                    if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                        length += 1
                        loop[dot_pos-n] = 2
                        dot_pos = dot_pos - 2 * n
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_x != m:
                    if loop[dot_pos+n] == 1:
                        length += 1
                        loop[dot_pos+n] = 2
                        dot_pos = dot_pos + 2 * n
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_y != 0:
                    if loop[dot_pos-1] == 1:
                        length += 1
                        loop[dot_pos-1] = 2
                        dot_pos = dot_pos - 2
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_y != n-1:
                    if loop[dot_pos+1] == 1:
                        length += 1
                        loop[dot_pos+1] = 2
                        dot_pos = dot_pos + 2
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos == pos - 1:
                    return 1
                end_pos2 = dot_pos
                break
        else:
            dot_pos = pos - n
            dot_pos_y = dot_pos % n
            dot_pos_x = dot_pos - dot_pos_y
            while 1:
                if dot_pos_x != 0:
                    if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                        length += 1
                        loop[dot_pos-n] = 2
                        dot_pos = dot_pos - 2 * n
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_x != m:
                    if loop[dot_pos+n] == 1:
                        length += 1
                        loop[dot_pos+n] = 2
                        dot_pos = dot_pos + 2 * n
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_y != 0:
                    if loop[dot_pos-1] == 1:
                        length += 1
                        loop[dot_pos-1] = 2
                        dot_pos = dot_pos - 2
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_y != n-1:
                    if loop[dot_pos+1] == 1:
                        length += 1
                        loop[dot_pos+1] = 2
                        dot_pos = dot_pos + 2
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos == pos + n:
                    return 1
                end_pos1 = dot_pos
                break
            dot_pos = pos + n
            dot_pos_y = dot_pos % n
            dot_pos_x = dot_pos - dot_pos_y
            while 1:
                if dot_pos_x != 0:
                    if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                        length += 1
                        loop[dot_pos-n] = 2
                        dot_pos = dot_pos - 2 * n
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_x != m:
                    if loop[dot_pos+n] == 1:
                        length += 1
                        loop[dot_pos+n] = 2
                        dot_pos = dot_pos + 2 * n
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_y != 0:
                    if loop[dot_pos-1] == 1:
                        length += 1
                        loop[dot_pos-1] = 2
                        dot_pos = dot_pos - 2
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos_y != n-1:
                    if loop[dot_pos+1] == 1:
                        length += 1
                        loop[dot_pos+1] = 2
                        dot_pos = dot_pos + 2
                        dot_pos_y = dot_pos % n
                        dot_pos_x = dot_pos - dot_pos_y
                        continue
                if dot_pos == pos - n:
                    return 1
                end_pos2 = dot_pos
                break
        return end_pos1, end_pos2, length
    def _no_other_loop(self, loop):
        """不能局部成环"""
        last_step = 1
        new_loop = loop.copy()
        n = self.width*2+1
        m = self.height*2*n
        ends = []
        def search_end(loop, pos):
            """给定线段，寻找所连折线的末端以及有没有连成环
            pos：整数，表示要找的位置

            返回
            长度，末端，是否环
            """
            if pos % 2 != 1:  # 不是连线
                raise ValueError("invalid value pos {} for loop".format(pos))
            if loop[pos] == None or loop[pos] == 0:  # 相应位置没有连线
                raise ValueError("invalid value pos {} for loop".format(pos))
            n = self.width*2+1
            m = self.height*2*n
            loop[pos] = 2  # 标记初始线段
            length = 1
            if (pos % n) % 2 == 1:
                dot_pos = pos - 1
                dot_pos_y = dot_pos % n
                dot_pos_x = dot_pos - dot_pos_y
                while 1:
                    if dot_pos_x != 0:
                        if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                            length += 1
                            loop[dot_pos-n] = 2
                            dot_pos = dot_pos - 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_x != m:
                        if loop[dot_pos+n] == 1:
                            length += 1
                            loop[dot_pos+n] = 2
                            dot_pos = dot_pos + 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != 0:
                        if loop[dot_pos-1] == 1:
                            length += 1
                            loop[dot_pos-1] = 2
                            dot_pos = dot_pos - 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != n-1:
                        if loop[dot_pos+1] == 1:
                            length += 1
                            loop[dot_pos+1] = 2
                            dot_pos = dot_pos + 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos == pos + 1:
                        return 1
                    end_pos1 = dot_pos
                    break
                dot_pos = pos + 1
                dot_pos_y = dot_pos % n
                dot_pos_x = dot_pos - dot_pos_y
                while 1:
                    if dot_pos_x != 0:
                        if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                            length += 1
                            loop[dot_pos-n] = 2
                            dot_pos = dot_pos - 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_x != m:
                        if loop[dot_pos+n] == 1:
                            length += 1
                            loop[dot_pos+n] = 2
                            dot_pos = dot_pos + 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != 0:
                        if loop[dot_pos-1] == 1:
                            length += 1
                            loop[dot_pos-1] = 2
                            dot_pos = dot_pos - 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != n-1:
                        if loop[dot_pos+1] == 1:
                            length += 1
                            loop[dot_pos+1] = 2
                            dot_pos = dot_pos + 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos == pos - 1:
                        return 1
                    end_pos2 = dot_pos
                    break
            else:
                dot_pos = pos - n
                dot_pos_y = dot_pos % n
                dot_pos_x = dot_pos - dot_pos_y
                while 1:
                    if dot_pos_x != 0:
                        if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                            length += 1
                            loop[dot_pos-n] = 2
                            dot_pos = dot_pos - 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_x != m:
                        if loop[dot_pos+n] == 1:
                            length += 1
                            loop[dot_pos+n] = 2
                            dot_pos = dot_pos + 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != 0:
                        if loop[dot_pos-1] == 1:
                            length += 1
                            loop[dot_pos-1] = 2
                            dot_pos = dot_pos - 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != n-1:
                        if loop[dot_pos+1] == 1:
                            length += 1
                            loop[dot_pos+1] = 2
                            dot_pos = dot_pos + 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos == pos + n:
                        return 1
                    end_pos1 = dot_pos
                    break
                dot_pos = pos + n
                dot_pos_y = dot_pos % n
                dot_pos_x = dot_pos - dot_pos_y
                while 1:
                    if dot_pos_x != 0:
                        if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                            length += 1
                            loop[dot_pos-n] = 2
                            dot_pos = dot_pos - 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_x != m:
                        if loop[dot_pos+n] == 1:
                            length += 1
                            loop[dot_pos+n] = 2
                            dot_pos = dot_pos + 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != 0:
                        if loop[dot_pos-1] == 1:
                            length += 1
                            loop[dot_pos-1] = 2
                            dot_pos = dot_pos - 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != n-1:
                        if loop[dot_pos+1] == 1:
                            length += 1
                            loop[dot_pos+1] = 2
                            dot_pos = dot_pos + 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos == pos - n:
                        return 1
                    end_pos2 = dot_pos
                    break
            return end_pos1, end_pos2, length
        for x in range(0, m+n, 2*n):
            for y in range(1, n, 2):
                if new_loop[x+y] == 1:
                    search = search_end(new_loop, x+y)
                    if search != 1:
                        ends.append(search)
        for x in range(n, m, 2*n):
            for y in range(0, n, 2):
                if new_loop[x+y] == 1:
                    search = search_end(new_loop, x+y)
                    if search != 1:
                        ends.append(search)
        if len(ends) == 1:  #
            for x in range(n, m, 2*n):
                for y in range(1, n, 2):
                    a = x + y
                    if loop[a]!= None and loop[a] != 0:
                        if [loop[a-n], loop[a+1], loop[a-1], loop[a+n]].count(1) < loop[a] - 1:  # 防止只有两个端点却有非零数字周围没有线段时错连接
                            last_step = 0
                            break
                if last_step == 0:
                    break
            else:  # 防止最后一步不能被连接
                return None
        for end in ends:
            if end[2] > 1:
                end_pos1, end_pos2 = end[0], end[1]
                if end_pos1 - end_pos2 == 2:
                    if loop[end_pos1-1] == None:
                        loop[end_pos1-1] = 0
                elif end_pos2 - end_pos1 == 2:
                    if loop[end_pos2-1] == None:
                        loop[end_pos2-1] = 0
                elif end_pos1 - end_pos2 == 2*n:
                    if loop[end_pos1-n] == None:
                        loop[end_pos1-n] = 0
                elif end_pos2 - end_pos1 == 2*n:
                    if loop[end_pos2-n] == None:
                        loop[end_pos2-n] = 0
    def _line_next_to_numbers(self, loop, pos):
        n = self.width*2+1
        y = pos % n
        x = pos - y
        m = self.height*n*2
        if x % (2*n) == 0 and y % 2 == 1:  # 水平方向
            if x != 0:
                if loop[pos-n] != None:
                    return True
                if y != 1:
                    if loop[pos-n-2] != None:
                        return True
                if y != n - 2:
                    if loop[pos-n+2] != None:
                        return True
            if x != m:
                if loop[pos+n] != None:
                    return True
                if y != 1:
                    if loop[pos+n-2] != None:
                        return True
                if y != n-2:
                    if loop[pos+n+2] != None:
                        return True  
            return False
        elif x % (2*n) == n and y % 2 == 0:  # 竖直方向
            if y != 0:
                if loop[pos-1] != None:
                    return True
                if x != n:
                    if loop[pos-2*n-1] != None:
                        return True
                if x != m - n:
                    if loop[pos+2*n-1] != None:
                        return True
            if y != n-1:
                if loop[pos+1] != None:
                    return True
                if x != n:
                    if loop[pos-2*n+1] != None:
                        return True
                if x != m - n:
                    if loop[pos+2*n+1] != None:
                        return True
            return False
        else:
            raise ValueError("invalid pos {} for loop".format(pos))
    def _diagonal_32(self, loop):
        """对角相邻的3和2，如果2远离3的两条边不能同时连线，那么这个3远离2的两条边连线，且如果2远离3的其中一条边不能连线，剩下的那一条边连线
        . . . 0 .      . . . 0 .
        . . . 2 .      . . . 2 1
        . . . . .  ->  . . . . .
        . 3 . . .      1 3 . . .
        . . . . .      . 1 . . .
        
        若
        . . . 0 .      . . . 0 .      . . . 0 .
        . . . 2 0      . . 1 2 0      . . 1 2 0
        . . . . .  ->  . . . 1 .  ->  . 0 . 1 .
        . 3 . . .      . 3 . . .      . 3 0 . . 
        . . . . .      . . . . .      . . . . . 则3周围只剩两个位置可以连线，矛盾

        若
        . . . 0 .      . . . 0 .      . . . 0 .
        . . . 2 .      . . . 2 .      . . 0 2 .
        . . . . .  ->  . 1 . . .  ->  . 1 . 0 .
        0 3 . . .      0 3 1 . .      0 3 1 . . 
        . . . . .      . 1 . . .      . 1 . . . 则2周围只剩一个位置可以连线，矛盾
        """
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if loop[x][y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            if 1 <= x+2*i < self.height-1 and 1 <= y+2*j < self.width-1:
                                if loop[x+2*i][y+2*j] == 2:
                                    lines_pos = [(x+2*i, y+3*j), (x+3*i, y+2*j)]
                                    lines = [loop[x[0]][x[1]] for x in lines_pos]
                                    if 0 in lines:
                                        loop[x-i][y], loop[x][y-j] = 1, 1
                                        for pos in lines_pos:
                                            if loop[pos[0]][pos[1]] == None:
                                                loop[pos[0]][pos[1]] = 1
    
    def _diagonal_31(self, loop):
        """对角相邻的3和1，如果3远离1的两条边都已经连线，那么这个1远离3的两条边不能连线
        . . . . .      . . . 0 .
        . . . 1 .      . . . 1 0
        . . . . .  ->  . . . . .
        1 3 . . .      1 3 . . .
        . 1 . . .      . 1 . . .      / . . . 1 .
                                      | . . 0 1 0
        若                            | . 1 . 0 .
        . . . 1 .      . . . 1 .      | 1 3 0 . . 
        . . . 1        . . 0 1 0      | . 1 . . .
        . . . . .  ->  . . . 0 .  -> /
        1 3 . . .      1 3 . . .     \\ 或
        . 1 . . .      . 1 . . .      | . . . 1 .
                                      | . . 0 1 0
                                      | . 0 . 0 .
                                      | 1 3 1 . .
                                     \\ . 1 . . . 3和1之间的点总会有一个端点陷入死胡同无法连线，矛盾
        """  # 如果只用一个反斜杠"\"会出现警告
             # Warning (from warnings module):
             # File "D:\Python\e1.py", line 363
             # """对角相邻的3和1，如果3远离1的两条边都已经连线，那么这个1远离3的两条边不能连线
             # SyntaxWarning: invalid escape sequence '\ '
             # >>> 
             # = RESTART: D:\Python\e1.py
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if loop[x][y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            if 1 <= x+2*i < self.height-1 and 1 <= y+2*j < self.width-1:
                                if loop[x+2*i][y+2*j] == 1 and loop[x-i][y] == 1 and loop[x][y-j] == 1:
                                    loop[x+2*i][y+3*j], loop[x+3*i][y+2*j] = 0, 0

    def _corner_around_1(self,loop):
        """
        1 . 1 . 1      1 . 1 . 1
        . . . 1 .      . . 0 1 .
        1 0 1 . 1  ->  1 0 1 0 1
        . . 0 . .      . . 0 . .
        1 . 1 . 1      1 . 1 . 1
        """
        loop = loop.copy()
        n = self.width * 2 + 1
        m = self.height * 2 * n
        #多次使用这种技巧时四个角重复寻找可能稍慢一点，而且corner_1(self,loop)结合其他技巧足以删数。此处为了效率不讨论四个角。
        #if loop[n+1] == 1:
        #    if loop[3] == 0:
        #        if loop[n+2] == None:
        #            loop[n+2] = 0
        #    if loop[3*n] == 0:
        #        if loop[2*n+1] == None:
        #            loop[2*n+1] = 0
        #if loop[2*n-2] == 1:
        #    if loop[n-4] == 0:
        #        if loop[2*n-3] == None:
        #            loop[2*n-3] = 0
        #    if loop[4*n-1] == 0:
        #        if loop[3*n-2] = None:
        #            loop[3*n-2] = 0
        for y in range(3, n-3, 2):  #(n,3)-(n,n-4)
            if loop[y+n] == 1:
                if loop[y-2] == 0:
                    if loop[y+n-1] == None:
                        loop[y+n-1] = 0
                    if loop[y] == None:
                        loop[y] = 0
                if loop[y+2] == 0:
                    if loop[y+n+1] == None:
                        loop[y+n+1] = 0
                    if loop[y] == None:
                        loop[y] = 0
                if loop[y+2*n-2] == 0 and loop[y+3*n-1] == 0:
                    if loop[y+n-1] == None:
                        loop[y+n-1] = 0
                    if loop[y+2*n] == None:
                        loop[y+2*n] = 0
                if loop[y+2*n+2] == 0 and loop[y+3*n+1] == 0:
                    if loop[y+n+1] == None:
                        loop[y+n+1] = 0
                    if loop[y+2*n] == None:
                        loop[y+2*n] = 0
       for y in range(3, n-3, 2):  #(m-n,3)-(m-n,n-4)
            if loop[y+m-n] == 1:
                if loop[y+m-2] == 0:
                    if loop[y+m-n-1] == None:
                        loop[y+m-n-1] = 0
                    if loop[y+m] == None:
                        loop[y+m] = 0
                if loop[y+m+2] == 0:
                    if loop[y+m-n+1] == None:
                        loop[y+m-n+1] = 0
                    if loop[y+m] == None:
                        loop[y+m] = 0
                if loop[y+m-2*n-2] == 0 and loop[y+m-3*n-1] == 0:
                    if loop[y+m-n-1] == None:
                        loop[y+m-n-1] = 0
                    if loop[y+m-2*n] == None:
                        loop[y+m-2*n] = 0
        for x in range(3*n, m-2*n, 2*n):
            if loop[x+1] == 1:
                if loop[x-2*n] == 0:
                    if loop[x+1-n] == None:
                        loop[x+1-n] = 0
                    if loop[x] == None:
                        loop[x] = 0
                if loop[x+2*n] == 0:
                    if loop[x+1+n] == None:
                        loop[x+1+n] = 0
                    if loop[x] == None:
                        loop[x] = 0
        for x in range(3*n, m-2*n, 2*n):
            if loop[x+n-2] == 1:
                if loop[x-n-1] == 0:
                    if loop[x-2] == None:
                        loop[x-2] = 0
                    if loop[x+n-1] == None:
                        loop[x+n-1] = 0
                if loop[x+3*n-1] == 0:
                    if loop[x+2*n-2] == None:
                        loop[x+2*n-2] = 0
                    if loop[x+n-1] == None:
                        loop[x+n-1] = 0
        for x in range(3*n, m-2*n, 2*n):
            for y in range(3, n-3, 2):
                if loop[x+y] == 1:
                    a = x + y
                    if loop[a-2*n-1] == 0 and loop[a-n-2] == 0:
                        if loop[a-n] == None:
                            loop[a-n] = 0
                        if loop[a-1] == None:
                            loop[a-1] = 0
                    if loop[a-2*n+1] == 0 and loop[a-n+2] == 0:
                        if loop[a-n] == None:
                            loop[a-n] = 0
                        if loop[a+1] == None:
                            loop[a+1] = 0
                    if loop[a+2*n-1] == 0 and loop[a+n-2] == 0:
                        if loop[a+n] == None:
                            loop[a+n] = 0
                        if loop[a-1] == None:
                            loop[a-1] = 0
                    if loop[a+2*n+1] == 0 and loop[a+n+2] == 0:
                        if loop[a+n] == None:
                            loop[a+n] = 0
                        if loop[a+1] == None:
                            loop[a+1] = 0
        return loop
    def corner_around_2(self,loop):
        pass
    def corner_around_3(self,loop):
        pass
    def end_to_1(self,loop):
        """
        1 . 1 . 1      1 . 1 0 1
        . . . 1 .      . . . 1 0
        1 1 1 . 1  ->  1 1 1 . 1
        . . 0 . .      . . 0 . .
        1 . 1 . 1      1 . 1 . 1
        """
        pass
    def last_line_around_num(self, loop):
        """数字x周围只剩x个位置->都连线
        例
        1 0 1      1 0 1
        0 1 0  ->  0 1 0
        1 . 1      1 1 1
        
        1 0 1      1 0 1
        0 2 .  ->  0 2 1
        1 . 1      1 1 1

        1 . 1      1 1 1
        . 3 .  ->  1 3 1
        1 0 1      1 0 1
        """
        new_loop = loop.copy()
        n = self.width*2+1
        for x in range(n, self.height*2*n+n, 2*n):
            for y in range(1, n, 2):
                a = x + y
                if loop[a] != None and loop[a] != 0:  # python 版本：3.12.0  如果还用x作为内层循环的变量，这个x会覆盖掉外层循环变量x的值，在内层循环执行完成之后，外层这一次循环完成之前，x都是内层循环时最后一次循环的循环变量值，是一个元组，不是整数，从而在这里出错。
                    lines = [loop[a-1], loop[a+1], loop[a-n], loop[a+n]]
                    if lines.count(1) + lines.count(None) == loop[a]:
                        if loop[a-1] == None:  # 4个if比for加if稍快一些
                            new_loop[a-1] = 1
                        if loop[a+1] == None:
                            new_loop[a+1] = 1
                        if loop[a-n] == None:
                            new_loop[a-n] = 1
                        if loop[a+n] == None:
                            new_loop[a+n] = 1
        return new_loop
    def eliminate_line_around_num(self, loop):
        """如果一个数字x周围已有x个位置可以连线，那么其余位置都不能连线"""
        new_loop = loop.copy()
        n = self.width*2+1
        for x in range(n, self.height*2*n+n, 2*n):
            for y in range(1, n, 2):
                a = x + y
                if loop[a] != None and loop[a] != 0:
                    if [loop[a-1], loop[a+1], loop[a-n], loop[a+n]].count(1) == loop[a]:
                        if loop[a-1] == None:
                            new_loop[a-1] = 0
                        if loop[a+1] == None:
                            new_loop[a+1] = 0
                        if loop[a-n] == None:
                            new_loop[a-n] = 0
                        if loop[a+n] == None:
                            new_loop[a+n] = 0
        return new_loop
    def eliminate_line_around_dot(self, loop):
        """如果一个没有连线的点只有一个可能位置能连线，则这个位置不能连线"""
        new_loop = loop.copy()
        n = self.width*2+1
        m = self.height*2*n
        if loop[1] == 0:  #(0, 0)
            new_loop[n] = 0
        if loop[n] == 0:
            new_loop[1] = 0
        if loop[n-2] == 0:  #(0, n-1)
            new_loop[n*2-1] = 0
        if loop[n*2-1] == 0:
            new_loop[n-2] = 0
        if loop[m+1] == 0:  #(m, 0)
            new_loop[m-n] = 0
        if loop[m-n] == 0:
            new_loop[m+1] = 0
        if loop[m+n-2] == 0:  #(m, n-1)
            new_loop[m-1] = 0
        if loop[m-1] == 0:
            new_loop[m+n-2] = 0
        for y in range(2, n-1, 2):  #(0,1)-(0,n-2)
            if [loop[y+n], loop[y-1], loop[y+1]].count(0) == 2:
                if loop[y+n] == None:
                    new_loop[y+n] = 0
                if loop[y-1] == None:
                    new_loop[y-1] = 0
                if loop[y+1] == None:
                    new_loop[y+1] = 0
        for y in range(2, n-1, 2):  #(m,1)-(m,n-2)
            if [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(0) == 2:
                if loop[m+y-n] == None:
                    new_loop[m+y-n] = 0
                if loop[m+y-1] == None:
                    new_loop[m+y-1] = 0
                if loop[m+y+1] == None:
                    new_loop[m+y+1] = 0
        for x in range(2*n, m, 2*n):  #(n,0)-(m-1,0)
            if [loop[x+1], loop[x+n], loop[x-n]].count(0) == 2:
                if loop[x+1] == None:
                    new_loop[x+1] = 0
                if loop[x+n] == None:
                    new_loop[x+n] = 0
                if loop[x-n] == None:
                    new_loop[x-n] = 0
        for x in range(2*n, m, 2*n):  #(n,n-1)-(m-1,n-1)
            if [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(0) == 2:
                if loop[x+n-2] == None:
                    new_loop[x+n-2] = 0
                if loop[x-1] == None:
                    new_loop[x-1] = 0
                if loop[x+2*n-1] == None:
                    new_loop[x+2*n-1] = 0
        for x in range(2*n, m, 2*n):  #(n,1)-(m-1,n-2)
            for y in range(2, n-1, 2):
                a = x + y
                if [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(0) == 3:
                    if loop[a-n] == None:
                        new_loop[a-n] = 0
                    if loop[a+n] == None:
                        new_loop[a+n] = 0
                    if loop[a-1] == None:
                        new_loop[a-1] = 0
                    if loop[a+1] == None:
                        new_loop[a+1] = 0
        return new_loop
    def no_branches(self, loop):
        """没有分叉"""
        new_loop = loop.copy()
        n = self.width*2+1
        m = self.height*2*n
        for y in range(2, n-1, 2):  #(0,1)-(0,n-2)
            if [loop[y+n], loop[y-1], loop[y+1]].count(1) == 2:
                if loop[y+n] == None:
                    new_loop[y+n] = 0
                if loop[y-1] == None:
                    new_loop[y-1] = 0
                if loop[y+1] == None:
                    new_loop[y+1] = 0
        for y in range(2, n-1, 2):  #(m,1)-(m,n-2)
            if [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(1) == 2:
                if loop[m+y-n] == None:
                    new_loop[m+y-n] = 0
                if loop[m+y-1] == None:
                    new_loop[m+y-1] = 0
                if loop[m+y+1] == None:
                    new_loop[m+y+1] = 0
        for x in range(2*n, m, 2*n):  #(n,0)-(m-1,0)
            if [loop[x+1], loop[x+n], loop[x-n]].count(1) == 2:
                if loop[x+1] == None:
                    new_loop[x+1] = 0
                if loop[x+n] == None:
                    new_loop[x+n] = 0
                if loop[x-n] == None:
                    new_loop[x-n] = 0
        for x in range(2*n, m, 2*n):  #(n,n-1)-(m-1,n-1)
            if [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(1) == 2:
                if loop[x+n-2] == None:
                    new_loop[x+n-2] = 0
                if loop[x-1] == None:
                    new_loop[x-1] = 0
                if loop[x+2*n-1] == None:
                    new_loop[x+2*n-1] = 0
        for x in range(2*n, m, 2*n):  #(n,1)-(m-1,n-2)
            for y in range(2, n-1, 2):
                a = x + y
                if [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(1) == 2:
                    if loop[a-n] == None:
                        new_loop[a-n] = 0
                    if loop[a+n] == None:
                        new_loop[a+n] = 0
                    if loop[a-1] == None:
                        new_loop[a-1] = 0
                    if loop[a+1] == None:
                        new_loop[a+1] = 0
        return new_loop
    def no_end(self, loop):
        """没有独立端点"""
        new_loop = loop.copy()
        n = self.width*2+1
        m = self.height*2*n
        if loop[1] == 1 and loop[n] == None:  #(0, 0)
            new_loop[n] = 1
        if loop[n] == 1 and loop[1] == None:
            new_loop[1] = 1
        if loop[n-2] == 1 and loop[n*2-1] == None:  #(0, n-1)
            new_loop[n*2-1] = 1
        if loop[n*2-1] == 1 and loop[n-2] == None:
            new_loop[n-2] = 1
        if loop[m+1] == 1 and loop[m-n] == None:  #(m, 0)
            new_loop[m-n] = 1
        if loop[m-n] == 1 and loop[m+1] == None:
            new_loop[m+1] = 1
        if loop[m+n-2] == 1 and loop[m-1] == None:  #(m, n-1)
            new_loop[m-1] = 1
        if loop[m-1] == 1 and loop[m+n-2] == None:
            new_loop[m+n-2] = 1
        for y in range(2, n-1, 2):  #(0,1)-(0,n-2)
            if [loop[y+n], loop[y-1], loop[y+1]].count(0) == 1 and [loop[y+n], loop[y-1], loop[y+1]].count(1) == 1:
                if loop[y+n] == None:
                    new_loop[y+n] = 1
                if loop[y-1] == None:
                    new_loop[y-1] = 1
                if loop[y+1] == None:
                    new_loop[y+1] = 1
        for y in range(2, n-1, 2):  #(m,1)-(m,n-2)
            if [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(0) == 1 and [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(1) == 1:
                if loop[m+y-n] == None:
                    new_loop[m+y-n] = 1
                if loop[m+y-1] == None:
                    new_loop[m+y-1] = 1
                if loop[m+y+1] == None:
                    new_loop[m+y+1] = 1
        for x in range(2*n, m, 2*n):  #(n,0)-(m-1,0)
            if [loop[x+1], loop[x+n], loop[x-n]].count(0) == 1 and [loop[x+1], loop[x+n], loop[x-n]].count(1) == 1:
                if loop[x+1] == None:
                    new_loop[x+1] = 1
                if loop[x+n] == None:
                    new_loop[x+n] = 1
                if loop[x-n] == None:
                    new_loop[x-n] = 1
        for x in range(2*n, m, 2*n):  #(n,n-1)-(m-1,n-1)
            if [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(0) == 1 and [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(1) == 1:
                if loop[x+n-2] == None:
                    new_loop[x+n-2] = 1
                if loop[x-1] == None:
                    new_loop[x-1] = 1
                if loop[x+2*n-1] == None:
                    new_loop[x+2*n-1] = 1
        for x in range(2*n, m, 2*n):  #(n,1)-(m-1,n-2)
            for y in range(2, n-1, 2):
                a = x + y
                if [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(0) == 2 and [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(1) == 1:
                    if loop[a-n] == None:
                        new_loop[a-n] = 1
                    if loop[a+n] == None:
                        new_loop[a+n] = 1
                    if loop[a-1] == None:
                        new_loop[a-1] = 1
                    if loop[a+1] == None:
                        new_loop[a+1] = 1
        return new_loop
    def no_other_loop(self, loop):
        """不能局部成环"""
        last_step = 1
        new_loop = loop.copy()
        newloop = loop.copy()
        n = self.width*2+1
        m = self.height*2*n
        ends = []
        def search_end(loop, pos):
            """给定线段，寻找所连折线的末端以及有没有连成环
            pos：整数，表示要找的位置

            返回
            长度，末端，是否环
            """
            if pos % 2 != 1:  # 不是连线
                raise ValueError("invalid value pos {} for loop".format(pos))
            if loop[pos] == None or loop[pos] == 0:  # 相应位置没有连线
                raise ValueError("invalid value pos {} for loop".format(pos))
            n = self.width*2+1
            m = self.height*2*n
            loop[pos] = 2  # 标记初始线段
            length = 1
            if (pos % n) % 2 == 1:
                dot_pos = pos - 1
                dot_pos_y = dot_pos % n
                dot_pos_x = dot_pos - dot_pos_y
                while 1:
                    if dot_pos_x != 0:
                        if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                            length += 1
                            loop[dot_pos-n] = 2
                            dot_pos = dot_pos - 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_x != m:
                        if loop[dot_pos+n] == 1:
                            length += 1
                            loop[dot_pos+n] = 2
                            dot_pos = dot_pos + 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != 0:
                        if loop[dot_pos-1] == 1:
                            length += 1
                            loop[dot_pos-1] = 2
                            dot_pos = dot_pos - 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != n-1:
                        if loop[dot_pos+1] == 1:
                            length += 1
                            loop[dot_pos+1] = 2
                            dot_pos = dot_pos + 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos == pos + 1:
                        return 1
                    end_pos1 = dot_pos
                    break
                dot_pos = pos + 1
                dot_pos_y = dot_pos % n
                dot_pos_x = dot_pos - dot_pos_y
                while 1:
                    if dot_pos_x != 0:
                        if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                            length += 1
                            loop[dot_pos-n] = 2
                            dot_pos = dot_pos - 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_x != m:
                        if loop[dot_pos+n] == 1:
                            length += 1
                            loop[dot_pos+n] = 2
                            dot_pos = dot_pos + 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != 0:
                        if loop[dot_pos-1] == 1:
                            length += 1
                            loop[dot_pos-1] = 2
                            dot_pos = dot_pos - 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != n-1:
                        if loop[dot_pos+1] == 1:
                            length += 1
                            loop[dot_pos+1] = 2
                            dot_pos = dot_pos + 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos == pos - 1:
                        return 1
                    end_pos2 = dot_pos
                    break
            else:
                dot_pos = pos - n
                dot_pos_y = dot_pos % n
                dot_pos_x = dot_pos - dot_pos_y
                while 1:
                    if dot_pos_x != 0:
                        if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                            length += 1
                            loop[dot_pos-n] = 2
                            dot_pos = dot_pos - 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_x != m:
                        if loop[dot_pos+n] == 1:
                            length += 1
                            loop[dot_pos+n] = 2
                            dot_pos = dot_pos + 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != 0:
                        if loop[dot_pos-1] == 1:
                            length += 1
                            loop[dot_pos-1] = 2
                            dot_pos = dot_pos - 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != n-1:
                        if loop[dot_pos+1] == 1:
                            length += 1
                            loop[dot_pos+1] = 2
                            dot_pos = dot_pos + 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos == pos + n:
                        return 1
                    end_pos1 = dot_pos
                    break
                dot_pos = pos + n
                dot_pos_y = dot_pos % n
                dot_pos_x = dot_pos - dot_pos_y
                while 1:
                    if dot_pos_x != 0:
                        if loop[dot_pos-n] == 1:  # 哪个是1找哪个
                            length += 1
                            loop[dot_pos-n] = 2
                            dot_pos = dot_pos - 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_x != m:
                        if loop[dot_pos+n] == 1:
                            length += 1
                            loop[dot_pos+n] = 2
                            dot_pos = dot_pos + 2 * n
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != 0:
                        if loop[dot_pos-1] == 1:
                            length += 1
                            loop[dot_pos-1] = 2
                            dot_pos = dot_pos - 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos_y != n-1:
                        if loop[dot_pos+1] == 1:
                            length += 1
                            loop[dot_pos+1] = 2
                            dot_pos = dot_pos + 2
                            dot_pos_y = dot_pos % n
                            dot_pos_x = dot_pos - dot_pos_y
                            continue
                    if dot_pos == pos - n:
                        return 1
                    end_pos2 = dot_pos
                    break
            return end_pos1, end_pos2, length
        for x in range(0, m+n, 2*n):
            for y in range(1, n, 2):
                if new_loop[x+y] == 1:
                    search = search_end(new_loop, x+y)
                    if search != 1:
                        ends.append(search)
        for x in range(n, m, 2*n):
            for y in range(0, n, 2):
                if new_loop[x+y] == 1:
                    search = search_end(new_loop, x+y)
                    if search != 1:
                        ends.append(search)
        if len(ends) == 1:  #
            for x in range(n, m, 2*n):
                for y in range(1, n, 2):
                    a = x + y
                    if loop[a]!= None and loop[a] != 0:
                        if [loop[a-n], loop[a+1], loop[a-1], loop[a+n]].count(1) < loop[a] - 1:  # 防止只有两个端点却有非零数字周围没有线段时错连接
                            last_step = 0
                            break
                if last_step == 0:
                    break
            else:  # 防止最后一步不能被连接
                return loop # 现在所有步骤的方法都有返回值 
        for end in ends:
            if end[2] > 1:
                end_pos1, end_pos2 = end[0], end[1]
                if end_pos1 - end_pos2 == 2:
                    if loop[end_pos1-1] == None:
                        newloop[end_pos1-1] = 0
                elif end_pos2 - end_pos1 == 2:
                    if loop[end_pos2-1] == None:
                        newloop[end_pos2-1] = 0
                elif end_pos1 - end_pos2 == 2*n:
                    if loop[end_pos1-n] == None:
                        newloop[end_pos1-n] = 0
                elif end_pos2 - end_pos1 == 2*n:
                    if loop[end_pos2-n] == None:
                        newloop[end_pos2-n] = 0
        return newloop
    def recurse_solve(self, loop):
        """回溯解题，检查题目是否具有唯一解，盘面较大的谜题建议先用其他技巧以免递归次数过多，若多解，为了防止打印用时过长，最多只打印前3个解"""
        def recurse(loop, solution_count, recursion_count, solutions):
            """回溯，每调用一次recursion_count加1"""
            recursion_count += 1
            new_loop = loop.copy()
            n = self.width*2+1
            for x in range(0, self.height*2*n+n, n):
                for y in range(n):
                    if (x+y) % 2 == 1:
                        if new_loop[x+y] == None:
                            new_loop[x+y] = 1
                            if not self.check(new_loop):
                                new_loop[x+y] = 0
                                """
                                if not self.check(new_loop):  # 更慢
                                    return solution_count, recursion_count, solutions
                                    """
                            elif self.check_solution(new_loop):
                                solution_count += 1
                                if solution_count <= 3:
                                    solutions.append(new_loop.copy())
                            else:
                                solution_count, recursion_count, solutions = recurse(new_loop, solution_count, recursion_count, solutions)
                                new_loop[x+y] = 0
            else:
                return solution_count, recursion_count, solutions
        if not self.check_num(loop):
            return '题目出错或无解'
        solution_count = 0
        recursion_count = 0
        solutions = []
        try:
            s = recurse(loop, solution_count, recursion_count, solutions)
            #for solution in s[2][:3]:
            #self.print_loop(solution)
            return s
        except RecursionError:
            return '递归深度达到极限也未能解出'
    def check_num(self, loop):
        """检查数字"""
        n = self.width*2+1
        for x in range(n, self.height*2*n, 2*n):
            for y in range(1, n-1, 2):
                if loop[x+y] not in [None, 0, 1, 2, 3, 4]:
                    return False
        return True
    def check(self, loop):
        """检查是否满足规则"""
        n = self.width*2+1
        for x in range(n, self.height*2*n, 2*n):  # 数字表示周围连线数量
            for y in range(1, n-1, 2):
                if loop[x+y] != None:
                    a = x + y
                    lines = [loop[a+1], loop[a-1], loop[a+n], loop[a-n]]
                    if lines.count(1) > loop[a] or lines.count(0) > 4 - loop[a]:
                        return False
        m = self.height*2*n  # 没有分支，没有死胡同
        if loop[1] == 1 and loop[n] == 0:  #(0, 0)
            return False
        if loop[n] == 1 and loop[1] == 0:
            return False
        if loop[n-2] == 1 and loop[n*2-1] == 0:  #(0, n-1)
            return False
        if loop[n*2-1] == 1 and loop[n-2] == 0:
            return False
        if loop[m+1] == 1 and loop[m-n] == 0:  #(m, 0)
            return False
        if loop[m-n] == 1 and loop[m+1] == 0:
            return False
        if loop[m+n-2] == 1 and loop[m-1] == 0:  #(m, n-1)
            return False
        if loop[m-1] == 1 and loop[m+n-2] == 0:
            return False
        for y in range(2, n-1, 2):  #(0,1)-(0,n-2)
            count_1 = [loop[y+n], loop[y-1], loop[y+1]].count(1)
            if count_1 == 1 and [loop[y+n], loop[y-1], loop[y+1]].count(0) == 2 or count_1 == 3:
                return False
        for y in range(2, n-1, 2):  #(m,1)-(m,n-2)
            count_1 = [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(1)
            if count_1 == 1 and [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(0) == 2 or count_1 == 3:
                return False
        for x in range(2*n, m, 2*n):  #(n,0)-(m-1,0)
            count_1 = [loop[x+1], loop[x+n], loop[x-n]].count(1)
            if count_1 == 1 and [loop[x+1], loop[x+n], loop[x-n]].count(0) == 2 or count_1 == 3:
                return False
        for x in range(2*n, m, 2*n):  #(n,n-1)-(m-1,n-1)
            count_1 = [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(1)
            if count_1 == 1 and [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(0) == 2 or count_1 == 3:
                return False
        for x in range(2*n, m, 2*n):  #(n,1)-(m-1,n-2)
            for y in range(2, n-1, 2):
                a = x + y
                count_1 = [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(1)
                if count_1 == 1 and [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(0) == 3 or count_1 > 2:
                    return False
        check_loops = loop.copy()  # 不能局部成环
        count = 0
        ends = 0
        for x in range(0, m+n, 2*n):
            for y in range(1, n, 2):
                if check_loops[x+y] == 1:
                    search = self._search_end(check_loops, x+y)
                    if search == 1:
                        count += 1
                    else: ends += 1
                if count > 1:
                    return False
        for x in range(n, m, 2*n):
            for y in range(0, n, 2):
                if check_loops[x+y] == 1:
                    search = self._search_end(check_loops, x+y)
                    if search == 1:
                        count += 1
                if count > 1:
                    return False
        if count == 1:
            if ends >= 1:
                return False
            for x in range(n, m, 2*n):
                for y in range(1, n, 2):
                    a = x + y
                    if check_loops[a]!= None and check_loops[a] != 0:
                        if [check_loops[a-n], check_loops[a+1], check_loops[a-1], check_loops[a+n]].count(2) < check_loops[a]:
                            return False
        return True
    def check_solution(self, loop):
        """检查是否得到一个解"""
        n = self.width*2+1
        for x in range(n, self.height*2*n, 2*n):  # 数字表示周围连线数量
            for y in range(1, n-1, 2):
                if loop[x+y] != None:
                    a = x + y
                    lines = [loop[a+1], loop[a-1], loop[a+n], loop[a-n]]
                    if lines.count(1) != loop[a]:
                        return False
        m = self.height*2*n  # 没有分支，没有独立末端
        if loop[1] == 1 and loop[n] == 0:  #(0, 0)
            return False
        if loop[n] == 1 and loop[1] == 0:
            return False
        if loop[n-2] == 1 and loop[n*2-1] == 0:  #(0, n-1)
            return False
        if loop[n*2-1] == 1 and loop[n-2] == 0:
            return False
        if loop[m+1] == 1 and loop[m-n] == 0:  #(m, 0)
            return False
        if loop[m-n] == 1 and loop[m+1] == 0:
            return False
        if loop[m+n-2] == 1 and loop[m-1] == 0:  #(m, n-1)
            return False
        if loop[m-1] == 1 and loop[m+n-2] == 0:
            return False
        for y in range(2, n-1, 2):  #(0,1)-(0,n-2)
            if [loop[y+n], loop[y-1], loop[y+1]].count(1) == 1:
                return False
        for y in range(2, n-1, 2):  #(m,1)-(m,n-2)
            if [loop[m+y-n], loop[m+y-1], loop[m+y+1]].count(1) == 1:
                return False
        for x in range(2*n, m, 2*n):  #(n,0)-(m-1,0)
            if [loop[x+1], loop[x+n], loop[x-n]].count(1) == 1:
                return False
        for x in range(2*n, m, 2*n):  #(n,n-1)-(m-1,n-1)
            if [loop[x+n-2], loop[x-1], loop[x+2*n-1]].count(1) == 1:
                return False
        for x in range(2*n, m, 2*n):  #(n,1)-(m-1,n-2)
            for y in range(2, n-1, 2):
                a = x + y
                count_1 = [loop[a-n], loop[a+n], loop[a-1], loop[a+1]].count(1)
                if count_1 == 1 or count_1 > 2:
                    return False
        check_loops = loop.copy()  # 不能局部成环
        ends = 0
        count = 0
        for x in range(0, m+n, 2*n):
            for y in range(1, n, 2):
                if check_loops[x+y] == 1:
                    search = self._search_end(check_loops, x+y)
                    if search == 1:
                        count += 1
                    else:
                        ends += 1
        for x in range(n, m, 2*n):
            for y in range(0, n, 2):
                if check_loops[x+y] == 1:
                    search = self._search_end(check_loops, x+y)
                    if search == 1:
                        count += 1
                    else:
                        ends += 1
        if count != 1:
            return False
        else:
            if ends >= 1:
                return False
            for x in range(n, m, 2*n):
                for y in range(1, n, 2):
                    a = x + y
                    if check_loops[a]!= None and check_loops[a] != 0:
                        if [check_loops[a-n], check_loops[a+1], check_loops[a-1], check_loops[a+n]].count(2) < check_loops[a]:
                            return False
        return True
    def trial_and_error(self, loop, numbers=True, max_depth=1, deep=0):
        new_loop = loop.copy()
        n = self.width*2+1
        depth = 1  # 先搜索只假设连一条边的情况看是否有解
        while depth <= max_depth:
            #print('depth:{}'.format(depth))
            for x in range(0, self.height*2*n+n, n):
                for y in range(n):
                    if (x+y) % 2 == 1:  # 线的位置
                        if numbers:
                            if not self._line_next_to_numbers(loop, x+y):
                                continue
                        if new_loop[x+y] == None:  # 当心：如果load方法更改，检查此处。
                            new_loop[x+y] = 1
                            newloop = new_loop.copy()
                            newloop2 = newloop.copy()
                            while 1:
                                for technique in self._techniques.values():
                                    technique(newloop2)
                                if not self.check(newloop2):  # 找到会导致矛盾的假设，否定这个假设
                                    #print('depth:{}; if {} == 1 then contradiction'.format(depth, (x//n, y)))
                                    new_loop[x+y] = 0
                                    loop = new_loop
                                    #slither_link.print_loop(loop)
                                    return loop
                                if newloop2 == newloop:
                                    if depth >= 2 and max_depth >= 2:  # 如果没达到最大深度继续找
                                        newloop2 = self.trial_and_error(newloop, numbers=numbers, max_depth=max_depth-1, deep=deep)  # 最大深度减1
                                        if newloop2 == newloop:
                                            break
                                        else:  # 原来的假设还没验证完
                                            newloop = newloop2.copy()
                                    else:
                                        break
                                else:
                                    newloop = newloop2.copy()
                            #if depth >= 2 and max_depth >= 2:
                            #   newloop = self.trial_and_error(newloop, numbers=numbers, max_depth=max_depth-1, deep=deep)
                            new_loop[x+y] = None  # 如果没有找到，放弃这个假设，再找下一个
            depth += 1
        if loop == new_loop:
            #slither_link.print_loop(loop)
            return loop
    def _solve(self, loop):
        self.zeros(loop)
        self.corner3(loop)
        self.corner1(loop)
        self.adjacent3s(loop)
        self.diagonal_3s(loop)
        self.extended_diagonal_3s(loop)
        while 1:
            self.solvable = 1
            new_loop = loop.copy()
            for technique in self._techniques.values():
                technique(new_loop)
            if new_loop == loop:
                if self.check_solution(new_loop):
                    break
                else:
                    self.solvable = 0
                    #print('unsolvable except perhaps trial and error steps')
                    #slither_link.print_loop(loop)
                    new_loop = self.trial_and_error(loop, max_depth=1)
                    if new_loop == loop:
                        return loop
                    else:
                        loop = new_loop.copy()
            else:
                loop = new_loop.copy()
        return loop
    def solve(self):
        loop = self._solve(self.loop)
        self.print_loop(self.loop)

puzzle = "...330.3...."
size = (4,3)

slither_link = Slither_link(size, puzzle)
slither_link.load(size, puzzle)

# 徒手出题
# (4,3), "...330.3...."
# (5,4), '1..1..2..2.2.3.21..2'
# (9,10), '1.22..3..221.12.22..212.1..1.3....13..3.11......2.3..2212.1.2.1..33.212..3.1..313.2...3...'

"""
简陋数回解题器
用一维列表
然后进一步优化

2025/8/26 - 2025/10/26
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
        for x in range(n, self.height*2*n, 2*n):  # 横向
            for y in range(1, n-2, 2):
                if loop[x+y] == 3 and loop[x+y+2] == 3:
                    loop[x+y-1], loop[x+y+1], loop[x+y+3] = 1, 1, 1
                    eliminate_pos = [(x-2*n, y+1), (x+2*n, y+1)]
                    eliminate_pos = [x for x in eliminate_pos if 0 <= x[0] < self.height*2*n and 0 <= x[1] < n]
                    for pos in eliminate_pos:
                        loop[pos[0]+pos[1]] = 0
        for x in range(n, (self.height*2-2)*n, 2*n):  # 纵向
            for y in range(1, n, 2):
                if loop[x+y] == 3 and loop[x+2*n+y] == 3:
                    loop[x-n+y], loop[x+n+y], loop[x+3*n+y] = 1, 1, 1
                    eliminate_pos = [(x+n, y-2), (x+n, y+2)]
                    eliminate_pos = [x for x in eliminate_pos if 0 <= x[0] < self.height*2*n and 0 <= x[1] < n]
                    for pos in eliminate_pos:
                        loop[pos[0]+pos[1]] = 0
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
        for x in range(n, self.height*2*n, 2*n):
            for y in range(1, n-1, 2):
                if loop[x+y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            if 1 <= x+2*i*n < self.height*2*n and 1 <= y+2*j < n-1:
                                if loop[x+2*i*n+y+2*j] == 3:
                                    lines_pos = [(x+2*i*n, y+3*j), (x+3*i*n, y+2*j), (x, y-j), (x-i*n, y)]
                                    for pos in lines_pos:
                                        if loop[pos[0]+pos[1]] == None:
                                            loop[pos[0]+pos[1]] = 1
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
        for x in range(n, self.height*2*n, 2*n):
            for y in range(1, n-1, 2):
                if loop[x+y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            if 1 <= x+2*i*n < self.height*2*n and 1 <= y+2*j < n-1 and loop[x+2*i*n+y+2*j] == 2:
                                search_3 = 4
                                while search_3:
                                    if 1 <= x+search_3*i*n < self.height*2*n and 1 <= y+search_3*j < n-1:
                                        if loop[x+search_3*i*n+y+search_3*j] == 3:
                                            lines_pos = [(x+search_3*i*n, y+(search_3+1)*j), (x+(search_3+1)*i*n, y+search_3*j), (x, y-j), (x-i*n, y)]
                                            for pos in lines_pos:
                                                if loop[pos[0]+pos[1]] == None:
                                                    loop[pos[0]+pos[1]] = 1
                                            search_3 = 0
                                        elif loop[x+search_3*i*n+y+search_3*j] == 2:
                                            search_3 += 2
                                        else:
                                            search_3 = 0
                                    else:
                                        search_3 = 0
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
        pos_y = pos % n
        pos_x = pos - pos_y
        loop = loop.copy()
        loop[pos] = 2  # 标记初始线段
        if pos_x % (2*n) == 0:
            d_pos = [pos-1, pos+1]
        else:
            d_pos = [pos-n, pos+n]
        length = 1
        end_pos = []
        for dot_pos in d_pos:
            start_pos = dot_pos
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
                if dot_pos != start_pos and dot_pos in d_pos:
                    return loop, 1
                end_pos.append(dot_pos)
                break
        return loop, end_pos, length
    def _search_end_2(self, loop, pos):
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
    def _recurse_solve(self, loop):
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
                            if not self._check(new_loop):
                                new_loop[x+y] = 0
                                """
                                if not self.check(new_loop):  # 更慢
                                    return solution_count, recursion_count, solutions
                                    """
                            elif self._check_solution(new_loop):
                                solution_count += 1
                                if solution_count <= 3:
                                    solutions.append(new_loop.copy())
                                new_loop[x+y] = 0  # 注意假设这里连线找到一个解之后还要讨论如果没有线有没有解，否则可能会漏掉一些解。
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
    def _check_num(self, loop):
        """检查数字"""
        n = self.width*2+1
        for x in range(n, self.height*2*n, 2*n):
            for y in range(1, n-1, 2):
                if loop[x+y] not in [None, 0, 1, 2, 3, 4]:
                    return False
        return True
    def _check(self, loop):
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
                    search = self._search_end_2(check_loops, x+y)
                    if search == 1:
                        count += 1
                    else: ends += 1
                if count > 1:
                    return False
        for x in range(n, m, 2*n):
            for y in range(0, n, 2):
                if check_loops[x+y] == 1:
                    search = self._search_end_2(check_loops, x+y)
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
    def _check_solution(self, loop):
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
        count = 0
        for x in range(0, m+n, 2*n):
            for y in range(1, n, 2):
                if check_loops[x+y] == 1:
                    search = self._search_end_2(check_loops, x+y)
                    if search == 1:
                        count += 1
        for x in range(n, m, 2*n):
            for y in range(0, n, 2):
                if check_loops[x+y] == 1:
                    search = self._search_end_2(check_loops, x+y)
                    if search == 1:
                        count += 1
        if count != 1:
            return False
        return True
    def _line_next_to_numbers2(self, loop, pos):
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
    def _trial_and_error(self, loop, numbers=True, max_depth=1, deep=0):
        new_loop = loop.copy()
        n = self.width*2+1
        depth = 1  # 先搜索只假设连一条边的情况看是否有解
        while depth <= max_depth:
            #print('depth:{}'.format(depth))
            for x in range(0, self.height*2*n+n, n):
                for y in range(n):
                    if (x+y) % 2 == 1:  # 线的位置
                        if numbers:
                            if not self._line_next_to_numbers2(loop, x+y):
                                continue
                        if new_loop[x+y] == None:  # 当心：如果load方法更改，检查此处。
                            new_loop[x+y] = 1
                            newloop = new_loop.copy()
                            newloop2 = newloop.copy()
                            while 1:
                                for technique in self._techniques.values():
                                    technique(newloop2)
                                if not self._check(newloop2):  # 找到会导致矛盾的假设，否定这个假设
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
                if loop[x+y] != None and loop[x+y] != 0:
                    lines_pos = [(x, y-1), (x, y+1), (x-n, y), (x+n, y)]  # python 版本：3.12.0  如果还用x作为内层循环的变量，这个x会覆盖掉外层循环变量x的值，在内层循环执行完成之后，外层这一次循环完成之前，x都是内层循环时最后一次循环的循环变量值，是一个元组，不是整数，从而在这里出错。
                    lines = [loop[pos[0]+pos[1]] for pos in lines_pos]
                    if lines.count(1) + lines.count(None) == loop[x+y]:
                        for pos in lines_pos:
                            if loop[pos[0]+pos[1]] == None:
                                new_loop[pos[0]+pos[1]] = 1
        return new_loop
    
    def eliminate_line_around_num(self, loop):
        """如果一个数字x周围已有x个位置可以连线，那么其余位置都不能连线"""
        new_loop = loop.copy()
        n = self.width*2+1
        for x in range(n, self.height*2*n+n, 2*n):
            for y in range(1, n, 2):
                lines_pos = [(x, y-1), (x, y+1), (x-n, y), (x+n, y)]
                lines = [loop[x[0]+x[1]] for x in lines_pos]
                if lines.count(1) == loop[x+y]:
                    for pos in lines_pos:
                        if loop[pos[0]+pos[1]] == None:
                            #self.solvable = 1
                            new_loop[pos[0]+pos[1]] = 0
        return new_loop
    
    def eliminate_line_around_dot(self, loop):
        """如果一个没有连线的点只有一个可能位置能连线，则这个位置不能连线"""
        new_loop = loop.copy()
        n = self.width*2+1
        for x in range(0, self.height*2*n+n, 2*n):
            for y in range(0, n, 2):
                lines_pos = [(x-n, y), (x+n, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height*2*n+n and 0 <= x[1] < n]
                lines = [loop[x[0]+x[1]] for x in lines_pos]
                if lines.count(0) == len(lines) - 1:
                    for pos in lines_pos:
                        if loop[pos[0]+pos[1]] == None:
                            #self.solvable = 1
                            new_loop[pos[0]+pos[1]] = 0
        return new_loop
    
    def no_branches(self, loop):
        """没有分叉"""
        new_loop = loop.copy()
        n = self.width*2+1
        for x in range(0, self.height*2*n+n, 2*n):
            for y in range(0, n, 2):
                lines_pos = [(x-n, y), (x+n, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height*2*n+n and 0 <= x[1] < n]
                lines = [loop[x[0]+x[1]] for x in lines_pos]
                if lines.count(1) == 2:
                    for pos in lines_pos:
                        if loop[pos[0]+pos[1]] == None:
                            #self.solvable = 1
                            new_loop[pos[0]+pos[1]] = 0
        return new_loop
    def no_end(self, loop):
        """没有独立端点"""
        new_loop = loop.copy()
        n = self.width*2+1
        for x in range(0, self.height*2*n+n, 2*n):
            for y in range(0, n, 2):
                lines_pos = [(x-n, y), (x+n, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height*2*n+n and 0 <= x[1] < n]
                lines = [loop[x[0]+x[1]] for x in lines_pos]
                if lines.count(0) == len(lines) - 2 and lines.count(1) == 1:
                    for pos in lines_pos:
                        if loop[pos[0]+pos[1]] == None:
                            #self.solvable = 1
                            new_loop[pos[0]+pos[1]] = 1
        return new_loop
    def eliminate_line_around_dot2(self, loop):
        """如果一个没有连线的点只有一个可能位置能连线，则这个位置不能连线"""
        loop=loop.copy()
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
        return loop
    def no_branches2(self, loop):
        """没有分叉"""
        loop=loop.copy()
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
        return loop
    def no_end2(self, loop):
        """没有独立端点"""
        loop=loop.copy()
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
        return loop
    def search_end(self, loop, pos):
        """给定线段，寻找所连折线的末端以及有没有连成环"""
        loop = loop.copy()
        n = self.width*2+1
        pos_x = pos[0]
        pos_y = pos[1]
        if pos_x % (2*n) == 0 and pos_y % 2 == 0 or pos_x % (2*n) == n and pos_y % 2 == 1:  # 不是连线
            return loop, [], -1
        if loop[pos_x+pos_y] == None or loop[pos_x+pos_y] == 0:  # 相应位置没有连线
            return loop, [], -1
        loop[pos_x+pos_y] = 2  # 标记初始线段
        if pos_x % (2*n) == 0:
            d_pos = [(pos_x, pos_y-1), (pos_x, pos_y+1)]
        else:
            d_pos = [(pos_x-n, pos_y), (pos_x+n, pos_y)]
        length = 1
        end_pos = []
        for dot_pos in d_pos:
            start_pos = dot_pos
            search = 1
            dot_pos_x = dot_pos[0]
            dot_pos_y = dot_pos[1]
            lines_pos = [(dot_pos_x-n, dot_pos_y), (dot_pos_x+n, dot_pos_y), (dot_pos_x, dot_pos_y-1), (dot_pos_x, dot_pos_y+1)]
            lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height*2*n+n and 0 <= x[1] < n]
            while search:
                for line_pos in lines_pos:
                    line_pos_x = line_pos[0]
                    line_pos_y = line_pos[1]
                    if loop[line_pos_x+line_pos_y] == 1:  # 没有分叉，故最多只有一条线段没有被标记
                        loop[line_pos_x+line_pos_y] = 2
                        dot_pos_x = 2 * line_pos_x - dot_pos_x
                        dot_pos_y = 2 * line_pos_y - dot_pos_y
                        lines_pos = [(dot_pos_x-n, dot_pos_y), (dot_pos_x+n, dot_pos_y), (dot_pos_x, dot_pos_y-1), (dot_pos_x, dot_pos_y+1)]
                        lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height*2*n+n and 0 <= x[1] < n]
                        length += 1
                        break
                else:
                    search = 0
            else:  # 已经到达端点
                if start_pos != (dot_pos_x, dot_pos_y) and (dot_pos_x, dot_pos_y) in d_pos:  # 给定的线段属于一个环
                    return loop, 1
                end_pos.append((dot_pos_x, dot_pos_y))
        return loop, end_pos, length
    def no_other_loop(self, loop):
        """不能局部成环"""
        last_step = 1
        new_loop = loop.copy()
        newloop = loop.copy()
        n = self.width*2+1
        ends = []
        for x in range(0, self.height*2*n+n, 2*n):
            for y in range(0, n, 2):
                lines_pos = [(x-n, y), (x, y+1), (x, y-1), (x+n, y)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height*2*n+n and 0 <= x[1] < n]
                for pos in lines_pos:
                    if new_loop[pos[0]+pos[1]] == 1:
                        new_loop[pos[0]+pos[1]] = 2
                        search = self.search_end(new_loop, pos)
                        if search[1] != 1:
                            new_loop, end_pos, length = search  # 寻找折线，只差一步就可以连接成环
                            ends.append([end_pos, length])
        if len(ends) == 1:  #
            for x in range(n, self.height*2*n, 2*n):
                for y in range(1, n, 2):
                    if loop[x+y]!= None and loop[x+y] != 0:
                        lines_pos = [(x, y-1), (x, y+1), (x-n, y), (x+n, y)]
                        lines = [loop[x[0]+x[1]] for x in lines_pos]
                        if lines.count(1) < loop[x+y] - 1:  # 防止只有两个端点却有非零数字周围没有线段时错连接
                            last_step = 0
                            break
                if last_step == 0:
                    break
            else:  # 防止最后一步不能被连接
                return loop # 现在所有步骤的方法都有返回值 
        for end in ends:
            if end[1] > 1:
                end1 = end[0][0]
                end2 = end[0][1]
                if end1[0] == end2[0] and abs(end1[1] - end2[1]) == 2:
                    if loop[end1[0]+(end1[1] + end2[1]) // 2] == None:
                        newloop[end1[0]+(end1[1] + end2[1]) // 2] = 0
                elif end1[1] == end2[1] and abs(end1[0] - end2[0]) == 2*n:
                    if loop[(end1[0] + end2[0]) // 2 + end1[1]] == None:
                        newloop[(end1[0] + end2[0]) // 2+end1[1]] = 0
        return newloop
    def no_other_loop2(self, loop):
        """不能局部成环"""
        last_step = 1
        loop = loop.copy()
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
                return loop # 现在所有步骤的方法都有返回值 
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
        return loop
    def recurse_solve(self, loop):
        """回溯解题，检查题目是否具有唯一解，盘面较大的谜题建议先用其他技巧以免递归次数过多，若多解，为了防止打印用时过长，最多只打印前3个解"""
        def recurse(loop, solution_count, recursion_count, solutions):
            """回溯，每调用一次recursion_count加1"""
            recursion_count += 1  # 5x5的盘面都要好几秒递归几千次,慢
            new_loop = loop.copy()
            n = self.width*2+1
            for x in range(0, self.height*2*n+n, n):
                for y in range(n):
                    if x % (2*n) == 0 and y % 2 == 1 or x % (2*n) == n and y % 2 == 0:
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
                                solutions.append(new_loop.copy())
                                new_loop[x+y] = 0  # 注意假设这里连线找到一个解之后还要讨论如果没有线有没有解，否则可能会漏掉一些解。
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
                    lines_pos = [(x, y-1), (x, y+1), (x-n, y), (x+n, y)]
                    lines = [loop[x[0]+x[1]] for x in lines_pos]
                    if lines.count(1) > loop[x+y] or lines.count(0) > len(lines) - loop[x+y]:
                        return False
        for x in range(0, self.height*2*n+n, 2*n):  # 没有分支，没有死胡同
            for y in range(0, n, 2):
                lines_pos = [(x-n, y), (x+n, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height*2*n+n and 0 <= x[1] < n]
                lines = [loop[x[0]+x[1]] for x in lines_pos]
                if lines.count(0) > len(lines) - 2 and lines.count(1) == 1 or lines.count(1) > 2:
                    return False
        check_loops = loop.copy()  # 不能局部成环
        count = 0
        for x in range(0, self.height*2*n+n, n):
            for y in range(n):
                if x % (2*n) == 0 and y % 2 == 1 or x % (2*n) == n and y % 2 == 0:
                    if check_loops[x+y] == 1:
                        search = self.search_end(check_loops, (x, y))
                        if search[1] == 1:
                            check_loops = search[0]
                            count += 1
                if count >= 2:
                    return False
        return True
    def check2(self, loop):
        """检查是否满足规则"""
        n = self.width*2+1
        for x in range(n, self.height*2*n, 2*n):  # 数字表示周围连线数量
            for y in range(1, n-1, 2):
                if loop[x+y] != None:
                    lines_pos = [(x, y-1), (x, y+1), (x-n, y), (x+n, y)]
                    lines = [loop[x[0]+x[1]] for x in lines_pos]
                    if lines.count(1) > loop[x+y] or lines.count(0) > len(lines) - loop[x+y]:
                        return False
        for x in range(0, self.height*2*n+n, 2*n):  # 没有分支，没有死胡同
            for y in range(0, n, 2):
                lines_pos = [(x-n, y), (x+n, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height*2*n+n and 0 <= x[1] < n]
                lines = [loop[x[0]+x[1]] for x in lines_pos]
                if lines.count(0) > len(lines) - 2 and lines.count(1) == 1 or lines.count(1) > 2:
                    return False
        check_loops = loop.copy()  # 不能局部成环
        count = 0
        ends = 0
        for x in range(0, self.height*2*n+n, n):
            for y in range(n):
                if x % (2*n) == 0 and y % 2 == 1 or x % (2*n) == n and y % 2 == 0:
                    if check_loops[x+y] == 1:
                        search = self.search_end(check_loops, (x, y))
                        if search[1] == 1:
                            check_loops = search[0]
                            count += 1
                        else:
                            ends += 1
                if count >= 2:
                    return False
        if count == 1:
            if ends >= 1:
                return False
            for x in range(n, self.height*2*n, 2*n):
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
                    lines_pos = [(x, y-1), (x, y+1), (x-n, y), (x+n, y)]
                    lines = [loop[x[0]+x[1]] for x in lines_pos]
                    if lines.count(1) != loop[x+y]:
                        return False
        for x in range(0, self.height*2*n+n, 2*n):  # 没有分支，没有独立末端
            for y in range(0, n, 2):
                lines_pos = [(x-n, y), (x+n, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height*2*n+n and 0 <= x[1] < n]
                lines = [loop[x[0]+x[1]] for x in lines_pos]
                if lines.count(1) != 2 and lines.count(1) != 0:
                    return False
        check_loops = loop.copy()  # 不能局部成环
        count = 0
        for x in range(0, self.height*2*n+n, 2*n):
            for y in range(n):
                if x % (2*n) == 0 and y % 2 == 1 or x % (2*n) == n and y % 2 == 0:
                    if check_loops[x+y] == 1:
                        search = self.search_end(check_loops, (x, y))
                        if search[1] == 1:
                            check_loops = search[0]
                            count += 1
        if count != 1:
            return False
        return True
    def _line_next_to_numbers(self, loop, position):
        x = position[0]
        y = position[1]
        n = self.width*2+1
        if x % (2*n) == 0 and y % 2 == 1:  # 水平方向
            number_position = [(x+n, y), (x-n, y), (x+n, y-2), (x-n, y-2), (x+n, y+2), (x+n, y-2)]
            number_position = [pos for pos in number_position if 0 <= pos[0] < self.height*2*n+n and 0 <= pos[1] < n]
            for pos in number_position:
                if loop[pos[0]+pos[1]] in [0, 1, 2, 3, 4]:
                    return True
            else:
                return False
        if x % (2*n) == n and y % 2 == 0:  # 竖直方向
            number_position = [(x, y+1), (x, y-1), (x-2*n, y+1), (x-2*n, y-1), (x+2*n, y+1), (x+2*n, y-1)]
            number_position = [pos for pos in number_position if 0 <= pos[0] < self.height*2*n+n and 0 <= pos[1] < n]
            for pos in number_position:
                if loop[pos[0]+pos[1]] in [0, 1, 2, 3, 4]:  # 当心：如果load方法更改，检查此处。
                    return True
            else:
                return False
    def trial_and_error(self, loop, numbers=True, max_depth=1, deep=0):
        new_loop = loop.copy()
        n = self.width*2+1
        depth = 1  # 先搜索只假设连一条边的情况看是否有解
        while depth <= max_depth:
            print('depth:{}'.format(depth))
            for x in range(0, self.height*2*n+n, n):
                for y in range(n):
                    if x % (2*n) == 0 and y % 2 == 1 or x % (2*n) == n and y % 2 == 0:  # 线的位置
                        if numbers:
                            if not self._line_next_to_numbers(loop, (x, y)):
                                continue
                        if new_loop[x+y] == None:  # 当心：如果load方法更改，检查此处。
                            new_loop[x+y] = 1
                            newloop = new_loop.copy()
                            newloop2 = newloop.copy()
                            while 1:
                                for technique in self._techniques.values():
                                    technique(newloop2)
                                if not self.check2(newloop2):  # 找到会导致矛盾的假设，否定这个假设
                                    print('depth:{}; if {} == 1 then contradiction'.format(depth, (x//n, y)))
                                    new_loop[x+y] = 0
                                    loop = new_loop
                                    slither_link.print_loop(loop)
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
            slither_link.print_loop(loop)
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
                    print('unsolvable except perhaps trial and error steps')
                    slither_link.print_loop(loop)
                    new_loop = self._trial_and_error(loop, max_depth=1)
                    if new_loop == loop:
                        return loop
                    else:
                        loop = new_loop
            else:
                loop = new_loop
        return loop
    def solve(self):
        self.loop = self._solve(self.loop)
        self.print_loop(self.loop)

puzzle = "...330.3...."
size = (4,3)

slither_link = Slither_link(size, puzzle)
slither_link.load(size, puzzle)

# 徒手出题
# (4,3), "...330.3...."
# (5,4), '1..1..2..2.2.3.21..2'
# (9,10), '1.22..3..221.12.22..212.1..1.3....13..3.11......2.3..2212.1.2.1..33.212..3.1..313.2...3...'

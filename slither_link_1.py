import copy

class Slither_link():
    def __init__(self, loop):
        self.loop = loop
        self.score = 0
        self.solvable = 1
        self.technique = []

    def _test_diagonal_3s(self):
        self.load((10, 10), '.3......3.3........3..3....3.....3..3..........................3..3.....3....3..3........3.3......3.')
        self.print_loop(self.loop)
        self.diagonal_3s()
        self.print_loop(self.loop)
        self.load((10, 10), '3........3.3......3....3........3.3....................3........3..........3.....3......3.3........3')
        self.print_loop(self.loop)
        self.diagonal_3s()
        self.print_loop(self.loop)
    
    def _test_diagonal_32(self):
        self.load((5, 5), '.3.3.2...20...02...2.3.3.')
        self.zeros()
        self.print_loop(self.loop)
        self.diagonal_32()
        self.print_loop(self.loop)
        self.load((5, 5), '3...3.202.......202.3...3')
        self.zeros()
        self.print_loop(self.loop)
        self.diagonal_32()
        self.print_loop(self.loop)
        self.load((10, 10), '..3..........2.........0................3...3....0.2.2.2...2.0.0.0..3................3.......02.....')
        self.zeros()
        self.print_loop(self.loop)
        self.diagonal_32()
        self.print_loop(self.loop)
    
    def _test_diagonal_31(self):
        self.load((10, 10), '.310..013.1.0....0.1...101.....1..3....03.......0110.......30...1...1.....03....1.0.1..0.1.310..013.')
        self.zeros()
        self.eliminate_line_around_dot()
        self.last_line_around_num()
        self.no_end()
        self.print_loop(self.loop)
        self.diagonal_31()
        self.print_loop(self.loop)
        self.load((10, 10), '3...310..3.1.1.0..1..............1.1.......230.......111.3.....0....3............1..0.1.1.3..013...3')
        self.zeros()
        self.corner3()
        self.eliminate_line_around_dot()
        self.last_line_around_num()
        self.no_end()
        self.print_loop(self.loop)
        self.diagonal_31()
        self.print_loop(self.loop)
    
    def _test_eliminate_lines_around_1(self):
        self.load((10, 10), '1..101...1..........1...2.....0....0....1.....3.....111..1.1..101....0..111....1..........1..101...1')
        self.zeros()
        self.print_loop(self.loop)
        self.eliminate_lines_around_1()
        self.print_loop(self.loop)
    
    def _test_lines_around_3(self):
        self.load((12, 10), '3..3.3.....3....0.......1..........3...03.....0..1....0.....3.3..........0....3.3...3.3....0.......2..3...3.3..3.30....3')
        self.zeros()
        self.print_loop(self.loop)
        self.lines_around_3()
        self.print_loop(self.loop)
    
    def _test_diagonal_2(self):
        self.load((12, 10), '3..3.3.....3....0.......1..........3...03.....0..1....0.....3.3..........0....3.3...3.3....0.......2..3...3.3..3.30....3')
        self.zeros()
        self.print_loop(self.loop)
        self.diagonal_2()
        self.print_loop(self.loop)
    
    def load(self, size, loop):
        """加载一道数回题目，用.表示没有数字，用01234表示题目中相应的数字，这里的数回题目由于一个数字周围最多连4条线不可能出现其他数字"""
        loop1 = [[None for x in range(2*size[0]+1)] for y in range(2*size[1]+1)]
        if len(loop) > size[0] * size[1]:
            return '题目出错'
        for x in range(len(loop)):
            if loop[x] == '.':
                pass
            elif loop[x] in ['0', '1', '2', '3', '4']:
                loop1[2*(x//size[0])+1][2*(x%size[0])+1] = int(loop[x])
            else:
                return '题目出错'
        self.loop = copy.deepcopy(loop1)
        self.solvable = 1
    
    @property
    def width(self):
        return len(self.loop[0])
    
    @property
    def height(self):
        return len(self.loop)
    
    def zeros(self):
        """0周围没有连线"""
        for x in range(1, self.height, 2):
            for y in range(1, self.width, 2):
                if self.loop[x][y] == 0:
                    self.loop[x-1][y], self.loop[x+1][y], self.loop[x][y-1], self.loop[x][y+1] = 0, 0, 0, 0
    
    def corner3(self):
        """角落3定式"""
        for x in [1, self.height-2]:
            for y in [1, self.width-2]:
                if self.loop[x][y] == 3:
                    lines_pos = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
                    lines_pos = [x for x in lines_pos if not 2 <= x[0] < self.height-2 and not 2 <= x[1] < self.width-2]
                    for pos in lines_pos:
                        if self.loop[pos[0]][pos[1]] == None:
                            self.loop[pos[0]][pos[1]] = 1
    
    def corner1(self):
        """角落1定式"""
        for x in [1, self.height-2]:
            for y in [1, self.width-2]:
                if self.loop[x][y] == 1:
                    lines_pos = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
                    lines_pos = [x for x in lines_pos if not 2 <= x[0] < self.height-2 and not 2 <= x[1] < self.width-2]
                    for pos in lines_pos:
                        if self.loop[pos[0]][pos[1]] == None:
                            self.loop[pos[0]][pos[1]] = 0
    
    def adjacent3s(self):
        """相邻3定式"""
        for x in range(1, self.height, 2):  # 横向
            for y in range(1, self.width-2, 2):
                if self.loop[x][y] == 3 and self.loop[x][y+2] == 3:
                    self.loop[x][y-1], self.loop[x][y+1], self.loop[x][y+3] = 1, 1, 1
                    eliminate_pos = [(x-2, y+1), (x+2, y+1)]
                    eliminate_pos = [x for x in eliminate_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                    for pos in eliminate_pos:
                        self.loop[pos[0]][pos[1]] = 0
        for x in range(1, self.height - 2, 2):  # 纵向
            for y in range(1, self.width, 2):
                if self.loop[x][y] == 3 and self.loop[x+2][y] == 3:
                    self.loop[x-1][y], self.loop[x+1][y], self.loop[x+3][y] = 1, 1, 1
                    eliminate_pos = [(x+1, y-2), (x+1, y+2)]
                    eliminate_pos = [x for x in eliminate_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                    for pos in eliminate_pos:
                        self.loop[pos[0]][pos[1]] = 0
    
    def diagonal_3s(self):
        """对角3定式，对角相邻的两个3，远离另外一个3的两边连线
        . . . . .      . . . 1 .
        . . . 3 .      . . . 3 1
        . . . . .  ->  . . . . .
        . 3 . . .      1 3 . . .
        . . . . .      . 1 . . .
        
        若
        . . . 0 .      . . . 0 .      . . . 0 .
        . . . 3 .      . . 1 3 1      . . 1 3 1
        . . . . .  ->  . . . 1 .  ->  . 0 . 1 .
        . 3 . . .      1 3 . . .      . 3 0 . . 
        . . . . .      . 1 . . .      . . . . .则总有一个3周围只剩两个位置可以连线，矛盾
        """
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            if 1 <= x+2*i < self.height-1 and 1 <= y+2*j < self.width-1:
                                if self.loop[x+2*i][y+2*j] == 3:
                                    lines_pos = [(x+2*i, y+3*j), (x+3*i, y+2*j), (x, y-j), (x-i, y)]
                                    for pos in lines_pos:
                                        if self.loop[pos[0]][pos[1]] == None:
                                            self.loop[pos[0]][pos[1]] = 1
    
    def extended_diagonal_3s(self):
        """扩展版的对角3定式，在一条对角线上的两个3中间间隔任意数量的2，且这些2和3彼此对角相邻，两个3远离另外一个3和中间的2的两边连线
        . . . . . . .      . . . . . 1 .
        . . . . . 3 .      . . . . . 3 1
        . . . . . . .      . . . . . . .
        . . . 2 . . .  ->  . . . 2 . . .
        . . . . . . .      . . . . . . .
        . 3 . . . . .      1 3 . . . . .
        . . . . . . .      . 1 . . . . .

        若
        . . . 0 .      . . . 0 .      . . . 0 .
        . . . 3 .      . . 1 3 1      . . 1 3 1
        . . . . .  ->  . . . 1 .  ->  . 0 . 1 .
        . 3 . . .      1 3 . . .      . 3 0 . . 
        . . . . .      . 1 . . .      . . . . . 则总有一个3周围只剩两个位置可以连线，矛盾

        . . . . . . . . . . .      . . . . . . . . . 1 .
        . . . . . . . . . 3 .      . . . . . . . . . 3 1
        . . . . . . . . . . .      . . . . . . . . . . .
        . . . . . . . 2 . . .      . . . . . . . 2 . . .
        .           . . . . .      .           . . . . .
        .         .   . . . .  ->  .         .   . . . .
        .       .     . . . .      .       .     . . . .
        . . . 2       . . . .      . . . 2       . . . .
        . . . .       . . . .      . . . .       . . . .
        . 3 . .       . . . .      1 3 . .       . . . .
        . . . . . . . . . . .      . 1 . . . . . . . . .

        若
        . . . . . . . . . 0 .      . . . . . . . . . 0 .      . . . . . . . . . 0 .      . . . . . . . . . 0 .               . . . . . . . . . 0 .      . . . . . . . . . 0 .
        . . . . . . . . . 3 .      . . . . . . . . 1 3 1      . . . . . . . . 1 3 1      . . . . . . . . 1 3 1               . . . . . . . . 1 3 1      . . . . . . . . 1 3 1
        . . . . . . . . . . .      . . . . . . . . . 1 .      . . . . . . . 0 . 1 .      . . . . . . . 0 . 1 .               . . . . . . . 0 . 1 .      . . . . . . . . . 1 .
        . . . . . . . 2 . . .      . . . . . . . 2 . . .      . . . . . . . 2 0 . .      . . . . . . 1 2 0 . .               . . . . . . 1 2 0 . .      . . . . . . . 2 . . .
        .           . . . . .      .           . . . . .      .           . . . . .      .           . 1 . . .               .           . 1 . . .      .           . . . . .
        .         .   . . . .  ->  .         .   . . . .  ->  .         .   . . . .  ->  .         .   . . . .  ->  ...  ->  .         .   . . . .  ->  .         .   . . . .
        .       .     . . . .      .       .     . . . .      .       .     . . . .      .       .     . . . .               .       .     . . . .      .       .     . . . .
        . . . 2       . . . .      . . . 2       . . . .      . . . 2       . . . .      . . . 2       . . . .               . . 1 2       . . . .      . . 1 2       . . . .
        . . . .       . . . .      . . . .       . . . .      . . . .       . . . .      . . . .       . . . .               . . . 1       . . . .      . 0 . 1       . . . .
        . 3 . .       . . . .      . 3 . .       . . . .      . 3 . .       . . . .      . 3 . .       . . . .               . 3 . .       . . . .      . 3 0 .       . . . .
        . . . . . . . . . . .      . . . . . . . . . . .      . . . . . . . . . . .      . . . . . . . . . . .               . . . . . . . . . . .      . . . . . . . . . . . 则总有一个3周围只剩两个位置可以连线，矛盾
        """
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            if 1 <= x+2*i < self.height-1 and 1 <= y+2*j < self.width-1 and self.loop[x+2*i][y+2*j] == 2:
                                search_3 = 4
                                while search_3:
                                    if 1 <= x+search_3*i < self.height-1 and 1 <= y+search_3*j < self.width-1:
                                        if self.loop[x+search_3*i][y+search_3*j] == 3:
                                            lines_pos = [(x+search_3*i, y+(search_3+1)*j), (x+(search_3+1)*i, y+search_3*j), (x, y-j), (x-i, y)]
                                            for pos in lines_pos:
                                                if self.loop[pos[0]][pos[1]] == None:
                                                    self.loop[pos[0]][pos[1]] = 1
                                            search_3 = 0
                                        elif self.loop[x+search_3*i][y+search_3*j] == 2:
                                            search_3 += 2
                                        else:
                                            search_3 = 0
                                    else:
                                        search_3 = 0
        
    def last_line_around_num(self):
        """如果一个数字x周围只有x个位置可以连线，那么这些位置都连线"""
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height, 2):
            for y in range(1, self.width, 2):
                if self.loop[x][y] != None and self.loop[x][y] != 0:
                    lines_pos = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]  # python 版本：3.12.0  如果还用x作为内层循环的变量，这个x会覆盖掉外层循环变量x的值，在内层循环执行完成之后，外层这一次循环完成之前，x都是内层循环时最后一次循环的循环变量值，是一个元组，不是整数，从而在这里出错。
                    lines = [self.loop[x[0]][x[1]] for x in lines_pos]
                    if lines.count(1) + lines.count(None) == self.loop[x][y]:
                        for pos in lines_pos:
                            if self.loop[pos[0]][pos[1]] == None:
                                new_loop[pos[0]][pos[1]] = 1
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop
    
    def eliminate_line_around_num(self):
        """如果一个数字x周围已有x个位置可以连线，那么其余位置都不能连线"""
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height, 2):
            for y in range(1, self.width, 2):
                lines_pos = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
                lines = [self.loop[x[0]][x[1]] for x in lines_pos]
                if lines.count(1) == self.loop[x][y]:
                    for pos in lines_pos:
                        if self.loop[pos[0]][pos[1]] == None:
                            new_loop[pos[0]][pos[1]] = 0
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop
    
    def eliminate_line_around_dot(self):
        """如果一个没有连线的点只有一个可能位置能连线，则这个位置不能连线"""
        new_loop = copy.deepcopy(self.loop)
        for x in range(0, self.height, 2):
            for y in range(0, self.width, 2):
                lines_pos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                lines = [self.loop[x[0]][x[1]] for x in lines_pos]
                if lines.count(0) == len(lines) - 1:
                    for pos in lines_pos:
                        if self.loop[pos[0]][pos[1]] == None:
                            new_loop[pos[0]][pos[1]] = 0
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop
    
    def no_branches(self):
        """没有分叉"""
        new_loop = copy.deepcopy(self.loop)
        for x in range(0, self.height, 2):
            for y in range(0, self.width, 2):
                lines_pos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                lines = [self.loop[x[0]][x[1]] for x in lines_pos]
                if lines.count(1) == 2:
                    for pos in lines_pos:
                        if self.loop[pos[0]][pos[1]] == None:
                            new_loop[pos[0]][pos[1]] = 0
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop

    def no_end(self):
        """没有独立端点"""
        new_loop = copy.deepcopy(self.loop)
        for x in range(0, self.height, 2):
            for y in range(0, self.width, 2):
                lines_pos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                lines = [self.loop[x[0]][x[1]] for x in lines_pos]
                if lines.count(0) == len(lines) - 2 and lines.count(1) == 1:
                    for pos in lines_pos:
                        if self.loop[pos[0]][pos[1]] == None:
                            new_loop[pos[0]][pos[1]] = 1
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop    
    
    def search_end(self, loop, pos):
        """给定线段，寻找所连折线的末端以及有没有连成环"""
        loop = copy.deepcopy(loop)
        pos_x = pos[0]
        pos_y = pos[1]
        if pos_x % 2 == 0 and pos_y % 2 == 0 or pos_x % 2 == 1 and pos_y % 2 == 1:  # 不是连线
            return loop, [], -1
        if loop[pos_x][pos_y] == None or loop[pos_x][pos_y] == 0:  # 相应位置没有连线
            return loop, [], -1
        loop[pos_x][pos_y] = 2  # 标记初始线段
        if pos_x % 2 == 0:
            d_pos = [(pos_x, pos_y-1), (pos_x, pos_y+1)]
        else:
            d_pos = [(pos_x-1, pos_y), (pos_x+1, pos_y)]
        length = 1
        end_pos = []
        for dot_pos in d_pos:
            start_pos = dot_pos
            search = 1
            dot_pos_x = dot_pos[0]
            dot_pos_y = dot_pos[1]
            lines_pos = [(dot_pos_x-1, dot_pos_y), (dot_pos_x+1, dot_pos_y), (dot_pos_x, dot_pos_y-1), (dot_pos_x, dot_pos_y+1)]
            lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
            while search:
                for line_pos in lines_pos:
                    line_pos_x = line_pos[0]
                    line_pos_y = line_pos[1]
                    if loop[line_pos_x][line_pos_y] == 1:  # 没有分叉，故最多只有一条线段没有被标记
                        loop[line_pos_x][line_pos_y] = 2
                        dot_pos_x = 2 * line_pos_x - dot_pos_x
                        dot_pos_y = 2 * line_pos_y - dot_pos_y
                        lines_pos = [(dot_pos_x-1, dot_pos_y), (dot_pos_x+1, dot_pos_y), (dot_pos_x, dot_pos_y-1), (dot_pos_x, dot_pos_y+1)]
                        lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                        length += 1
                        break
                else:
                    search = 0
            else:  # 已经到达端点
                if start_pos != (dot_pos_x, dot_pos_y) and (dot_pos_x, dot_pos_y) in d_pos:  # 给定的线段属于一个环
                    return loop, 1
                end_pos.append((dot_pos_x, dot_pos_y))
        return loop, end_pos, length
            
    def no_other_loop(self):
        """不能局部成环"""
        last_step = 1
        new_loop = copy.deepcopy(self.loop)
        newloop = copy.deepcopy(self.loop)
        ends = []
        for x in range(0, self.height, 2):
            for y in range(0, self.width, 2):
                lines_pos = [(x-1, y), (x, y+1), (x, y-1), (x+1, y)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                for pos in lines_pos:
                    if new_loop[pos[0]][pos[1]] == 1:
                        new_loop[pos[0]][pos[1]] = 2
                        search = self.search_end(new_loop, pos)
                        if search[1] != 1:
                            new_loop, end_pos, length = search  # 寻找折线，只差一步就可以连接成环
                            ends.append([end_pos, length])
        if len(ends) == 1:  #
            for x in range(1, self.height, 2):
                for y in range(1, self.width, 2):
                    if self.loop[x][y]!= None and self.loop[x][y] != 0:
                        lines_pos = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
                        lines = [self.loop[x[0]][x[1]] for x in lines_pos]
                        if lines.count(1) < self.loop[x][y] - 1:  # 防止只有两个端点却有非零数字周围没有线段时错连接
                            last_step = 0
                            break
                if last_step == 0:
                    break
            else:  # 防止最后一步不能被连接
                return
        for end in ends:
            if end[1] > 1:
                end1 = end[0][0]
                end2 = end[0][1]
                if end1[0] == end2[0] and abs(end1[1] - end2[1]) == 2:
                    if self.loop[end1[0]][(end1[1] + end2[1]) // 2] == None:
                        newloop[end1[0]][(end1[1] + end2[1]) // 2] = 0
                elif end1[1] == end2[1] and abs(end1[0] - end2[0]) == 2:
                    if self.loop[end1[0]][(end1[1] + end2[1]) // 2] == None:
                        newloop[(end1[0] + end2[0]) // 2][end1[1]] = 0
        if self.loop != newloop:
            self.solvable = 1
            self.loop = newloop
        
    def diagonal_32(self):
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
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            if 1 <= x+2*i < self.height-1 and 1 <= y+2*j < self.width-1:
                                if self.loop[x+2*i][y+2*j] == 2:
                                    lines_pos = [(x+2*i, y+3*j), (x+3*i, y+2*j)]
                                    lines = [self.loop[x[0]][x[1]] for x in lines_pos]
                                    if 0 in lines:
                                        new_loop[x-i][y], new_loop[x][y-j] = 1, 1
                                        for pos in lines_pos:
                                            if self.loop[pos[0]][pos[1]] == None:
                                                new_loop[pos[0]][pos[1]] = 1
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop 
                                 
    def diagonal_31(self):
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
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            if 1 <= x+2*i < self.height-1 and 1 <= y+2*j < self.width-1:
                                if self.loop[x+2*i][y+2*j] == 1 and self.loop[x-i][y] == 1 and self.loop[x][y-j] == 1:
                                    new_loop[x+2*i][y+3*j], new_loop[x+3*i][y+2*j] = 0, 0
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop 
                                
    def eliminate_lines_around_1(self):
        """如果数字1的某个顶点只剩位于这个1的两边可以连线，则这两边不能连线
        . . . . .      . . . . .
        . . . 1 .      . . 0 1 .
        . 0 . . .  ->  . 0 . 0 .
        . . 0 . .      . . 0 . .
        . . . . .      . . . . .
        
        若
        . . . . .      . . . 0 .
        . . 1 1 .      . . 1 1 0
        . 0 . . .  ->  . 0 . 0 .
        . . 0 . .      . . 0 . .     
        . . . . .      . . . . .

        或者
        . . . . .      . . . 0 .
        . . . 1 .      . . 0 1 0
        . 0 . 1 .  ->  . 0 . 1 .
        . . 0 . .      . . 0 . .
        . . . . .      . . . . . 如果这两边有一边连线一定会陷入死胡同
        把数字四个顶点当中每个顶点朝向这个数字的两端叫做这个顶点对这个数字的近端，远离这个数字的两端叫做这个数字对这个顶点的远端
        数字只剩近端可以连线的顶点叫做数字的近端顶点
        那么数字的近端顶点要么两端都连线要么两端都不连线
        1的近端顶点不连线
        编码：202410191434
        """
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 1:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            line_pos = [(x+2*i, y+j), (x+i, y+2*j)]
                            line_pos = [x for x in line_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                            lines = [self.loop[x[0]][x[1]] for x in line_pos]
                            if lines.count(0) == len(lines) and new_loop[x][y+j] != 1 and new_loop[x+i][y] != 1:  # 问题：如果一开始的题目无解，会不会陷入死循环？
                                new_loop[x][y+j], new_loop[x+i][y] = 0, 0
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop 

    def lines_around_3(self):
        """如果数字3的某个顶点只剩位于这个3的两边可以连线，则这两边一定连线
        . . . . .      . . . . .
        . . . 3 .      . . 1 3 .
        . 0 . . .  ->  . 0 . 1 .
        . . 0 . .      . . 0 . .
        . . . . .      . . . . .
        
        若
        . . . . .      . . . 1 .
        . . 0 3 .      . . 0 3 1
        . 0 . . .  ->  . 0 . 1 .
        . . 0 . .      . . 0 . .     
        . . . . .      . . . . .

        或者
        . . . . .      . . . 1 .
        . . . 3 .      . . 1 3 1
        . 0 . 0 .  ->  . 0 . 0 .
        . . 0 . .      . . 0 . .
        . . . . .      . . . . . 如果这两边有一边不连线一定会有一端最后陷入死胡同
        3的近端顶点连线
        """
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            line_pos = [(x+2*i, y+j), (x+i, y+2*j)]
                            line_pos = [x for x in line_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                            lines = [self.loop[x[0]][x[1]] for x in line_pos]
                            if lines.count(0) == len(lines):
                                if self.loop[x][y+j] == None:
                                    new_loop[x][y+j] = 1
                                if self.loop[x+i][y] == None:
                                    new_loop[x+i][y] = 1
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop
    
    def end_to_2(self):
        """如果四边没有线的2有端点连有线，而且2的对侧有一条线不能连接，那么这个端点不能形成对着2的角，而且对侧另外一条线连接
        如果四边没有线的2有端点远端一端连有线另一端不能连线，而且2的对侧有一条线不能连接，那么对侧另外一条线连接
        . . . . . . .      . . . . . . .
        . . . . . . .      . . . . . . .
        . . . 0 . . .      . . . 0 . . .
        . . . 2 . . .  ->  . . . 2 1 . .
        . 1 . . . . .      . 1 . . . . .
        . . . . . . .      . . 0 . . . .
        . . . . . . .      . . . . . . .

        若
        . . . . . . .      . . . . . . .
        . . . . . . .      . . . . . . .
        . . . 0 . . .      . . . 0 . . .
        . . . 2 . . .  ->  . . 0 2 . . .
        . 1 . . . . .      . 1 . 0 . . .
        . . 1 . . . .      . . 1 . . . .
        . . . . . . .      . . . . . . . 2周围只有一条边可以连线，矛盾

        若
        . . . . . . .      . . . . . . .
        . . . . . . .      . . . . . . .
        . . . 0 . . .      . . . 0 . . .
        . . . 2 0 . .  ->  . . 1 2 0 . .
        . 1 . . . . .      . 1 . 1 . . .
        . . . . . . .      . . . . . . .
        . . . . . . .      . . . . . . . 有分叉，矛盾
        """
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 2:
                    if 1 not in [self.loop[x+1][y], self.loop[x-1][y], self.loop[x][y+1], self.loop[x][y-1]]:
                        for i in [-1, 1]:
                            for j in [-1, 1]:
                                find_1_lines_pos = [(x+2*i, y+j), (x+i, y+2*j)]
                                find_1_lines_pos = [x for x in find_1_lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                                find_1 = [self.loop[x[0]][x[1]] for x in find_1_lines_pos]
                                find_0_lines_pos = [(x-i, y), (x, y-j)]  # 这里0的可能位置不可能超出谜题范围
                                find_0 = [self.loop[x[0]][x[1]] for x in find_0_lines_pos]
                                if find_0.count(0) == 1 and find_1.count(1) == 1:
                                    for pos in find_1_lines_pos:
                                        if self.loop[pos[0]][pos[1]] == None:
                                            new_loop[pos[0]][pos[1]] = 0
                                    for pos in find_0_lines_pos:
                                        if self.loop[pos[0]][pos[1]] == None:
                                            new_loop[pos[0]][pos[1]] = 1
        if self.loop != new_loop:
            self.solvable = 1
            self.loop = new_loop
    
    def diagonal_2(self):
        """对角的2的连线也在对角可以传递
        如果四边没有线的2有端点连有线，而且2的对侧的两条线不能都连接，那么这个端点不能形成对着2的角
        . . . . .      . . . . .
        . . . . .      . . 0 . .
        . 1 . . .  ->  . 1 . 0 .
        0 2 1 . .      0 2 1 . .
        . 0 . . .      . 0 . . .

        . . . . . . .      . . . . . . .      . . . . . . .      . . . . . . .
        . . . . . . .      . . . . . . .      . . . . . . .      . . . . 0 . .
        . . . . . . .      . . . . . . .      . . . 1 . . .      . . . 1 . 0 . 
        . . . 2 . . .  ->  . . 0 2 . . .  ->  . . 0 2 1 . .  ->  . . 0 2 1 . .
        . 1 . . . . .      . 1 . 0 . . .      . 1 . 0 . . .      . 1 . 0 . . .
        0 2 1 . . . .      0 2 1 . . . .      0 2 1 . . . .      0 2 1 . . . .
        . 0 . . . . .      . 0 . . . . .      . 0 . . . . .      . 0 . . . . .

        第一种
        . . . . . . .      . . . . . . .
        . . . . . . .      . . . . . . .
        . . . 0 . . .      . . . 0 . . .
        . . . 2 . . .  ->  . . . 2 . . .
        . 1 . . . . .      . 1 . . . . .
        . . . . . . .      . . 0 . . . .
        . . . . . . .      . . . . . . .

        若
        . . . . . . .      . . . . . . .
        . . . . . . .      . . . . . . .
        . . . 0 . . .      . . . 0 . . .
        . . . 2 . . .  ->  . . 0 2 . . .
        . 1 . . . . .      . 1 . 0 . . .
        . . 1 . . . .      . . 1 . . . .
        . . . . . . .      . . . . . . . 2周围只有一条边可以连线，矛盾

        第二种
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
        [diagonal_32的例子]
        由于数字3周围任意两边至少有一条边连线，所以如果3的某顶点近端没有都连线则对侧位置顶点近端都连线：
        . . . 1 .      . . . . .
        . . . 3 1      . . 1 3 .
        . . . . .  或  . . . 1 .
        . . . . .      . . . . .
        . . . . .      . . . . . 有且只有一种情况成立
        实际上已经包含在diagonal_32之中
        第三种
        . . . . . . .      . . . . . . .
        . . . . 1 . .      . . . . 1 . .
        . . . . . . .      . . . . . 0 .
        . . . 2 . . .  ->  . . . 2 . . .
        . 1 . . . . .      . 1 . . . . .
        . . . . . . .      . . 0 . . . .
        . . . . . . .      . . . . . . .

        若
        . . . . . . .      . . . . . . .      . . . . . . .
        . . . . 1 . .      . . . . 1 . .      . . . . 1 . .
        . . . . . . .      . . . . . . .      . . . 1 . . .
        . . . 2 . . .  ->  . . 0 2 . . .  ->  . . 0 2 1 . .
        . 1 . . . . .      . 1 . 0 . . .      . 1 . 0 . . .
        . . 1 . . . .      . . 1 . . . .      . . 1 . . . .
        . . . . . . .      . . . . . . .      . . . . . . . 有分叉，矛盾
        这里只有第一种
        """
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 2:
                    if 1 not in [self.loop[x+1][y], self.loop[x-1][y], self.loop[x][y+1], self.loop[x][y-1]]:
                        for i in [-1, 1]:
                            for j in [-1, 1]:
                                find_1_lines_pos = [(x+2*i, y+j), (x+i, y+2*j)]
                                find_1_lines_pos = [x for x in find_1_lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                                find_1 = [self.loop[x[0]][x[1]] for x in find_1_lines_pos]
                                find_0_lines_pos = [(x-i, y), (x, y-j)]  # 这里0的可能位置不可能超出谜题范围
                                find_0 = [self.loop[x[0]][x[1]] for x in find_0_lines_pos]
                                if find_0.count(0) == 1 and find_1.count(1) == 1:
                                    for pos in find_1_lines_pos:
                                        if self.loop[pos[0]][pos[1]] == None:
                                            new_loop[pos[0]][pos[1]] = 0
        if self.loop != new_loop:
            self.solvable = 1
            self.loop = new_loop
                            
    def end_to_3(self):
        """如果四边没有线的3的一个端点连有线，那么：这个3的对侧端点连线，并且这个端点不能形成对着3的角
        . . . . .      . . . . .
        . . . . .      . . 0 . .
        . 1 . . .  ->  . 1 . . .
        . . . 3 .      . . . 3 1
        . . . . .      . . . 1 .
        
        由于数字3周围任意两边至少有一条边连线，所以如果3的某顶点近端没有都连线则对侧位置顶点近端都连线：
        . . . 1 .      . . . . .
        . . . 3 1      . . 1 3 .
        . . . . .  或  . . . 1 .
        . . . . .      . . . . .
        . . . . .      . . . . . 有且只有一种情况成立

        现考虑3远端连有线的顶点（记作a）和对侧顶点（记作b）:
        . . .  .  .      . . . . .
        . . a3  .  .      . . 0 . .
        . 1 a  a1 .  -> . 1 . . .
        . . a2 3  b1      . . . 3 1
        . . .  b2 b      . . . 1 .
        则要么a的近端[a1, a2]都连线要么b的近端[b1, b2]都连线
        然而a的近端最多连一条线，从而b的近端都连线:
        . . .  .  .
        . . a3  .  .
        . 1 a  a1 .
        . . a2 3  1
        . . .  1  b
        此时由于数字3周围3条线，a1和a2至少连一条线，a1的远端不可能连第二条线，即a3处无线：
        . . .  .  .
        . . 0  .  .
        . 1 a  a1 .
        . . a2 3  1
        . . .  1  b
        """
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 3:
                    if 1 not in [self.loop[x+1][y], self.loop[x-1][y], self.loop[x][y+1], self.loop[x][y-1]]:
                        for i in [-1, 1]:
                            for j in [-1, 1]:
                                find_1_lines_pos = [(x+2*i, y+j), (x+i, y+2*j)]
                                find_1_lines_pos = [x for x in find_1_lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                                find_1 = [self.loop[x[0]][x[1]] for x in find_1_lines_pos]
                                if find_1.count(1) == 1:
                                    if self.loop[x-i][y] == None:
                                        new_loop[x-i][y] = 1
                                    if self.loop[x][y-j] == None:
                                        new_loop[x][y-j] = 1
                                    for pos in find_1_lines_pos:
                                        if self.loop[pos[0]][pos[1]] == None:
                                            new_loop[pos[0]][pos[1]] = 0
        if self.loop != new_loop:
            self.solvable = 1
            self.loop = new_loop
    
    def end_to_1(self):
        """如果四边没有线的1的一个端点连有线且一定经过这个1，则这个1对侧端点的两边不能连线
        . . . . . . .      . . . . . . .
        . . . . . . .      . . . . . . .
        . . . . . . .      . . . 0 . . .
        . . . 1 . . .  ->  . . . 1 0 . .
        . 1 . . . . .      . 1 . . . . .
        . . 0 . . . .      . . 0 . . . .
        . . . . . . .      . . . . . . .

        若
        . . . . . . .      . . . . . . .
        . . . . . . .      . . . . . . .
        . . . 1 . . .      . . . 1 . . .
        . . . 1 . . .  ->  . . 0 1 0 . .
        . 1 . . . . .      . 1 . 0 . . .
        . . 0 . . . .      . . 0 . . . .
        . . . . . . .      . . . . . . . 有一端陷入死胡同，矛盾
        """
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 1:
                    if 1 not in [self.loop[x+1][y], self.loop[x-1][y], self.loop[x][y+1], self.loop[x][y-1]]:
                        for i in [-1, 1]:
                            for j in [-1, 1]:
                                find_1_lines_pos = [(x+2*i, y+j), (x+i, y+2*j)]
                                find_1_lines_pos = [x for x in find_1_lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                                find_1 = [self.loop[x[0]][x[1]] for x in find_1_lines_pos]
                                if find_1.count(1) == 1 and find_1.count(1) + find_1.count(0) == len(find_1):
                                    if new_loop[x-i][y] == None:
                                        new_loop[x-i][y] = 0
                                    if new_loop[x][y-j] == None:
                                        new_loop[x][y-j] = 0
        if self.loop != new_loop:
            self.solvable = 1
            self.loop = new_loop
    
    def lines_leave_2(self):
        """如果数字2的某个顶点近端有且只有一端可以连线，且远端有一端不能连线，那么远端剩下的一端连线
        . . . 0 .      . . . 0 .
        . . . 2 1      . . . 2 1
        . . . . .  ->  . 1 . . .
        . . 0 . .      . . 0 . .
        . . . . .      . . . . .
        
        若
        . . . 0 .      . . . 0 .
        . . . 2 1      . . 1 2 1
        . 0 . . .  ->  . 0 . 1 .
        . . 0 . .      . . 0 . .     
        . . . . .      . . . . . 2周围有3条线，矛盾
        """
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 2:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            d1_lines_pos = [(x+2*i, y+j), (x+i, y+2*j)]
                            d1_lines_pos = [x for x in d1_lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                            d1_lines = [self.loop[x[0]][x[1]] for x in d1_lines_pos]
                            d2_lines_pos = [(x-i, y), (x, y-j)]  # 挨着2的线不可能超出谜题范围
                            d2_lines = [self.loop[x[0]][x[1]] for x in d2_lines_pos]
                            if (len(d1_lines) == 2 and d1_lines.count(0) == 1 or len(d1_lines) == 1 and d1_lines.count(None) == 1) \
                            and d2_lines.count(0) == 1 and d2_lines.count(1) == 1 and self.loop[x][y+j] == None and self.loop[x+i][y] == None:
                                for pos in d1_lines_pos:
                                    if self.loop[pos[0]][pos[1]] == None:
                                        new_loop[pos[0]][pos[1]] = 1
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop
    
    def lines_leave_1(self):
        """如果数字1的某个顶点近端有且只有一端可以连线，且远端有一端不能连线，那么远端剩下的一端连线
        . . . 0 .      . . . 0 .
        . . . 1 0      . . . 1 0
        . . . . .  ->  . 1 . . .
        . . 0 . .      . . 0 . .
        . . . . .      . . . . .

        若
        . . . 0 .      . . . 0 .
        . . . 1 0      . . 1 1 0
        . 0 . . .  ->  . 0 . 1 .
        . . 0 . .      . . 0 . .
        . . . . .      . . . . . 1周围有两条线，矛盾
        """
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 1:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            d1_lines_pos = [(x+2*i, y+j), (x+i, y+2*j)]
                            d1_lines_pos = [x for x in d1_lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                            d1_lines = [self.loop[x[0]][x[1]] for x in d1_lines_pos]
                            d2_lines_pos = [(x-i, y), (x, y-j)]  # 挨着1的线不可能超出谜题范围
                            d2_lines = [self.loop[x[0]][x[1]] for x in d2_lines_pos]
                            if (len(d1_lines) == 2 and d1_lines.count(0) == 1 or len(d1_lines) == 1 and d1_lines.count(None) == 1) \
                            and d2_lines.count(0) == 2 and self.loop[x][y+j] == None and self.loop[x+i][y] == None:
                                for pos in d1_lines_pos:
                                    if self.loop[pos[0]][pos[1]] == None:
                                        new_loop[pos[0]][pos[1]] = 1
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop
    
    def lines_leave_3(self):
        """如果数字3的某个顶点近端有且只有一端可以连线，且远端有一端不能连线，那么远端剩下的一端连线
        . . . 1 .      . . . 1 .
        . . . 3 1      . . . 3 1
        . . . . .  ->  . 1 . . .
        . . 0 . .      . . 0 . .
        . . . . .      . . . . .

        若
        . . . 1 .      . . . 1 .
        . . . 3 1      . . 1 3 1
        . 0 . . .  ->  . 0 . 1 .
        . . 0 . .      . . 0 . .
        . . . . .      . . . . . 局部成环，矛盾
        """
        new_loop = copy.deepcopy(self.loop)
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if self.loop[x][y] == 3:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            d1_lines_pos = [(x+2*i, y+j), (x+i, y+2*j)]
                            d1_lines_pos = [x for x in d1_lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                            d1_lines = [self.loop[x[0]][x[1]] for x in d1_lines_pos]
                            d2_lines_pos = [(x-i, y), (x, y-j)]  # 挨着3的线不可能超出谜题范围
                            d2_lines = [self.loop[x[0]][x[1]] for x in d2_lines_pos]
                            if (len(d1_lines) == 2 and d1_lines.count(0) == 1 or len(d1_lines) == 1 and d1_lines.count(None) == 1) \
                            and d2_lines.count(1) == 2 and self.loop[x][y+j] == None and self.loop[x+i][y] == None:
                                for pos in d1_lines_pos:
                                    if self.loop[pos[0]][pos[1]] == None:
                                        new_loop[pos[0]][pos[1]] = 1
        if new_loop != self.loop:
            self.solvable = 1
            self.loop = new_loop
    """
    def split_num(self):
        \"""对于一个数字2，如果其四边可以分成彼此相对的两组，每组两边相邻且恰好有一条边能连线，那么这种组合可以沿对角线方向传递，直到可以确定连线为止\"""
    def no_other_loop_with_3(self):
        \"""不能局部连接的扩展，现在只差两步局部连成环，且两个缺口之间间隔一个3\"""
    def trial_and_error(self):
        \"""没有办法的办法，猜，然后看有没有矛盾\"""
    """
    def check_num(self, loop):
        """检查数字"""
        for x in range(1, self.height-1, 2):
            for y in range(1, self.width-1, 2):
                if loop[x][y] not in [None, 0, 1, 2, 3, 4]:
                    return False
        return True
    
    def check(self, loop):
        """检查是否满足规则"""
        for x in range(1, self.height-1, 2):  # 数字表示周围连线数量
            for y in range(1, self.width-1, 2):
                if loop[x][y] != None:
                    lines_pos = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
                    lines = [loop[x[0]][x[1]] for x in lines_pos]
                    if lines.count(1) > loop[x][y] or lines.count(0) > len(lines) - loop[x][y]:
                        return False
        for x in range(0, self.height, 2):  # 没有分支，没有死胡同
            for y in range(0, self.width, 2):
                lines_pos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                lines = [loop[x[0]][x[1]] for x in lines_pos]
                if lines.count(0) > len(lines) - 2 and lines.count(1) == 1 or lines.count(1) > 2:
                    return False
        check_loops = copy.deepcopy(loop)  # 不能局部成环
        count = 0
        for x in range(self.height):
            for y in range(self.width):
                if x % 2 == 0 and y % 2 == 1 or x % 2 == 1 and y % 2 == 0:
                    if check_loops[x][y] == 1:
                        search = self.search_end(check_loops, (x, y))
                        if search[1] == 1:
                            check_loops = search[0]
                            count += 1
                if count >= 2:
                    return False
        return True
        
    def check_solution(self, loop):
        """检查是否得到一个解"""
        for x in range(1, self.height-1, 2):  # 数字表示周围连线数量
            for y in range(1, self.width-1, 2):
                if loop[x][y] != None:
                    lines_pos = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
                    lines = [loop[x[0]][x[1]] for x in lines_pos]
                    if lines.count(1) != loop[x][y]:
                        return False
        for x in range(0, self.height, 2):  # 没有分支，没有独立末端
            for y in range(0, self.width, 2):
                lines_pos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                lines_pos = [x for x in lines_pos if 0 <= x[0] < self.height and 0 <= x[1] < self.width]
                lines = [loop[x[0]][x[1]] for x in lines_pos]
                if lines.count(1) != 2 and lines.count(1) != 0:
                    return False
        check_loops = copy.deepcopy(loop)  # 不能局部成环
        count = 0
        for x in range(self.height):
            for y in range(self.width):
                if x % 2 == 0 and y % 2 == 1 or x % 2 == 1 and y % 2 == 0:
                    if check_loops[x][y] == 1:
                        search = self.search_end(check_loops, (x, y))
                        if search[1] == 1:
                            check_loops = search[0]
                            count += 1
        if count != 1:
            return False
        return True
    
    def recurse_solve(self, loop):
        """回溯解题，检查题目是否具有唯一解，盘面较大的谜题建议先用其他技巧以免递归次数过多，若多解，为了防止打印用时过长，最多只打印前3个解"""
        def recurse(loop, solution_count, recursion_count, solutions):
            """回溯，每调用一次recursion_count加1"""
            recursion_count += 1  # 5x5的盘面都要好几秒递归几千次,慢
            new_loop = copy.deepcopy(loop)
            for x in range(self.height):
                for y in range(self.width):
                    if x % 2 == 0 and y % 2 == 1 or x % 2 == 1 and y % 2 == 0:
                        if new_loop[x][y] == None:
                            new_loop[x][y] = 1
                            if not self.check(new_loop):
                                new_loop[x][y] = 0
                                """
                                if not self.check(new_loop):  # 更慢
                                    return solution_count, recursion_count, solutions
                                    """
                            elif self.check_solution(new_loop):
                                solution_count += 1
                                solutions.append(copy.deepcopy(new_loop))
                                new_loop[x][y] = 0  # 注意假设这里连线找到一个解之后还要讨论如果没有线有没有解，否则可能会漏掉一些解。
                            else:
                                solution_count, recursion_count, solutions = recurse(new_loop, solution_count, recursion_count, solutions)
                                new_loop[x][y] = 0
            else:
                return solution_count, recursion_count, solutions
        if not self.check_num(loop):
            return '题目出错或无解'
        solution_count = 0
        recursion_count = 0
        solutions = []
        try:
            s = recurse(loop, solution_count, recursion_count, solutions)
            for solution in s[2][:3]:
                self.print_loop(solution)
            return s
        except RecursionError:
            return '递归深度达到极限也未能解出'
    
        
    def print_loop(self, loop):
        """打印数回谜题"""
        for i, x in enumerate(loop):
            for j, y in enumerate(x):
                if i % 2 == 0 and j % 2 == 0:
                    print(1, end=' ')
                elif i % 2 == 0 and j % 2 == 1 or i % 2 == 1 and j % 2 == 0:
                    if y == 1:
                        print(y, end=' ')
                    elif y == 0:
                        print('x', end=' ')
                    else:
                        print('.', end=' ')
                else:
                    if y == None:
                        print('.', end=' ')
                    else:
                        print(y, end=' ')
            print()
        print()
    
    def solve(self):
        self.zeros()
        self.corner3()
        self.corner1()
        self.adjacent3s()
        self.diagonal_3s()
        self.extended_diagonal_3s()
        while self.solvable:
            self.solvable = 0
            self.lines_around_3()
            self.eliminate_lines_around_1()
            self.last_line_around_num()
            self.eliminate_line_around_num()
            self.eliminate_line_around_dot()
            self.no_branches()
            self.no_end()
            self.diagonal_32()
            self.diagonal_31()
            self.no_other_loop()
            self.end_to_2()
            self.end_to_3()
            self.end_to_1()
            self.lines_leave_2()
            self.lines_leave_1()
            self.lines_leave_3()
        self.print_loop(self.loop)

slither_link = Slither_link(1)
slither_link.load((4,3), "...330.3....")

# 徒手出题
# (4,3), "...330.3...."
# (5,4), '1..1..2..2.2.3.21..2'
# (9,10), '1.22..3..221.12.22..212.1..1.3....13..3.11......2.3..2212.1.2.1..33.212..3.1..313.2...3...'

import sys

class Resolver:
    """
        Class used to resolve the biggest possible square

        Args:
            map_file (str, PathObject): path to the file containg the map

        Attributes:
            map_size (int): the number of lines on the map
            solution (tuple(int, int, int)): tuple containing: size of the biggest square, starting line idx, starting col index
            obstacle (str): char representing an obstacle
            full (str): char representing a full case
            empty (str): char representing an empty case
            map (list(list(bool))): a 2d list containing the map: True for an obstacle, False for an empty case
    """
    def __init__(self, map_file):
        # attrs init
        self.map_size = None
        self.obstacle = None
        self.solution = None
        self.full = None
        self.map = None

        self._parse_map(map_file)

    def _parse_map(self, map_file):
        """Parse map given in map_file and raises an AssertionError if an error is found in the map

        Args:
            map_file ([str, PathObject]): the path of the file containing the map

        Raises:
                AssertionError: raise an error if a problem is found in map format
        """
        with open(map_file) as f:
            *map_size, self.empty, self.obstacle, self.full = f.readline()[:-1]
            self.map_size = int(''.join(map_size))
            self.map = []
            len_line = None
            for line in f:
                # every line must ends with \n
                assert line[-1] == '\n'
                
                # every line must have the same length
                assert len_line is None or len_line == len(line)
                
                len_line = len(line)
                char_set = {self.obstacle, self.empty, self.full}
                
                # we store each line as an array of boolean, True meaning there is an obstacle
                new_line = [el == self.obstacle for el in line[:-1] if el in char_set]
                
                # every char in the map must be one of the file's first line
                assert len(new_line) == len_line - 1
                self.map.append(new_line)
            # every map must be at least 1x1
            assert len(self.map) >= 1 and len(self.map[0]) >= 1

    def get_biggest_square(self, i, j, starting_size):
        """Find the biggest possible square for a point on map

        Args:
            i (int): line index for starting point
            j (int): col index for starting point
            starting_size (int): biggest square size for now

        Returns:
            int: size of the biggest possible square
        """
        size = starting_size
        next_start = 0# to avoid restarting from 0 for each size iteration
        while size + i <= len(self.map) and size + j <= len(self.map[0]):
            # while the square fits on the map
            for c in range(next_start, size):
                # we look for an obstacle on the edges of the square
                if any(e[j + c] for e in self.map[i:i + c + 1]) or any(self.map[i + c][j:j + c + 1]):
                    return c
            next_start = c
            size += 1
        return size - 1

    def _resolve(self):
        """Find the biggest possible square in self.map
            Returns:
                tuple(int, int, int): tuple containing: size of the biggest square, starting line, starting col
        """
        biggest = (0, 0, 0)
        i = 0
        while i + biggest[0] < len(self.map):
            # while there is enough lines to make a bigger square
            j = 0
            line = self.map[i]
            while j + biggest[0] < len(self.map[0]):
                # while there is enough spaces to make a bigger square
                case = line[j]
                if not case:
                    # if no obstacle on the case, we look for the biggest possible square on this map
                    biggest_tmp = self.get_biggest_square(i, j, biggest[0] + 1)
                    if biggest[0] < biggest_tmp:
                        biggest = biggest_tmp, i, j
                j += 1
            i += 1
        return biggest

    def print_solution(self):
        """Print the new map according to self.solution
        """
        big_size, big_i, big_j = self.solution
        # we make a big list in ret containg all lines and print them with str.join
        ret = []
        for i, line in enumerate(self.map):
            new_line = []
            for j, case in enumerate(line):
                if i >= big_i and j >= big_j and i < big_i + big_size and j < big_j + big_size:
                    # if the case is part of the biggest square
                    new_line.append(self.full)
                else:
                    new_line.append(self.obstacle if case else self.empty)
            ret.append(''.join(new_line))
        print('\n'.join(ret))

    def resolve(self):
        """resolve and print found solution if any
        """
        self.solution = self._resolve()
        self.print_solution()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing parameters')
        exit(1)

    for map_file in sys.argv[1:]:    
        try:
            # parse and validate map
            resolver = Resolver(map_file)
            
            # resolve and print solution
            resolver.resolve()
        except FileNotFoundError:
            print('file error', file=sys.stderr)
        except AssertionError:
            print('map error', file=sys.stderr)
        


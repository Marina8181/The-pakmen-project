import math

"""
Реализация алгоритма поиска 

Структуры списка смежности в виде:
{
"идентификатор узла":"f": 0, "g": int, "h": int, "n": [идентификатор узла, идентификатор узла, идентификатор узла ...],
"идентификатор узла": "g": int, "h": int, "n": [идентификатор узла, идентификатор узла, идентификатор узла ...],
...
}

где:
g = стоимость поездки к узлу
h = подход к цели
f = комбинированная стоимость
n = список подключений к другим узлам.
"""
class GridPath:
    def __init__(self, grid, start, target, walls=None):
        # grid - седка двухмерного массива
        self.grid = grid
        self.start = start
        self.target = target
        if walls is None:
            self.walls = ["1"]
        else:
            self.walls = ["1"] + walls

        self.adjacency_list = self.construct_adjacency_list(self.grid, self.target)
        # список смежности для каждой точки, исключая стены

    def construct_adjacency_list(self, grid, target):
        adjacency_list = {}
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] not in self.walls:
                    adjacency_list[str([row, col])] = {
                        "f": 0,
                        "g": 1,
                        "h": self.get_heuristic([row, col], self.target),
                        "n": self.get_adjacent([row, col], self.grid),
                    }
                #словарь для каждой точки стоимости эвристике(приближенная велечина от точки до цели) стожных точках и общей цене

        return adjacency_list

    def get_adjacent(self, point, grid):
        all_neighbours = [
            [point[0], point[1] - 1],  # впереди
            [point[0] + 1, point[1]],  # справа
            [point[0], point[1] + 1],  # сзади
            [point[0] - 1, point[1]],  # слева
        ]

        # удаляет если пределы сетки
        filtered_neighbours = [str([row, col]) for row, col in all_neighbours
                               if row in range(0, len(grid))
                               if col in range(0, len(grid[0]))
                               if grid[row][col] not in self.walls]
        return filtered_neighbours

    def get_heuristic(self, start, end): #рассчет расстояния
        x_distance = abs(start[0] - end[0])
        y_distance = abs(start[1] - end[1])
        return round(math.sqrt(x_distance ** 2 + y_distance ** 2))

    def get_path(self):
        return FindPath(self.adjacency_list, self.start, self.target).get_path()

class FindPath:
    def __init__(self, adjacency_list, start, target):
        self.adjacency_list = adjacency_list

        self.start = str(start)
        self.target = str(target)

        self.current_node = None #Текущий путь
        self.closed_nodes = []
        self.open_nodes = []
        self.path = None #итоговый путь

        self.run()

    def run(self):
        self.open_nodes.append(self.start)

        while len(self.open_nodes) > 0:

            self.current_node = self.open_nodes[0]
            self.open_nodes.remove(self.current_node)
            self.closed_nodes.append(self.current_node)

            if self.current_node == self.target:
                self.construct_path()

            children = self.adjacency_list[self.current_node]["n"]
            for child in children: # Для каждого смежного узла
                if child not in self.closed_nodes:
                    self.adjacency_list[child]["g"] += self.adjacency_list[self.current_node]["g"]
                    self.adjacency_list[child]["f"] = self.adjacency_list[child]["g"] + self.adjacency_list[child]["h"]
                    self.adjacency_list[child]["next_step"] = self.current_node
                    #обновляем значения g f next
                    if child not in self.open_nodes:
                        if self.adjacency_list[child]["g"] > self.adjacency_list[self.current_node]["g"]:
                            self.open_nodes.append(child)
                    #добавляем

    def construct_path(self): #строит путь к стартовой точке
        self.path = []
        current = self.current_node
        while current != self.start:
            self.path.append(eval(current))
            current = self.adjacency_list[current]["next_step"]

        self.path = self.path[::-1] # переворачиваем для итога

    def get_path(self):
        return self.path

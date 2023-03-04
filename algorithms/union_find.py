
class UnionFind:
    """
    Implementacja struktury danych Union-Find.
    """

    def __init__(self, n):
        self.parent = [-1 for i in range(0, n)]
        self.rank = [-1 for i in range(0, n)]

    def makeset(self, x):
        """
        Funkcja o charakterze inicjacyjnym - każdy zbiór jest jednoelementowy.
        """

        self.parent[x] = x
        self.rank[x] = 0

    def find(self, x):
        """
        Szukanie reprezentanta zbioru, w którym znajduje się x.
        """

        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, x, y):
        """
        Łączenie drzew reprezentujących zbiory.
        """

        parent_of_x = self.find(x)
        parent_of_y = self.find(y)

        if parent_of_x == parent_of_y:
            return

        rank_of_x = self.rank[parent_of_x]
        rank_of_y = self.rank[parent_of_y]

        if rank_of_x > rank_of_y:
            self.parent[parent_of_y] = parent_of_x
        else:
            self.parent[parent_of_x] = parent_of_y

            if self.rank[x] == self.rank[y]:
                self.rank[y] += 1

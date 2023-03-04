import heapq


class KruskalPriorityQueue:
    """
    Klasa kolejki priorytetowej, w której są trzymane krawędzie grafu (waga krawędzi jest kluczem). Ta struktura danych
    jest wykorzystywana w algorytmie Kruskala.
    """

    def __init__(self):
        self._data = []

    def is_empty(self):
        """
        Funkcja sprawdzająca, czy kolejka priorytetowa jest pusta.
        """

        return len(self._data) == 0

    def push_edge(self, weight, u, v):
        """
        Funkcja umieszczająca krawędź w kolejce priorytetowej.
        """

        heapq.heappush(self._data, (weight, (u, v)))

    def pop_edge(self):
        """
        Funkcja usuwająca krawędź z kolejki priorytetowej.
        """

        return heapq.heappop(self._data)

    def create_kruskal_priority_queue(self, neighbours_list):
        """
        Funkcja dodająca krawędzie grafu (z listy sąsiedztwa) do kolejki priorytetowej.
        """

        guarding_set = set()

        for i in range(0, len(neighbours_list)):
            guarding_set.add(i)
            for j in range(0, len(neighbours_list[i])):
                second_vertex = neighbours_list[i][j][0]
                edge_weight = neighbours_list[i][j][1]

                if second_vertex in guarding_set:
                    continue

                self.push_edge(edge_weight, i, second_vertex)

    def queue_state_as_string(self):
        """
        Funkcja zwracająca stan kolejki priorytetowej (jej zawartość) jako napis.
        """

        state_string = f''

        for i in range(0, len(self._data)):
            weight, edge = self._data[i]
            u, v = edge

            if i < len(self._data) - 1:
                state_string += f' krawędź: {{{u}, {v}}}, waga: {weight} ;'
            else:
                state_string += f' krawędź: {{{u}, {v}}}, waga: {weight} '

        return state_string

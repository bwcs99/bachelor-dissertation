import heapq


class PrimPriorityQueue:
    """
    Klasa kolejki priorytetowej, w której są trzymane wierzchołki grafu (koszt wierzchołka jest kluczem). Ta struktura
    danych jest wykorzystywana w algorytmie Prima.
    """

    def __init__(self):
        self._data = []

    def is_empty(self):
        """
        Funkcja sprawdzająca, czy kolejka priorytetowa jest pusta.
        """

        return len(self._data) == 0

    def push_vertex(self, vertex_cost, vertex_number):
        """
        Funkcja dodająca wierzchołek do kolejki priorytetowej.
        """

        heapq.heappush(self._data, (vertex_cost, vertex_number))

    def pop_vertex(self):
        """
        Funkcja usuwająca wierzchołek z kolejki priorytetowej.
        """

        return heapq.heappop(self._data)

    def create_new_priority_queue(self, costs_table, in_vertices_set):
        """
        Funkcja dodająca wierzchołki do kolejki priorytetowej na podstawie tablicy kosztów i tego,
        czy dany wierzchołek był już usunięty z kolejki priorytetowej.
        """

        while len(self._data) > 0:
            self.pop_vertex()

        for i in range(0, len(costs_table)):
            if in_vertices_set[i]:
                continue

            self.push_vertex(costs_table[i], i)

    def queue_state_as_string(self):
        """
        Funkcja zwracająca stan kolejki priorytetowej (jej zawartość) jako napis.
        """

        state_string = f' '

        for i in range(0, len(self._data)):
            cost, vertex = self._data[i]

            if i < len(self._data) - 1:
                state_string += f'wierzchołek: {vertex}, koszt: {cost} ; '
            else:
                state_string += f'wierzchołek: {vertex}, koszt: {cost} '

        return state_string

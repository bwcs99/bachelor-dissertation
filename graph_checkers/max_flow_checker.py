from resources import strings
from graph_checkers.checkers_interface import CheckerFormalInterface


class MaxFlowChecker(CheckerFormalInterface):
    """
    Klasa sprawdzająca, czy na danej sieci przepływowej można wykonać algorytm szukania maksymalnego przepływu.
    """

    def __init__(self, graph_neighbour_list, directed_flag):
        self.neighbour_list = graph_neighbour_list
        self.is_graph_directed = directed_flag

        self.error_messages = []

    def check_if_graph_is_empty(self):
        """
        Funkcja sprawdzająca, czy dany graf jest pusty.
        """

        if len(self.neighbour_list) == 0:
            self.error_messages.append(strings.graph_empty_error_message)
            return True
        else:
            return False

    def explore(self, v, visited, undirected_graph):
        visited[v] = 1

        for neighbour_vertex_number in undirected_graph[v]:

            if not visited[neighbour_vertex_number]:
                self.explore(neighbour_vertex_number, visited, undirected_graph)

    def check_graph_connectivity(self):
        """
        Funkcja sprawdzająca, czy dany graf jest spójny.
        """

        visited = [0 for _ in range(0, len(self.neighbour_list))]
        undirected_graph = [[] for _ in range(0, len(self.neighbour_list))]

        for i in range(0, len(self.neighbour_list)):
            for j in range(0, len(self.neighbour_list[i])):
                first_vertex = i
                second_vertex = self.neighbour_list[i][j][0]

                undirected_graph[first_vertex].append(second_vertex)
                undirected_graph[second_vertex].append(first_vertex)

        self.explore(0, visited, undirected_graph)

        check_if_graph_is_connected = set(visited)

        if len(check_if_graph_is_connected) == 1:
            return True
        else:
            self.error_messages.append(strings.graph_has_isolated_components)
            return False

    def check_if_graph_is_directed(self):
        """
        Funkcja sprawdzająca, czy dany graf jest skierowany.
        """

        if not self.is_graph_directed:
            self.error_messages.append(strings.graph_not_directed_error_message)

        return self.is_graph_directed

    def check_if_graph_has_weights(self):
        """
        Funkcja sprawdzająca, czy wszystkie krawędzie w danym grafie mają wagi.
        """

        flag = True

        for i in range(0, len(self.neighbour_list)):
            for j in range(0, len(self.neighbour_list[i])):
                first_vertex = i
                second_vertex = self.neighbour_list[i][j][0]
                edge_weight = self.neighbour_list[i][j][1]

                if edge_weight is None:
                    self.error_messages.append(
                        f'GC> Błąd ! Krawędź {first_vertex}, {second_vertex} nie ma przepustowości.')
                    flag = False
                else:
                    continue

        return flag

    def check_if_weights_are_nonnegative(self):
        """
        Funkcja sprawdzająca, czy wagi wszystkich krawędzi są dodatnie.
        """

        flag = True

        for i in range(0, len(self.neighbour_list)):
            for j in range(0, len(self.neighbour_list[i])):
                first_vertex = i
                second_vertex = self.neighbour_list[i][j][0]
                edge_weight = self.neighbour_list[i][j][1]

                if edge_weight is not None and int(edge_weight) < 0:
                    self.error_messages.append(
                        f'GC> Błąd ! Krawędź {first_vertex}, {second_vertex} ma ujemną przepustowość.')
                    flag = False
                else:
                    continue

        return flag

    def check_if_graph_has_forbidden_edges(self):
        """
        Funkcja sprawdzająca, czy w grafie nie ma dwóch przeciwnie skierowanych krawędzi.
        """

        flag = True

        for i in range(0, len(self.neighbour_list)):
            for j in range(0, len(self.neighbour_list[i])):
                u = i
                v = self.neighbour_list[i][j][0]

                for k in range(0, len(self.neighbour_list[v])):
                    if self.neighbour_list[v][k][0] == u:
                        flag = False
                        self.error_messages.append(f'GC> Błąd ! W grafie nie może być dwóch przeciwnie skierowanych krawędzi: '
                                                   f'({u}, {v}) i ({v}, {u}).')

        return flag

    def find_source_and_target(self):
        """
        Funkcja znajdująca źródło i ujście w danym grafie skierowanym.
        """

        sources = set()
        targets = set()

        for i in range(0, len(self.neighbour_list)):
            if len(self.neighbour_list[i]) == 0:
                targets.add(i)
                break

        reversed_graph = [[] for i in range(0, len(self.neighbour_list))]

        for i in range(0, len(self.neighbour_list)):
            for j in range(0, len(self.neighbour_list[i])):
                first_vertex = i
                second_vertex = self.neighbour_list[i][j][0]

                reversed_graph[second_vertex].append(first_vertex)

        for i in range(0, len(reversed_graph)):
            if len(reversed_graph[i]) == 0:
                sources.add(i)
                break

        if len(sources) == 0:
            self.error_messages.append(strings.no_source_node_error_message)

            if len(targets) == 0:
                self.error_messages.append(strings.no_target_node_error_message)

            return False, None, None

        if len(sources) > 1:
            self.error_messages.append(strings.multi_source_error_message)

            if len(targets) > 1:
                self.error_messages.append(strings.multi_target_error_message)

            return False, None, None

        source = sources.pop()
        target = targets.pop()

        return True, source, target

    def check_all_necessary_conditions(self):
        """
        Funkcja sprawdzająca, czy dany graf spełnia wszystkie konieczne warunki do wykonania na nim algorytmu.
        """

        is_empty_flag = self.check_if_graph_is_empty()

        if is_empty_flag:
            return False, None, None, self.error_messages

        is_directed_flag = self.check_if_graph_is_directed()

        if not is_directed_flag:
            return False, None, None, self.error_messages

        is_connected_flag = self.check_graph_connectivity()

        if not is_connected_flag:
            return False, None, None, self.error_messages

        has_weights_flag = self.check_if_graph_has_weights()

        if not has_weights_flag:
            return False, None, None, self.error_messages

        are_weights_nonnegative_flag = self.check_if_weights_are_nonnegative()

        if not are_weights_nonnegative_flag:
            return False, None, None, self.error_messages

        has_source_and_target_flag, source, target = self.find_source_and_target()

        if not has_source_and_target_flag:
            return False, None, None, self.error_messages

        forbidden_edges_flag = self.check_if_graph_has_forbidden_edges()

        if not forbidden_edges_flag:
            return False, None, None, self.error_messages

        return True, source, target, []



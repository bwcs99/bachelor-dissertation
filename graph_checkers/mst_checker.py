from resources import strings
from graph_checkers.checkers_interface import CheckerFormalInterface


class MSTChecker(CheckerFormalInterface):
    """
    Klasa sprawdzająca, czy na danym grafie można wykonać algorytm szukania minimalnego drzewa rozpinającego.
    """

    def __init__(self, graph_neighbour_list, directed_flag):
        self.neighbour_list = graph_neighbour_list
        self.is_graph_directed = directed_flag

        self.error_messages = []

    def check_if_graph_is_empty(self):
        if len(self.neighbour_list) == 0:
            self.error_messages.append(strings.graph_empty_error_message)
            return True
        else:
            return False

    def explore(self, v, visited):
        visited[v] = 1

        for neighbours in self.neighbour_list[v]:
            u = neighbours[0]

            if not visited[u]:
                self.explore(u, visited)

    def check_graph_connectivity(self):
        n = len(self.neighbour_list)

        visited = [0 for i in range(0, n)]

        self.explore(0, visited)

        check_if_all_vertices_visited = set(visited)

        if len(check_if_all_vertices_visited) == 1:
            return True
        else:
            self.error_messages.append(strings.graph_is_not_connected_message)
            return False

    def check_if_graph_is_directed(self):
        if self.is_graph_directed:
            self.error_messages.append(strings.graph_directed_error_message)

        return not self.is_graph_directed

    def check_if_graph_has_weights(self):
        flag = True

        for i in range(0, len(self.neighbour_list)):
            for j in range(0, len(self.neighbour_list[i])):
                first_vertex = i
                second_vertex = self.neighbour_list[i][j][0]
                edge_weight = self.neighbour_list[i][j][1]

                if edge_weight is None:
                    self.error_messages.append(f'GC> Błąd ! Krawędź {first_vertex}, {second_vertex} nie ma wagi.')
                    flag = False
                else:
                    continue

        return flag

    def check_if_weights_are_nonnegative(self):
        for i in range(0, len(self.neighbour_list)):
            for j in range(0, len(self.neighbour_list[i])):
                edge_weight = self.neighbour_list[i][j][1]

                if edge_weight < 0:
                    self.error_messages.append(strings.graph_has_negative_weights_error_message)
                    return False

        return True

    def check_all_necessary_conditions(self):
        is_empty_flag = self.check_if_graph_is_empty()

        if is_empty_flag:
            return False, self.error_messages

        is_directed_flag = self.check_if_graph_is_directed()

        if not is_directed_flag:
            return False, self.error_messages

        is_connected_flag = self.check_graph_connectivity()

        if not is_connected_flag:
            return False, self.error_messages

        has_weights_flag = self.check_if_graph_has_weights()

        if not has_weights_flag:
            return False, self.error_messages

        doesnt_have_negative_weights = self.check_if_weights_are_nonnegative()

        if not doesnt_have_negative_weights:
            return False, self.error_messages

        return True, []


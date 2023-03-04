from resources import strings
from graph_checkers.checkers_interface import CheckerFormalInterface


class SCCChecker(CheckerFormalInterface):
    """
    Klasa sprawdzająca, czy na danym grafie można wykonać algorytm szukania silnie spójnych składowych.
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

    def check_graph_connectivity(self):
        return

    def check_if_graph_is_directed(self):
        if not self.is_graph_directed:
            self.error_messages.append(strings.graph_not_directed_error_message)

        return self.is_graph_directed

    def check_if_graph_has_weights(self):
        return

    def check_if_weights_are_nonnegative(self):
        return

    def check_all_necessary_conditions(self):
        is_empty_flag = self.check_if_graph_is_empty()
        is_directed_flag = self.check_if_graph_is_directed()

        if is_empty_flag:
            return False, self.error_messages

        if not is_directed_flag:
            return False, self.error_messages

        return True, []

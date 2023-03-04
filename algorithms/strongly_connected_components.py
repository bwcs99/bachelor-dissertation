from resources import strings


class SCCFinder:
    """
    Klasa, w której jest zaimplementowany algorytm szukania silnie spójnych składowych w grafie skierowanym,
    wraz z funkcjami pomocniczymi.
    """

    def __init__(self, neighbours_list, n):
        self.clock = 0
        self.pre = [-1 for _ in range(0, n)]
        self.post = [-1 for _ in range(0, n)]
        self.visited = [False for _ in range(0, n)]
        self.neighbours_list = neighbours_list
        self.component_number = 0
        self.components = [0 for _ in range(0, n)]

    def previsit(self, v):
        """
        Wyznaczanie numeru \"pre\" dla danego wierzchołka.
        """

        self.components[v] = self.component_number
        self.pre[v] = self.clock

        self.clock += 1

    def postvisit(self, v):
        """
        Wyznaczanie numeru \"post\" dla danego wierzchołka.
        """

        self.post[v] = self.clock
        self.clock += 1

    def get_post_data_text_list(self):
        data_text_list = []
        for i in range(0, len(self.post)):
            data_text_list.append(str(self.post[i]))

        return data_text_list

    def get_components_data_text_list(self):
        data_text_list = []
        for i in range(0, len(self.components)):
            data_text_list.append(str(self.components[i]))

        return data_text_list

    def explore(self, neighbours_list, terminal_messages, instructions_list, v, flag=False):
        """
        Funkcja używana przez algorytm DFS - dla danego wierzchołka wyznacza wszystkie wierzchołki z niego osiągalne.
        """

        self.visited[v] = True
        self.previsit(v)

        for edge in neighbours_list[v]:
            u = edge[0]

            if not self.visited[u]:
                terminal_messages.append(strings.scc_dfs_visiting_vertex_neighbour_message + f'{u}, wierzchołka {v}.')

                terminal_messages.append(strings.stop_string)
                instructions_list.append((strings.select_edge_mnemonic, v, u))

                terminal_messages.append(strings.stop_string)
                instructions_list.append((strings.select_vertex_mnemonic, u))

                self.explore(neighbours_list, terminal_messages, instructions_list, u, flag)
            else:
                terminal_messages.append(strings.scc_dfs_not_visiting_vertex_neighbour_message + f'{u} był już '
                                                                                                 f'odwiedzony.')

        self.postvisit(v)

        terminal_messages.append(strings.scc_dfs_post_vertex_message + f'{v} i go opuszczam.')

        data_text_list = self.get_post_data_text_list()

        if not flag:
            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.display_vertices_data_mnemonic, data_text_list))

    def dfs(self, neighbours_list, terminal_messages, instructions_list, flag=False, sorted_vertices=None):
        """
        Funkcja wykonująca algorytm DFS z wyznaczaniem numerów \"pre\" i \"post\".
        """

        if not flag:
            for i in range(0, len(neighbours_list)):
                if not self.visited[i]:
                    terminal_messages.append(strings.scc_dfs_on_reversed_graph_init + f'{i}.')

                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.select_vertex_mnemonic, i))

                    self.component_number += 1
                    self.explore(neighbours_list, terminal_messages, instructions_list, i)

                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.clear_dfs_path_mnemonic,))
        else:
            for vertex in sorted_vertices.keys():
                if not self.visited[vertex]:
                    terminal_messages.append(strings.scc_dfs_on_reversed_graph_init + f'{vertex}.')

                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.select_vertex_mnemonic, vertex))

                    self.component_number += 1
                    self.explore(neighbours_list, terminal_messages, instructions_list, vertex, True)

                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.clear_dfs_path_mnemonic,))

    def find_graph_reversal(self):
        """
        Funkcja konstruująca graf odwrotny.
        """

        number_of_vertices = len(self.neighbours_list)
        reversed_neighbours_list = [[] for i in range(0, number_of_vertices)]

        for i in range(0, len(self.neighbours_list)):
            for j in range(0, len(self.neighbours_list[i])):
                neighbour_number = self.neighbours_list[i][j][0]
                reversed_neighbours_list[neighbour_number].append((i, None))

        return reversed_neighbours_list

    def counting_sort(self, array):
        """
        Funkcja sortująca - algorytm sortowania przez zliczanie.
        """

        k = max(array)

        n = len(array)

        b = [0 for _ in range(0, len(array))]
        c = [0 for _ in range(0, k + 1)]

        for i in range(0, len(array)):
            c[array[i]] += 1

        for i in range(1, len(c)):
            c[i] = c[i] + c[i - 1]

        for i in range(0, len(array)):
            if c[array[i]] > 0:
                c[array[i]] -= 1

                if c[array[i]] >= 0:
                    b[n - c[array[i]] - 1] = array[i]

        return b

    def sort_post_values(self):
        """
        Sortowanie wierzchołków względem wartości ich numeru \"post\" (kolejność malejąca).
        """

        sorted_by_post = self.counting_sort(self.post)
        result = {}

        for i in sorted_by_post:
            for j in range(0, len(self.post)):
                if self.post[j] == i:
                    result[j] = i

        return result

    def find_strongly_connected_components(self):
        """
        Funkcja wykonująca algorytm znajdowania silnie spójnych składowych w grafie skierowanym.
        """

        instructions_list = []
        terminal_messages = []

        terminal_messages.append(strings.scc_initial_message)
        terminal_messages.append(strings.scc_graph_reversal_message)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [1]))

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.reverse_graph_mnemonic,))

        reversed_neighbours_list = self.find_graph_reversal()

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [2]))

        terminal_messages.append(strings.scc_dfs_on_reversed_graph)

        self.dfs(reversed_neighbours_list, terminal_messages, instructions_list)

        terminal_messages.append(strings.scc_sorting_vertices_by_post_value)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [3]))

        sorted_vertices = self.sort_post_values()

        terminal_messages.append(strings.scc_sorting_result_message + f'{sorted_vertices}.')

        self.clear()

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [4]))

        terminal_messages.append(strings.scc_dfs_on_normal_graph_message)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.reverse_graph_mnemonic,))

        self.dfs(self.neighbours_list, terminal_messages, instructions_list, True, sorted_vertices)

        scc_components = self.prepare_components_dictionary()

        terminal_messages.append(strings.scc_final_message + f'{scc_components}.')

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.mark_components_mnemonic, scc_components, sorted_vertices))

        components_data_text_list = self.get_components_data_text_list()

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_vertices_data_mnemonic, components_data_text_list))

        instructions_list.append((scc_components, components_data_text_list))

        return terminal_messages, instructions_list

    def prepare_components_dictionary(self):
        components_dictionary = dict()

        for i in range(1, self.component_number + 1):
            components_dictionary[i] = []

        for i in range(0, len(self.components)):
            components_dictionary[self.components[i]].append(i)

        return components_dictionary

    def clear(self):
        n = len(self.neighbours_list)

        self.clock = 0
        self.pre = [-1 for _ in range(0, n)]
        self.visited = [False for _ in range(0, n)]
        self.component_number = 0
        self.components = [0 for _ in range(0, n)]

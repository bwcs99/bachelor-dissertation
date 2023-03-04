import math
from queue import Queue
from resources import strings, colors


class MaximumFlowFinder:
    """
    Klasa, w której są zaimplementowane dwa algorytmy szukania maksymalnego przepływu w sieciach przepływowych: algorytm
    Forda-Fulkersona oraz algorytm Edmondsa-Karpa.
    """

    def __init__(self, neighbours_list, source, target):
        self.neighbours_list = neighbours_list
        self.source = source
        self.target = target

    def get_flow_network(self):
        """
        Funkcja zwracająca sieć przepływową.
        """

        current_flow_network = [[] for i in range(0, len(self.neighbours_list))]

        for i in range(0, len(self.neighbours_list)):
            for j in range(0, len(self.neighbours_list[i])):
                vertex_number = self.neighbours_list[i][j][0]
                current_flow_network[i].append((vertex_number, 0, colors.flow_network_color))

        return current_flow_network

    def get_copy_of_flow_network(self, flow_network):
        """
        Funkcja kopiująca sieć przepływową.
        """

        flow_network_copy = [[] for i in range(0, len(flow_network))]

        for i in range(0, len(flow_network)):
            for j in range(0, len(flow_network[i])):
                data_tuple = flow_network[i][j]

                flow_network_copy[i].append(data_tuple)

        return flow_network_copy

    def construct_residual_network(self, flow_network, neighbours_list):
        """
        Funkcja zwracająca graf residualny, indukowany przez aktualną sieć przepływową.
        """

        residual_network = [[] for _ in range(0, len(neighbours_list))]

        for i in range(0, len(neighbours_list)):
            for j in range(0, len(neighbours_list[i])):
                first_vertex = i
                second_vertex = neighbours_list[i][j][0]
                edge_capacity = neighbours_list[i][j][1]
                current_edge_flow = flow_network[i][j][1]

                left_over = edge_capacity - current_edge_flow

                if left_over > 0:
                    residual_network[first_vertex].append((second_vertex, left_over))

                if current_edge_flow != 0:
                    residual_network[second_vertex].append((first_vertex, current_edge_flow))

        return residual_network

    def bfs_for_augumenting_path(self, s, t, neighbour_list):
        """
        Funkcja wykonująca algorytm BFS, w celu znalezienia ścieżki ze źródła do ujścia.
        """

        n = len(neighbour_list)
        pre = [-1 for i in range(0, n)]
        path = []
        dist = [math.inf for i in range(0, n)]
        vertices_queue = Queue()

        dist[s] = 0
        vertices_queue.put(s)

        while not vertices_queue.empty():
            u = vertices_queue.get()

            for neighbour in neighbour_list[u]:
                v = neighbour[0]
                if dist[v] == math.inf:
                    vertices_queue.put(v)
                    pre[v] = u
                    dist[v] = dist[u] + 1

        i = t
        while i != -1:
            if i != s and pre[i] == -1:
                return None
            path.append((pre[i], i))
            i = pre[i]

        path.pop()
        path.reverse()
        return path

    def explore(self, vertex, visited, pre, neighbours_list):
        """Funkcja wykorzystywana przez algorytm DFS."""

        visited[vertex] = True

        for neighbour in neighbours_list[vertex]:
            neighbour_vertex = neighbour[0]

            if not visited[neighbour_vertex]:
                pre[neighbour_vertex] = vertex
                self.explore(neighbour_vertex, visited, pre, neighbours_list)

    def dfs_for_augumenting_path(self, s, t, neighbours_list):
        """Funkcja wykonująca algorytm DFS, w celu znalezienia ścieżki ze źródła do ujścia."""

        n = len(neighbours_list)
        visited = [False for i in range(0, n)]
        path = []
        pre = [-1 for i in range(0, n)]

        visited[s] = True

        self.explore(s, visited, pre, neighbours_list)

        i = t
        while i != -1:
            
            if i != s and pre[i] == -1:
                return None

            path.append((pre[i], i))
            i = pre[i]

        path.pop()
        path.reverse()

        return path

    def get_residual_capacity(self, path, neighbours_list):
        """
        Funkcja służąca do znalezienia przepustowości i krawędzi residualnej dla
        aktualnej ścieżki ze źródła do ujścia.
        """

        capacities = []
        edges = []

        for edge in path:
            u = edge[0]
            v = edge[1]

            for neighbour in neighbours_list[u]:
                if neighbour[0] == v:
                    capacities.append(neighbour[1])
                    edges.append((u, v))

        residual_capacity = min(capacities)
        residual_capacity_index = capacities.index(residual_capacity)

        u, v = edges[residual_capacity_index][0], edges[residual_capacity_index][1]

        return residual_capacity, u, v

    def ford_fulkerson(self):
        """
        Funkcja wykonująca algorytm Forda-Fulkersona na danej sieci przepływowej.
        """

        terminal_messages = []
        instructions_list = []

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [1, 2]))

        flow_network = self.get_flow_network()
        residual_graph = self.construct_residual_network(flow_network, self.neighbours_list)
        st_path = self.dfs_for_augumenting_path(self.source, self.target, residual_graph)
        total_flow = 0

        terminal_messages.append(strings.ford_fulkerson_initial_message)

        terminal_messages.append(strings.initial_flow_network_message)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_flow_network_mnemonic, self.get_copy_of_flow_network(flow_network)))

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [3]))

        terminal_messages.append(strings.residual_network_message)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_residual_graph_mnemonic, residual_graph))

        terminal_messages.append(strings.found_augumenting_path_message + f" {st_path}.")

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_augumenting_path_mnemonic, st_path))

        while st_path is not None:

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_line_in_pseudocode_instruction, [4]))

            residual_capacity, u, v = self.get_residual_capacity(st_path, residual_graph)
            total_flow += residual_capacity
            flag = False

            terminal_messages.append(strings.residual_capacity_message + f" {residual_capacity}.")

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_edge_mnemonic, u, v))

            terminal_messages.append(strings.flow_network_message)

            terminal_messages.append(strings.stop_string)
            instructions_list.append(
                (strings.display_flow_network_mnemonic, self.get_copy_of_flow_network(flow_network)))

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_line_in_pseudocode_instruction, [5]))

            for edge in st_path:
                u = edge[0]
                v = edge[1]

                for i in range(0, len(flow_network[u])):

                    if flow_network[u][i][0] == v:
                        current_flow = flow_network[u][i][1]
                        edge_color = flow_network[u][i][2]

                        terminal_messages.append(strings.stop_string)
                        instructions_list.append((strings.select_line_in_pseudocode_instruction, [5, 6, 7]))

                        flow_network[u][i] = (v, current_flow + residual_capacity, edge_color)
                        flag = True

                        terminal_messages.append(f"GC> Krawędź ({u}, {v}) jest w pierwotnej sieci przepływowej. "
                                                 f"Zwiększam "
                                                 f" przepływ na tej krawędzi o {residual_capacity}.")

                        terminal_messages.append(strings.stop_string)
                        instructions_list.append((strings.display_altered_edge_flow_mnemonic, u, v,
                                                  current_flow + residual_capacity, colors.increase_edge_flow_color))

                if not flag:

                    for i in range(0, len(flow_network[v])):
                        if flow_network[v][i][0] == u:
                            current_flow = flow_network[v][i][1]
                            edge_color = flow_network[u][i][2]

                            terminal_messages.append(strings.stop_string)
                            instructions_list.append((strings.select_line_in_pseudocode_instruction, [5, 8, 9]))

                            flow_network[v][i] = (u, current_flow - residual_capacity, edge_color)

                            terminal_messages.append(
                                f"GC> Krawędzi ({u}, {v}) nie było w pierwotnej sieci przepływowej. Zmniejszam"
                                f" przepływ na krawędzi ({v}, {u}) o {residual_capacity}.")

                            terminal_messages.append(strings.stop_string)
                            instructions_list.append((strings.display_altered_edge_flow_mnemonic, v, u,
                                                      current_flow - residual_capacity,
                                                      colors.decrease_edge_flow_color))

                flag = False

            residual_graph = self.construct_residual_network(flow_network, self.neighbours_list)

            terminal_messages.append(strings.residual_network_message)

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.display_residual_graph_mnemonic, residual_graph))

            st_path = self.dfs_for_augumenting_path(self.source, self.target, residual_graph)

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_line_in_pseudocode_instruction, [3]))

            if st_path is None:
                terminal_messages.append(
                    strings.found_augumenting_path_message + f" nie ma już scieżek powiększających.")

            else:
                terminal_messages.append(strings.found_augumenting_path_message + f" {st_path}.")

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.display_augumenting_path_mnemonic, st_path))

        terminal_messages.append(strings.ford_fulkerson_final_message + f"{total_flow}.")

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_flow_network_mnemonic, self.get_copy_of_flow_network(flow_network)))

        instructions_list.append((flow_network,))

        return terminal_messages, instructions_list

    def edmonds_karp(self):
        """
        Funkcja wykonująca algorytm Edmondsa-Karpa na danej sieci przepływowej.
        """

        terminal_messages = []
        instructions_list = []

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [1, 2]))

        flow_network = self.get_flow_network()
        residual_graph = self.construct_residual_network(flow_network, self.neighbours_list)
        st_path = self.bfs_for_augumenting_path(self.source, self.target, residual_graph)
        total_flow = 0

        terminal_messages.append(strings.edmonds_karp_initial_message)

        terminal_messages.append(strings.initial_flow_network_message)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_flow_network_mnemonic, self.get_copy_of_flow_network(flow_network)))

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [3]))

        terminal_messages.append(strings.residual_network_message)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_residual_graph_mnemonic, residual_graph))

        terminal_messages.append(strings.found_augumenting_path_message + f" {st_path}.")

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_augumenting_path_mnemonic, st_path))

        while st_path is not None:
            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_line_in_pseudocode_instruction, [4]))

            residual_capacity, u, v = self.get_residual_capacity(st_path, residual_graph)
            total_flow += residual_capacity
            flag = False

            terminal_messages.append(strings.residual_capacity_message + f" {residual_capacity}.")

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_edge_mnemonic, u, v))

            terminal_messages.append(strings.flow_network_message)

            terminal_messages.append(strings.stop_string)
            instructions_list.append(
                (strings.display_flow_network_mnemonic, self.get_copy_of_flow_network(flow_network)))

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_line_in_pseudocode_instruction, [5]))

            for edge in st_path:
                u = edge[0]
                v = edge[1]

                for i in range(0, len(flow_network[u])):
                    if flow_network[u][i][0] == v:
                        current_flow = flow_network[u][i][1]
                        edge_color = flow_network[u][i][2]

                        terminal_messages.append(strings.stop_string)
                        instructions_list.append((strings.select_line_in_pseudocode_instruction, [5, 6, 7]))

                        flow_network[u][i] = (v, current_flow + residual_capacity, edge_color)
                        flag = True

                        terminal_messages.append(f"GC> Krawędź ({u}, {v}) jest w pierwotnej sieci przepływowej. "
                                                 f"Zwiększam "
                                                 f" przepływ na tej krawędzi o {residual_capacity}.")

                        terminal_messages.append(strings.stop_string)
                        instructions_list.append((strings.display_altered_edge_flow_mnemonic, u, v,
                                                  current_flow + residual_capacity, colors.increase_edge_flow_color))

                if not flag:
                    for i in range(0, len(flow_network[v])):
                        if flow_network[v][i][0] == u:
                            current_flow = flow_network[v][i][1]
                            edge_color = flow_network[u][i][2]

                            terminal_messages.append(strings.stop_string)
                            instructions_list.append((strings.select_line_in_pseudocode_instruction, [5, 8, 9]))

                            flow_network[v][i] = (u, current_flow - residual_capacity, edge_color)

                            terminal_messages.append(
                                f"GC> Krawędzi ({u}, {v}) nie było w pierwotnej sieci przepływowej. Zmniejszam"
                                f" przepływ na krawędzi ({v}, {u}) o {residual_capacity}.")

                            terminal_messages.append(strings.stop_string)
                            instructions_list.append((strings.display_altered_edge_flow_mnemonic, v, u,
                                                      current_flow - residual_capacity,
                                                      colors.decrease_edge_flow_color))

                flag = False

            residual_graph = self.construct_residual_network(flow_network, self.neighbours_list)

            terminal_messages.append(strings.residual_network_message)

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.display_residual_graph_mnemonic, residual_graph))

            st_path = self.bfs_for_augumenting_path(self.source, self.target, residual_graph)

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_line_in_pseudocode_instruction, [3]))

            if st_path is None:
                terminal_messages.append(strings.found_augumenting_path_message + f" nie ma już scieżek powiększających.")

            else:
                terminal_messages.append(strings.found_augumenting_path_message + f" {st_path}.")

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.display_augumenting_path_mnemonic, st_path))

        terminal_messages.append(strings.edmonds_karp_final_message + f"{total_flow}.")

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_flow_network_mnemonic, self.get_copy_of_flow_network(flow_network)))

        instructions_list.append((flow_network,))

        return terminal_messages, instructions_list

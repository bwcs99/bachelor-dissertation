import math
from resources import strings
from algorithms.union_find import UnionFind
from data_structures.prim_priority_queue import PrimPriorityQueue
from data_structures.kruskal_priority_queue import KruskalPriorityQueue


class MSTFinder:
    """
    Klasa, w której są zaimplementowane algorytmy szukania minimalnego drzewa rozpinającego - algorytm Prima oraz
    algorytm Kruskala.
    """

    def __init__(self, neighbours_list):
        self.neighbours_list = neighbours_list

    def get_vertex_data_text(self, cost, prev):
        """
        Funkcja służąca do pobierania danych związanych z wierzchołkami (w postaci tekstowej).
        """

        data_text_list = []
        for i in range(0, len(self.neighbours_list)):

            if cost[i] == math.inf:
                cost_text = 'inf'
            else:
                cost_text = str(cost[i])

            prev_text = str(prev[i])

            data_text = f'{cost_text}/{prev_text}'

            data_text_list.append(data_text)

        return data_text_list

    def prim(self):
        """
        Funkcja wykonująca algorytm Prima na danym grafie.
        """

        cost = [math.inf for _ in range(0, len(self.neighbours_list))]
        prev = [-1 for _ in range(0, len(self.neighbours_list))]
        s = set()

        terminal_messages = []
        instructions_list = []

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [1, 2, 3, 4, 5, 6]))

        terminal_messages.append(strings.prim_initial_message)

        initial_vertex = 0
        cost[initial_vertex] = 0

        terminal_messages.append(strings.prim_post_initial_message + f'{initial_vertex}, ' + f' {cost[initial_vertex]}.')

        data_text_list = self.get_vertex_data_text(cost, prev)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_vertices_data_mnemonic, data_text_list))

        in_vertices_set = [False for _ in range(0, len(self.neighbours_list))]

        my_queue = PrimPriorityQueue()
        my_queue.create_new_priority_queue(cost, in_vertices_set)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.select_line_in_pseudocode_instruction, [7]))

        while not my_queue.is_empty():
            queue_state_string = my_queue.queue_state_as_string()

            terminal_messages.append(strings.priority_queue_state + f'{queue_state_string}')

            v = my_queue.pop_vertex()

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_line_in_pseudocode_instruction, [8, 9]))

            v_number = v[1]
            in_vertices_set[v_number] = True

            s.add(v_number)

            terminal_messages.append(strings.prim_select_vertex_message + f'{v_number}.' + f' Jego koszt: {cost[v_number]}.')

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.include_vertex_mnemonic, v_number))

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_line_in_pseudocode_instruction, [10]))

            for neighbour in self.neighbours_list[v_number]:
                z_number = neighbour[0]
                v_z_weight = neighbour[1]

                terminal_messages.append(strings.prim_selected_vertex_neighbour + f'{z_number}.')

                terminal_messages.append(strings.stop_string)
                instructions_list.append((strings.select_edge_mnemonic, v_number, z_number))

                terminal_messages.append(strings.prim_pre_update_message)

                terminal_messages.append(strings.stop_string)
                instructions_list.append((strings.select_line_in_pseudocode_instruction, [11]))

                if cost[z_number] > v_z_weight and not in_vertices_set[z_number]:
                    cost[z_number] = v_z_weight
                    prev[z_number] = v_number

                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.select_line_in_pseudocode_instruction, [12, 13, 14]))

                    data_text_list = self.get_vertex_data_text(cost, prev)

                    terminal_messages.append(strings.prim_update_message + f'{v_z_weight} oraz {v_number}.')

                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.select_vertex_mnemonic, z_number))

                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.display_vertices_data_mnemonic, data_text_list))

                    my_queue.create_new_priority_queue(cost, in_vertices_set)

                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.select_line_in_pseudocode_instruction, [10]))

                else:
                    terminal_messages.append(strings.prim_not_update_message)

                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.select_line_in_pseudocode_instruction, [10]))

                terminal_messages.append(strings.stop_string)
                instructions_list.append((strings.exclude_edge_mnemonic, v_number, z_number))

                if z_number not in s:
                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.exclude_vertex_mnemonic, z_number))
                else:
                    terminal_messages.append(strings.stop_string)
                    instructions_list.append((strings.include_vertex_mnemonic, z_number))

            terminal_messages.append(strings.stop_string)
            instructions_list.append((strings.select_line_in_pseudocode_instruction, [7]))

        x = set()
        tree_cost = sum(cost)

        for i in range(0, len(self.neighbours_list)):
            if i == initial_vertex:
                continue

            edge = (i, prev[i])
            x.add(edge)

        terminal_messages.append(strings.stop_string)
        instructions_list.append((strings.display_MST_mnemonic, prev))

        instructions_list.append((prev, cost))

        terminal_messages.append(strings.prim_final_message + f'{x}.' + f' Koszt MST : {tree_cost}.')

        return terminal_messages, instructions_list

    def kruskal(self):
        """
        Funkcja wykonująca algorytm Kruskala na danym grafie.
        """

        number_of_vertices = len(self.neighbours_list)
        tree_cost = 0

        terminal_messages = []
        canvas_instructions = []

        terminal_messages.append(strings.kruskal_initial_message)

        uf = UnionFind(number_of_vertices)

        for i in range(0, number_of_vertices):
            uf.makeset(i)

        terminal_messages.append(strings.stop_string)
        canvas_instructions.append((strings.select_line_in_pseudocode_instruction, [1, 2]))

        pq = KruskalPriorityQueue()
        pq.create_kruskal_priority_queue(self.neighbours_list)

        x = set()

        terminal_messages.append(strings.stop_string)
        canvas_instructions.append((strings.select_line_in_pseudocode_instruction, [3]))

        terminal_messages.append(strings.stop_string)
        canvas_instructions.append((strings.select_line_in_pseudocode_instruction, [4]))

        priority_queue_state_string = pq.queue_state_as_string()
        terminal_messages.append(strings.priority_queue_initial_state + f'{priority_queue_state_string}')

        terminal_messages.append(strings.stop_string)
        canvas_instructions.append((strings.select_line_in_pseudocode_instruction, [5]))

        while not pq.is_empty():
            priority_queue_state_string = pq.queue_state_as_string()
            terminal_messages.append(strings.priority_queue_state + f'{priority_queue_state_string}')

            edge = pq.pop_edge()

            u = edge[1][0]
            v = edge[1][1]
            weight = edge[0]

            terminal_messages.append(strings.mst_select_edge + f'{{{u}, {v}}}, waga: {weight}.')

            terminal_messages.append(strings.stop_string)
            canvas_instructions.append((strings.select_edge_mnemonic, u, v))

            terminal_messages.append(strings.stop_string)
            canvas_instructions.append((strings.select_line_in_pseudocode_instruction, [6]))

            if uf.find(u) != uf.find(v):
                terminal_messages.append(strings.kruskal_include_edge + f'Dodaje krawędź {{{u}, {v}}} do MST.')

                terminal_messages.append(strings.stop_string)
                canvas_instructions.append((strings.include_edge_mnemonic, u, v))

                tree_cost += weight

                x.add(edge[1])

                uf.union(u, v)

                terminal_messages.append(strings.stop_string)
                canvas_instructions.append((strings.select_line_in_pseudocode_instruction, [7, 8]))

                terminal_messages.append(strings.stop_string)
                canvas_instructions.append((strings.select_line_in_pseudocode_instruction, [5]))
            else:
                terminal_messages.append(strings.kruskal_exclude_edge +
                                         f'Krawędź {{{u}, {v}}} nie należy do MST.')

                terminal_messages.append(strings.stop_string)
                canvas_instructions.append((strings.exclude_edge_mnemonic, u, v))

                terminal_messages.append(strings.stop_string)
                canvas_instructions.append((strings.select_line_in_pseudocode_instruction, [5]))

        terminal_messages.append(strings.kruskal_final_message + f'{x}.' + f' Koszt MST : {tree_cost}.')

        canvas_instructions.append((x,))

        return terminal_messages, canvas_instructions

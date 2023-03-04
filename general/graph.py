import copy
import math
import random
from resources import constants, colors


class Graph:
    """
    Klasa, w której są zaimplementowane metody służące do tworzenia reprezentacji grafu i manipulowania nią.
    """

    def __init__(self):
        """
        Funkcja tworząca obiekty klasy Graph.
        """

        self.is_directed = None
        self.neighbours_list = []
        self.helping_neighbour_list = []
        self.vertices = []

        self.vertices_size = constants.default_vertex_size

        self.flow_network = None

        self.residual_vertices = None
        self.residual_graph = None

        self.changed_after_animation = False

        self.is_graph_reversed = False

        self.is_graph_saved = False

    def get_graph_saved_flag(self):
        return self.is_graph_saved

    def set_graph_saved_flag(self, new_boolean_value):
        self.is_graph_saved = new_boolean_value

    def get_residual_graph(self):
        return self.residual_graph

    def set_residual_graph(self, new_residual_graph):
        self.residual_graph = new_residual_graph

    def get_flow_network(self):
        return self.flow_network

    def set_flow_network(self, new_flow_network):
        self.flow_network = new_flow_network

    def get_graph_reversed_flag(self):
        return self.is_graph_reversed

    def get_changed_after_animation_flag(self):
        return self.changed_after_animation

    def set_changed_after_animation(self):
        self.changed_after_animation = True

    def unset_changed_after_animation(self):
        self.changed_after_animation = False

    def set_vertices_size(self, vertices_new_size):
        self.vertices_size = vertices_new_size

    def get_number_of_vertices_in_graph(self):
        return len(self.neighbours_list)

    def get_data_tuple(self):
        """
        Funkcja zwracająca krotkę z danymi, które są niezbędne do reprezentacji grafu.
        """

        is_directed = self.is_directed
        neighbours_list = copy.copy(self.neighbours_list)
        helping_neighbour_list = copy.copy(self.helping_neighbour_list)
        vertices = copy.copy(self.vertices)
        vertices_size = self.vertices_size
        edges_width = constants.default_line_width

        if self.changed_after_animation:
            for i in range(0, len(vertices)):
                cx, cy, number, vertex_color, data, vertex_data_x, vertex_data_y = vertices[i]

                vertex_new_data_tuple = (cx, cy, number, colors.normal_color, None, vertex_data_x, vertex_data_y)
                vertices[i] = vertex_new_data_tuple

            for i in range(0, len(neighbours_list)):
                for j in range(0, len(neighbours_list[i])):
                    second_vertex, weight, coordinates, color, weight_x, weight_y = neighbours_list[i][j]

                    edge_new_data_tuple = (second_vertex, weight, coordinates, colors.normal_color, weight_x, weight_y)
                    neighbours_list[i][j] = edge_new_data_tuple

        data = (is_directed, neighbours_list, helping_neighbour_list, vertices, vertices_size, edges_width)

        return data

    def restore_graph_from_data_tuple(self, data_tuple):
        """
        Funkcja służąca do wczytania danych z otworzonego pliku.
        """

        direction_flag_from_tuple = data_tuple[0]
        neighbours_list_from_tuple = data_tuple[1]
        helping_neighbour_list_from_tuple = data_tuple[2]
        vertices_from_tuple = data_tuple[3]
        vertices_size = data_tuple[4]
        edges_width = data_tuple[5]

        reconstructed_helping_neighbours_list = [[] for _ in range(0, len(neighbours_list_from_tuple))]

        for i in range(0, len(neighbours_list_from_tuple)):
            for j in range(0, len(neighbours_list_from_tuple[i])):
                reconstructed_helping_neighbours_list[i].append(tuple(helping_neighbour_list_from_tuple[i][j]))

        self.is_directed = direction_flag_from_tuple
        self.neighbours_list = neighbours_list_from_tuple
        self.helping_neighbour_list = reconstructed_helping_neighbours_list
        self.vertices = vertices_from_tuple

        self.vertices_size = vertices_size
        self.edges_width = edges_width

    def get_is_directed_flag(self):
        return self.is_directed

    def set_is_directed_flag(self, flag_value):
        self.is_directed = flag_value

    def get_neighbour_number(self, i, j):
        return self.neighbours_list[i][j][0]

    def find_given_neighbour(self, vertex_number, neighbour_number):
        list_with_requested_element = list(filter(lambda x: x[0] == neighbour_number,
                                                  self.neighbours_list[vertex_number]))

        if len(list_with_requested_element) <= 0:
            return
        else:
            try:
                requested_index = self.neighbours_list[vertex_number].index(list_with_requested_element[0])
                return requested_index
            except ValueError:
                return None

    def get_graph_neighbours_list(self):
        return self.neighbours_list

    def get_graph_helping_neighbours_list(self):
        return self.helping_neighbour_list

    def add_new_vertex(self, cx, cy, number_of_vertex, vertex_color, additional_data=None):
        """
        Funkcja dodająca nowy wierzchołek do listy sąsiedztwa.
        """

        data_x = cx
        data_y = cy

        self.vertices.append((cx, cy, number_of_vertex, vertex_color, additional_data, data_x, data_y))
        self.neighbours_list.append([])
        self.helping_neighbour_list.append([])

        self.set_graph_saved_flag(False)

    def remove_vertex(self, vertex_number):
        """
        Funkcja usuwająca dany wierzchołek z listy sąsiedztwa.
        """

        self.vertices.pop(vertex_number)
        self.neighbours_list.pop(vertex_number)
        self.helping_neighbour_list.pop(vertex_number)
        self.set_graph_saved_flag(False)

    def decrement_vertices_numbers(self, vertex_to_remove_number):
        """
        Funkcja zmniejszająca numery odpowiednich wierzchołków, po usunięciu jakiegoś wierzchołka.
        """

        for i in range(vertex_to_remove_number + 1, len(self.vertices)):
            vertex = self.vertices[i]
            new_vertex = (vertex[0], vertex[1], vertex[2] - 1, vertex[3], vertex[4], vertex[5], vertex[6])

            self.vertices[i] = new_vertex

    def remove_deleted_vertex_from_neighbours_list(self, vertex_to_remove_number):
        """
        Funkcja usuwająca dany wierzchołek z listy sąsiadów innych wierzchołków.
        """

        for i in range(0, len(self.neighbours_list)):
            for j in range(0, len(self.neighbours_list[i])):
                if i >= len(self.neighbours_list) or j >= len(self.neighbours_list[i]):
                    break
                neighbour = self.neighbours_list[i][j]
                neighbour_vertex_number = neighbour[0]

                if neighbour_vertex_number == vertex_to_remove_number:
                    self.neighbours_list[i].pop(j)
                    self.helping_neighbour_list[i].pop(j)
                    continue

    def decrement_vertices_numbers_in_neighbours_list(self, vertex_to_remove_number):
        for i in range(0, len(self.neighbours_list)):
            list_with_requested_items = list(filter(lambda x: x[0] >= vertex_to_remove_number + 1,
                                                    self.neighbours_list[i]))

            for requested_item in list_with_requested_items:
                try:
                    idx = self.neighbours_list[i].index(requested_item)

                    new_number_of_vertex, edge_weight = self.neighbours_list[i][idx][0] - 1, \
                                                        self.neighbours_list[i][idx][1]
                    edge_coordinates, edge_color = self.neighbours_list[i][idx][2], self.neighbours_list[i][idx][3]
                    weight_x, weight_y = self.neighbours_list[i][idx][4], self.neighbours_list[i][idx][5]

                    new_neighbour = (new_number_of_vertex, edge_weight, edge_coordinates, edge_color, weight_x,
                                     weight_y)

                    self.neighbours_list[i][idx], self.helping_neighbour_list[i][idx] = new_neighbour, (
                        new_number_of_vertex, edge_weight)

                except ValueError:
                    continue

    def alter_vertex_coordinates(self, vertex_number, new_center_x, new_center_y, dx=None, dy=None):
        """
        Funkcja służąca do zmiany współrzędnych położenia wierzchołka.
        """

        vertex_color = self.vertices[vertex_number][3]

        cx = self.vertices[vertex_number][0]
        cy = self.vertices[vertex_number][1]

        data_x = self.vertices[vertex_number][5]
        data_y = self.vertices[vertex_number][6]

        if dx is not None and dy is not None:
            data_x = cx + dx
            data_y = cy + dy

        new_coordinates = (new_center_x, new_center_y, vertex_number, vertex_color, None, data_x, data_y)

        self.vertices[vertex_number] = new_coordinates
        self.set_graph_saved_flag(False)

    def check_if_over_vertex(self, mx, my):

        for vertex in self.vertices:
            vx, vy, n_vertex = vertex[0], vertex[1], vertex[2]

            dist = math.sqrt(pow(mx - vx, 2) + pow(my - vy, 2))

            if dist <= self.vertices_size:
                return True, n_vertex

        return False, None

    def check_if_over_vertex_data(self, mouse_x, mouse_y):
        """
        Funkcja sprawdzająca, czy współrzędne kursora myszy są nad przykładowymi danymi związanymi z wierzchołkiem.
        """

        for i in range(0, len(self.vertices)):
            additional_data = self.vertices[i][4]
            if additional_data is not None:
                data_x = self.vertices[i][5]
                data_y = self.vertices[i][6]

                x_lower_bound = data_x - len(
                    str(additional_data)) * constants.space_for_one_digit - constants.shift_value
                y_lower_bound = data_y - constants.height - constants.shift_value

                if x_lower_bound <= mouse_x <= data_x and y_lower_bound <= mouse_y <= data_y:
                    return True, i
        return False, None

    def alter_vertex_color(self, vertex, color):
        vertex_data_tuple = self.vertices[vertex]

        self.vertices[vertex] = (vertex_data_tuple[0], vertex_data_tuple[1], vertex_data_tuple[2], color,
                                 vertex_data_tuple[4], vertex_data_tuple[5], vertex_data_tuple[6])

    def alter_vertex_additional_data(self, vertex, additional_data):
        vertex_data_tuple = self.vertices[vertex]

        self.vertices[vertex] = (vertex_data_tuple[0], vertex_data_tuple[1], vertex_data_tuple[2], vertex_data_tuple[3],
                                 additional_data, vertex_data_tuple[5], vertex_data_tuple[6])

    def alter_vertex_data_coordinates(self, vertex, new_x, new_y):
        vertex_data_tuple = self.vertices[vertex]

        self.vertices[vertex] = (vertex_data_tuple[0], vertex_data_tuple[1], vertex_data_tuple[2], vertex_data_tuple[3],
                                 vertex_data_tuple[4], new_x, new_y)

        self.set_graph_saved_flag(False)

    def restore_vertices_default_data(self):
        for i in range(0, len(self.vertices)):
            vertex_data_tuple = self.vertices[i]

            vertex_new_data_tuple = (vertex_data_tuple[0], vertex_data_tuple[1], vertex_data_tuple[2],
                                     colors.normal_color, None, vertex_data_tuple[5], vertex_data_tuple[6])

            self.vertices[i] = vertex_new_data_tuple

    def restore_vertices_default_color(self):
        for i in range(0, len(self.vertices)):
            vertex_data_tuple = self.vertices[i]

            vertex_new_data_tuple = (vertex_data_tuple[0], vertex_data_tuple[1], vertex_data_tuple[2],
                                     colors.normal_color, vertex_data_tuple[4],
                                     vertex_data_tuple[5], vertex_data_tuple[6])

            self.vertices[i] = vertex_new_data_tuple

    def get_vertex(self, vertex_number):
        return self.vertices[vertex_number]

    def get_all_vertices_data(self):
        return self.vertices

    def get_vertices_size(self):
        return self.vertices_size

    def add_new_edge(self, first_vertex, second_vertex, edge_coordinates, edge_color, weight_x, weight_y):
        if self.is_directed:
            self.neighbours_list[first_vertex].append((second_vertex, None, edge_coordinates, edge_color, weight_x,
                                                       weight_y))
            self.helping_neighbour_list[first_vertex].append((second_vertex, None))
        else:
            self.neighbours_list[first_vertex].append((second_vertex, None, edge_coordinates, edge_color, weight_x,
                                                       weight_y))
            self.neighbours_list[second_vertex].append((first_vertex, None, edge_coordinates, edge_color, weight_x,
                                                        weight_y))
            self.helping_neighbour_list[first_vertex].append((second_vertex, None))
            self.helping_neighbour_list[second_vertex].append((first_vertex, None))

        self.set_graph_saved_flag(False)

    def remove_edge(self, first_vertex, second_vertex):
        for i in range(0, len(self.neighbours_list[first_vertex])):

            if i > len(self.neighbours_list[first_vertex]) - 1:
                break

            neighbour = self.neighbours_list[first_vertex][i]

            if neighbour[0] == second_vertex:
                self.neighbours_list[first_vertex].pop(i)
                self.helping_neighbour_list[first_vertex].pop(i)

        if not self.is_directed:

            for i in range(0, len(self.neighbours_list[second_vertex])):

                if i > len(self.neighbours_list[second_vertex]) - 1:
                    break

                neighbour = self.neighbours_list[second_vertex][i]

                if neighbour[0] == first_vertex:
                    self.neighbours_list[second_vertex].pop(i)
                    self.helping_neighbour_list[second_vertex].pop(i)

        self.set_graph_saved_flag(False)

    def check_if_edge_exists(self, start_vertex, end_vertex):
        indicator_list = list(filter(lambda x: x[0] == end_vertex, self.neighbours_list[start_vertex]))
        return len(indicator_list) >= 1

    def check_for_double_directed_edge(self, start_vertex, end_vertex):
        indicator_list = list(filter(lambda x: x[0] == start_vertex, self.neighbours_list[end_vertex]))
        return len(indicator_list) >= 1

    def set_edge_weight_for_directed_graph(self, first_vertex, second_vertex, weight):
        neighbours = self.neighbours_list[first_vertex]

        list_with_requested_items = list(filter(lambda x: x[0] == second_vertex, neighbours))

        for item in list_with_requested_items:
            try:
                i = neighbours.index(item)

                new_edge = (neighbours[i][0], weight, neighbours[i][2], neighbours[i][3], neighbours[i][4],
                            neighbours[i][5])
                new_edge1 = (neighbours[i][0], weight)

                self.neighbours_list[first_vertex][i] = new_edge
                self.helping_neighbour_list[first_vertex][i] = new_edge1

                self.set_graph_saved_flag(False)

            except ValueError:
                return

    def set_edge_weight_for_undirected_graph(self, first_vertex, second_vertex, weight):
        first_neighbours = self.neighbours_list[first_vertex]
        second_neighbours = self.neighbours_list[second_vertex]

        for i in range(0, len(first_neighbours)):
            current_vertex_number = first_neighbours[i][0]

            if current_vertex_number == second_vertex:
                self.neighbours_list[first_vertex][i] = (current_vertex_number, weight, first_neighbours[i][2],
                                                         first_neighbours[i][3], first_neighbours[i][4],
                                                         first_neighbours[i][5])
                self.helping_neighbour_list[first_vertex][i] = (current_vertex_number, weight)

        for i in range(0, len(second_neighbours)):
            current_vertex_number = second_neighbours[i][0]

            if current_vertex_number == first_vertex:
                self.neighbours_list[second_vertex][i] = (current_vertex_number, weight, second_neighbours[i][2],
                                                          second_neighbours[i][3], second_neighbours[i][4],
                                                          second_neighbours[i][5])
                self.helping_neighbour_list[second_vertex][i] = (current_vertex_number, weight)

        self.set_graph_saved_flag(False)

    def set_random_weights_to_all_edges_in_graph(self):
        considered_undirected_edges = set()
        considered_directed_edges = set()

        for i in range(0, len(self.neighbours_list)):
            for j in range(0, len(self.neighbours_list[i])):
                first_vertex = i
                second_vertex = self.neighbours_list[i][j][0]
                edge_weight = self.neighbours_list[i][j][1]

                if not self.is_directed and {first_vertex,
                                             second_vertex} not in considered_undirected_edges and edge_weight is None:
                    considered_undirected_edges.add(frozenset({first_vertex, second_vertex}))

                    edge_data_tuple = self.neighbours_list[i][j]

                    random_weight = random.randint(constants.lower_weight_value, constants.upper_weight_value)

                    self.neighbours_list[i][j] = (edge_data_tuple[0], random_weight, edge_data_tuple[2],
                                                  colors.normal_color, edge_data_tuple[4], edge_data_tuple[5])
                    self.helping_neighbour_list[i][j] = (edge_data_tuple[0], random_weight)

                    for k in range(0, len(self.neighbours_list[second_vertex])):
                        if self.neighbours_list[second_vertex][k][0] == first_vertex:
                            edge_data_tuple = self.neighbours_list[second_vertex][k]

                            self.neighbours_list[second_vertex][k] = (edge_data_tuple[0],
                                                                      random_weight, edge_data_tuple[2],
                                                                      colors.normal_color, edge_data_tuple[4],
                                                                      edge_data_tuple[5])
                            self.helping_neighbour_list[second_vertex][k] = (edge_data_tuple[0],
                                                                             random_weight)
                            break
                elif self.is_directed and (
                        first_vertex, second_vertex) not in considered_directed_edges and edge_weight is None:
                    considered_directed_edges.add((first_vertex, second_vertex))

                    edge_data_tuple = self.neighbours_list[i][j]

                    random_weight = random.randint(constants.lower_weight_value, constants.upper_weight_value)

                    self.neighbours_list[i][j] = (edge_data_tuple[0], random_weight, edge_data_tuple[2],
                                                  colors.normal_color, edge_data_tuple[4], edge_data_tuple[5])
                    self.helping_neighbour_list[i][j] = (edge_data_tuple[0], random_weight)

        self.set_graph_saved_flag(False)

    def check_if_over_edge(self, click_x, click_y):
        h_width = 11

        for vertex_number in range(0, len(self.neighbours_list)):
            for edges in range(0, len(self.neighbours_list[vertex_number])):
                neighbour_vertex = self.neighbours_list[vertex_number][edges]

                neighbour_vertex_number = neighbour_vertex[0]
                edge_coordinates = neighbour_vertex[2]

                start_x = edge_coordinates[0]
                start_y = edge_coordinates[1]
                end_x = edge_coordinates[2]
                end_y = edge_coordinates[3]

                if abs(start_x - end_x) <= constants.line_horizontal_coordinates_difference:
                    lower_x = start_x - h_width / 2
                    upper_x = end_x + h_width / 2

                    if lower_x <= click_x <= upper_x and (start_y <= click_y <= end_y or end_y <= click_y <= start_y):
                        return vertex_number, neighbour_vertex_number, True
                else:

                    try:
                        a = (end_y - start_y) / (end_x - start_x)
                        b = (start_y * end_x - start_x * end_y) / (end_x - start_x)
                    except ZeroDivisionError:
                        return

                    f1 = a * click_x + b - h_width
                    f2 = a * click_x + b + h_width

                    if (start_x <= click_x <= end_x or end_x <= click_x <= start_x) and f1 <= click_y <= f2:
                        return vertex_number, neighbour_vertex_number, True
        return None, None, False

    def check_weight_bounds(self, weight_new_x, weight_new_y):
        upper_x_value = constants.upper_x_value
        l_weight_x = constants.lower_weight_x_value
        upper_y_value = constants.upper_y_value
        l_weight_y = constants.lower_weight_y_value

        if weight_new_x >= upper_x_value or weight_new_x <= l_weight_x or weight_new_y >= upper_y_value or weight_new_y <= l_weight_y:
            return False

        return True

    def alter_edge_coordinates_during_movement(self, v_to_update):
        """
        Funkcja służąca do zmiany współrzędnych krawędzi, podczas przesuwania wierzchołka z nimi incydentnego.
        """

        for i in range(0, len(self.neighbours_list[v_to_update])):
            neighbour = self.neighbours_list[v_to_update][i]

            vertex_number = neighbour[0]
            edge_weight = neighbour[1]
            beg_x, beg_y, end_x, end_y = neighbour[2]
            edge_color = neighbour[3]
            edge_weight_x, edge_weight_y = neighbour[4], neighbour[5]

            edge_center_x, edge_center_y = (beg_x + end_x) / 2, (beg_y + end_y) / 2

            weight_x_transition = edge_weight_x - edge_center_x
            weight_y_transition = edge_weight_y - edge_center_y

            try:
                beg_x, beg_y, end_x, end_y = self.correction(v_to_update, vertex_number)
            except TypeError:
                return

            new_center_x, new_center_y = (beg_x + end_x) / 2, (beg_y + end_y) / 2

            edge_weight_new_x = new_center_x + weight_x_transition
            edge_weight_new_y = new_center_y + weight_y_transition

            if self.check_weight_bounds(edge_weight_new_x, edge_weight_new_y):
                edge_weight_x, edge_weight_y = edge_weight_new_x, edge_weight_new_y

            self.neighbours_list[v_to_update][i] = (vertex_number, edge_weight, [beg_x, beg_y, end_x, end_y],
                                                    edge_color, edge_weight_x, edge_weight_y)

            if not self.is_directed:
                for j in range(0, len(self.neighbours_list[vertex_number])):
                    neighbour = self.neighbours_list[vertex_number][j]

                    if neighbour[0] == v_to_update:
                        weight_x = neighbour[4]
                        weight_y = neighbour[5]

                        if self.check_weight_bounds(edge_weight_new_x, edge_weight_new_y):
                            weight_x = edge_weight_new_x
                            weight_y = edge_weight_new_y

                        self.neighbours_list[vertex_number][j] = (neighbour[0], neighbour[1],
                                                                  [beg_x, beg_y, end_x, end_y],
                                                                  colors.normal_color, weight_x,
                                                                  weight_y)

        if self.is_directed:
            for i in range(0, len(self.neighbours_list)):
                if i == v_to_update:
                    continue

                for j in range(0, len(self.neighbours_list[i])):
                    edge = self.neighbours_list[i][j]

                    if edge[0] == v_to_update:
                        weight_x = edge[4]
                        weight_y = edge[5]

                        beg_x, beg_y, end_x, end_y = edge[2]

                        center_x, center_y = (beg_x + end_x) / 2, (beg_y + end_y) / 2

                        weight_x_transition, weight_y_transition = weight_x - center_x, weight_y - center_y

                        try:
                            beg_x, beg_y, end_x, end_y = self.correction(i, v_to_update)
                        except TypeError:
                            return

                        new_center_x, new_center_y = (beg_x + end_x) / 2, (beg_y + end_y) / 2

                        x_new_weight = new_center_x + weight_x_transition
                        y_new_weight = new_center_y + weight_y_transition

                        if self.check_weight_bounds(x_new_weight, y_new_weight):
                            weight_x = x_new_weight
                            weight_y = y_new_weight

                        self.neighbours_list[i][j] = (edge[0], edge[1], [beg_x, beg_y, end_x, end_y],
                                                      colors.normal_color, weight_x, weight_y)

        self.set_graph_saved_flag(False)

    def alter_edge_color(self, u, v, color):
        second_vertex_index = self.find_given_neighbour(u, v)
        requested_edge = self.neighbours_list[u][second_vertex_index]

        weight = requested_edge[1]
        edge_coordinates = requested_edge[2]

        edge_new_data = (v, weight, edge_coordinates, color, requested_edge[4], requested_edge[5])
        self.neighbours_list[u][second_vertex_index] = edge_new_data

        if not self.is_directed:
            first_vertex_index = self.find_given_neighbour(v, u)
            requested_edge = self.neighbours_list[v][first_vertex_index]

            self.neighbours_list[v][first_vertex_index] = (
                u, requested_edge[1], requested_edge[2], color, requested_edge[4], requested_edge[5])

    def edge_translation(self, first_vertex, second_vertex, dx, dy):
        """
        Funkcja służąca do przesuwania krawędzi (podwójnych, przeciwnie skierowanych).
        """

        second_vertex_index = self.find_given_neighbour(first_vertex, second_vertex)

        edge_weight = self.neighbours_list[first_vertex][second_vertex_index][1]
        edge_coordinates = self.neighbours_list[first_vertex][second_vertex_index][2]
        edge_color = self.neighbours_list[first_vertex][second_vertex_index][3]
        weight_x = self.neighbours_list[first_vertex][second_vertex_index][4]
        weight_y = self.neighbours_list[first_vertex][second_vertex_index][5]

        start_x, start_y, end_x, end_y = edge_coordinates[0], edge_coordinates[1], edge_coordinates[2], \
                                         edge_coordinates[3]

        edge_old_center_x, edge_old_center_y = (start_x + end_x) / 2, (start_y + end_y) / 2

        weight_transition_x, weight_transition_y = weight_x - edge_old_center_x, weight_y - edge_old_center_y

        start_x += dx
        start_y += dy
        end_x += dx
        end_y += dy

        edge_new_center_x, edge_new_center_y = (start_x + end_x) / 2, (start_y + end_y) / 2

        weight_new_x, weight_new_y = edge_new_center_x + weight_transition_x, edge_new_center_y + weight_transition_y

        if self.check_weight_bounds(weight_new_x, weight_new_y):
            weight_x = weight_new_x
            weight_y = weight_new_y

        self.neighbours_list[first_vertex][second_vertex_index] = (second_vertex, edge_weight,
                                                                   [start_x, start_y, end_x, end_y], edge_color,
                                                                   weight_x, weight_y)

        self.set_graph_saved_flag(False)

    def restore_edges_default_data(self):
        for i in range(0, len(self.neighbours_list)):
            for j in range(0, len(self.neighbours_list[i])):
                edge_data_tuple = self.neighbours_list[i][j]

                edge_new_data_tuple = (edge_data_tuple[0], edge_data_tuple[1], edge_data_tuple[2], colors.normal_color,
                                       edge_data_tuple[4], edge_data_tuple[5])
                self.neighbours_list[i][j] = edge_new_data_tuple

    def get_edge(self, u, v):
        v_index = self.find_given_neighbour(u, v)

        if v_index is not None:
            return self.neighbours_list[u][v_index]

    def get_all_edges_data(self):
        return self.neighbours_list

    def get_edge_data_for_loop(self, i, j):
        return (self.neighbours_list[i][j][0], self.neighbours_list[i][j][1], self.neighbours_list[i][j][2],
                self.neighbours_list[i][j][3], self.neighbours_list[i][j][4], self.neighbours_list[i][j][5])

    def alter_edge_coordinates_after_vertices_resize(self):
        for i in range(0, len(self.neighbours_list)):
            for j in range(0, len(self.neighbours_list[i])):
                first_vertex = i
                second_vertex = self.neighbours_list[i][j][0]

                try:
                    nsx, nsy, nex, ney = self.correction(first_vertex, second_vertex)
                except TypeError:
                    return

                self.neighbours_list[i][j] = (self.neighbours_list[i][j][0], self.neighbours_list[i][j][1],
                                              [nsx, nsy, nex, ney], self.neighbours_list[i][j][3],
                                              self.neighbours_list[i][j][4], self.neighbours_list[i][j][5])

    def check_if_over_edge_weight(self, mouse_x, mouse_y):
        for i in range(0, len(self.neighbours_list)):
            for j in range(0, len(self.neighbours_list[i])):
                weight, weight_x, weight_y = self.neighbours_list[i][j][1], self.neighbours_list[i][j][4], \
                                             self.neighbours_list[i][j][5]

                if weight is not None:
                    number_of_digits = len(str(weight))

                    total_width = number_of_digits * constants.space_for_one_digit
                    height = constants.height

                    upper_x_bound = weight_x + total_width
                    upper_y_bound = weight_y + height

                    if weight_x <= mouse_x <= upper_x_bound and weight_y <= mouse_y <= upper_y_bound:
                        return True, i, j

        return False, None, None

    def alter_edge_weight_coordinates(self, i, j, new_x, new_y):
        edge_new_data = (self.neighbours_list[i][j][0], self.neighbours_list[i][j][1], self.neighbours_list[i][j][2],
                         self.neighbours_list[i][j][3], new_x, new_y)

        self.neighbours_list[i][j] = edge_new_data

        self.set_graph_saved_flag(False)

    def get_residual_edge_coordinates(self, first_vertex, second_vertex):
        edge_coordinates = None
        found = False

        for i in range(0, len(self.neighbours_list[first_vertex])):
            current_vertex = self.neighbours_list[first_vertex][i][0]

            if current_vertex == second_vertex:
                edge_coordinates = copy.copy(self.neighbours_list[first_vertex][i][2])
                found = True
                break

        if not found:
            first_vertex, second_vertex = second_vertex, first_vertex

            for i in range(0, len(self.neighbours_list[first_vertex])):
                current_vertex = self.neighbours_list[first_vertex][i][0]

                if current_vertex == second_vertex:
                    edge_coordinates = copy.copy(self.neighbours_list[first_vertex][i][2])
                    break

            temp1 = edge_coordinates[0:2]
            temp2 = edge_coordinates[2:4]

            edge_coordinates[0:2] = temp2
            edge_coordinates[2:4] = temp1

        return found, edge_coordinates

    def toggle_reversed_flag(self):
        if self.is_graph_reversed:
            self.is_graph_reversed = False
        else:
            self.is_graph_reversed = True

    def reverse_graph(self):
        """
        Funkcja służąca do tworzenia grafu odwrotnego.
        """

        n = len(self.neighbours_list)
        reversed_neighbours_list = [[] for i in range(0, n)]
        reversed_helping_neighbours_list = [[] for i in range(0, n)]

        self.toggle_reversed_flag()

        for i in range(0, n):
            for j in range(0, len(self.neighbours_list[i])):
                neighbour_vertex_number = self.neighbours_list[i][j][0]
                edge_weight = self.neighbours_list[i][j][1]
                edge_coordinates = self.neighbours_list[i][j][2]
                edge_color = self.neighbours_list[i][j][3]
                edge_weight_x = self.neighbours_list[i][j][4]
                edge_weight_y = self.neighbours_list[i][j][5]

                temp1 = edge_coordinates[0:2]
                temp2 = edge_coordinates[2:4]

                edge_coordinates[0:2] = temp2
                edge_coordinates[2:4] = temp1

                reversed_edge = (i, edge_weight, edge_coordinates, edge_color, edge_weight_x, edge_weight_y)

                reversed_neighbours_list[neighbour_vertex_number].append(reversed_edge)
                reversed_helping_neighbours_list[neighbour_vertex_number].append((i, edge_weight))

        self.neighbours_list = reversed_neighbours_list
        self.helping_neighbour_list = reversed_helping_neighbours_list

    def reverse_directed_edge(self, edge_coordinates):
        edge_coordinates_copy = copy.copy(edge_coordinates)

        temp1 = edge_coordinates_copy[0:2]
        temp2 = edge_coordinates_copy[2:4]

        edge_coordinates_copy[0:2] = temp2
        edge_coordinates_copy[2:4] = temp1

        return edge_coordinates_copy

    def create_residual_graph(self):
        """
        Funkcja służąca do tworzenia grafu residualnego.
        """

        n = len(self.neighbours_list)
        space_for_one_digit = constants.space_for_one_digit

        residual_graph = [[] for i in range(0, n)]

        for i in range(0, n):
            for j in range(0, len(self.neighbours_list[i])):
                first_vertex, second_vertex = i, self.neighbours_list[i][j][0]
                edge_weight = self.neighbours_list[i][j][1]
                edge_coordinates = self.neighbours_list[i][j][2]
                edge_color = colors.residual_graph_color
                weight_x = self.neighbours_list[i][j][4]
                weight_y = self.neighbours_list[i][j][5]

                residual_data_tuple = (second_vertex, edge_weight, edge_coordinates, edge_color, weight_x,
                                       weight_y, True)

                residual_graph[first_vertex].append(residual_data_tuple)

                reversed_edge_coordinates = self.reverse_directed_edge(edge_coordinates)

                edge_center_x = (reversed_edge_coordinates[0] + reversed_edge_coordinates[2]) / 2
                edge_center_y = (reversed_edge_coordinates[1] + reversed_edge_coordinates[3]) / 2

                edge_center_x += space_for_one_digit / 3
                edge_center_y += space_for_one_digit / 3

                residual_data_tuple = (first_vertex, 0, reversed_edge_coordinates, colors.residual_backward_edge_color,
                                       edge_center_x, edge_center_y, False)

                residual_graph[second_vertex].append(residual_data_tuple)

        self.residual_graph = residual_graph

    def alter_flow_in_residual_graph(self, u, v, new_flow):
        is_edge_visible = True

        if self.residual_graph is not None:

            for i in range(0, len(self.residual_graph[u])):

                if self.residual_graph[u][i][0] == v:

                    if new_flow == 0:
                        is_edge_visible = False

                    edge_altered_data = (self.residual_graph[u][i][0], new_flow, self.residual_graph[u][i][2],
                                         self.residual_graph[u][i][3], self.residual_graph[u][i][4],
                                         self.residual_graph[u][i][5], is_edge_visible)

                    self.residual_graph[u][i] = edge_altered_data

                    break

    def get_residual_edge(self, u, v):
        if self.residual_graph is not None:
            list_with_residual_edge = list(filter(lambda x: x[0] == v, self.residual_graph[u]))
            if len(list_with_residual_edge) <= 0:
                return

            return list_with_residual_edge[0]

    def correction(self, first_center, second_center):
        """
        Funkcja służąca do \"poprawiania\" rysownanych krawędzi tak, aby ich końcówki nie były rysowane w obrębie
        wierzchołków.
        """

        radius = self.vertices_size
        h_radius = (radius + 3) / 2
        first_center_coordinates = self.vertices[first_center]
        second_center_coordinates = self.vertices[second_center]

        fcx = (2 * first_center_coordinates[0] + radius) / 2
        fcy = (2 * first_center_coordinates[1] + radius) / 2
        scx = (2 * second_center_coordinates[0] + radius) / 2
        scy = (2 * second_center_coordinates[1] + radius) / 2

        dx = scx - fcx
        dy = scy - fcy

        length = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

        flag = False

        if abs(length - 0.0) <= constants.difference_precision:
            flag = True

        if not flag:

            try:
                factor = h_radius / length
            except ZeroDivisionError:
                return

            correction_vector = [factor * dx, factor * dy]
            negative_correction_vector = [-factor * dx, -factor * dy]

            beg_x = fcx + correction_vector[0]
            beg_y = fcy + correction_vector[1]
            end_x = scx + negative_correction_vector[0]
            end_y = scy + negative_correction_vector[1]

            return beg_x, beg_y, end_x, end_y
        else:
            return

    def clear_whole_graph_data(self):
        self.neighbours_list = []
        self.helping_neighbour_list = []
        self.vertices = []
        self.set_graph_saved_flag(False)

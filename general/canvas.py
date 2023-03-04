import re
import copy
import math
from resources import colors
from resources import strings
from resources import constants
from general.graph import Graph
from PyQt5.QtCore import Qt, QSize
from dialogs.add_weight_dialog import WeightDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QToolBar, QToolButton, QLabel, QMenu, QAction, QMessageBox, QTextEdit, \
    QHBoxLayout


class Canvas(QWidget):
    """
    Klasa, w której są zaimplementowane metody odpowiedzialne za tworzenie rysunku grafu i manipulowanie nim.
    """

    def __init__(self, parent, application_terminal):
        """
        Funkcja tworząca obiekty klasy Canvas (konstruktor).
        """

        QWidget.__init__(self)

        drawing_layout = QVBoxLayout()
        drawing_layout.setSpacing(0)

        additional_layout = QHBoxLayout()

        self.parent = parent
        self.canvas_application_terminal = application_terminal

        tool_bar = QToolBar()

        self.vertices_tool = QToolButton()
        self.vertices_tool.setText(strings.add_vertex_action)
        self.vertices_tool.setCheckable(True)
        self.vertices_tool.setAutoExclusive(True)
        self.vertices_tool.clicked.connect(self.adding_vertices_mode)
        tool_bar.addWidget(self.vertices_tool)

        self.edges_tool = QToolButton()
        self.edges_tool.setText(strings.add_edge_action)
        self.edges_tool.setCheckable(True)
        self.edges_tool.setAutoExclusive(True)
        self.edges_tool.clicked.connect(self.adding_edges_mode)
        tool_bar.addWidget(self.edges_tool)

        self.off_tool = QToolButton()
        self.off_tool.setText(strings.normal_mode_action)
        self.off_tool.setCheckable(True)
        self.off_tool.setAutoExclusive(True)
        self.off_tool.setChecked(True)
        self.off_tool.clicked.connect(self.off_mode)
        tool_bar.addWidget(self.off_tool)

        self.display_vertices_data_tool = QToolButton()
        self.display_vertices_data_tool.setText(strings.vertices_data_action)
        self.display_vertices_data_tool.setCheckable(True)
        self.display_vertices_data_tool.setAutoExclusive(True)
        self.display_vertices_data_tool.clicked.connect(self.display_example_vertices_data)
        tool_bar.addWidget(self.display_vertices_data_tool)

        self.restore_tool = QToolButton()
        self.restore_tool.setText(strings.restore_action)
        self.restore_tool.setCheckable(True)
        self.restore_tool.setAutoExclusive(True)
        self.restore_tool.clicked.connect(self.restore_canvas)
        tool_bar.addWidget(self.restore_tool)

        self.clear_canvas_tool = QToolButton()
        self.clear_canvas_tool.setText(strings.clear_action)
        self.clear_canvas_tool.setCheckable(True)
        self.clear_canvas_tool.setAutoExclusive(True)
        self.clear_canvas_tool.clicked.connect(self.show_clearing_warning_dialog)
        tool_bar.addWidget(self.clear_canvas_tool)

        self.drawing_label = QLabel()

        self.counter = 0

        self.beg_x = None
        self.beg_y = None
        self.end_x = None
        self.end_y = None

        self.v_start = None
        self.v_end = None

        self.v_to_update = None

        self.graph = Graph()

        self.selected_edge = None
        self.selected_vertex = None

        self.vertices_color = colors.normal_color

        self.vertices_size = constants.default_vertex_size
        self.edges_width = constants.default_line_width

        self.adding_vertices_selected = False
        self.adding_edges_selected = False
        self.normal_mode_selected = True
        self.displaying_vertices_data_mode_selected = False

        self.animation_running = False
        self.animation_type = None

        self.graph_vertices_size = constants.default_vertex_size

        self.selected_edge_vertices = None

        self.selected_weight_position1 = None
        self.selected_weight_position2 = None

        self.selected_vertex_data = None

        self.moving_edge_start_x = None
        self.moving_edge_start_y = None
        self.moving_edge_first_vertex = None
        self.moving_edge_second_vertex = None
        self.double_directed_edge_flag = False

        self.mouse_start_x = None
        self.mouse_start_y = None

        self.first_time = True

        self.vertex_data_vector = None

        pix_map_size = QSize(self.parent.width(), self.parent.height())

        pix_map = QPixmap(pix_map_size)
        pix_map.fill(Qt.white)

        self.drawing_label.setPixmap(pix_map)
        self.drawing_label.setMouseTracking(True)
        self.drawing_label.setMargin(0)

        self.drawing_label.setMaximumWidth(parent.width())
        self.drawing_label.setFixedHeight(parent.height())

        self.algorithm_presentation = QTextEdit()
        self.algorithm_presentation.setReadOnly(True)

        self.algorithm_presentation.setMinimumWidth(constants.algorithm_presentation_window_width)

        drawing_layout.addWidget(tool_bar)

        additional_layout.addWidget(self.drawing_label)
        additional_layout.addWidget(self.algorithm_presentation)

        drawing_layout.addLayout(additional_layout)

        self.setLayout(drawing_layout)

    def get_canvas_graph(self):
        """
        Funkcja zwracająca graf znajdujący się na danym \"płótnie\".
        """

        return self.graph

    def get_animation_type(self):
        """
        Funkcja zwracająca algortym, którego animacja jest uruchomiona na danym \"płótnie\".
        """

        return self.animation_type

    def get_animation_running_flag(self):
        """
        Funkcja zwracająca informację o tym, czy na danym płótnie jest uruchomiona jakaś
        animacja  (wartość logiczna True/False).
        """

        return self.animation_running

    def clear_algorithm_presentation(self):
        """
        Funkcja służąca do usunięcia zbędnego pseudokodu.
        """

        self.algorithm_presentation.clear()

    def append_whole_pseudocode(self, whole_pseudocode):
        """
        Funkcja służąca do wyświetlenia danego pseudokodu.
        """

        for line in whole_pseudocode:
            self.algorithm_presentation.setTextColor(QColor(colors.algorithm_presentation_normal_line_color))
            self.algorithm_presentation.append(line)

    def select_certain_lines_in_pseudocode(self, whole_pseudocode, selected_lines):
        """
        Funkcja służąca do zaznaczenia odpowiednich linii w danym pseudokodzie.
        """

        self.algorithm_presentation.setTextColor(QColor(colors.algorithm_presentation_normal_line_color))
        self.clear_algorithm_presentation()

        n = len(whole_pseudocode)

        for i in range(0, n):
            current_line = whole_pseudocode[i]

            if i + 1 in selected_lines:
                self.algorithm_presentation.setTextColor(QColor(colors.algorithm_presentation_selected_line_color))
                self.algorithm_presentation.append(current_line)
            else:
                self.algorithm_presentation.setTextColor(QColor(colors.algorithm_presentation_normal_line_color))
                self.algorithm_presentation.append(current_line)

    def restore_algorithm_presentation(self):
        """
        Funkcja służąca do przywrócenia stanu początkowego danego pseudokodu (nie ma wyróżnionych linii w pseudokodzie).
        """

        self.clear_algorithm_presentation()

        if self.animation_type == strings.prim_final_result:
            self.append_whole_pseudocode(strings.whole_prim_pseudocode)

        elif self.animation_type == strings.kruskal_final_result:
            self.append_whole_pseudocode(strings.whole_kruskal_pseudocode)

        elif self.animation_type == strings.scc_final_result:
            self.append_whole_pseudocode(strings.whole_scc_pseudocode)

        elif self.animation_type == strings.ford_fulkerson_final_result or self.animation_type == strings.edmonds_karp_final_result:
            self.append_whole_pseudocode(strings.whole_max_flow_pseudocode)

    def adding_vertices_mode(self):
        """
        Funkcja włączająca tryb dodawania nowych wierzchołków.
        """

        self.turn_off_displaying_vertices_example_data()
        self.adding_edges_selected = False
        self.normal_mode_selected = False
        self.adding_vertices_selected = True
        self.displaying_vertices_data_mode_selected = False

    def adding_edges_mode(self):
        """
        Funkcja włączająca tryb dodawania nowych krawędzi.
        """

        self.turn_off_displaying_vertices_example_data()
        self.adding_vertices_selected = False
        self.normal_mode_selected = False
        self.adding_edges_selected = True
        self.displaying_vertices_data_mode_selected = False

    def off_mode(self):
        """
        Funkcja włączająca tryb normalny.
        """

        if self.graph.get_changed_after_animation_flag():
            return

        self.turn_off_displaying_vertices_example_data()
        self.adding_edges_selected = False
        self.adding_vertices_selected = False
        self.normal_mode_selected = True
        self.displaying_vertices_data_mode_selected = False

    def display_example_vertices_data(self):
        """
        Funkcja wyświetlająca przykładowe dane związane z wierzchołkami.
        """

        if self.graph.get_changed_after_animation_flag():
            return

        self.displaying_vertices_data_mode_selected = True
        self.adding_edges_selected = False
        self.normal_mode_selected = False
        self.adding_vertices_selected = False

        for i in range(0, len(self.graph.get_all_vertices_data())):
            self.graph.alter_vertex_additional_data(i, str(i))

        self.clear()
        self.redraw()

    def turn_off_displaying_vertices_example_data(self):
        """
        Funkcja wyłączająca tryb wyświetlania przykładowych danych związanych z wierzchołkami.
        """

        if self.displaying_vertices_data_mode_selected:
            self.displaying_vertices_data_mode_selected = False

            self.restore_canvas()

    def get_canvas_graph_reversed_flag(self):
        """
        Funkcja zwracająca informację o tym, czy dany graf jest grafem odwrotnym (wartość logiczna True/False).
        """

        reversed_flag = self.graph.get_graph_reversed_flag()

        return reversed_flag

    def set_canvas_vertices_counter_from_neighbours_list(self):
        """
        Funkcja ustawiająca licznik wierzchołków (potrzebna, gdy rysunek jest otwierany z pliku).
        """

        self.counter = self.graph.get_number_of_vertices_in_graph()

    def show_clearing_warning_dialog(self):
        """
        Funkcja wyświetlająca dialog z ostrzeżeniem, o możliwości utraty wszystkich danych związanych z grafem.
        """

        def _off_mode_helper():
            self.off_tool.setChecked(True)
            self.off_mode()
            self.update()

        warning_box = QMessageBox()

        warning_box.setIcon(QMessageBox.Warning)

        warning_box.setWindowTitle(strings.warning_text)
        warning_box.setText(strings.warning_dialog_informative_text)

        warning_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return_value = warning_box.exec()

        if return_value == QMessageBox.Ok:
            self.clear_whole_canvas_data()
            _off_mode_helper()
        else:
            _off_mode_helper()
            return

    def clear_whole_canvas_data(self):
        """
        Funkcja służąca do usunięcia bieżącego rysunku grafu (z \"płótna\").
        """

        self.graph.clear_whole_graph_data()
        self.graph.set_graph_saved_flag(False)
        self.counter = 0

        self.clear()
        self.redraw()

    def set_animation_running(self, new_value):
        """
        Funkcja ustawiająca flagę oznaczjącą, że na danym \"płótnie\" jest uruchomiona animacja. Funkcja nie
        powoduje żadnych innych efektów (tylko zmiana flagi animation_running).
        """

        self.animation_running = new_value

    def set_animation_running_to_true(self, animation_type):
        self.animation_running = True
        self.animation_type = animation_type

        self.vertices_tool.setEnabled(False)
        self.edges_tool.setEnabled(False)
        self.off_tool.setEnabled(False)
        self.display_vertices_data_tool.setEnabled(False)
        self.clear_canvas_tool.setEnabled(False)
        self.restore_tool.setEnabled(False)
        self.graph.set_changed_after_animation()

        self.update()

    def set_animation_running_to_false(self):
        self.animation_running = False
        self.animation_type = None

        self.vertices_tool.setEnabled(True)
        self.edges_tool.setEnabled(True)
        self.off_tool.setEnabled(True)
        self.display_vertices_data_tool.setEnabled(True)
        self.clear_canvas_tool.setEnabled(True)
        self.restore_tool.setEnabled(True)

        self.off_mode()
        self.off_tool.setChecked(True)

        self.update()

    def alter_graph_vertices_size(self, vertices_new_size):
        """
        Funkcja służąca do zmiany rozmiarów wierzchołków w danym grafie.
        """

        self.vertices_size = vertices_new_size

        self.graph.set_vertices_size(vertices_new_size)

        self.graph.alter_edge_coordinates_after_vertices_resize()

        self.clear()
        self.redraw()

    def contextMenuEvent(self, event):
        """
        Funkcja włączająca menu kontekstowe.
        """

        if not self.animation_running:
            context_menu = QMenu()

            remove_vertex_action = QAction(strings.delete_vertex_action)
            remove_vertex_action.triggered.connect(lambda: self.remove_vertex_from_graph(event))
            context_menu.addAction(remove_vertex_action)
            context_menu.addSeparator()

            remove_edge_action = QAction(strings.delete_edge_action)
            remove_edge_action.triggered.connect(lambda: self.remove_edge_from_graph(event))
            context_menu.addAction(remove_edge_action)
            context_menu.addSeparator()

            add_weight_action = QAction(strings.add_weight_action)
            add_weight_action.triggered.connect(lambda: self.display_add_weight_dialog(event))
            context_menu.addAction(add_weight_action)
            context_menu.addSeparator()

            automatically_add_weights = QAction(strings.add_weight_action_auto)
            automatically_add_weights.triggered.connect(lambda: self.add_random_weights_to_all_edges(event))
            context_menu.addAction(automatically_add_weights)
            context_menu.addSeparator()

            cancel_action = QAction(strings.cancel_operations_action)
            cancel_action.triggered.connect(self.context_menu_cancel_operation)
            context_menu.addAction(cancel_action)

            context_menu.aboutToHide.connect(self.context_menu_cancel_operation)

            _ = context_menu.exec(self.mapToGlobal(event.pos()))

    def check_bounds(self, current_x, current_y, flag=False):
        """
        Funkcja sprawdzająca, czy dane współrzędne nie wychodzą poza miejsce do rysowania.
        """

        lower_x_value = constants.lower_x_value
        upper_x_value = constants.upper_x_value

        lower_y_value = constants.lower_y_value
        upper_y_value = constants.upper_y_value

        l_weight_x = constants.lower_weight_x_value
        l_weight_y = constants.lower_weight_y_value

        if flag:
            if current_x >= upper_x_value or current_x <= l_weight_x or current_y >= upper_y_value or current_y <= l_weight_y:
                return False

            return True
        else:
            if current_x >= upper_x_value or current_x <= lower_x_value or current_y >= upper_y_value or current_y <= lower_y_value:
                return False

            return True

    def remove_vertex_from_graph(self, event):
        """
        Funkcja służąca do usuwania wybranego wierzchołka z grafu.
        """

        mx, my = self.get_mapped_mouse_position(event)

        result, vertex_number = self.graph.check_if_over_vertex(mx, my)

        if result:
            self.counter -= 1

            self.graph.decrement_vertices_numbers(vertex_number)

            self.graph.remove_vertex(vertex_number)

            self.graph.remove_deleted_vertex_from_neighbours_list(vertex_number)

            self.graph.decrement_vertices_numbers_in_neighbours_list(vertex_number)

            self.selected_vertex = None

            self.clear()
            self.redraw()

    def remove_edge_from_graph(self, event):
        """
        Funkcja służąca do usuwania wybranej krawędzi z grafu.
        """

        click_x, click_y = self.get_mapped_mouse_position(event)

        first_vertex, second_vertex, result = self.graph.check_if_over_edge(click_x, click_y)

        if result:
            self.graph.remove_edge(first_vertex, second_vertex)

            self.selected_edge = None

            self.clear()
            self.redraw()

    def set_first_time_flag(self, new_value):
        self.first_time = new_value

    def display_add_weight_dialog(self, event):
        """
        Funkcja odpowiadająca za wyświetlenie okienka dialogowego i pobranie wagi wybranej krawędzi od użytkownika.
        """

        click_x, click_y = self.get_mapped_mouse_position(event)

        first_vertex, second_vertex, result = self.graph.check_if_over_edge(click_x, click_y)

        if result:
            weight_dialog_box = WeightDialog(first_vertex, second_vertex)

            if weight_dialog_box.exec():
                input_value = weight_dialog_box.get_edge_weight()
                is_input_valid = self.validate_input(input_value)

                if is_input_valid:
                    weight = int(input_value)

                    if self.graph.get_is_directed_flag():
                        self.graph.set_edge_weight_for_directed_graph(first_vertex, second_vertex, weight)
                    else:
                        self.graph.set_edge_weight_for_undirected_graph(first_vertex, second_vertex, weight)

                    self.set_first_time_flag(True)

                    self.clear()
                    self.redraw()

                    self.set_first_time_flag(False)

                else:
                    self.canvas_application_terminal.display_error_messages(
                        [strings.edge_weight_not_valid_error_message])
            else:
                return

    def add_random_weights_to_all_edges(self, event):
        """
        Funkcja służąca do dodawania losowych wag do wszystkich krawędzi w grafie.
        """

        click_x, click_y = self.get_mapped_mouse_position(event)

        first_vertex, second_vertex, result = self.graph.check_if_over_edge(click_x, click_y)

        if result:
            self.graph.set_random_weights_to_all_edges_in_graph()

            self.set_first_time_flag(True)

            self.clear()
            self.redraw()

            self.set_first_time_flag(False)

    def context_menu_cancel_operation(self):
        """
        Funkcja przywracająca pierwotny kolor wybranych przez użytkownika wierzchołków lub krawędzi.
        """

        if self.selected_vertex is not None:
            cx, cy, number = self.selected_vertex[0], self.selected_vertex[1], self.selected_vertex[2]

            self.graph.alter_vertex_color(number, colors.normal_color)

            self.clear()
            self.redraw()

            self.selected_vertex = None

        elif self.selected_edge is not None:
            first_vertex, second_vertex = self.selected_edge_vertices

            self.graph.alter_edge_color(first_vertex, second_vertex, colors.normal_color)

            self.clear()
            self.redraw()

            self.selected_edge = None
            self.selected_edge_vertices = None

    def validate_input(self, edge_weight):
        """
        Funkcja służąca do sprawdzania poprawności wagi, pobranej od użytkownika.
        """

        matches = re.findall("^[-]?[0-9]+$", edge_weight)

        if len(matches) == 1:
            return True
        else:
            return False

    def mousePressEvent(self, event):
        """
        Funkcja obsługująca zdarzenia związane z wciśnięciem przycisku (lewego/prawego) myszy.
        """

        flag = self.graph.get_changed_after_animation_flag()

        if flag or self.animation_running:
            return

        elif event.buttons() & Qt.LeftButton & self.adding_vertices_selected:
            x, y = self.get_mapped_mouse_position(event)

            if not self.check_bounds(x, y):
                return

            self.graph.add_new_vertex(x, y, self.counter, colors.normal_color)

            self.draw_vertices(x, y, colors.normal_color)

        elif event.buttons() & Qt.LeftButton & self.adding_edges_selected:
            current_x, current_y = self.get_mapped_mouse_position(event)
            result, number = self.graph.check_if_over_vertex(current_x, current_y)

            if result:
                self.v_start, self.beg_x, self.beg_y = number, current_x, current_y

        elif event.buttons() & Qt.LeftButton & self.normal_mode_selected:
            current_x, current_y = self.get_mapped_mouse_position(event)

            over_vertex_result, number = self.graph.check_if_over_vertex(current_x, current_y)
            over_weight_result, position1, position2 = self.graph.check_if_over_edge_weight(current_x, current_y)
            first_vertex, second_vertex, over_edge_result = self.graph.check_if_over_edge(current_x, current_y)

            if over_vertex_result:
                self.v_to_update, self.mouse_start_x, self.mouse_start_y = number, current_x, current_y

                vertex_x, vertex_y, _, _, _, data_x, data_y = self.graph.get_vertex(self.v_to_update)

                self.vertex_data_vector = [data_x - vertex_x, data_y - vertex_y]
            elif over_weight_result:
                self.selected_weight_position1 = position1
                self.selected_weight_position2 = position2
            elif over_edge_result:
                if self.graph.get_is_directed_flag():
                    self.double_directed_edge_flag = self.graph.check_for_double_directed_edge(first_vertex,
                                                                                               second_vertex)
                    if self.double_directed_edge_flag:
                        self.moving_edge_start_x = current_x
                        self.moving_edge_start_y = current_y

                        self.moving_edge_first_vertex = first_vertex
                        self.moving_edge_second_vertex = second_vertex

        elif event.buttons() & Qt.RightButton:
            click_x, click_y = self.get_mapped_mouse_position(event)

            first_vertex, second_vertex, over_edge_result = self.graph.check_if_over_edge(click_x, click_y)
            over_vertex_result, vertex_number = self.graph.check_if_over_vertex(click_x, click_y)

            if over_edge_result:

                self.selected_edge = self.graph.get_edge(first_vertex, second_vertex)
                self.selected_edge_vertices = (first_vertex, second_vertex)

                self.graph.alter_edge_color(first_vertex, second_vertex, colors.selected_color)

                self.clear()
                self.redraw()

            elif over_vertex_result:

                vertex_data = self.graph.get_vertex(vertex_number)

                self.selected_vertex = vertex_data

                self.graph.alter_vertex_color(vertex_number, colors.selected_color)

                self.clear()
                self.redraw()

        elif event.buttons() & Qt.LeftButton & self.displaying_vertices_data_mode_selected:
            mouse_x, mouse_y = self.get_mapped_mouse_position(event)

            over_data_result, vertex = self.graph.check_if_over_vertex_data(mouse_x, mouse_y)

            if over_data_result:
                self.selected_vertex_data = vertex

    def mouseMoveEvent(self, event):
        """
        Funkcja obsługująca zdarzenia związane z poruszaniem myszy.
        """

        flag = self.graph.get_changed_after_animation_flag()

        if flag or self.animation_running:
            return

        elif self.adding_edges_selected and self.beg_x is not None:
            self.end_x, self.end_y = self.get_mapped_mouse_position(event)

            self.clear()

            self.redraw()
            self.draw_edges(self.beg_x, self.beg_y, self.end_x, self.end_y, colors.normal_color)

            self.end_x, self.end_y = None, None

        elif self.v_to_update is not None:
            current_x, current_y = self.get_mapped_mouse_position(event)

            if not self.check_bounds(current_x, current_y):
                return

            dx = current_x - self.mouse_start_x
            dy = current_y - self.mouse_start_y

            data_dx = self.vertex_data_vector[0]
            data_dy = self.vertex_data_vector[1]

            self.mouse_start_x, self.mouse_start_y = current_x, current_y

            self.graph.alter_vertex_coordinates(self.v_to_update, current_x, current_y, data_dx, data_dy)

            self.graph.alter_edge_coordinates_during_movement(self.v_to_update)

            self.clear()
            self.redraw()

        elif self.moving_edge_start_x is not None and self.moving_edge_start_y is not None:
            if self.graph.get_is_directed_flag():
                current_x, current_y = self.get_mapped_mouse_position(event)

                if not self.check_bounds(current_x, current_y):
                    return

                dx = current_x - self.moving_edge_start_x
                dy = current_y - self.moving_edge_start_y

                self.moving_edge_start_x = current_x
                self.moving_edge_start_y = current_y

                self.graph.edge_translation(self.moving_edge_first_vertex, self.moving_edge_second_vertex, dx, dy)

                self.clear()
                self.redraw()

        elif self.selected_weight_position1 is not None and self.selected_weight_position2 is not None:
            mouse_current_x, mouse_current_y = self.get_mapped_mouse_position(event)

            if not self.check_bounds(mouse_current_x, mouse_current_y, True):
                return

            self.graph.alter_edge_weight_coordinates(self.selected_weight_position1, self.selected_weight_position2,
                                                     mouse_current_x, mouse_current_y)

            if not self.graph.get_is_directed_flag():
                second_vertex = self.graph.get_neighbour_number(self.selected_weight_position1,
                                                                self.selected_weight_position2)
                first_vertex_index = self.graph.find_given_neighbour(second_vertex, self.selected_weight_position1)

                self.graph.alter_edge_weight_coordinates(second_vertex, first_vertex_index, mouse_current_x,
                                                         mouse_current_y)

            self.clear()
            self.redraw()

        elif self.selected_vertex_data is not None:
            mouse_x, mouse_y = self.get_mapped_mouse_position(event)

            if not self.check_bounds(mouse_x, mouse_y, True):
                return

            self.graph.alter_vertex_data_coordinates(self.selected_vertex_data, mouse_x, mouse_y)

            self.clear()
            self.redraw()

    def mouseReleaseEvent(self, event):
        """
        Funkcja obsługująca zdarzenia związane z puszczeniem przycisku myszy.
        """

        flag = self.graph.get_changed_after_animation_flag()

        if flag or self.animation_running:
            return

        elif self.adding_edges_selected and self.beg_x is not None:
            current_x, current_y = self.get_mapped_mouse_position(event)
            self.end_x, self.end_y = current_x, current_y

            result, number = self.graph.check_if_over_vertex(self.end_x, self.end_y)

            if not result:
                self.v_start, self.v_end, self.beg_x, self.beg_y, self.end_x, self.end_y = None, None, None, None, None, None
                self.clear()
                self.redraw()
                return

            self.v_end = number

            if self.v_end is None or self.v_start is None:
                self.clear()
                self.redraw()
                return

            edge_exists_flag = self.graph.check_if_edge_exists(self.v_start, self.v_end)

            if result and self.v_start != self.v_end and not edge_exists_flag:
                self.v_end = number

                try:
                    self.beg_x, self.beg_y, self.end_x, self.end_y = self.graph.correction(self.v_start, self.v_end)
                except TypeError:
                    return

                weight_current_x = (self.beg_x + self.end_x) / 2
                weight_current_y = (self.beg_y + self.end_y) / 2

                self.graph.add_new_edge(self.v_start, self.v_end, [self.beg_x, self.beg_y, self.end_x, self.end_y],
                                        colors.normal_color, weight_current_x, weight_current_y)

                self.clear()
                self.redraw()
            else:
                self.clear()
                self.redraw()

            self.v_start, self.v_end, self.beg_x, self.beg_y, self.end_x, self.end_y = None, None, None, None, None, None

        elif self.v_to_update is not None:
            current_x, current_y = self.get_mapped_mouse_position(event)

            if not self.check_bounds(current_x, current_y):
                return

            dx = current_x - self.mouse_start_x
            dy = current_y - self.mouse_start_y

            data_dx = self.vertex_data_vector[0]
            data_dy = self.vertex_data_vector[1]

            self.graph.alter_vertex_coordinates(self.v_to_update, current_x, current_y, data_dx, data_dy)

            self.graph.alter_edge_coordinates_during_movement(self.v_to_update)

            self.clear()
            self.redraw()

            self.v_to_update, self.mouse_start_x, self.mouse_start_y, self.vertex_data_vector = None, None, None, None

        elif self.moving_edge_start_x is not None and self.moving_edge_start_y is not None:
            if self.graph.get_is_directed_flag():
                current_x, current_y = self.get_mapped_mouse_position(event)

                if not self.check_bounds(current_x, current_y):
                    return

                dx = current_x - self.moving_edge_start_x
                dy = current_y - self.moving_edge_start_y

                self.graph.edge_translation(self.moving_edge_first_vertex, self.moving_edge_second_vertex, dx, dy)

                self.clear()
                self.redraw()

                self.moving_edge_start_x, self.moving_edge_start_y = None, None
                self.moving_edge_first_vertex, self.moving_edge_second_vertex = None, None

                self.double_directed_edge_flag = False

        elif self.selected_weight_position1 is not None and self.selected_weight_position2 is not None:
            mouse_current_x, mouse_current_y = self.get_mapped_mouse_position(event)

            if not self.check_bounds(mouse_current_x, mouse_current_y, True):
                return

            self.graph.alter_edge_weight_coordinates(self.selected_weight_position1, self.selected_weight_position2,
                                                     mouse_current_x, mouse_current_y)

            if not self.graph.get_is_directed_flag():
                second_vertex = self.graph.get_neighbour_number(self.selected_weight_position1,
                                                                self.selected_weight_position2)
                first_vertex_index = self.graph.find_given_neighbour(second_vertex, self.selected_weight_position1)

                self.graph.alter_edge_weight_coordinates(second_vertex, first_vertex_index, mouse_current_x,
                                                         mouse_current_y)

            self.clear()
            self.redraw()

            self.selected_weight_position1, self.selected_weight_position2 = None, None

        elif self.selected_vertex_data is not None:
            mouse_x, mouse_y = self.get_mapped_mouse_position(event)

            if not self.check_bounds(mouse_x, mouse_y, True):
                return

            self.graph.alter_vertex_data_coordinates(self.selected_vertex_data, mouse_x, mouse_y)

            self.selected_vertex_data = None

            self.clear()
            self.redraw()

    def clear(self):
        """
        Funkcja służąca do czyszczenia \"płótna\".
        """

        pix_map = self.drawing_label.pixmap()
        pix_map.fill(Qt.white)
        self.drawing_label.setPixmap(pix_map)

    def vector_normalization(self, dx, dy):
        """
        Funkcja służąca do normalizacji wektorów.
        """

        length = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

        if abs(length - 0.0) >= constants.difference_precision:
            return dx / length, dy / length
        else:
            return dx, dy

    def get_color_from_integer(self, number):
        """Funkcja zwracająca wartość liczbową, odpowiadającą danemu kolorowi."""

        if number == colors.normal_color:
            return colors.normal_color
        elif number == colors.selected_color:
            return colors.selected_color
        elif number == colors.included_color:
            return colors.included_color
        elif number == colors.components_colors[0]:
            return colors.components_colors[0]
        elif number == colors.components_colors[1]:
            return colors.components_colors[1]
        elif number == colors.components_colors[2]:
            return colors.components_colors[2]
        elif number == colors.components_colors[3]:
            return colors.components_colors[3]
        elif number == colors.components_colors[4]:
            return colors.components_colors[4]
        elif number == colors.components_colors[5]:
            return colors.components_colors[5]
        elif number == colors.components_colors[6]:
            return colors.components_colors[6]
        elif number == colors.components_colors[7]:
            return colors.components_colors[7]
        elif number == colors.increase_edge_flow_color:
            return colors.increase_edge_flow_color
        elif number == colors.decrease_edge_flow_color:
            return colors.decrease_edge_flow_color
        elif number == colors.flow_network_color:
            return colors.flow_network_color
        elif number == colors.residual_graph_color:
            return colors.residual_graph_color
        elif number == colors.residual_backward_edge_color:
            return colors.residual_backward_edge_color

    def center_text_in_vertex(self, center_x, center_y):
        """
        Funkcja centrująca tekst w wierzchołku.
        """

        difference = self.vertices_size - constants.default_vertex_size

        if difference == 0:
            return center_x, center_y
        else:
            shift = ((math.sqrt(2)) / 2) * difference

            center_y += shift - 2

            return center_x, center_y

    def draw_vertices(self, cx, cy, color, red=False, count=0):
        """
        Funkcja służąca do rysowania wierzchołków.
        """

        radius = self.vertices_size

        pix_map = self.drawing_label.pixmap()

        painter = QPainter()

        painter.begin(pix_map)

        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.Antialiasing, True)

        painter.setPen(QPen(color, constants.default_circle_line_width, Qt.SolidLine))

        painter.drawEllipse(cx, cy, radius, radius)

        center_x, center_y = self.center_text_in_vertex(cx, cy)

        if not red:
            painter.drawText(center_x, center_y, radius, radius, constants.text_font_size, str(self.counter))
        else:
            painter.drawText(center_x, center_y, radius, radius, constants.text_font_size, str(count))

        painter.end()

        self.drawing_label.setPixmap(pix_map)

        if not red:
            self.counter += 1

    def display_vertices_data(self, vertex, text):
        """
        Funkcja rysująca przykładowe dane związane z wierzchołkami.
        """

        painter = QPainter()
        pix_map = self.drawing_label.pixmap()

        shift = constants.shift_value
        letter_width = constants.space_for_one_digit
        letter_height = constants.height

        _, _, _, _, _, x, y = self.graph.get_vertex(vertex)

        number_of_characters = len(text)

        x_origin = x - number_of_characters * letter_width - shift
        y_origin = y - letter_height - shift

        painter.begin(pix_map)

        painter.setPen(QPen(colors.vertex_data_color, 3, Qt.SolidLine))

        painter.drawText(x_origin, y_origin, number_of_characters * letter_width, letter_height, 4,
                         text)

        painter.end()

        self.drawing_label.setPixmap(pix_map)

    def draw_edges(self, beg_x, beg_y, end_x, end_y, color):
        """
        Funkcja rysująca krawędzie.
        """

        if self.graph.is_directed:

            self.draw_arrow(beg_x, beg_y, end_x, end_y, color)

        else:
            pix_map = self.drawing_label.pixmap()

            painter = QPainter()

            painter.begin(pix_map)

            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

            painter.setPen(QPen(color, self.edges_width, Qt.SolidLine))

            painter.drawLine(beg_x, beg_y, end_x, end_y)

            painter.end()

            self.drawing_label.setPixmap(pix_map)

    def draw_arrow(self, start_x, start_y, end_x, end_y, color):
        """
        Funkcja rysująca krawędzie skierowane (czyli strzałki).
        """

        h_basis_length = constants.arrow_basis_length
        head_height = constants.arrow_head_height

        n_dx = start_x - end_x
        n_dy = start_y - end_y

        vector_length = math.sqrt(math.pow(n_dx, 2) + math.pow(n_dy, 2))

        if abs(vector_length - 0.0) > constants.difference_precision:
            try:
                factor = head_height / vector_length
            except ZeroDivisionError:
                return

            arrow_height_vector_x = factor * n_dx
            arrow_height_vector_y = factor * n_dy

            head_basis_x = end_x + arrow_height_vector_x
            head_basis_y = end_y + arrow_height_vector_y

            perpendicular_vector_length = math.sqrt(math.pow(start_y - end_y, 2) + math.pow(end_x - start_x, 2))

            try:
                first_coordinate_of_perpendicular_vector = (start_y - end_y) / perpendicular_vector_length
                second_coordinate_of_perpendicular_vector = (end_x - start_x) / perpendicular_vector_length
            except ZeroDivisionError:
                return

            first_coordinate_of_negative_perpendicular_vector = (-1) * first_coordinate_of_perpendicular_vector
            second_coordinate_of_negative_perpendicular_vector = (-1) * second_coordinate_of_perpendicular_vector

            perpendicular_vector = [first_coordinate_of_perpendicular_vector,
                                    second_coordinate_of_perpendicular_vector]
            perpendicular_vector_negative = [first_coordinate_of_negative_perpendicular_vector,
                                             second_coordinate_of_negative_perpendicular_vector]

            first_arrow_point_x = head_basis_x + perpendicular_vector[0] * h_basis_length
            first_arrow_point_y = head_basis_y + perpendicular_vector[1] * h_basis_length

            second_arrow_point_x = head_basis_x + perpendicular_vector_negative[0] * h_basis_length
            second_arrow_point_y = head_basis_y + perpendicular_vector_negative[1] * h_basis_length

            pix_map = self.drawing_label.pixmap()

            painter = QPainter()

            painter.begin(pix_map)

            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

            painter.setPen(QPen(color, self.edges_width + 1, Qt.SolidLine))

            painter.drawLine(start_x, start_y, end_x, end_y)

            painter.drawLine(end_x, end_y, first_arrow_point_x, first_arrow_point_y)

            painter.drawLine(end_x, end_y, second_arrow_point_x, second_arrow_point_y)
            painter.drawLine(first_arrow_point_x, first_arrow_point_y, second_arrow_point_x, second_arrow_point_y)

            painter.end()

            self.drawing_label.setPixmap(pix_map)
        else:
            return

    def compute_line_slope(self, edge_coordinates):
        """
        Funkcja obliczająca tangens kąta nachylenia linii (krawędzi).
        """

        nom = edge_coordinates[2] - edge_coordinates[0]
        denom = edge_coordinates[3] - edge_coordinates[1]

        try:
            slope = nom / denom
        except ZeroDivisionError:
            return None

        return slope

    def adjust_edge_weight_coordinates(self, first_vertex, second_vertex, weight_new_x, weight_new_y):
        """
        Funkcja służąca do ustalenia odpowiednich współrzędnych miejsca, gdzie ma być rysowana waga danej krawędzi.
        """

        index = self.graph.find_given_neighbour(first_vertex, second_vertex)

        if index is not None:
            self.graph.alter_edge_weight_coordinates(first_vertex, index, weight_new_x, weight_new_y)

        index = self.graph.find_given_neighbour(second_vertex, first_vertex)

        if index is not None:
            self.graph.alter_edge_weight_coordinates(second_vertex, index, weight_new_x, weight_new_y)

    def check_if_weight_adjusting_is_necessary(self, edge_center_x, edge_center_y, weight_x, weight_y):
        """
        Funkcja sprawdzająca, czy dana krawędź musi mieć ustalone współrzędne miejsca, gdzie ma być rysowana
        waga krawędzi.
        """

        if abs(weight_x - edge_center_x) <= constants.difference_precision and abs(weight_y - edge_center_y) <= constants.difference_precision:
            return True

        return False

    def draw_weight_over_edge(self, first_vertex, second_vertex, weight_value, edge_color, flag=False):
        """
        Funkcja służąca do rysowania wagi danej krawędzi.
        """

        _, _, edge_coordinates, _, weight_x, weight_y = self.graph.get_edge(first_vertex, second_vertex)

        if edge_coordinates is not None:
            number_of_digits = len(str(weight_value))
            space_for_one_digit = constants.space_for_one_digit
            total_width = space_for_one_digit * number_of_digits
            height = constants.height

            edge_center_x = (edge_coordinates[0] + edge_coordinates[2]) / 2
            edge_center_y = (edge_coordinates[1] + edge_coordinates[3]) / 2

            rectangle_x = weight_x
            rectangle_y = weight_y

            if self.first_time and self.check_if_weight_adjusting_is_necessary(edge_center_x, edge_center_y, weight_x, weight_y):
                line_slope = self.compute_line_slope(edge_coordinates)

                if line_slope is None:
                    rectangle_x = edge_center_x + space_for_one_digit / 3
                    rectangle_y = edge_center_y
                    self.adjust_edge_weight_coordinates(first_vertex, second_vertex, rectangle_x, rectangle_y)
                elif abs(line_slope - 0.0) <= constants.difference_precision:
                    rectangle_x = edge_center_x
                    rectangle_y = edge_center_y - space_for_one_digit / 3
                    self.adjust_edge_weight_coordinates(first_vertex, second_vertex, rectangle_x, rectangle_y)
                elif line_slope > 0:
                    rectangle_x = edge_center_x
                    rectangle_y = edge_center_y - height - 2
                    self.adjust_edge_weight_coordinates(first_vertex, second_vertex, rectangle_x, rectangle_y)
                else:
                    rectangle_x = edge_center_x + space_for_one_digit / 3
                    rectangle_y = edge_center_y + space_for_one_digit / 3
                    self.adjust_edge_weight_coordinates(first_vertex, second_vertex, rectangle_x, rectangle_y)

            if flag:
                rectangle_y = rectangle_y + height + 2

            pix_map = self.drawing_label.pixmap()

            painter = QPainter()

            painter.begin(pix_map)

            painter.setPen(QPen(edge_color, 4, Qt.SolidLine))

            painter.drawText(rectangle_x, rectangle_y, total_width, height, 4, str(weight_value))

            painter.end()

            self.drawing_label.setPixmap(pix_map)

    def redraw(self, not_to_redraw=-1):
        """
        Funkcja służąca do \"odrysowywania\" grafu.
        """

        vertices_data = self.graph.get_all_vertices_data()
        neighbours_list = self.graph.get_all_edges_data()

        if len(vertices_data) > 0 or len(neighbours_list) > 0:

            for vertex in vertices_data:
                vx = vertex[0]
                vy = vertex[1]
                number = vertex[2]
                vertex_color = self.get_color_from_integer(int(vertex[3]))
                vertex_data_text = vertex[4]

                if vertex_data_text is not None:
                    self.display_vertices_data(number, vertex_data_text)

                if number != not_to_redraw:
                    self.draw_vertices(vx, vy, vertex_color, True, number)

            for i in range(0, len(neighbours_list)):
                for j in range(0, len(neighbours_list[i])):
                    first_vertex = i
                    neighbour = neighbours_list[i][j]

                    second_vertex, edge_weight, edge_coordinates = neighbour[0], neighbour[1], neighbour[2]

                    sx, sy, ex, ey = edge_coordinates

                    edge_color = self.get_color_from_integer(neighbour[3])

                    self.draw_edges(sx, sy, ex, ey, edge_color)

                    if edge_weight is not None:
                        self.draw_weight_over_edge(first_vertex, second_vertex, edge_weight, edge_color)

    def select_vertex(self, vertex):
        """
        Funkcja oznaczająca dany wierzchołek jako przetwarzany (kolor fioletowy).
        """

        self.graph.alter_vertex_color(vertex, colors.selected_color)

        self.clear()
        self.redraw()

    def select_edge(self, u, v):
        """
        Funkcja oznaczająca daną krawędź jako przetwarzaną (kolor fioletowy).
        """

        self.graph.alter_edge_color(u, v, colors.selected_color)

        self.clear()
        self.redraw()

    def include_vertex(self, vertex):
        """
        Funkcja oznaczająca dany wierzchołek jako element jakiejś struktury (np. dany wierzchołek należy do MST).
        """

        self.graph.alter_vertex_color(vertex, colors.included_color)

        self.clear()
        self.redraw()

    def include_edge(self, u, v):
        """
        Funkcja oznaczająca daną krawędź jako element jakiejś struktury (np. dana krawędź należy do MST).
        """

        self.graph.alter_edge_color(u, v, colors.included_color)

        self.clear()
        self.redraw()

    def exclude_vertex(self, vertex):
        """
        Funkcja oznaczająca dany wierzchołek jako aktualnie nieprzetwarzany.
        """

        self.graph.alter_vertex_color(vertex, colors.normal_color)

        self.clear()
        self.redraw()

    def exclude_edge(self, u, v):
        """
        Funkcja oznaczająca daną krawędź jako aktualnie nieprzetwarzaną.
        """

        self.graph.alter_edge_color(u, v, colors.normal_color)

        self.clear()
        self.redraw()

    def display_current_MST(self, array):
        """
        Funkcja rysująca aktualne minimalne drzewo rozpinające.
        """

        for i in range(0, len(array)):
            if array[i] == -1:
                continue

            self.include_edge(i, array[i])

    def set_vertices_data_text(self, data_text_list):
        """
        Funkcja ustalająca dane związane z poszczególnymi wierzchołkami.
        """

        for i in range(0, len(self.graph.get_all_vertices_data())):
            self.graph.alter_vertex_additional_data(i, data_text_list[i])

        self.clear()
        self.redraw()

    def draw_reversed_graph(self):
        """
        Funkcja rysująca graf odwrotny.
        """

        self.graph.reverse_graph()

        self.clear()
        self.redraw()

    def clear_dfs_path(self):
        """
        Funkcja służąca do \"odznaczania\" krawędzi (po operacji mają kolor czarny), wchodzących w skład ścieżki
        znalezionej przez algorytm DFS.
        """

        self.graph.restore_vertices_default_color()
        self.graph.restore_edges_default_data()

        self.clear()
        self.redraw()

    def mark_vertex_using_custom_color(self, vertex_number, color):
        """
        Funkcja służąca do oznaczenia wierzchołka dowolnym kolorem.
        """

        self.graph.alter_vertex_color(vertex_number, color)

        self.clear()
        self.redraw()

    def mark_connected_components(self, connected_components):
        """
        Funkcja służąca do oznaczania znalezionych silnie spójnych składowych w grafie skierowanym.
        """

        marking_colors = colors.components_colors
        components = eval(connected_components)

        for i in components.keys():
            vertices_in_components = components.get(i)
            first_vertex_in_component = vertices_in_components[0]
            position = int(i) % len(marking_colors)
            marking_color = marking_colors[position]

            self.display_vertices_data(first_vertex_in_component, str(i))

            for vertex in vertices_in_components:
                self.mark_vertex_using_custom_color(vertex, marking_color)

    def display_flow_network(self, flow_network):
        """
        Funkcja służąca do wyświetlenia aktualnej sieci przepływowej.
        """

        self.graph.set_flow_network(flow_network)

        self.clear()

        for i in range(0, len(flow_network)):
            vx, vy, vertex_number, _, _, _, _ = self.graph.get_vertex(i)

            self.draw_vertices(vx, vy, colors.flow_network_color, True, vertex_number)

        for i in range(0, len(flow_network)):
            for j in range(0, len(flow_network[i])):
                first_vertex = i
                second_vertex = flow_network[i][j][0]
                edge_flow = flow_network[i][j][1]
                edge_color = self.get_color_from_integer(flow_network[i][j][2])

                _, edge_capacity, edge_coordinates, _, _, _ = self.graph.get_edge_data_for_loop(i, j)

                edge_beg_x, edge_beg_y, edge_end_x, edge_end_y = edge_coordinates

                text_over_edge = f"{copy.copy(edge_flow)}/{edge_capacity}"

                self.draw_edges(edge_beg_x, edge_beg_y, edge_end_x, edge_end_y, edge_color)
                self.draw_weight_over_edge(first_vertex, second_vertex, text_over_edge, edge_color)

    def get_residual_edge_coordinates(self, first_vertex, second_vertex):
        """
        Funkcja służąca do pobierania współrzędnych danej krawędzi w grafie residualnym.
        """

        found, edge_coordinates = self.graph.get_residual_edge_coordinates(first_vertex, second_vertex)
        return found, edge_coordinates

    def display_residual_graph(self, residual_graph):
        """
        Funkcja służąca do wyświetlenia bieżącego grafu residualnego.
        """

        self.graph.set_residual_graph(residual_graph)

        self.clear()

        for i in range(0, len(residual_graph)):
            vx, vy, vertex_number, _, _, _, _ = self.graph.get_vertex(i)

            self.draw_vertices(vx, vy, colors.residual_graph_color, True, vertex_number)

        for i in range(0, len(residual_graph)):
            for j in range(0, len(residual_graph[i])):
                first_vertex = i
                second_vertex = residual_graph[i][j][0]
                edge_capacity = residual_graph[i][j][1]
                found, edge_coordinates = self.get_residual_edge_coordinates(first_vertex, second_vertex)

                edge_beg_x, edge_beg_y, edge_end_x, edge_end_y = edge_coordinates

                if found:
                    self.draw_edges(edge_beg_x, edge_beg_y, edge_end_x, edge_end_y, colors.residual_graph_color)
                    self.draw_weight_over_edge(first_vertex, second_vertex, edge_capacity, colors.residual_graph_color)
                else:
                    self.draw_edges(edge_beg_x, edge_beg_y, edge_end_x, edge_end_y, colors.residual_backward_edge_color)
                    self.draw_weight_over_edge(second_vertex, first_vertex, edge_capacity,
                                               colors.residual_backward_edge_color, True)

    def display_augumenting_path(self, augumenting_path):
        """
        Funkcja służąca do wyświetlenia znalezionej s-t ścieżki (ścieżka ze źródła do ujścia).
        """

        for edge in augumenting_path:
            u, v = edge

            found, edge_coordinates = self.get_residual_edge_coordinates(u, v)

            edge_beg_x, edge_beg_y, edge_end_x, edge_end_y = edge_coordinates

            edge_capacity = None

            for i in range(0, len(self.graph.residual_graph[u])):
                if self.graph.residual_graph[u][i][0] == v:
                    edge_capacity = self.graph.residual_graph[u][i][1]
                    break

            if found:
                self.draw_edges(edge_beg_x, edge_beg_y, edge_end_x, edge_end_y, colors.selected_color)
                self.draw_weight_over_edge(u, v, edge_capacity, colors.selected_color)
            else:
                self.draw_edges(edge_beg_x, edge_beg_y, edge_end_x, edge_end_y, colors.selected_color)
                self.draw_weight_over_edge(v, u, edge_capacity, colors.selected_color, True)

    def select_residual_edge(self, u, v):
        """
        Funkcja służąca do zaznaczenia danej krawędzi w grafie residualnym (krawędź z najmniejszą przepustowością).
        """

        found, edge_coordinates = self.get_residual_edge_coordinates(u, v)

        edge_beg_x, edge_beg_y, edge_end_x, edge_end_y = edge_coordinates

        edge_capacity = None

        for i in range(0, len(self.graph.residual_graph[u])):
            if self.graph.residual_graph[u][i][0] == v:
                edge_capacity = self.graph.residual_graph[u][i][1]
                break

        if found:
            self.draw_edges(edge_beg_x, edge_beg_y, edge_end_x, edge_end_y, colors.bottleneck_edge_color)
            self.draw_weight_over_edge(u, v, edge_capacity, colors.bottleneck_edge_color)
        else:
            self.draw_edges(edge_beg_x, edge_beg_y, edge_end_x, edge_end_y, colors.bottleneck_edge_color)
            self.draw_weight_over_edge(v, u, edge_capacity, colors.bottleneck_edge_color, True)

    def display_altered_edge_flow(self, u, v, flow, edge_color):
        """
        Funkcja służąca do modyfikacji przepływu na danej krawędzi.
        """

        requested_edge = None
        second_vertex_index = None

        for i in range(0, len(self.graph.flow_network[u])):
            current_vertex_number = self.graph.flow_network[u][i][0]

            if current_vertex_number == v:
                requested_edge = self.graph.flow_network[u][i]
                second_vertex_index = i
                break

        if requested_edge is not None and second_vertex_index is not None:
            edge_new_data = (requested_edge[0], flow, edge_color)
            self.graph.flow_network[u][second_vertex_index] = edge_new_data

            self.display_flow_network(self.graph.flow_network)

            edge_new_data = (requested_edge[0], flow, colors.flow_network_color)
            self.graph.flow_network[u][second_vertex_index] = edge_new_data

    def restore_canvas(self):
        """
        Funkcja przywracjąca pierwotny stan płótna do rysowania.
        """

        self.graph.restore_vertices_default_data()
        self.graph.restore_edges_default_data()
        self.graph.unset_changed_after_animation()

        self.clear_algorithm_presentation()
        self.clear()
        self.redraw()

    def get_mapped_mouse_position(self, event):
        """
        Funkcja służąca do pobierania bieżącej pozycji kursora myszy.
        """

        mouse_position = self.drawing_label.mapFromParent(event.pos())
        return mouse_position.x(), mouse_position.y()

    def set_graph_object(self, graph_object):
        """
        Funkcja pobierająca obiekt klasy Graph. Jest potrzebna, gdy graf jest wczytywany z pliku.
        """

        self.graph = graph_object
        self.vertices_size = self.graph.get_vertices_size()

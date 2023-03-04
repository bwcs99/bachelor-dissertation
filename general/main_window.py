from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from graph_checkers.mst_checker import *
from graph_checkers.scc_checker import *
from graph_checkers.max_flow_checker import *
from dialogs.delete_file_dialog import *
from dialogs.closing_info_dialog import *
from dialogs.graph_not_saved_dialog import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QSplitter
from animators.prim_animator import *
from animators.kruskal_animator import *
from animators.scc_animator import *
from animators.flow_finder_animator import *
from algorithms.flow_finder import *
from dialogs.graph_parameters_dialog import ParametersDialog
from algorithms.mst_finder import *
from dialogs.open_file_dialog import OpenDialog
from dialogs.settings_dialogs import *
from algorithms.strongly_connected_components import *
from dialogs.manual_dialog import *
from general.application_terminal import *
from general.canvas import *


class MainWindow(QWidget):
    """
    Klasa okna głównego aplikacji, w której są zaimplementowane metody odpowiadające za interakcję z użytkownikiem.
    """

    def __init__(self):
        """
        Funkcja służąca do tworzenia obiektów klasy MainWindow (konstruktor).
        """

        QWidget.__init__(self)

        super().__init__()
        box_layout = QVBoxLayout()

        menu_bar = QMenuBar()

        file_menu = menu_bar.addMenu(strings.file_menu_name)

        file_action1 = QAction(strings.file_action1_name, self)
        file_action1.setShortcut(strings.file_action1_sct)
        file_action1.setStatusTip(strings.file_action1_desc)
        file_action1.triggered.connect(self.add_new_page)

        file_action2 = QAction(strings.file_action2_name, self)
        file_action2.setShortcut(strings.file_action2_sct)
        file_action2.setStatusTip(strings.file_action2_desc)
        file_action2.triggered.connect(self.open_existing_file)

        file_action3 = QAction(strings.file_action3_name, self)
        file_action3.setShortcut(strings.file_action3_sct)
        file_action3.setStatusTip(strings.file_action3_desc)
        file_action3.triggered.connect(self.save_graph)

        file_action4 = QAction(strings.file_action4_name, self)
        file_action4.setStatusTip(strings.file_action4_desc)
        file_action4.triggered.connect(self.delete_file)

        file_menu.addAction(file_action1)
        file_menu.addSeparator()
        file_menu.addAction(file_action2)
        file_menu.addSeparator()
        file_menu.addAction(file_action3)
        file_menu.addSeparator()
        file_menu.addAction(file_action4)

        algorithm_menu = menu_bar.addMenu(strings.algorithms_menu_name)

        algorithm_action1 = QAction(strings.prim_algorithm_string, self)
        algorithm_action1.setStatusTip(strings.prim_description_string)
        algorithm_action1.triggered.connect(self.begin_prim_animation)

        algorithm_action2 = QAction(strings.kruskal_algorithm_string, self)
        algorithm_action2.setStatusTip(strings.kruskal_description_string)
        algorithm_action2.triggered.connect(self.begin_kruskal_animation)

        algorithm_action3 = QAction(strings.scc_algorithm_string, self)
        algorithm_action3.setStatusTip(strings.scc_description_string)
        algorithm_action3.triggered.connect(self.begin_scc_animation)

        algorithm_action4 = QAction(strings.ford_fulkerson_algorithm_string, self)
        algorithm_action4.setStatusTip(strings.ford_fulkerson_description_string)
        algorithm_action4.triggered.connect(self.begin_ford_fulkerson_animation)

        algorithm_action5 = QAction(strings.edmonds_karp_algorithm_string, self)
        algorithm_action5.setStatusTip(strings.edmonds_karp_description_string)
        algorithm_action5.triggered.connect(self.begin_edmonds_karp_animation)

        algorithm_menu.addAction(algorithm_action1)
        algorithm_menu.addSeparator()
        algorithm_menu.addAction(algorithm_action2)
        algorithm_menu.addSeparator()
        algorithm_menu.addAction(algorithm_action3)
        algorithm_menu.addSeparator()
        algorithm_menu.addAction(algorithm_action4)
        algorithm_menu.addSeparator()
        algorithm_menu.addAction(algorithm_action5)

        animation_menu = menu_bar.addMenu(strings.animation_menu_name)

        animation_action1 = QAction(strings.end_animation_string, self)
        animation_action1.setStatusTip(strings.end_animation_description)
        animation_action1.triggered.connect(self.kill_animation_wrapper)

        animation_action2 = QAction(strings.end_animation_display_results, self)
        animation_action2.setStatusTip(strings.end_animation_display_results_description)
        animation_action2.triggered.connect(self.end_animation_and_display_effect)

        animation_menu.addAction(animation_action1)
        animation_menu.addSeparator()
        animation_menu.addAction(animation_action2)

        terminal_menu = menu_bar.addMenu(strings.terminal_menu_name)

        terminal_action1 = QAction(strings.clear_terminal_string, self)
        terminal_action1.setStatusTip(strings.clear_terminal_description)
        terminal_action1.triggered.connect(self.clear_current_terminal)

        terminal_menu.addAction(terminal_action1)

        settings_menu = menu_bar.addMenu(strings.settings_menu_name)

        settings_action1 = QAction(strings.settings_action1_string, self)
        settings_action1.setStatusTip(strings.settings_action1_string)
        settings_action1.triggered.connect(self.alter_vertices_size)

        settings_menu.addAction(settings_action1)

        help_menu = menu_bar.addMenu(strings.help_menu_string)

        help_action1 = QAction(strings.info_action_string, self)
        help_action1.setStatusTip(strings.info_action_desc)
        help_action1.triggered.connect(self.display_app_manual)

        help_menu.addAction(help_action1)

        self.page_counter = 0

        self.opened_pages = []
        self.application_terminals = []

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(False)
        self.tab_widget.tabCloseRequested.connect(lambda index: self.remove_selected_page(index))

        pages_layout = QVBoxLayout()
        self.tab_widget.setLayout(pages_layout)
        self.tab_widget.tabBarClicked.connect(lambda index: self.change_terminal_and_current_index(index))

        self.tab_widget.setMinimumHeight(self.tab_widget.height())
        self.tab_widget.setMinimumWidth(self.tab_widget.width())

        application_terminal = ApplicationTerminal()

        self.application_terminal = application_terminal
        self.application_terminals.append(application_terminal)
        self.terminals_counter = 1

        self.splitter = QSplitter(Qt.Vertical)

        self.splitter.addWidget(self.tab_widget)
        self.splitter.addWidget(self.application_terminal)

        self.splitter.setCollapsible(1, False)
        self.splitter.setStretchFactor(1, 1)

        box_layout.addWidget(menu_bar)
        box_layout.addWidget(self.splitter)

        self.application_terminal.display_text(strings.application_initial_message)

        self.current_active_page_index = -1

        self.setLayout(box_layout)
        self.setWindowTitle(strings.main_application_name)
        self.setWindowIcon(QIcon(strings.icon_file_name))

        self.animation_threads = []
        self.animation_workers = []

        self.algorithm_final_results = []
        self.algorithm_final_result_messages = []

        self.animation_mutex = QMutex()

        self.current_page_canvas = None

        sh, sw = self.get_screen_geometry()

        self.splitter.setSizes([int(3 * sh / 4), int(sh / 4)])

    def display_app_manual(self):
        """
        Funkcja służąca do wyświetlania instrukcji obsługi aplikacji.
        """

        manual_dialog = ManualDialog()
        manual_dialog.exec()

    def alter_vertices_size(self):
        """
        Funkcja służąca do zmiany rozmiaru wierzchołków.
        """

        vertices_size_dialog = VerticesSizeDialog()
        _, current_canvas, _ = self.get_current_canvas_and_terminal()

        if current_canvas is None:
            return

        if current_canvas.get_animation_running_flag():
            return

        if vertices_size_dialog.exec():
            vertices_new_size = vertices_size_dialog.get_vertex_size()

            current_canvas.alter_graph_vertices_size(vertices_new_size)
        else:
            return

    def clear_current_terminal(self):
        """
        Funkcja obsługująca żądanie użytkownika, usunięcia niepotrzebnych komunikatów z terminala aplikacji.
        """

        index, current_canvas, current_terminal = self.get_current_canvas_and_terminal()

        if current_canvas is None:
            self.application_terminal.clear_terminal()
            return

        if not current_canvas.get_animation_running_flag():
            current_terminal.clear_terminal()

    def get_current_canvas_and_terminal(self):
        """
        Funkcja zwracająca bieżące miejsce do rysowania i bieżący terminal aplikacji.
        """

        index = self.tab_widget.currentIndex()

        if index == -1:
            return None, None, None

        return index, self.opened_pages[index][0], self.application_terminals[index + 1]

    def change_terminal_and_current_index(self, index):
        """
        Funkcja służąca do zmiany bieżącego terminala aplikacji i bieżącego miejsca do rysowania.
        """

        if index == -1:
            self.current_active_page_index = -1
            return

        self.splitter.replaceWidget(1, self.application_terminals[index + 1])
        self.application_terminal = self.application_terminals[index + 1]

        self.current_active_page_index = index

    def add_new_page(self):
        """
        Funkcja tworząca nową zakładkę z nowym terminalem i miejscem do rysowania grafu.
        """

        parameters_dialog = ParametersDialog(self)

        if parameters_dialog.exec():
            direction_flag = parameters_dialog.get_is_graph_directed_flag()
            graph_file_name = parameters_dialog.get_graph_file_name()

            self.page_counter += 1

            new_application_terminal = ApplicationTerminal()

            page_canvas = Canvas(self.tab_widget, new_application_terminal)

            page_canvas.get_canvas_graph().set_is_directed_flag(direction_flag)

            self.application_terminal = new_application_terminal
            self.application_terminals.append(new_application_terminal)
            self.terminals_counter += 1

            self.application_terminal.display_text(strings.creating_file_terminal_message + f"{graph_file_name}.")

            self.splitter.replaceWidget(1, self.application_terminal)

            self.animation_threads.append(None)
            self.animation_workers.append(None)

            self.algorithm_final_results.append(None)
            self.algorithm_final_result_messages.append(None)

            page_name = graph_file_name

            page_data = (page_canvas, page_name)

            self.opened_pages.append(page_data)
            self.tab_widget.addTab(page_canvas, graph_file_name)
            self.tab_widget.setCurrentIndex(self.page_counter - 1)

            self.current_active_page_index = self.page_counter - 1

        else:
            return

    def open_page_from_file(self, file_name_list):
        """
        Funkcja obsługująca żądanie użytkownika, otworzenia pliku z rysunkiem grafu.
        """

        for file_name in file_name_list:
            file_handle = FileHandler()

            file_handle.set_file_name(file_name)

            graph_from_file = file_handle.read_from_file()

            if graph_from_file is None:
                self.application_terminal.display_error_messages([strings.file_reading_error_message])
                continue

            self.page_counter += 1

            new_application_terminal = ApplicationTerminal()

            page_canvas = Canvas(self.tab_widget, new_application_terminal)

            page_canvas.set_first_time_flag(False)

            graph_from_file.set_graph_saved_flag(True)

            page_canvas.set_graph_object(graph_from_file)
            page_canvas.set_canvas_vertices_counter_from_neighbours_list()
            page_canvas.restore_canvas()

            new_application_terminal.display_text(strings.opening_file_terminal_message + f"{file_name}.")

            self.application_terminal = new_application_terminal
            self.application_terminals.append(self.application_terminal)
            self.terminals_counter += 1

            self.splitter.replaceWidget(1, self.application_terminal)

            page_name = file_name

            page_data = (page_canvas, page_name)

            self.opened_pages.append(page_data)

            self.animation_threads.append(None)
            self.animation_workers.append(None)

            self.algorithm_final_results.append(None)
            self.algorithm_final_result_messages.append(None)

            self.tab_widget.addTab(page_canvas, page_name)
            self.tab_widget.setCurrentIndex(self.page_counter - 1)

            self.current_active_page_index = self.page_counter - 1

    def remove_selected_page(self, index):
        """
        Funkcja zamykająca wybraną przez użytkownika zakładkę.
        """

        page_canvas = self.opened_pages[index][0]
        current_page_index, _, _ = self.get_current_canvas_and_terminal()

        if page_canvas.get_animation_running_flag():
            if current_page_index != index:
                closing_dialog = ClosingInfoDialog()

                _ = closing_dialog.exec()

                return

            self.kill_animation(True)

        graph_on_canvas = page_canvas.get_canvas_graph()

        if not graph_on_canvas.get_graph_saved_flag():
            saving_info_dialog = SavingGraphInfoDialog()

            if not saving_info_dialog.exec():
                return

        self.tab_widget.removeTab(index)

        self.animation_threads.pop(index)
        self.animation_workers.pop(index)

        self.algorithm_final_results.pop(index)
        self.algorithm_final_result_messages.pop(index)

        self.opened_pages.pop(index)

        self.page_counter -= 1
        self.terminals_counter -= 1

        self.tab_widget.setCurrentIndex(0)

        self.current_active_page_index = 0

        number_of_terminals = len(self.application_terminals)

        self.application_terminals.pop(index + 1)

        if number_of_terminals >= 3:
            terminal = self.splitter.widget(1)

            if terminal == self.application_terminals[1]:
                return

            self.splitter.replaceWidget(1, self.application_terminals[1])
            self.application_terminal = self.application_terminals[1]
        else:
            terminal = self.splitter.widget(1)

            if terminal == self.application_terminals[0]:
                return

            self.splitter.replaceWidget(1, self.application_terminals[0])
            self.application_terminal = self.application_terminals[0]

        if self.page_counter < -1:
            self.page_counter = -1
            self.terminals_counter = 1

    def open_existing_file(self):
        """
        Funkcja służąca do pobrania i otworzenia wybranych przez użytkownika plików.
        """

        opening_file_dialog = OpenDialog()
        opening_file_dialog.selected_files.connect(self.open_page_from_file)

        if opening_file_dialog.exec():
            pass

    def save_graph(self):
        """
        Funkcja służąca do zapisania wybranego przez użytkownika pliku.
        """

        currently_active_page = self.tab_widget.currentIndex()
        _, page_canvas, _ = self.get_current_canvas_and_terminal()

        if page_canvas is None:
            return

        animation_running_flag = page_canvas.get_animation_running_flag()

        if currently_active_page == -1 or animation_running_flag:
            return

        file_name = self.tab_widget.tabText(currently_active_page)
        file_handle = FileHandler()

        currently_displayed_canvas = self.tab_widget.currentWidget()
        graph_on_canvas = currently_displayed_canvas.get_canvas_graph()

        file_handle.set_file_name(file_name)
        file_handle.set_graph_object(graph_on_canvas)

        saving_result_flag = file_handle.save_to_file()

        if not saving_result_flag:
            self.application_terminal.display_error_messages([strings.file_saving_error_message])
            return

        graph_on_canvas.set_graph_saved_flag(True)

        self.application_terminal.display_text(strings.saving_file_done_terminal_message + f"{file_name}.")

    def delete_file(self):
        """
        Funkcja służąca do pobrania i usunięcia, wybranego przez użytkownika pliku.
        """

        _, current_canvas, _ = self.get_current_canvas_and_terminal()

        if current_canvas is not None:
            if current_canvas.get_animation_running_flag():
                return

        deletion_dialog = DeleteFileDialog(self.application_terminal)

        if deletion_dialog.exec():
            return

    def kill_animation_wrapper(self):
        """
        Wrapper na funkcję do wyłączania wybranej przez użytkownika animacji.
        """

        _, current_canvas, _ = self.get_current_canvas_and_terminal()

        if current_canvas is None:
            return

        self.kill_animation(False)
        current_canvas.clear_algorithm_presentation()

    def kill_animation(self, flag=False):
        """
        Funkcja służąca do wyłączania wybranej przez użytkownika animacji.
        """

        index, current_canvas, current_terminal = self.get_current_canvas_and_terminal()

        if current_canvas.get_animation_running_flag():

            current_canvas.set_animation_running(False)

            if not flag:
                self.animation_mutex.lock()
                self.animation_workers[index].return_condition = True
                self.animation_mutex.unlock()
            else:
                self.animation_mutex.lock()
                self.animation_workers[index].return_condition2 = True
                self.animation_mutex.unlock()

            self.animation_threads[index].quit()
            self.animation_threads[index].wait()

            current_terminal.display_text(strings.animation_stopped_message, colors.error_text_color_hex)

            return True

        return False

    def end_animation_and_display_effect(self):
        """
        Funkcja służąca do wyłączenia wybranej animacji i wyświetlenia efektu końcowego działania algorytmu.
        """

        index, page_canvas, current_terminal = self.get_current_canvas_and_terminal()

        if page_canvas is None:
            return

        animation_type = page_canvas.get_animation_type()

        result = self.kill_animation(True)

        if result:
            result_message = self.algorithm_final_result_messages[index]
            current_terminal.display_text(result_message)

            if animation_type == strings.prim_final_result:
                prev = self.algorithm_final_results[index][0]
                cost = self.algorithm_final_results[index][1]

                page_canvas.restore_canvas()
                page_canvas.get_canvas_graph().set_changed_after_animation()

                self.display_prim_final_result(prev, cost, page_canvas)

            elif animation_type == strings.kruskal_final_result:
                edges_set = self.algorithm_final_results[index][0]

                page_canvas.restore_canvas()
                page_canvas.get_canvas_graph().set_changed_after_animation()

                self.display_kruskal_final_result(edges_set, page_canvas)

            elif animation_type == strings.scc_final_result:
                scc_components = self.algorithm_final_results[index][0]
                data_text_list = self.algorithm_final_results[index][1]

                self.restore_scc_canvas(page_canvas)
                page_canvas.get_canvas_graph().set_changed_after_animation()

                self.mark_components(str(scc_components), page_canvas, True)
                self.display_vertices_data(data_text_list, page_canvas, True)

            elif animation_type == strings.ford_fulkerson_final_result:
                flow_network = self.algorithm_final_results[index][0]

                page_canvas.restore_canvas()
                page_canvas.get_canvas_graph().set_changed_after_animation()

                self.display_flow_network(flow_network, page_canvas, True)

            elif animation_type == strings.edmonds_karp_final_result:
                flow_network = self.algorithm_final_results[index][0]

                page_canvas.restore_canvas()
                page_canvas.get_canvas_graph().set_changed_after_animation()

                self.display_flow_network(flow_network, page_canvas, True)

    def display_prim_final_result(self, prev, cost, canvas):
        """
        Funkcja wyświetlająca efekt końcowy działania algorytmu Prima.
        """

        data_text_list = []

        for i in range(0, len(prev)):
            data_text_list.append(f"{cost[i]}/{prev[i]}")

        canvas.set_vertices_data_text(data_text_list)

        for i in range(0, len(prev)):
            canvas.include_vertex(i)

            if prev[i] == -1:
                continue

            canvas.include_edge(i, prev[i])

    def display_kruskal_final_result(self, edges_set, canvas):
        """
        Funkcja wyświetlająca efekt końcowy działania algorytmu Kruskala.
        """

        marked_vertices = set()

        for edge in edges_set:
            u = edge[0]
            v = edge[1]

            canvas.include_edge(u, v)

            if u not in marked_vertices:
                canvas.include_vertex(u)
                marked_vertices.add(u)

            if v not in marked_vertices:
                canvas.include_vertex(v)
                marked_vertices.add(v)

        self.update()

    def begin_prim_animation(self):
        """
        Funkcja uruchamiająca animację przedstawiającą wykonanie algorytmu Prima.
        """

        index, page_canvas, current_terminal = self.get_current_canvas_and_terminal()

        if page_canvas is None:
            return

        if not page_canvas.get_animation_running_flag():

            mst_checker = MSTChecker(page_canvas.get_canvas_graph().get_graph_helping_neighbours_list(),
                                     page_canvas.get_canvas_graph().get_is_directed_flag())

            flag, error_messages = mst_checker.check_all_necessary_conditions()

            if flag:
                mst_finder = MSTFinder(page_canvas.get_canvas_graph().get_graph_helping_neighbours_list())

                terminal_messages, instructions_list = mst_finder.prim()

                page_canvas.restore_canvas()

                page_canvas.append_whole_pseudocode(strings.whole_prim_pseudocode)

                page_canvas.set_animation_running_to_true(strings.prim_final_result)

                self.animation_threads[index] = QThread()
                self.animation_workers[index] = PrimAnimationThread(terminal_messages, instructions_list, page_canvas,
                                                                    current_terminal)
                final_data_to_display = instructions_list.pop()

                self.algorithm_final_results[index] = final_data_to_display
                self.algorithm_final_result_messages[index] = terminal_messages[-1]

                prim_thread = self.animation_threads[index]
                prim_worker = self.animation_workers[index]

                prim_worker.moveToThread(prim_thread)

                prim_thread.started.connect(prim_worker.run)

                prim_worker.finished.connect(prim_thread.quit)
                prim_worker.finished.connect(prim_worker.deleteLater)
                prim_thread.finished.connect(prim_thread.deleteLater)
                prim_thread.finished.connect(prim_thread.quit)

                prim_worker.finish_animation.connect(self.finish_animation)

                prim_worker.display_vertices_data.connect(self.display_vertices_data)
                prim_worker.display_MST.connect(self.display_current_MST)
                prim_worker.select_vertex.connect(self.select_vertex)
                prim_worker.include_vertex.connect(self.include_vertex)
                prim_worker.exclude_vertex.connect(self.exclude_vertex)
                prim_worker.select_edge.connect(self.select_edge)
                prim_worker.exclude_edge.connect(self.exclude_edge)
                prim_worker.select_line_in_pseudocode.connect(self.select_line_in_pseudocode)

                prim_worker.finish_and_restore_canvas.connect(self.restore_canvas)

                prim_worker.print_to_terminal.connect(self.print_to_terminal)

                prim_thread.start()

            else:
                current_terminal.display_error_messages(error_messages)

    def begin_kruskal_animation(self):
        """
        Funkcja uruchamiająca animację przedstawiającą wykonanie algorytmu Kruskala.
        """
        index, page_canvas, current_terminal = self.get_current_canvas_and_terminal()

        if page_canvas is None:
            return

        if not page_canvas.get_animation_running_flag():

            mst_checker = MSTChecker(page_canvas.get_canvas_graph().get_graph_helping_neighbours_list(),
                                     page_canvas.get_canvas_graph().get_is_directed_flag())

            flag, error_messages = mst_checker.check_all_necessary_conditions()

            if flag:

                mst_finder = MSTFinder(page_canvas.get_canvas_graph().get_graph_helping_neighbours_list())

                terminal_messages, instructions = mst_finder.kruskal()

                page_canvas.restore_canvas()

                page_canvas.append_whole_pseudocode(strings.whole_kruskal_pseudocode)

                page_canvas.set_animation_running_to_true(strings.kruskal_final_result)

                self.animation_threads[index] = QThread()
                self.animation_workers[index] = KruskalAnimationThread(terminal_messages, instructions,
                                                                       len(page_canvas.get_canvas_graph().get_all_vertices_data()),
                                                                       page_canvas,
                                                                       current_terminal)

                final_data_to_display = instructions.pop()

                self.algorithm_final_results[index] = final_data_to_display
                self.algorithm_final_result_messages[index] = terminal_messages[-1]

                kruskal_thread = self.animation_threads[index]
                kruskal_worker = self.animation_workers[index]

                kruskal_worker.moveToThread(kruskal_thread)

                kruskal_thread.started.connect(kruskal_worker.run)
                kruskal_worker.finished.connect(kruskal_thread.quit)
                kruskal_worker.finished.connect(kruskal_worker.deleteLater)
                kruskal_thread.finished.connect(kruskal_thread.deleteLater)

                kruskal_worker.finish_animation.connect(self.finish_animation)

                kruskal_worker.select_edge.connect(self.select_edge)
                kruskal_worker.select_vertex.connect(self.select_vertex)
                kruskal_worker.include_edge.connect(self.include_edge)
                kruskal_worker.include_vertex.connect(self.include_vertex)
                kruskal_worker.exclude_vertex.connect(self.exclude_vertex)
                kruskal_worker.exclude_edge.connect(self.exclude_edge)
                kruskal_worker.print_to_terminal.connect(self.print_to_terminal)
                kruskal_worker.select_line_in_pseudocode.connect(self.select_line_in_pseudocode)

                kruskal_worker.finish_and_restore_canvas.connect(self.restore_canvas)

                kruskal_thread.start()

            else:
                current_terminal.display_error_messages(error_messages)

    def begin_scc_animation(self):
        """
        Funkcja uruchamiająca animację przedstawiającą wykonanie algorytmu szukania silnie spójnych składowych
        w grafie skierowanym.
        """

        index, page_canvas, current_terminal = self.get_current_canvas_and_terminal()

        if page_canvas is None:
            return

        if not page_canvas.get_animation_running_flag():

            scc_checker = SCCChecker(page_canvas.get_canvas_graph().get_graph_helping_neighbours_list(),
                                     page_canvas.get_canvas_graph().get_is_directed_flag())

            flag, error_messages = scc_checker.check_all_necessary_conditions()

            if flag:

                scc_finder = SCCFinder(page_canvas.get_canvas_graph().get_graph_neighbours_list(),
                                       len(page_canvas.get_canvas_graph().get_all_vertices_data()))

                terminal_messages, instructions_list = scc_finder.find_strongly_connected_components()

                page_canvas.restore_canvas()

                page_canvas.append_whole_pseudocode(strings.whole_scc_pseudocode)

                page_canvas.set_animation_running_to_true(strings.scc_final_result)

                self.animation_threads[index] = QThread()
                self.animation_workers[index] = SCCAnimationThread(terminal_messages, instructions_list,
                                                                   page_canvas, current_terminal)

                scc_thread = self.animation_threads[index]
                scc_worker = self.animation_workers[index]

                final_data_to_display = instructions_list.pop()

                self.algorithm_final_results[index] = final_data_to_display
                self.algorithm_final_result_messages[index] = terminal_messages[-3]

                scc_worker.moveToThread(scc_thread)

                scc_thread.started.connect(scc_worker.run)
                scc_worker.finished.connect(scc_thread.quit)
                scc_worker.finished.connect(scc_worker.deleteLater)
                scc_thread.finished.connect(scc_worker.deleteLater)

                scc_worker.finish_animation.connect(self.finish_animation)

                scc_worker.draw_reversed_graph.connect(self.draw_reversed_graph)
                scc_worker.select_vertex.connect(self.select_vertex)
                scc_worker.select_edge.connect(self.select_edge)
                scc_worker.display_vertices_data.connect(self.display_vertices_data)
                scc_worker.clear_dfs_path.connect(self.clear_dfs_path)
                scc_worker.restore_canvas.connect(self.restore_scc_canvas)
                scc_worker.mark_components.connect(self.mark_components)
                scc_worker.select_line_in_pseudocode.connect(self.select_line_in_pseudocode)

                scc_worker.finish_and_restore_canvas.connect(self.restore_scc_canvas)

                scc_worker.print_to_terminal.connect(self.print_to_terminal)

                scc_thread.start()

            else:
                current_terminal.display_error_messages(error_messages)

    def begin_ford_fulkerson_animation(self):
        """
        Funkcja uruchamiająca animację przedstawiającą wykonanie algorytmu Forda-Fulkersona.
        """

        index, page_canvas, current_terminal = self.get_current_canvas_and_terminal()

        if page_canvas is None:
            return

        if not page_canvas.get_animation_running_flag():

            flow_checker = MaxFlowChecker(page_canvas.get_canvas_graph().get_graph_helping_neighbours_list(),
                                          page_canvas.get_canvas_graph().get_is_directed_flag())

            flag, source, target, error_messages = flow_checker.check_all_necessary_conditions()

            if flag:
                flow_finder = MaximumFlowFinder(page_canvas.get_canvas_graph().get_graph_helping_neighbours_list(),
                                                source, target)

                terminal_messages, instructions_list = flow_finder.ford_fulkerson()

                residual_graph = page_canvas.get_canvas_graph().get_residual_graph()

                if residual_graph is None:
                    page_canvas.get_canvas_graph().create_residual_graph()

                page_canvas.restore_canvas()

                page_canvas.append_whole_pseudocode(strings.whole_max_flow_pseudocode)

                page_canvas.set_animation_running_to_true(strings.ford_fulkerson_final_result)

                self.animation_threads[index] = QThread()
                self.animation_workers[index] = FlowFinderAnimationThread(terminal_messages, instructions_list, page_canvas,
                                                                          current_terminal)

                flow_network = instructions_list.pop()

                self.algorithm_final_results[index] = flow_network
                self.algorithm_final_result_messages[index] = terminal_messages[-2]

                flow_thread = self.animation_threads[index]
                flow_worker = self.animation_workers[index]

                flow_worker.moveToThread(flow_thread)

                flow_thread.started.connect(flow_worker.run)
                flow_worker.finished.connect(flow_thread.quit)
                flow_worker.finished.connect(flow_worker.deleteLater)
                flow_thread.finished.connect(flow_thread.deleteLater)

                flow_worker.finish_animation.connect(self.finish_animation)

                flow_worker.display_flow_network.connect(self.display_flow_network)
                flow_worker.display_residual_graph.connect(self.display_residual_graph)
                flow_worker.select_edge.connect(self.select_residual_edge)
                flow_worker.display_altered_edge_flow.connect(self.display_altered_edge_flow)
                flow_worker.display_augumenting_path.connect(self.display_augumenting_path)
                flow_worker.select_line_in_pseudocode.connect(self.select_line_in_pseudocode)

                flow_worker.print_to_terminal.connect(self.print_to_terminal)

                flow_worker.finish_and_restore_canvas.connect(self.restore_canvas)

                flow_thread.start()

            else:
                current_terminal.display_error_messages(error_messages)

    def begin_edmonds_karp_animation(self):
        """
        Funkcja uruchamiająca animację przedstawiającą wykonanie algorytmu Edmondsa-Karpa.
        """

        index, page_canvas, current_terminal = self.get_current_canvas_and_terminal()

        if page_canvas is None:
            return

        if not page_canvas.get_animation_running_flag():

            flow_checker = MaxFlowChecker(page_canvas.get_canvas_graph().get_graph_helping_neighbours_list(),
                                          page_canvas.get_canvas_graph().get_is_directed_flag())

            flag, source, target, error_messages = flow_checker.check_all_necessary_conditions()

            if flag:
                flow_finder = MaximumFlowFinder(page_canvas.get_canvas_graph().get_graph_helping_neighbours_list(),
                                                source, target)

                terminal_messages, instructions_list = flow_finder.edmonds_karp()

                page_canvas.restore_canvas()

                page_canvas.append_whole_pseudocode(strings.whole_max_flow_pseudocode)

                page_canvas.set_animation_running_to_true(strings.edmonds_karp_final_result)

                self.animation_threads[index] = QThread()
                self.animation_workers[index] = FlowFinderAnimationThread(terminal_messages, instructions_list, page_canvas,
                                                                          current_terminal)

                flow_network = instructions_list.pop()

                self.algorithm_final_results[index] = flow_network
                self.algorithm_final_result_messages[index] = terminal_messages[-2]

                flow_thread = self.animation_threads[index]
                flow_worker = self.animation_workers[index]

                flow_worker.moveToThread(flow_thread)

                flow_thread.started.connect(flow_worker.run)
                flow_worker.finished.connect(flow_thread.quit)
                flow_worker.finished.connect(flow_worker.deleteLater)
                flow_thread.finished.connect(flow_thread.deleteLater)

                flow_worker.finish_animation.connect(self.finish_animation)

                flow_worker.display_flow_network.connect(self.display_flow_network)
                flow_worker.display_residual_graph.connect(self.display_residual_graph)
                flow_worker.select_edge.connect(self.select_residual_edge)
                flow_worker.display_altered_edge_flow.connect(self.display_altered_edge_flow)
                flow_worker.display_augumenting_path.connect(self.display_augumenting_path)
                flow_worker.select_line_in_pseudocode.connect(self.select_line_in_pseudocode)

                flow_worker.print_to_terminal.connect(self.print_to_terminal)

                flow_worker.finish_and_restore_canvas.connect(self.restore_canvas)

                flow_thread.start()

            else:
                current_terminal.display_error_messages(error_messages)

    def select_vertex(self, vertex, canvas):
        """
        Funkcja służąca do zaznaczania aktualnie przetwarzanego wierzchołka.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag():
                canvas.select_vertex(vertex)

    def include_vertex(self, vertex, canvas, flag=False):
        """
        Funkcja służąca do zaznaczania wierzchołka, włączonego w jakąś szukaną strukturę (np. MST).
        """

        if canvas is not None:
            if canvas.get_animation_running_flag() or flag:
                canvas.include_vertex(vertex)

    def exclude_vertex(self, vertex, canvas):
        """
        Funkcja służąca do przywrócenia pierwotnego koloru wierzchołka
        (oznaczanie, że na razie nie jest przetwarzany).
        """

        if canvas is not None:
            if canvas.get_animation_running_flag():
                canvas.exclude_vertex(vertex)

    def select_edge(self, u, v, canvas):
        """
        Funkcja służąca do zaznaczenia aktualnie przetwarzanej krawędzi.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag():
                canvas.select_edge(u, v)

    def include_edge(self, u, v, canvas, flag=False):
        """
        Funkcja służąca do zaznaczenia, że dana krawędź wchodzi w skład szukanej struktury (np. MST).
        """

        if canvas is not None:
            if canvas.get_animation_running_flag() or flag:
                canvas.include_edge(u, v)

    def exclude_edge(self, u, v, canvas):
        """
        Funkcja służąca do oznaczenia, że dana krawędź nie jest przetwarzana.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag():
                canvas.exclude_edge(u, v)

    def display_vertices_data(self, data, canvas, flag=False):
        """
        Funkcja służąca do wyświetlania danych związanych z wierzchołkami.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag() or flag:
                canvas.set_vertices_data_text(data)

    def display_current_MST(self, prev_array, canvas, flag=False):
        """
        Funkcja służąca do wyświetlenia znalezionego minimalnego drzewa rozpinającego (MST).
        """

        if canvas is not None:
            if canvas.get_animation_running_flag() or flag:
                canvas.display_current_MST(prev_array)

    def draw_reversed_graph(self, canvas, flag=False):
        """
        Funkcja służąca do rysowania grafu odwrotnego.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag() or flag:
                canvas.draw_reversed_graph()

    def clear_dfs_path(self, canvas):
        """
        Funkcja służąca do \"odznaczania\" krawędzi (po operacji mają kolor czarny), wchodzących w skład ścieżki
        znalezionej przez algorytm DFS.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag():
                canvas.clear_dfs_path()

    def restore_scc_canvas(self, canvas):
        """
        Funkcja służąca do przywracania stanu początkowego \"płótna \" do rysowania, po animacji algorytmu szukania
        silnie spójnych składowych w grafie skierowanym.
        """

        if canvas is not None:
            reversed_flag = canvas.get_canvas_graph_reversed_flag()

            if reversed_flag:
                canvas.get_canvas_graph().reverse_graph()

            self.restore_canvas(canvas)

    def mark_components(self, components, canvas, flag=False):
        """
        Funkcja służąca do zaznaczania znalezionych silnie spójnych składowych w grafie skierowanym.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag() or flag:
                canvas.mark_connected_components(components)

    def display_flow_network(self, flow_network, canvas, flag=False):
        """
        Funkcja służąca do wyświetlania bieżącej sieci przepływowej.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag() or flag:
                canvas.display_flow_network(flow_network)

    def display_residual_graph(self, residual_graph, canvas):
        """
        Funkcja służąca do wyświetlania bieżącego grafu residualnego.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag():
                canvas.display_residual_graph(residual_graph)

    def display_altered_edge_flow(self, u, v, flow, color, canvas):
        """
        Funkcja służąca do modyfikacji przepływu na danej krawędzi.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag():
                canvas.display_altered_edge_flow(u, v, flow, color)

    def display_augumenting_path(self, path, canvas):
        """
        Funkcja służąca do wyświetlenia znalezionej s-t ścieżki (ścieżka ze źródła do ujścia).
        """

        if canvas is not None:
            if canvas.get_animation_running_flag():
                canvas.display_augumenting_path(path)

    def select_residual_edge(self, u, v, canvas):
        """
        Funkcja służąca do zaznaczania krawędzi residualnych.
        """

        if canvas is not None:
            if canvas.get_animation_running_flag():
                canvas.select_residual_edge(u, v)

    def print_to_terminal(self, text, terminal, canvas):
        """
        Funkcja służąca do wypisywania komunikatów związanych z animacją na terminal aplikacji.
        """

        if terminal is not None and canvas is not None:
            if canvas.get_animation_running_flag():
                terminal.display_text(text, colors.simulation_text_color_hex)

    def restore_canvas(self, canvas):
        """
        Funkcja służąca do przywracania stanu początkowego \"płótna\" po animacjach innych niż szukanie silnie
        spójnych składowych w grafie skierowanym.
        """

        if canvas is not None:
            canvas.restore_canvas()

    def finish_animation(self, canvas):
        """
        Funkcja służąca do przygotowania końca animacji (konkretnie - przygotowanie do wyświetlenia wyniku działania
        algorytmu).
        """

        if canvas is not None:
            canvas.restore_algorithm_presentation()
            canvas.set_animation_running_to_false()

    def select_line_in_pseudocode(self, whole_pseudocode, list_of_numbers, canvas):
        """
        Funkcja służąca do zaznaczania odpowiedniej linijki w danym pseudokodzie.
        """

        if canvas is not None:
            canvas.select_certain_lines_in_pseudocode(whole_pseudocode, list_of_numbers)

    def get_screen_geometry(self):
        """
        Funkcja służąca do pobierania rozmiarów (wysokość i szerokość) ekranu.
        """

        desktop = QApplication.desktop()

        screen_rectangle = desktop.screenGeometry()

        screen_height = screen_rectangle.height()
        screen_width = screen_rectangle.width()

        return screen_height, screen_width

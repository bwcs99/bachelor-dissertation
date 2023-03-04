import time
from resources import strings
from PyQt5.QtCore import QObject, pyqtSignal


class SCCAnimationThread(QObject):
    """
    Klasa odpowiedzialna za przedstawienie animacji algorytmu szukania silnie spójnych składowych.
    """

    print_to_terminal = pyqtSignal(str, object, object)

    select_line_in_pseudocode = pyqtSignal(list, list, object)
    draw_reversed_graph = pyqtSignal(object)
    select_vertex = pyqtSignal(int, object)
    select_edge = pyqtSignal(int, int, object)
    display_vertices_data = pyqtSignal(list, object)
    clear_dfs_path = pyqtSignal(object)
    restore_canvas = pyqtSignal(object)
    mark_components = pyqtSignal(str, object)

    finish_animation = pyqtSignal(object)
    finished = pyqtSignal()
    finish_and_restore_canvas = pyqtSignal(object)

    def __init__(self, terminal_messages, instructions_list, canvas, terminal):
        super().__init__()

        self.terminal_messages = terminal_messages
        self.instructions_list = instructions_list

        self.canvas = canvas
        self.terminal = terminal

        self.return_condition = False
        self.return_condition2 = False

    def run(self):
        """
        Funkcja (działająca w innym wątku) odpowiedzialna za \"taktowanie\" animacji i wysyłanie sygnałów,
        oznaczających odpowiednie akcje.
        """

        for t_message in self.terminal_messages:
            if self.return_condition:
                self.finish_animation.emit(self.canvas)
                self.finish_and_restore_canvas.emit(self.canvas)
                return
            elif self.return_condition2:
                self.finish_animation.emit(self.canvas)
                return

            time.sleep(1)
            if t_message == strings.stop_string:
                instruction = self.instructions_list.pop(0)

                mnemonic = instruction[0]

                if mnemonic == strings.reverse_graph_mnemonic:
                    self.draw_reversed_graph.emit(self.canvas)

                elif mnemonic == strings.select_vertex_mnemonic:
                    vertex = instruction[1]

                    self.select_vertex.emit(vertex, self.canvas)

                elif mnemonic == strings.select_edge_mnemonic:
                    u = instruction[1]
                    v = instruction[2]

                    self.select_edge.emit(u, v, self.canvas)

                elif mnemonic == strings.display_vertices_data_mnemonic:
                    vertices_data = instruction[1]

                    self.display_vertices_data.emit(vertices_data, self.canvas)

                elif mnemonic == strings.clear_dfs_path_mnemonic:

                    self.clear_dfs_path.emit(self.canvas)

                elif mnemonic == strings.restore_canvas_mnemonic:
                    self.restore_canvas.emit(self.canvas)

                elif mnemonic == strings.mark_components_mnemonic:
                    components = instruction[1]

                    self.mark_components.emit(str(components), self.canvas)

                elif mnemonic == strings.select_line_in_pseudocode_instruction:
                    lines_to_select = instruction[1]

                    self.select_line_in_pseudocode.emit(strings.whole_scc_pseudocode, lines_to_select,
                                                        self.canvas)
            else:
                self.print_to_terminal.emit(t_message, self.terminal, self.canvas)

        self.finish_animation.emit(self.canvas)
        self.finished.emit()

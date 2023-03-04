import time
from resources import strings
from PyQt5.QtCore import QObject, pyqtSignal


class KruskalAnimationThread(QObject):
    """
    Klasa odpowiedzialna za przedstawienie animacji algorytmu Kruskala.
    """

    print_to_terminal = pyqtSignal(str, object, object)

    select_line_in_pseudocode = pyqtSignal(list, list, object)
    select_edge = pyqtSignal(int, int, object)
    select_vertex = pyqtSignal(int, object)
    include_edge = pyqtSignal(int, int, object)
    include_vertex = pyqtSignal(int, object)
    exclude_vertex = pyqtSignal(int, object)
    exclude_edge = pyqtSignal(int, int, object)

    finish_animation = pyqtSignal(object)
    finished = pyqtSignal()
    finish_and_restore_canvas = pyqtSignal(object)

    def __init__(self, terminal_messages, instructions, number_of_vertices, canvas, terminal):
        super().__init__()

        self.terminal_messages = terminal_messages
        self.instructions = instructions
        self.included_vertices = [False for i in range(0, number_of_vertices)]

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
                instruction = self.instructions.pop(0)

                mnemonic = instruction[0]

                u, v = 0, 0

                if len(instruction) >= 3:
                    u = instruction[1]
                    v = instruction[2]

                if mnemonic == strings.select_edge_mnemonic:
                    self.select_edge.emit(u, v, self.canvas)

                    if not self.included_vertices[u]:
                        self.select_vertex.emit(u, self.canvas)

                    if not self.included_vertices[v]:
                        self.select_vertex.emit(v, self.canvas)

                elif mnemonic == strings.include_edge_mnemonic:
                    self.include_edge.emit(u, v, self.canvas)
                    self.include_vertex.emit(u, self.canvas)
                    self.include_vertex.emit(v, self.canvas)

                    self.included_vertices[u] = True
                    self.included_vertices[v] = True

                elif mnemonic == strings.exclude_edge_mnemonic:
                    self.exclude_edge.emit(u, v, self.canvas)

                    if not self.included_vertices[u]:
                        self.exclude_vertex.emit(u, self.canvas)

                    if not self.included_vertices[v]:
                        self.exclude_vertex.emit(v, self.canvas)

                elif mnemonic == strings.select_line_in_pseudocode_instruction:
                    list_of_lines_numbers = instruction[1]

                    self.select_line_in_pseudocode.emit(strings.whole_kruskal_pseudocode,
                                                        list_of_lines_numbers,
                                                        self.canvas)

            else:
                self.print_to_terminal.emit(t_message, self.terminal, self.canvas)

        self.finish_animation.emit(self.canvas)
        self.finished.emit()

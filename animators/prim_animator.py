import time
from resources import strings
from PyQt5.QtCore import QObject, pyqtSignal


class PrimAnimationThread(QObject):
    """
    Klasa odpowiedzialna za przedstawienie animacji algorytmu Prima.
    """

    print_to_terminal = pyqtSignal(str, object, object)

    select_line_in_pseudocode = pyqtSignal(list, list, object)
    display_vertices_data = pyqtSignal(list, object)
    display_MST = pyqtSignal(list, object)
    include_vertex = pyqtSignal(int, object)
    select_vertex = pyqtSignal(int, object)
    exclude_vertex = pyqtSignal(int, object)
    select_edge = pyqtSignal(int, int, object)
    exclude_edge = pyqtSignal(int, int, object)

    finished = pyqtSignal()
    finish_animation = pyqtSignal(object)
    finish_and_restore_canvas = pyqtSignal(object)

    def __init__(self, terminal_messages, instructions, canvas, terminal):
        super().__init__()

        self.terminal_messages = terminal_messages
        self.instructions = instructions

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

                if mnemonic == strings.display_vertices_data_mnemonic:
                    data_text_list = instruction[1]

                    self.display_vertices_data.emit(data_text_list, self.canvas)

                elif mnemonic == strings.display_MST_mnemonic:
                    prev = instruction[1]

                    self.display_MST.emit(prev, self.canvas)

                elif mnemonic == strings.include_vertex_mnemonic:
                    vertex = instruction[1]

                    self.include_vertex.emit(vertex, self.canvas)

                elif mnemonic == strings.select_vertex_mnemonic:
                    vertex = instruction[1]

                    self.select_vertex.emit(vertex, self.canvas)

                elif mnemonic == strings.exclude_vertex_mnemonic:
                    vertex = instruction[1]

                    self.exclude_vertex.emit(vertex, self.canvas)

                elif mnemonic == strings.select_edge_mnemonic:
                    u, v = instruction[1], instruction[2]

                    self.select_edge.emit(u, v, self.canvas)

                elif mnemonic == strings.exclude_edge_mnemonic:
                    u, v = instruction[1], instruction[2]

                    self.exclude_edge.emit(u, v, self.canvas)

                elif mnemonic == strings.select_line_in_pseudocode_instruction:
                    lines_to_select = instruction[1]

                    self.select_line_in_pseudocode.emit(strings.whole_prim_pseudocode, lines_to_select, self.canvas)
            else:
                self.print_to_terminal.emit(t_message, self.terminal, self.canvas)

        self.finish_animation.emit(self.canvas)
        self.finished.emit()

import time
from resources import strings
from PyQt5.QtCore import QObject, pyqtSignal


class FlowFinderAnimationThread(QObject):
    """
    Klasa odpowiedzialna za przedstawienie animacji algorytmów szukania maksymalnego przepływu: algorytmu Forda-Fulkersona oraz
    algorytmu Edmondsa-Karpa.
    """

    print_to_terminal = pyqtSignal(str, object, object)

    select_line_in_pseudocode = pyqtSignal(list, list, object)
    display_flow_network = pyqtSignal(list, object)
    display_residual_graph = pyqtSignal(list, object)
    select_edge = pyqtSignal(int, int, object)
    display_altered_edge_flow = pyqtSignal(int, int, int, int, object)
    display_augumenting_path = pyqtSignal(list, object)

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

                if mnemonic == strings.display_flow_network_mnemonic:
                    flow_network = instruction[1]

                    self.display_flow_network.emit(flow_network, self.canvas)

                elif mnemonic == strings.display_residual_graph_mnemonic:
                    residual_graph = instruction[1]

                    self.display_residual_graph.emit(residual_graph, self.canvas)

                elif mnemonic == strings.select_edge_mnemonic:
                    u = instruction[1]
                    v = instruction[2]

                    self.select_edge.emit(u, v, self.canvas)

                elif mnemonic == strings.display_altered_edge_flow_mnemonic:
                    u = instruction[1]
                    v = instruction[2]
                    edge_flow = instruction[3]
                    edge_color = instruction[4]

                    self.display_altered_edge_flow.emit(u, v, edge_flow, edge_color, self.canvas)

                elif mnemonic == strings.display_augumenting_path_mnemonic:
                    augumenting_path = instruction[1]

                    if augumenting_path is not None:
                        self.display_augumenting_path.emit(augumenting_path, self.canvas)

                elif mnemonic == strings.select_line_in_pseudocode_instruction:
                    lines_to_select = instruction[1]

                    self.select_line_in_pseudocode.emit(strings.whole_max_flow_pseudocode, lines_to_select,
                                                        self.canvas)

            else:
                self.print_to_terminal.emit(t_message, self.terminal, self.canvas)

        self.finish_animation.emit(self.canvas)
        self.finished.emit()

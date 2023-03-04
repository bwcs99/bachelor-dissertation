import os
from resources import strings
from resources import constants
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QDialogButtonBox, QRadioButton


class ParametersDialog(QDialog):
    """
    Klasa okna dialogowego, odpowiedzialnego za pobieranie nazwy nowego pliku oraz rodzaju rysowanego grafu
    (skierowany/nieskierowany).
    """

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.is_graph_directed = False
        self.graph_file_name = None

        file_name_label = QLabel(strings.new_file_label_string)
        self.file_name_input = QLineEdit()

        first_layout = QHBoxLayout()

        first_layout.addWidget(file_name_label)
        first_layout.addWidget(self.file_name_input)

        graph_kind_label = QLabel(strings.graph_kind_label_string)
        directed_graph_button = QRadioButton(strings.directed_label_string)
        undirected_graph_button = QRadioButton(strings.undirected_label_string)

        second_layout = QVBoxLayout()

        second_layout.addWidget(graph_kind_label)

        third_layout = QHBoxLayout()

        directed_graph_button.toggled.connect(self.set_graph_directed)
        undirected_graph_button.toggled.connect(self.set_graph_undirected)

        third_layout.addWidget(directed_graph_button)
        third_layout.addWidget(undirected_graph_button)

        second_layout.addLayout(third_layout)

        dialog_buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        dialog_buttons_box = QDialogButtonBox(dialog_buttons)

        dialog_buttons_box.accepted.connect(self.parameters_accepted)
        dialog_buttons_box.rejected.connect(self.parameters_rejected)

        main_layout = QVBoxLayout()

        main_layout.addLayout(first_layout)
        main_layout.addLayout(second_layout)
        main_layout.addWidget(dialog_buttons_box)

        self.setLayout(main_layout)

    def get_graph_file_name(self):
        return self.graph_file_name

    def get_is_graph_directed_flag(self):
        return self.is_graph_directed

    def set_graph_directed(self):
        self.is_graph_directed = True

    def set_graph_undirected(self):
        self.is_graph_directed = False

    def parameters_accepted(self):
        """
        Funkcja pobierająca nazwę nowego pliku i sprawdzająca czy nie ma innego pliku o tej samej nazwie.
        """

        self.graph_file_name = self.file_name_input.text()

        existing_files = os.listdir(constants.application_files_directory_path)

        if self.graph_file_name in existing_files:
            self.parent.application_terminal.display_error_messages([strings.file_already_exists_error_message])
            return

        self.accept()

    def parameters_rejected(self):
        """
        Funkcja wykonywana po wciśnięciu przez użytkownika przycisku \"Cancel\".
        """

        self.is_graph_directed = False
        self.graph_file_name = None

        self.reject()

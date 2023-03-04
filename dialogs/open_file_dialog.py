import os
from PyQt5 import QtWidgets
from resources import strings
from resources import constants
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QListWidget, QLabel, QDialogButtonBox, QVBoxLayout


class OpenDialog(QDialog):
    """
    Klasa okna dialogowego, odpowiedzialnego za wyświetlenie wyboru istniejących plików do otworzenia.
    """

    selected_files = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        choose_file_label = QLabel(strings.choose_file_label_string)

        self.files_list_view = QListWidget()
        self.files_list_view.setSortingEnabled(True)
        self.files_list_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        files = self.search_for_existing_projects()

        for file in files:
            self.files_list_view.addItem(file)

        self.selected_files_names = []

        dialog_buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.dialog_buttons_box = QDialogButtonBox(dialog_buttons)

        self.dialog_buttons_box.accepted.connect(self.accept_opening_process)
        self.dialog_buttons_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()

        main_layout.addWidget(choose_file_label)
        main_layout.addWidget(self.files_list_view)
        main_layout.addWidget(self.dialog_buttons_box)

        self.setLayout(main_layout)
        self.setWindowTitle(strings.open_file_dialog_title)

    def search_for_existing_projects(self):
        """
        Funkcja zwracająca listę nazw istniejących plików z zapisanymi rysunkami grafów.
        """

        return os.listdir(constants.application_files_directory_path)

    def accept_opening_process(self):
        """
        Funkcja pobierająca wybrane przez użytkownika pliki do otworzenia.
        """

        selected_files = self.files_list_view.selectedItems()

        for i in range(0, len(selected_files)):
            self.selected_files_names.append(selected_files[i].text())

        self.selected_files.emit(self.selected_files_names)

        self.selected_files_names = []

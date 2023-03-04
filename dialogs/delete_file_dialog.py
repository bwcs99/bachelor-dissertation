import os
from resources import constants, strings
from general.file_handler import FileHandler
from PyQt5.QtWidgets import QDialog, QLabel, QListWidget, QDialogButtonBox, QVBoxLayout


class DeleteFileDialog(QDialog):
    """
    Klasa okna dialogowego, odpowiedzialnego za wyświetlenie wyboru plików do usunięcia.
    """

    def __init__(self, current_application_terminal):
        super().__init__()

        choose_file_to_delete = QLabel(strings.select_file_to_delete_string)

        self.application_terminal = current_application_terminal

        self.files_list = QListWidget()
        self.files_list.setSortingEnabled(True)

        existing_files = self.list_existing_files()

        for file in existing_files:
            self.files_list.addItem(file)

        dialog_buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        dialog_buttons_box = QDialogButtonBox(dialog_buttons)

        dialog_buttons_box.accepted.connect(self.accept_file_deletion)
        dialog_buttons_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()

        main_layout.addWidget(choose_file_to_delete)
        main_layout.addWidget(self.files_list)
        main_layout.addWidget(dialog_buttons_box)

        self.setLayout(main_layout)
        self.setWindowTitle(strings.delete_file_dialog_window)

    def list_existing_files(self):
        """
        Funkcja zwracająca pliki, które są w katalogu używanym przez aplikację.
        """

        return os.listdir(constants.application_files_directory_path)

    def accept_file_deletion(self):
        """
        Funkcja pobierajaca nazwę pliku do usunięcia i usuwająca go.
        """

        file_to_delete_name = self.files_list.currentItem().text()

        file_handler = FileHandler()

        flag = file_handler.delete_selected_file(file_to_delete_name)

        if flag:
            self.application_terminal.display_text(strings.deleting_file_done_terminal_message +
                                                   f"{file_to_delete_name}.")
        else:
            self.application_terminal.display_text(strings.file_deletion_failure_terminal_message +
                                                   f"{file_to_delete_name}.")

        self.files_list.takeItem(self.files_list.currentRow())


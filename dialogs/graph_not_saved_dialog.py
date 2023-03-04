from resources import strings
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QDialogButtonBox


class SavingGraphInfoDialog(QDialog):
    """
    Klasa okna dialogowego odpowiedzialnego za wyświetlenie ostrzeżenia o niezapisanym grafie w zamykanej zakładce.
    """

    def __init__(self):
        super().__init__()

        description_label = QLabel(strings.graph_not_saved_description)

        main_layout = QVBoxLayout()

        dialog_buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        dialog_button_box = QDialogButtonBox(dialog_buttons)

        dialog_button_box.accepted.connect(self.accept)
        dialog_button_box.rejected.connect(self.reject)

        main_layout.addWidget(description_label)
        main_layout.addWidget(dialog_button_box)

        self.setLayout(main_layout)
        self.setWindowTitle(strings.closing_dialog_title)
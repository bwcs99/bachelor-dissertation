from resources import strings
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox


class ClosingInfoDialog(QDialog):
    """
    Klasa okna dialogowego odpowiedzialnego za wyświetlenie ostrzeżenia o działającej animacji w zamykanej zakładce.
    """

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        description_label = QLabel(strings.closing_info_description)

        dialog_button = QDialogButtonBox.Ok

        dialog_buttons_box = QDialogButtonBox(dialog_button)

        dialog_buttons_box.accepted.connect(self.accept)

        main_layout.addWidget(description_label)
        main_layout.addWidget(dialog_buttons_box)

        self.setLayout(main_layout)
        self.setWindowTitle(strings.closing_dialog_title)

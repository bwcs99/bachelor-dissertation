from resources import strings
from resources import constants
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QDialogButtonBox


class ManualDialog(QDialog):
    """
    Klasa okna dialogowego, odpowiedzialnego za wyświetlenie instrukcji obsługi aplikacji.
    """

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        self.manual_area = QTextEdit()
        self.manual_area.setReadOnly(True)

        self.manual_area.setText(strings.manual_string)

        dialog_button = QDialogButtonBox.Ok

        dialog_buttons_box = QDialogButtonBox(dialog_button)

        dialog_buttons_box.accepted.connect(self.accept)

        main_layout.addWidget(self.manual_area)
        main_layout.addWidget(dialog_buttons_box)

        self.setMinimumWidth(constants.manual_box_minimum_width)
        self.setMinimumHeight(constants.manual_box_minimum_height)

        self.setLayout(main_layout)
        self.setWindowTitle(strings.manual_dialog_title)

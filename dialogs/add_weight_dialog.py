from resources import strings
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QLabel, QVBoxLayout


class WeightDialog(QDialog):
    """
    Klasa okna dialogowego, odpowiedzialnego za pobieranie wagi wybranej krawędzi od użytkownika.
    """

    def __init__(self, edge_start, edge_end):
        super().__init__()

        self.edge_weight = None

        description_label = QLabel(f"{strings.add_weight_dialog_prompt} {edge_start} - {edge_end}")
        self.weight_input = QLineEdit()

        self.setWindowTitle(strings.add_weight_dialog_title)

        dialog_buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.dialog_buttons_box = QDialogButtonBox(dialog_buttons)

        self.dialog_buttons_box.accepted.connect(self.set_edge_weight)
        self.dialog_buttons_box.rejected.connect(self.unset_edge_weight)

        dialog_layout = QVBoxLayout()

        dialog_layout.addWidget(description_label)
        dialog_layout.addWidget(self.weight_input)
        dialog_layout.addWidget(self.dialog_buttons_box)

        self.setLayout(dialog_layout)

    def get_edge_weight(self):
        return self.edge_weight

    def set_edge_weight(self):
        self.edge_weight = self.weight_input.text()
        self.accept()

    def unset_edge_weight(self):
        self.edge_weight = None
        self.reject()

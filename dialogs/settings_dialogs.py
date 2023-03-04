from resources import strings
from PyQt5.QtWidgets import QDialog, QLabel, QRadioButton, QHBoxLayout, QVBoxLayout, QDialogButtonBox


class VerticesSizeDialog(QDialog):
    """
    Klasa okna dialogowego, odpowiedzialnego za pobranie i ustawienie nowego rozmiaru wierzchołków.
    """

    def __init__(self):
        super().__init__()

        first_size_label = QLabel(strings.twenty_label)
        second_size_label = QLabel(strings.thirty_label)
        third_size_label = QLabel(strings.fourty_label)
        fourth_size_label = QLabel(strings.fifty_label)

        self.vertex_size = int(strings.twenty_label)

        self.radio_button20 = QRadioButton()
        self.radio_button20.vertex_size = int(strings.twenty_label)
        self.radio_button20.setChecked(True)
        self.radio_button20.toggled.connect(self.set_vertex_size)

        self.radio_button30 = QRadioButton()
        self.radio_button30.vertex_size = int(strings.thirty_label)
        self.radio_button30.toggled.connect(self.set_vertex_size)

        self.radio_button40 = QRadioButton()
        self.radio_button40.vertex_size = int(strings.fourty_label)
        self.radio_button40.toggled.connect(self.set_vertex_size)

        self.radio_button50 = QRadioButton()
        self.radio_button50.vertex_size = int(strings.fifty_label)
        self.radio_button50.toggled.connect(self.set_vertex_size)

        h_layout1 = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        h_layout3 = QHBoxLayout()
        h_layout4 = QHBoxLayout()

        h_layout1.addWidget(self.radio_button20)
        h_layout1.addWidget(first_size_label)

        h_layout2.addWidget(self.radio_button30)
        h_layout2.addWidget(second_size_label)

        h_layout3.addWidget(self.radio_button40)
        h_layout3.addWidget(third_size_label)

        h_layout4.addWidget(self.radio_button50)
        h_layout4.addWidget(fourth_size_label)

        dialog_buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        dialog_button_box = QDialogButtonBox(dialog_buttons)

        dialog_button_box.accepted.connect(self.accept)
        dialog_button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()

        main_layout.addLayout(h_layout1)
        main_layout.addLayout(h_layout2)
        main_layout.addLayout(h_layout3)
        main_layout.addLayout(h_layout4)

        main_layout.addWidget(dialog_button_box)

        self.setLayout(main_layout)
        self.setWindowTitle(strings.set_vertices_size)

    def set_vertex_size(self):
        clicked_button = self.sender()

        if clicked_button.isChecked():
            self.vertex_size = clicked_button.vertex_size

    def get_vertex_size(self):
        return int(self.vertex_size)

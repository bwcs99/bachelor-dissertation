from resources import colors
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTextEdit, QWidget, QHBoxLayout


class ApplicationTerminal(QWidget):
    """
    Klasa terminala aplikacji z odpowiednimi funkcjami do manipulowania terminalem.
    """

    def __init__(self):
        """
        Funkcja służąca do tworzenia obiektów ApplicationTerminal (konstruktor).
        """

        super().__init__()

        main_layout = QHBoxLayout()

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)

        main_layout.addWidget(self.text_output)

        self.setLayout(main_layout)

    def display_text(self, text, color=colors.normal_text_color_hex):
        """
        Funkcja służąca do wyświetlania tekstu w terminalu aplikacji (można ustawić kolor wyświetlanego tekstu).
        """

        self.text_output.setTextColor(QColor(color))
        self.text_output.append(text)

    def display_error_messages(self, error_messages):
        """
        Funkcja służąca do wyświetlania komunikatów błędów w terminalu aplikacji.
        """

        for i in range(0, len(error_messages)):
            self.display_text(error_messages[i], colors.error_text_color_hex)

    def clear_terminal(self):
        """
        Funkcja służąca do usuwania niepotrzebnych komunikatów z terminala aplikacji.
        """

        self.text_output.setText("")

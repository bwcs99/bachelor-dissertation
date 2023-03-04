import os
import sys
from resources import constants
from PyQt5.QtWidgets import QApplication
from general.main_window import MainWindow

"""
Błażej Wróbel, 250070, W4N, informatyka algorytmiczna, 4. rok
"""


def initial_routine():
    """
    Funkcja tworząca katalog, gdzie są trzymane rysunki wykonane przez użytkownika.
    """

    application_working_directory = os.getcwd()
    directory_name = constants.application_files_directory

    directory_path = os.path.join(application_working_directory, directory_name)

    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    else:
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app_window = MainWindow()
    app_window.showMaximized()

    initial_routine()

    sys.exit(app.exec())

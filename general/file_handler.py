import os
import json
from general.graph import Graph
from resources import constants


class FileHandler:
    """
    Klasa, w której są zaimplementowane funkcje, odpowiadające za operacje na plikach tj. tworzenie nowych plików oraz
    otwieranie i usuwanie już istniejących plików.
    """

    def __init__(self):
        """
        Funkcja do tworzenia obiektów klasy FileHandler (konstruktor).
        """

        self.file_name = None
        self.graph_object = None

    def set_file_name(self, file_name):
        """
        Funkcja służąca do ustawiania nazwy pliku.
        """

        self.file_name = file_name

    def set_graph_object(self, graph_object):
        """
        Funkcja służąca do ustawiania obiektu reprezentującego graf.
        """

        self.graph_object = graph_object

    def save_to_file(self):
        """
        Funkcja służąca do zapisywania rysunku grafu do pliku.
        """

        file_main_path = os.path.join(constants.application_files_directory_path, self.file_name)

        if self.file_name is not None and self.graph_object is not None and isinstance(self.graph_object, Graph):
            with open(file_main_path, "w") as file_to_save:
                graph_data_tuple = self.graph_object.get_data_tuple()
                json.dump(graph_data_tuple, file_to_save)
                return True

        return False

    def read_from_file(self):
        """
        Funkcja służąca do odczytu grafu z zapisanego pliku.
        """

        if self.file_name is not None:
            file_main_path = os.path.join(constants.application_files_directory_path, self.file_name)
            with open(file_main_path) as file_to_read:
                data_from_json = json.load(file_to_read)

                decoded_graph_object = self.decode_graph_object(data_from_json)

                restored_graph = Graph()

                restored_graph.restore_graph_from_data_tuple(decoded_graph_object)

                return restored_graph

    def decode_graph_object(self, json_data):
        """
        Funkcja służąca do przetworzenia pliku JSON (zapisany graf) na listę sąsiedztwa reprezentującą dany graf.
        """

        direction_flag = json_data[0]
        neighbours_list_from_json = json_data[1]
        helping_neighbours_list_from_json = json_data[2]
        vertices_list_from_json = json_data[3]
        vertices_size_from_json = int(json_data[4])
        edges_width_from_json = int(json_data[5])

        correct_neighbours_list = []
        correct_helping_neighbours_list = []
        correct_vertices_list = []

        for i in range(0, len(neighbours_list_from_json)):
            correct_neighbours_list.append([])
            for j in range(0, len(neighbours_list_from_json[i])):
                tuple_from_list = tuple(neighbours_list_from_json[i][j])

                correct_neighbours_list[i].append(tuple_from_list)

        for i in range(0, len(helping_neighbours_list_from_json)):
            tuple_from_list = tuple(helping_neighbours_list_from_json[i])

            correct_helping_neighbours_list.append(tuple_from_list)

        for i in range(0, len(vertices_list_from_json)):
            tuple_from_list = tuple(vertices_list_from_json[i])

            correct_vertices_list.append(tuple_from_list)

        return direction_flag, correct_neighbours_list, correct_helping_neighbours_list, correct_vertices_list, vertices_size_from_json, edges_width_from_json

    def delete_selected_file(self, file_name):
        """
        Funkcja służąca do usuwania wybranego pliku.
        """

        try:
            path = os.path.join(constants.application_files_directory, file_name)
            os.remove(path)

            return True
        except OSError:
            return False

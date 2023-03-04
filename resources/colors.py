from PyQt5.QtCore import Qt

"""
Tutaj są kolory używane w aplikacji (np. do wyświetlania kolorowego tekstu czy do zaznaczania wierzchołków
lub krawędzi w grafie).
"""

normal_color = Qt.black
selected_color = Qt.magenta
included_color = Qt.red

vertex_data_color = Qt.green
weight_text_color = Qt.blue

vertex_post_number_color = Qt.green

vertex_component_number = Qt.red
connected_component_text_color = Qt.darkYellow
components_colors = [Qt.blue, Qt.green, Qt.yellow, Qt.cyan, Qt.darkYellow, Qt.gray, Qt.darkRed, Qt.darkMagenta]

normal_text_color_hex = '#000000'
simulation_text_color_hex = '#000000'
error_text_color_hex = '#FF0000'

flow_network_color = Qt.black
residual_graph_color = Qt.darkGreen
residual_backward_edge_color = Qt.cyan
bottleneck_edge_color = Qt.red
increase_edge_flow_color = Qt.red
decrease_edge_flow_color = Qt.blue

algorithm_presentation_normal_line_color = '#000000'
algorithm_presentation_selected_line_color = '#FF0000'

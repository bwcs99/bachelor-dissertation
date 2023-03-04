
"""
Tutaj jest większość napisów i komunikatów generowanych przez aplikację.
"""

main_application_name = f'GraphCharm'

file_menu_name = f'Plik'

file_action1_name = f'Nowy'
file_action2_name = f'Otwórz'
file_action3_name = f'Zapisz'
file_action4_name = f'Usuń'

file_action1_sct = f'Ctrl+N'
file_action2_sct = f'Ctrl+O'
file_action3_sct = f'Ctrl+S'

file_action1_desc = f'Tworzy nowy plik'
file_action2_desc = f'Otwiera istniejący plik'
file_action3_desc = f'Zapisuje graf znajdujacy się w aktywnym oknie'
file_action4_desc = f'Usuwa wybrany plik'

algorithms_menu_name = f'Algorytmy'

prim_algorithm_string = f'Algorytm Prima - szukanie MST'
prim_description_string = f'Wykonuje algorytm Prima na zadanym grafie'

kruskal_algorithm_string = f'Algorytm Kruskala - szukanie MST'
kruskal_description_string = f'Wykonuje algorytm Kruskala na zadanym grafie'

scc_algorithm_string = f'Szukanie silnie spójnych składowych'
scc_description_string = f'Szuka silnie spójnych składowych w grafie skierowanym'

ford_fulkerson_algorithm_string = f'Algorytm Forda-Fulkersona - szukanie maksymalnego przepływu'
ford_fulkerson_description_string = f'Znajduje maksymalny przepływ za pomocą algorytmu Forda-Fulkersona'

edmonds_karp_algorithm_string = f'Algorytm Edmondsa-Karpa - szukanie maksymalnego przepływu'
edmonds_karp_description_string = f'Znajduje maksymalny przepływ za pomocą algorytmu Edmondsa-Karpa'

animation_menu_name = f'Animacja'

end_animation_string = f'Zakończ'
end_animation_description = f'Kończy animację'

end_animation_display_results = f'Zakończ i wyświetl efekt końcowy'
end_animation_display_results_description = f'Kończy animację i wyświetla efekt końcowy'

terminal_menu_name = f'Terminal'

clear_terminal_string = f'Wyczyść terminal'
clear_terminal_description = f'Czyści widoczny na ekranie terminal'

settings_menu_name = f'Ustawienia'
settings_action1_string = f'Rozmiar wierzchołków'
settings_action1_desc = f'Zmienia rozmiar wierzchołków w grafie'

twenty_label = '20'
thirty_label = '30'
fourty_label = '40'
fifty_label = '50'

set_vertices_size = f'Ustaw rozmiar wierzchołków'

help_menu_string = f'Pomoc'
info_action_string = f'O programie'
info_action_desc = f'Wyświetla instrukcję obsługi programu'

manual_dialog_title = f'Instrukcja obsługi'

choose_file_label_string = f'Wybierz plik: '
open_file_dialog_title = f'Otwórz plik...'

new_file_label_string = f'Nazwa pliku: '
graph_kind_label_string = f'Rodzaj grafu: '
directed_label_string = f'Skierowany'
undirected_label_string = f'Nieskierowany'

select_file_to_delete_string = f'Wybierz plik do usunięcia: '
delete_file_dialog_window = f'Usuń wybrany plik...'

add_vertex_action = f'Dodaj wierzhołek'
add_edge_action = f'Dodaj krawędź'
normal_mode_action = f'Tryb normalny'
vertices_data_action = f'Wyświetl dane wierzchołków'
restore_action = f'Przywróć'
clear_action = f'Wyczyść'

delete_vertex_action = f'Usuń wierzchołek'
delete_edge_action = f'Usuń krawędź'
add_weight_action = f'Dodaj wagę'
add_weight_action_auto = f'Dodaj wagi automatycznie'
cancel_operations_action = f'Anuluj'

add_weight_dialog_title = f'Podaj wagę krawędzi...'
add_weight_dialog_prompt = f'Waga krawędzi'

warning_text = f'Ostrzeżenie'
warning_dialog_informative_text = f'Ta operacja spowoduje usunięcie wszystkich danych związanych z grafem. Czy chcesz ' \
                                  f'kontynuować ?'

closing_dialog_title = f'Uwaga !'
closing_info_description = f'W wybranej zakładce działa animacja. Proszę przejść do wybranej zakładki i jescze raz ją '\
                           f'zamknąć (w ten sam sposób).'

graph_not_saved_description = f'W zamykanej zakładce znajduje się niezapisany graf.\n' \
                              f'Zamknięcie tej zakładki spowoduje utracenie dokonanych zmian.\n'\
                              f'Czy kontynuować zamykanie ?'

application_initial_message = f'GC> Witaj w aplikacji wizualizującej algorytmy grafowe. Stwórz nowy plik lub wybierz ' \
                              f'już' \
                              f' istniejący...'

creating_file_terminal_message = f'GC> Stworzono plik: '

opening_file_terminal_message = f'GC> Otworzono plik: '

saving_file_done_terminal_message = f'GC> Zapisano plik: '

deleting_file_done_terminal_message = f'GC> Usunięto plik: '
file_deletion_failure_terminal_message = f'GC> Nie udało się usunąć pliku: '

graph_empty_error_message = f'GC> Błąd! Graf jest pusty.'
graph_directed_error_message = f'GC> Błąd ! Graf nie może być skierowany.'
graph_not_directed_error_message = f'GC> Błąd ! Graf musi być skierowany.'
graph_is_not_connected_message = f'GC> Błąd ! Graf musi być spójny.'
graph_has_isolated_components = f'GC> Błąd ! W grafie nie może być izolowanych składowych.'
no_target_node_error_message = f'GC> Błąd ! W sieci nie ma ujścia.'
no_source_node_error_message = f'GC> Błąd ! W sieci nie ma źródła.'
multi_source_error_message = f'GC> Błąd ! W sieci jest więcej niż jedno źródło.'
multi_target_error_message = f'GC> Błąd ! W sieci jest więcej niż jedno ujście.'
graph_has_negative_weights_error_message = f'GC> Błąd ! W grafie są krawędzie z ujemnymi wagami.'
edge_weight_not_valid_error_message = f'GC> Błąd ! Podano niepoprawną wagę krawędzi.'
file_already_exists_error_message = f'GC> Plik o podanej nazwie już istnieje. Spróbuj ponownie...'
file_reading_error_message = f'GC> Błąd przy wczytywaniu pliku ! Spróbuj ponownie...'
file_saving_error_message = f'GC> Błąd przy zapisywaniu pliku ! Spróbuj ponownie...'

stop_string = f'STOP'

animation_stopped_message = f'GC> Animacja została zakończona.'

mst_select_edge = f'GC> Wybrano krawędź: '

priority_queue_initial_state = f'GC> Początkowy stan kolejki priorytetowej: '
priority_queue_state = f'GC> Stan kolejki priorytetowej: '

kruskal_initial_message = f'GC> Rozpoczynam wykonanie algorytmu Kruskala. Każdy wierzchołek tworzy zbiór jednoelementowy' \
                          f' w strukturze Union-Find i zbiór na krawędzie MST jest pusty.'
kruskal_include_edge = f'GC> Końce krawędzi należą do różnych składowych. '
kruskal_exclude_edge = f'GC> Końce krawędzi należą do tych samych składowych. '
kruskal_final_message = f'GC> Koniec algorytmu. Krawędzie MST: '

prim_initial_message = f'GC> Rozpoczynam wykonanie algorytmu Prima. Ustawiam odpowiednie wartości dla każdego z' \
                       f' wierzchołków i tworzę kolejkę priorytetową z wierzchołkami.'
prim_post_initial_message = f'GC> Wierzchołek początkowy i jego koszt: '
prim_select_vertex_message = f'GC> Wybieram wierzchołek: '
prim_selected_vertex_neighbour = f'GC> Sąsiad wybranego wierzchołka: '
prim_pre_update_message = f'GC> Sprawdzam, czy koszt wierzchołka jest większy niż waga wybranej krawędzi, i czy wierzchołek jest w kolejce.'
prim_update_message = f'GC> Koszt wierzchołka był większy niż waga krawędzi. Zmieniam koszt i przodka wierzchołka na: '
prim_not_update_message = f'GC> Koszt wierzchołka nie był większy niż waga krawędzi lub wierzchołek został usunięty z kolejki. Nie zmieniam danych związanych z ' \
                          f'wierzchołkiem.'

prim_final_message = f'GC> Koniec algorytmu. Znalezione MST: '

scc_initial_message = f'GC> Rozpoczynam algorytm szukania silnie spójnych składowych...'
scc_graph_reversal_message = f'GC> Tworzę graf odwrotny do pierwotnego.'
scc_dfs_on_reversed_graph = f'GC> Wykonuje algorytm DFS na odwróconym grafie, w celu wyznaczenia numeru \'post\' dla ' \
                            f'każdego ' \
                            f'wierzchołka.'
scc_dfs_on_reversed_graph_init = f'GC> Startuje w wierzchołku: '
scc_dfs_visiting_vertex_neighbour_message = f'GC> Odwiedzam sąsiada: '
scc_dfs_not_visiting_vertex_neighbour_message = f'GC> Wierzchołek o numerze '
scc_dfs_post_vertex_message = f'GC> Ostatni raz jestem w wierzchołku '
scc_sorting_vertices_by_post_value = f'GC> Sortuje wierzchołki malejąco względem ich numeru \'post\'.'
scc_sorting_result_message = f'GC> Wynik sortowania: '
scc_dfs_on_normal_graph_message = f'GC> Wykonuje algorytm DFS na pierwotnym grafie. Wierzchołki przeglądam w kolejności ' \
                                  f'malejących numerów \'post\'.'
scc_final_message = f'GC> Koniec algorytmu. Znalezione silnie spójne składowe: '

ford_fulkerson_initial_message = f'GC> Rozpoczynam szukanie maksymalnego przepływu za pomocą algorytmu Forda-Fulkersona.' \
                                 f' Ustawiam przepływ dla każdej krawędzi w sieci na 0.'
edmonds_karp_initial_message = f'GC> Rozpoczynam szukanie maksymalnego przepływu za pomocą algorytmu Edmondsa-Karpa.' \
                               f' Ustawiam przepływ dla każdej krawędzi w sieci na 0.'

ford_fulkerson_final_message = f'GC> Koniec algorytmu Forda-Fulkersona. Znaleziona wartość maksymalnego przepływu: '
edmonds_karp_final_message = f'GC> Koniec algorytmu Edmondsa-Karpa. Znaleziona wartość maksymalnego przepływu: '

found_augumenting_path_message = f'GC> Znaleziona ścieżka powiększająca w sieci residualnej: '
residual_capacity_message = f'GC> Znaleziona przepustowość residualna: '

initial_flow_network_message = f'GC> Rysuje początkową sieć przepływową...'
flow_network_message = f'GC> Rysuje aktualną sieć przepływową...'

residual_network_message = f'GC> Rysuje sieć residualną dla aktualnej sieci przepływowej...'

current_flow_message = f'GC> Aktualny maksymalny przepływ: '

prim_final_result = f'prim'
kruskal_final_result = f'kruskal'
scc_final_result = f'scc'
ford_fulkerson_final_result = f'ford-fulkerson'
edmonds_karp_final_result = f'edmonds-karp'

display_vertices_data_mnemonic = f'dvd'

select_edge_mnemonic = f'sele'
include_edge_mnemonic = f'ince'
exclude_edge_mnemonic = f'exle'

select_vertex_mnemonic = f'selv'
include_vertex_mnemonic = f'incv'
exclude_vertex_mnemonic = f'exv'
update_vertex_mnemonic = f'upv'

reverse_graph_mnemonic = f'rvg'

display_MST_mnemonic = f'dmst'

restore_canvas_mnemonic = f'rec'

mark_components_mnemonic = f'mcom'

clear_dfs_path_mnemonic = f'cpat'

display_flow_network_mnemonic = f'dfn'
display_residual_graph_mnemonic = f'drg'
display_augumenting_path_mnemonic = f'dap'
display_edge_current_flow = f'decf'
mark_bootleneck_edge_mnemonic = f'mbe'
display_altered_edge_flow_mnemonic = f'daef'

select_line_in_pseudocode_instruction = f'select_line'

icon_file_name = 'resources/petersen.png'

adding_vertices_mode_string = 'adding_vertices_mode'
adding_edges_mode_string = 'adding_edges_mode'
normal_mode_string = 'normal_mode'
displaying_vertices_data_string = 'displaying_vertices_data_mode'
clearing_mode_string = 'clearing_mode'

prim_pseudocode_line_1 = f'1. for all u in V: '
prim_pseudocode_line_2 = f'2.   cost(u) = +inf'
prim_pseudocode_line_3 = f'3.   prev(u) = nil'
prim_pseudocode_line_4 = f'4.   known(u) = False'
prim_pseudocode_line_5 = f'5. cost(0) = 0'
prim_pseudocode_line_6 = f'6. H = makequeue(V)'
prim_pseudocode_line_7 = f'7. while H is not empty: '
prim_pseudocode_line_8 = f'8.   v = deletemin(H)'
prim_pseudocode_line_9 = f'9.   known(v) = True'
prim_pseudocode_line_10 = f'10. for each {{v, z}} in E: '
prim_pseudocode_line_11 = f'11.   if cost(z) > w(v, z) and not known(z): '
prim_pseudocode_line_12 = f'12.     cost(z) = w(v, z)'
prim_pseudocode_line_13 = f'13.     prev(z) = v'
prim_pseudocode_line_14 = f'14.     decreasekey(H, z)'

whole_prim_pseudocode = [
    prim_pseudocode_line_1,
    prim_pseudocode_line_2,
    prim_pseudocode_line_3,
    prim_pseudocode_line_4,
    prim_pseudocode_line_5,
    prim_pseudocode_line_6,
    prim_pseudocode_line_7,
    prim_pseudocode_line_8,
    prim_pseudocode_line_9,
    prim_pseudocode_line_10,
    prim_pseudocode_line_11,
    prim_pseudocode_line_12,
    prim_pseudocode_line_13,
    prim_pseudocode_line_14
]

kruskal_pseudocode_line1 = f'1. for all u in V: '
kruskal_pseudocode_line2 = f'2.   makeset(u)'
kruskal_pseudocode_line3 = f'3. X = {{}}'
kruskal_pseudocode_line4 = f'4. Sort edges in E by weight'
kruskal_pseudocode_line5 = f'5. for all edges {{u, v}} in E, in increasing order of weight: '
kruskal_pseudocode_line6 = f'6.   if find(u) != find(v): '
kruskal_pseudocode_line7 = f'7.     add edge {{u, v}} to X'
kruskal_pseudocode_line8 = f'8.     union(u, v)'

whole_kruskal_pseudocode = [
    kruskal_pseudocode_line1,
    kruskal_pseudocode_line2,
    kruskal_pseudocode_line3,
    kruskal_pseudocode_line4,
    kruskal_pseudocode_line5,
    kruskal_pseudocode_line6,
    kruskal_pseudocode_line7,
    kruskal_pseudocode_line8

]

scc_pseudocode_line1 = f'1. Construct graph reversal'
scc_pseudocode_line2 = f'2. Perform DFS on reversed graph'
scc_pseudocode_line3 = f'3. Sort vertices by post values (decreasing order)'
scc_pseudocode_line4 = f'4. Perform DFS on initial graph (process vertices by decreasing value of post number)'

whole_scc_pseudocode = [
    scc_pseudocode_line1,
    scc_pseudocode_line2,
    scc_pseudocode_line3,
    scc_pseudocode_line4
]

max_flow_pseudocode_line1 = f'1. for each edge (u, v) in G.E: '
max_flow_pseudocode_line2 = f'2.   (u, v).f = 0'
max_flow_pseudocode_line3 = f'3. while there exists a path p from s to t in residual network Gr: '
max_flow_pseudocode_line4 = f'4.   residual_capacity = min({{c(u, v) : (u, v) is in p}})'
max_flow_pseudocode_line5 = f'5.   for each edge (u, v) in p: '
max_flow_pseudocode_line6 = f'6.     if (u, v) in G.E: '
max_flow_pseudocode_line7 = f'7.       (u, v).f = (u, v).f + residual_capacity'
max_flow_pseudocode_line8 = f'8.     else: '
max_flow_pseudocode_line9 = f'9.       (v, u).f = (v, u).f - residual_capacity'

whole_max_flow_pseudocode = [
    max_flow_pseudocode_line1,
    max_flow_pseudocode_line2,
    max_flow_pseudocode_line3,
    max_flow_pseudocode_line4,
    max_flow_pseudocode_line5,
    max_flow_pseudocode_line6,
    max_flow_pseudocode_line7,
    max_flow_pseudocode_line8,
    max_flow_pseudocode_line9
]

manual_string = f'1. W celu utworzenia nowego pliku, proszę wybrać opcję \"Nowy\" w menu \"Plik\".\n' \
                f'2. W celu otworzenia istniejącego pliku, proszę wybrać opcję \"Otwórz\" w menu \"Plik\".\n' \
                f'3. W celu zapisania pliku, proszę wybrać opcję \"Zapisz\" w menu \"Plik\" lub kliknąć kombinacje ' \
                f'klawiszy \"Ctrl+S \". \n' \
                f'4. Istnieje możliwość otworzenia wcześniej przygotowanych plików z rysunkami grafów,' \
                f' na których można uruchomić wybraną' \
                f' animację. Wystarczy wybrać opcję \"Otwórz\" znajdującą się w menu \"Plik\".\n' \
                f'5. W celu usunięcia wybranego pliku, proszę wybrać opcję \"Usuń\" znajdującą się w menu \"Plik\".\n' \
                f'6. Podczas tworzenia nowego pliku, nie trzeba wybierać rodzaju grafu - domyślnie jest tworzony graf '\
                f'nieskierowany.\n' \
                f'7. W celu dodania wierzchołka, proszę wybrać opcję \"Dodaj wierzchołek\" dostępną w pasku narzędzi ' \
                f'(widocznym nad miejscem do rysowania) i wcisnąć lewy przycisk myszy w miejscu, w którym ma być ' \
                f'wierzchołek. \n' \
                f'8. W celu dodania krawędzi, proszę wybrać opcję \"Dodaj krawędź\" dostępną w pasku narzędzi ' \
                f'(widocznym nad miejscem do rysowania) oraz przeciągnąć kursor myszy z początkowego wierzchołka do ' \
                f'końcowego (lewy przycisk myszy ma być wciśnięty). Krawędź zostanie narysowana tylko wtedy, gdy ' \
                f'początek i koniec krawędzi leży nad wybranymi wierzchołkami. \n' \
                f'9. W celu przesuwania wierzchołków i wag krawędzi, proszę wybrać opcję \"Tryb normalny\" dostępną ' \
                f'w pasku narzędzi (widocznym nad miejscem do rysowania). W celu zmiany położenia ' \
                f'wierzchołka/wagi krawędzi, proszę kliknąć lewym przyciskiem myszy nad wybranym obiektem i przesunąć w '\
                f'miejsce docelowe. \n' \
                f'10. W celu wyświetlenia danych związanych z wierzchołkami, proszę wybrać opcję \"Wyświetl dane ' \
                f'wierzchołków\" dostępną w pasku narzędzi. Zmienianie pozycji wyświetlania danych związanych z ' \
                f'wierzchołkami odbywa się tak samo, jak zmiana położenia wierzchołków/wag krawędzi.\n' \
                f'11. W celu przywrócenia pierwotnej postaci grafu (po animacji lub po' \
                f' wyłączeniu animacji i wyświetleniu efektu końcowego), proszę wybrać opcję \"Przywróć\" ' \
                f'dostępną w pasku narzędzi (grafem zmienionym po animacji nie da się manipulować).\n' \
                f'12. W celu usunięcia rysunku grafu, proszę wybrać opcję \"Wyczyść\" dostępną w pasku narzędzi.\n' \
                f'13. W celu otworzenia menu kontekstowego (w zakładce do rysowania), proszę wcisnąć prawy ' \
                f'przycisk myszy. W menu kontekstowym są następujące opcje: \n' \
                f'  1. Usuwanie wierzchołka.\n' \
                f'  2. Usuwanie krawędzi.\n' \
                f'  3. Dodawanie wagi do krawędzi.\n' \
                f'  4. Automatyczne dodawanie wag do wszystkich krawędzi.\n' \
                f'  5. Anuluj - wyłączanie menu kontekstowego.\n' \
                f'14. W celu wybrania algorytmu i włączenia jego animacji, proszę wybrać jeden z dostępnych ' \
                f'algorytmów znajdujących się w menu \"Algorytmy\".\n' \
                f'15. Podczas animowania algorytmów w danej zakładce, nie ma możliwości zapisywania rysunku grafu do ' \
                f'pliku, usuwania wybranego pliku z rysunkiem grafu, uruchamiania innych animacji, usuwania komunikatów' \
                f' generowanych przez aplikację oraz zmieniania rozmiaru wierzchołków grafu - opcje odpowiadające tym ' \
                f'czynnościom nie działają. Te ograniczenie obejmuje tylko zakładki z działającą animacją - we ' \
                f'wszystkich innych zakładkach, w których nie jest animowany żaden algorytm, wspomniane opcje ' \
                f'działają.\n' \
                f'16. Podczas animowania algorytmu na wybranym grafie, nie ma możliwości manipulowania rysunkiem tego ' \
                f'grafu.\n'\
                f'17. W celu wyłączenia animacji lub wyłączenia animacji i wyświetlenia efektu końcowego, proszę wybrać ' \
                f'opcję (odpowiednio) \"Zakończ\"/\"Zakończ i wyświetl efekt końcowy\" znajdującą się w menu ' \
                f'\"Animacja\".\n' \
                f'18. W celu usunięcia komunikatów generowanych przez aplikację, proszę wybrać opcję ' \
                f'\"Wyczyść terminal\" znajdującą się w menu \"Terminal\".\n' \
                f'19. W celu zmiany rozmiaru wierzchołków grafu, proszę wybrać opcję \"Rozmiar wierzchołków\" ' \
                f'znajdującą się w menu \"Ustawienia\".\n' \
                f'20. Podczas animowania algorytmów szukania maksymalnego przepływu, krawędzie i wagi związane z grafem' \
                f' residualnym są oznaczone kolorem niebieskim (waga krawędzi \"powrotnej\" jest rysowana tuż pod wagą' \
                f' krawędzi z sieci przepływowej i ma kolor niebieski).\n'


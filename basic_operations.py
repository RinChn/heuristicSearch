import os

import psutil

from node import Node

MOVES = {
    (-1, 0): "UP",
    (1, 0): "DOWN",
    (0, -1): "LEFT",
    (0, 1): "RIGHT"
}


def get_initial_state() -> list:
    """
    Получение начального состояния.
    :return: Начальное состояние.
    """
    # return [
    #     [5, 6, 4],
    #     [2, 3, 8],
    #     [7, 1, 0]
    # ]
    return [
        [5, 6, 4],
        [2, 3, 0],
        [7, 1, 8]
    ]


def get_finish_state() -> list:
    """
    Получение конечного состояния.
    :return: Конечное состояние.
    """
    # return [
    #     [0, 1, 2],
    #     [3, 4, 5],
    #     [6, 7, 8]
    # ]
    return [
        [5, 6, 4],
        [2, 3, 8],
        [7, 1, 0]
    ]


def print_path(node: "Node"):
    """
    Вывод полного пути от начального до конечного состояния в консоль.
    :param node: Конечный узел выводимого пути.
    """
    path = []
    current_node = node

    while current_node.parent_node:
        path.append(current_node)
        current_node = current_node.parent_node
    path.append(current_node)

    for path_node in path[::-1]:
        print_node(path_node)
        print("^\n:\n:\n_\n")


def print_node(node: "Node", is_duplicate: bool = False):
    """
    Вывод информации об узле на экран.
    :param is_duplicate: Является ли состояние в узле повторным.
    :param node: Узел, информация о котором выводится.
    """
    parent_id = 0

    if node.parent_node:
        parent_id = node.parent_node.node_id

    node_prev_action = None
    if node.previous_action:
        node_prev_action = MOVES[node.previous_action]

    print(f"ID = {node.node_id}, ParentID = {parent_id}, " +
          f"Action = {node_prev_action}, \nDepth = {node.depth}, " +
          f"Cost = {node.path_cost}, \nState: ")
    print_state(node.current_state)
    if is_duplicate:
        print("Повторное состояние")
    print()


def print_state(state: list):
    """
    Вывод состояния матрицей.
    :param state: Двумерный список-состояние.
    """
    for row in state:
        print(" ".join(str(cell) if cell != 0 else " " for cell in row))


def check_final(current_state: list) -> bool:
    """
    Проверка состояния на то, является ли оно конечным.
    :param current_state: проверяемое состояние.
    :return: True, если состояние конечное; False иначе.
    """
    return current_state == get_finish_state()


def state_swap(descendant: dict, current_state: list, move: tuple, pos_i: int, pos_j: int):
    """
    Перемещение ячейки.
    :param descendant: Словарь наследников.
    :param current_state: Состояние-родитель.
    :param move: Передвижение, совершаемое "пустой ячейкой".
    :param pos_i: Координата пустой ячейки по оси Y.
    :param pos_j: Координата пустой ячейки по оси X.
    """
    new_state = [row[:] for row in current_state]
    new_pos_i = pos_i + move[0]
    new_pos_j = pos_j + move[1]

    if 0 <= new_pos_i <= 2 and 0 <= new_pos_j <= 2:
        new_state[pos_i][pos_j], new_state[new_pos_i][new_pos_j] = new_state[new_pos_i][new_pos_j], \
                                                                   new_state[pos_i][pos_j]
        descendant[move] = new_state


def get_empty_cell(state: list) -> tuple[int, int]:
    """
    Получение координат пустой ячейки.
    :param state: Состояние для поиска.
    :return: Координаты пустой ячейки.
    """
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def get_followers(current_state: list) -> dict[tuple, list[Node]]:
    """
    Функция последователей.
    :param current_state: состояние, последователей которого необходимо получить.
    :return: Последователи.
    """
    new_states = {}
    pos_i, pos_j = get_empty_cell(current_state)
    for move, action in MOVES.items():
        state_swap(new_states, current_state, move, pos_i, pos_j)
    return new_states


def print_info(iterations: int, time: float, visited_states: int, path_cost: int):
    """
    Вывод информации о результате поиска.
    :param iterations: Количество итераций в поиске.
    :param time: Время, за которое был произведен поиск.
    :param visited_states: Количество посещенных состояний во время поиска.
    :param path_cost: Стоимость пройденного пути.
    """
    print(f"\nКоличество УЗЛОВ в дереве: {Node.get_nodes_count()}")
    print(f"Количество ИТЕРАЦИЙ в поиске: {iterations}")
    print(f"Количество пройденных СОСТОЯНИЙ: {visited_states}")
    print(f"Затраченное ВРЕМЯ: {time * 1000} мс")
    print(f"Затраченная ПАМЯТЬ: {psutil.Process(os.getpid()).memory_info().rss} байт")
    print(f"СТОИМОСТЬ найденного пути: {path_cost}")


def state_hash(state: list) -> int:
    """
    Хеширование состояния.
    :param state: Состояние.
    :return: Хэш-таблица состояния.
    """
    return hash(tuple(map(tuple, state)))

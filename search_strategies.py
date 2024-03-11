import sys
from time import process_time

from node import Node
from basic_operations import print_info, check_final, state_hash, \
    get_followers, print_node, print_path, get_initial_state

sys.setrecursionlimit(10000)  # Предел рекурсии
DEBUG = False


def dfs(debug_flag: int, depth_limit: int = None):
    """
    Поиск в глубину.
    :param debug_flag: Выбор пользователя относительно пошагового вывода поиска.
    :param depth_limit: Ограничение для поиска с ограничением глубины.
    """
    global DEBUG
    DEBUG = debug_flag

    # Выводим сообщение о начале алгоритма DLS
    if depth_limit:
        print("ПОИСК В ГЛУБИНУ С ОГРАНИЧЕНИЕМ DLS — Deep-Limited Search.")
    else:
        print("ПОИСК СНАЧАЛА В ГЛУБИНУ DFS — Depth-first Search.")
    start_node = Node(get_initial_state(), None, None, 0, 0)  # Начальный узел
    visited_states = set()  # Множество посещенных состояний
    queue = [start_node]  # Очередь для хранения узлов
    result_node = None  # Переменная для хранения результата
    iterations = 0  # Счетчик итераций
    defining_sequences.limit_reached = False  # Ограничитель на рекурсию

    START_TIME = process_time()
    # Основной цикл алгоритма
    while queue:
        result_node, iterations = defining_sequences(queue.pop(0), visited_states, queue, iterations, depth_limit)
        if result_node is not None:
            break

    if result_node is not None:
        TIME_STOP = process_time()
        print("\n---Конечное состояние достигнуто!---")
        print_path(result_node)
        print("Информация о поиске:")
        print_info(iterations=iterations, time=TIME_STOP - START_TIME, visited_states=len(visited_states),
                   path_cost=result_node.path_cost)
    else:
        print("\nПуть к конечному состоянию не найден.")

    if not visited_states:
        print("\nВсе состояния были исследованы, но решение не было найдено.")


def defining_sequences(current_node: "Node", visited_states: set,
        queue: list, iterations: int, depth_limit: int = None):
    """
    Рекурсивная часть алгоритма поиска в глубину.
    :param current_node: Текущий обрабатываемый узел.
    :param visited_states: Список посещённых состояний.
    :param queue: Очередь узлов.
    :param iterations: Количество прошедших итераций.
    :param depth_limit: Ограничение в глубину для поиска с ограничением.
    :return: Найденное конечное состояние и затраченное для этого количество итераций.
    """
    iterations += 1  # Увеличиваем счетчик итераций

    # Проверяем, достигнуто ли конечное состояние
    if check_final(current_node.current_state):
        return current_node, iterations

    # Хэшируем текущее состояние для проверки посещенных состояний
    state_hash_value = state_hash(current_node.current_state)

    # Если состояние уже посещалось, пропускаем его
    if state_hash_value in visited_states:
        return None, iterations

    visited_states.add(state_hash_value)  # Добавляем текущее состояние в множество посещенных

    # Проверка для ограниченного по глубине поиска
    if depth_limit is not None and current_node.depth >= depth_limit:
        if not defining_sequences.limit_reached:
            print("\nДостигнуто ограничение глубины!")
            queue.clear()  # Очищаем очередь
            defining_sequences.limit_reached = True  # Меняем флаг достижения глубины
        return None, iterations

    new_states_dict = get_followers(current_node.current_state)  # Получаем новые состояния из текущего узла

    # Отладочный вывод текущего узла и всех его потомков по шагам
    if DEBUG:
        print(f"----------------Шаг {iterations}.---------------- \n")
        print("Текущий узел:", end=' ')
        if iterations == 1:
            print("Корень дерева")
        print_node(current_node)
        print("Потомки:")

    # Исследуем каждого потомка
    for child_action, child_state in new_states_dict.items():
        # Хэшируем состояние и инициализируем как узел
        child_hash_value = state_hash(child_state)
        child_node = Node(child_state, current_node, child_action, current_node.path_cost + 1,
                          current_node.depth + 1)

        if child_hash_value not in visited_states:
            if DEBUG:
                print_node(child_node)
            queue.append(child_node)  # Помещаем узел в очередь
        elif DEBUG:
            print_node(child_node, is_duplicate=True)
    if DEBUG:
        input("Нажмите 'Enter' для продолжения...")

    # Рекурсивно переходим к обработке полученных потомков, удаляя их постепенно из очереди
    while queue:
        result_node, iterations = defining_sequences(queue.pop(0), visited_states, queue, iterations, depth_limit)
        if result_node is not None:
            return result_node, iterations

    return None, iterations

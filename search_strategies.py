import sys
from time import process_time

from node import Node
from basic_operations import print_info, check_final, state_hash, \
    get_followers, print_state, print_node, print_path, get_initial_state, get_finish_state, MOVES, get_coordinates_cell

sys.setrecursionlimit(1000000)  # Предел рекурсии
DEBUG = False


def h1(state, print_flag: bool = False):
    """
    Эвристическая функция h1.
    :param state: Текущее состояние.
    :param print_flag: Флаг вывода фишек и их присутствия/отусутствия на нужных позициях.
    :return: количество фишек, стоящих не на своем месте.
    """
    # Получаем целевое состояние игры
    target_state = get_finish_state()

    # Счетчик фишек, не на своем месте
    misplaced_cells = 0

    if print_flag:
        print("\nФишки:")
    # Проходим по каждой клетке текущего состояния
    for i in range(3):
        for j in range(3):
            current_cell = state[i][j]
            target_cell = target_state[i][j]
            # Проверяем, является ли текущая клетка пустой
            if current_cell != 0:
                if current_cell != target_cell:
                    if print_flag:
                        print(f"({current_cell}) - НЕ на своем месте")
                    misplaced_cells += 1
                else:
                    if print_flag:
                        print(f"({current_cell}) + на своем месте")

    return misplaced_cells


def h2(state: list, print_flag: bool = False) -> int:
    """
    Эвристическая функция h2.
    :param state: Текущее состояние.
    :param print_flag: Флаг вывода расстояний фишек до целевых позиций.
    :return: Сумма расстояний каждой фишки до ее целевой позиции.
    """
    target_state = get_finish_state()  # Получаем целевое состояние
    total_distance = 0  # Инициализируем суммарное расстояние
    if print_flag:
        print("\nРасстояния:")

    # Проходим по всем клеткам текущего состояния
    for i in range(3):
        for j in range(3):
            cell = state[i][j]
            if cell != 0:  # Пропускаем пустую ячейку
                # Ищем координаты фишки в целевом состоянии
                target_i, target_j = get_coordinates_cell(target_state, cell)
                # Вычисляем расстояние между текущей позицией и целевой
                distance = abs(target_i - i) + abs(target_j - j)
                if print_flag:
                    print(f"({state[i][j]}) {distance}", end="  ")
                total_distance += distance
        if print_flag:
            print()

    return total_distance


def search(debug_flag: int, depth_limit: int = None, h_flag: int = None):
    """
    Поиск в глубину.
    :param debug_flag: Выбор пользователя относительно пошагового вывода поиска.
    :param depth_limit: Ограничение для поиска с ограничением глубины.
    :param h_flag: Флаг выбора эвристической функции.
    """
    global DEBUG
    DEBUG = debug_flag

    if depth_limit:
        print("\n\nПОИСК В ГЛУБИНУ С ОГРАНИЧЕНИЕМ DLS — Deep-Limited Search.")
    else:
        print("\n\nПОИСК СНАЧАЛА В ГЛУБИНУ DFS — Depth-first Search.")
    start_node = Node(get_initial_state(), None, None, 0, 0)  # Начальный узел
    visited_states = set()  # Множество посещенных состояний
    stack = [start_node]  # стек для хранения узлов
    result_node = None  # Переменная для хранения результата
    iterations = 0  # Счетчик итераций
    defining_sequences.limit_reached = False  # Ограничитель на рекурсию

    start_time = process_time()
    # Основной цикл алгоритма
    while stack:
        result_node, iterations = defining_sequences(stack.pop(), visited_states, stack, iterations, depth_limit,
                                                     h_flag)
        if result_node is not None:
            break

    if result_node is not None:
        time_stop = process_time()
        print("\n---Конечное состояние достигнуто!---")
        print_path(result_node)
        print("Информация о поиске:")
        print_info(iterations=iterations, time=time_stop - start_time, visited_states=len(visited_states),
                   path_cost=result_node.path_cost)
    else:
        print("\nПуть к конечному состоянию не найден.")

def defining_sequences(current_node: "Node", visited_states: set,
                       stack: list, iterations: int, depth_limit: int = None,
                       h_flag: int = None):
    """
    Рекурсивная часть алгоритма поиска в глубину с учетом выбранной эвристики.
    :param current_node: Текущий обрабатываемый узел.
    :param visited_states: Список посещённых состояний.
    :param stack: Стек узлов.
    :param iterations: Количество прошедших итераций.
    :param depth_limit: Ограничение в глубину для поиска с ограничением.
    :param h_flag: Флаг выбора эвристической функции.
    :return: Найденное конечное состояние и затраченное для этого количество итераций.
    """
    iterations += 1  # Увеличиваем счетчик итераций

    # Проверяем, достигнуто ли конечное состояние
    if check_final(current_node.current_state):
        return current_node, iterations

    # Хэшируем текущее состояние для проверки посещенных состояний
    state_hash_value = state_hash(current_node.current_state)

    # Добавляем текущее состояние в множество посещенных
    visited_states.add(state_hash_value)

    # Проверка для ограниченного по глубине поиска
    if depth_limit is not None and current_node.depth >= depth_limit:
        if not defining_sequences.limit_reached:
            print("\nДостигнуто ограничение глубины!")
            stack.clear()  # Очищаем стек
            defining_sequences.limit_reached = True  # Меняем флаг достижения глубины
        return None, iterations

    new_states_dict = get_followers(current_node.current_state)  # Получаем новые состояния из текущего узла

    # Сортировка в соответствии с выбранной функцией h в обратном порядке
    # (приоритет - состояние суммой наименьшего з-я эвристической ф-ции и стоимости пути до тек. узла)
    if h_flag == 1:
        new_states_sorted = sorted(new_states_dict.items(),
                                   key=lambda item: h1(item[1])+current_node.path_cost,
                                   reverse=True)
    elif h_flag == 2:
        new_states_sorted = sorted(new_states_dict.items(),
                                   key=lambda item: h2(item[1])+current_node.path_cost,
                                   reverse=True)
    else:
        # Если выбрана другая эвристика или она не выбрана, не выполняем сортировку
        new_states_sorted = new_states_dict.items()

    # Отладочный вывод текущего узла и всех его потомков по шагам
    if DEBUG:
        print(f"----------------Шаг {iterations}.---------------- \n")
        print("Текущий узел:", end=' ')
        if iterations == 1:
            print("Корень дерева")
        print_node(current_node)
        print("\nПотомки:")

    # Исследуем каждого потомка
    for child_action, child_state in new_states_sorted:
        # Хэшируем состояние и инициализируем как узел
        child_hash_value = state_hash(child_state)
        if child_hash_value not in visited_states:
            child_node = Node(child_state, current_node, child_action, current_node.path_cost + 1,
                              current_node.depth + 1)
            if DEBUG:
                print_node(child_node)  # Выводим информацию о потомке
                if h_flag == 1:
                    print("\nЗначение эвристической функции h1:", h1(child_node.current_state, print_flag=True)+child_node.path_cost)
                elif h_flag == 2:
                    print("\nЗначение эвристической функции h2:",
                          h2(child_node.current_state, print_flag=True)+child_node.path_cost)
                print()

            stack.append(child_node)  # Помещаем узел в стек
        elif DEBUG:
            print(f"\nПовторное состояние: \nAction = {MOVES[child_action]}, \nState: ")
            print_state(child_state)
            print()
    if DEBUG:
        input("Нажмите 'Enter' для продолжения...")

    # Рекурсивно переходим к обработке полученных потомков, удаляя их постепенно из очереди
    while stack:
        result_node, iterations = defining_sequences(stack.pop(), visited_states, stack, iterations, depth_limit,
                                                     h_flag)
        if result_node is not None:
            return result_node, iterations

    return None, iterations

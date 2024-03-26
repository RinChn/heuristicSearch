import sys
from time import process_time

from node import Node
from basic_operations import print_info, check_final, state_hash, \
    get_followers, print_state, print_node, print_path, get_initial_state, get_finish_state, MOVES, get_coordinates_cell

sys.setrecursionlimit(1000000)  # Предел рекурсии
DEBUG = False


def h1(state):
    """
    Эвристическая функция h1.
    :param state: Текущее состояние.
    :return: Количество фишек, стоящих не на своем месте.
    """
    # Получаем целевое состояние игры
    target_state = get_finish_state()

    # Счетчик фишек, не на своем месте
    misplaced_cells = 0

    if DEBUG:
        print("\nФишки:")
    # Проходим по каждой клетке текущего состояния
    for i in range(3):
        for j in range(3):
            current_cell = state[i][j]
            target_cell = target_state[i][j]
            # Проверяем, является ли текущая клетка пустой
            if current_cell != 0:
                if current_cell != target_cell:
                    if DEBUG:
                        print(f"({current_cell}) - НЕ на своем месте")
                    misplaced_cells += 1
                else:
                    if DEBUG:
                        print(f"({current_cell}) + на своем месте")

    return misplaced_cells


def h2(state: list) -> int:
    """
    Эвристическая функция h2.
    :param state: Текущее состояние.
    :return: Сумма расстояний каждой фишки до ее целевой позиции.
    """
    target_state = get_finish_state()  # Получаем целевое состояние
    total_distance = 0  # Инициализируем суммарное расстояние
    if DEBUG:
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
                if DEBUG:
                    print(f"({state[i][j]}) {distance}", end="  ")
                total_distance += distance
        if DEBUG:
            print()

    return total_distance


h_func = {1: h1, 2: h2}


def search(debug_flag: int, h_flag: int = None, greedy_flag: bool = None):
    """
    Поиск А*: подготовка структур данных, запуск поиска.
    :param greedy_flag: Флаг выбора жадного поиска
    :param debug_flag: Выбор пользователя относительно пошагового вывода поиска.
    :param h_flag: Флаг выбора эвристической функции.
    """
    global DEBUG
    DEBUG = debug_flag

    if greedy_flag:
        print("\n\nЖАДНЫЙ ПОИСК.")
    else:
        print("\n\nЭВРИСТИЧЕСКИЙ ПОИСК А*.")

    start_node = Node(get_initial_state(), None, None, 0, 0, 0)  # Начальный узел
    visited_states = set()  # Множество посещенных состояний
    queue = [start_node]  # Очередь с приоритетом для хранения узлов
    result_node = None  # Переменная для хранения результата
    iterations = 0  # Счетчик итераций

    start_time = process_time()

    # Основной цикл алгоритма
    while queue:
        result_node, iterations = defining_sequences(queue.pop(0), visited_states, queue, iterations,
                                                     h_flag, greedy_flag)
        if result_node is not None:
            break

    time_stop = process_time()
    print("\n---Конечное состояние достигнуто!---")
    print_path(result_node)
    print("Информация о поиске:")
    print_info(iterations=iterations, time=time_stop - start_time, visited_states=len(visited_states),
               path_cost=result_node.path_cost)


def defining_heuristic_node(h_numb: int, current_node: "Node", greedy_flag: bool):
    current_node.cost_estimation = h_func[h_numb](current_node.state)
    if not greedy_flag:
        current_node.cost_estimation += current_node.path_cost


def defining_sequences(current_node: "Node", visited_states: set,
                       queue: list, iterations: int,
                       h_flag: int = 0, greedy_flag: bool = False):
    """
    Рекурсивная часть алгоритма поиска А* с учетом выбранной эвристики.
    :param current_node: Текущий обрабатываемый узел.
    :param visited_states: Список посещённых состояний.
    :param queue: Очередь узлов.
    :param iterations: Количество прошедших итераций.
    :param h_flag: Флаг выбора эвристической функции.
    :param greedy_flag: Флаг выбора жадного поиска
    :return: Найденное конечное состояние и затраченное для этого количество итераций.
    """
    iterations += 1  # Увеличиваем счетчик итераций

    # Проверяем, достигнуто ли конечное состояние
    if check_final(current_node.state):
        return current_node, iterations

    # Хэшируем текущее состояние для проверки посещенных состояний
    state_hash_value = state_hash(current_node.state)

    # Добавляем текущее состояние в множество посещенных
    visited_states.add(state_hash_value)

    # Получаем новые состояния из текущего узла
    new_states_dict = get_followers(current_node.state)
    if iterations == 1:
        defining_heuristic_node(h_flag, current_node, greedy_flag)
    # Отладочный вывод текущего узла и всех его потомков по шагам
    if DEBUG:
        print(f"\n----------------Шаг {iterations}.---------------- \n")
        print("Текущий узел:", end=' ')
        if iterations == 1:
            print("Корень дерева")
        print_node(current_node)
        print("\nПотомки:")

    # Исследуем каждого потомка
    for child_action, child_state in new_states_dict.items():
        # Хэшируем состояние и инициализируем как узел
        child_hash_value = state_hash(child_state)
        child_node = Node(child_state, current_node, child_action, current_node.path_cost + 1,
                          current_node.depth + 1, 0)
        defining_heuristic_node(h_flag, child_node, greedy_flag)

        if child_hash_value not in visited_states:

            if DEBUG:
                print_node(child_node)  # Выводим информацию о потомке
                print()

            # Выравниваем стоимость для восстановления монотонности эвристики в A*
            if not greedy_flag and child_node.cost_estimation < current_node.cost_estimation:
                child_node.cost_estimation = max(child_node.cost_estimation, current_node.cost_estimation)

            queue.append(child_node)  # Помещаем узел в очередь

        else:
            if DEBUG:
                print(f"\nПовторное состояние: \nСтоимость = {child_node.cost_estimation}\n"
                      f"Action = {MOVES[child_action]}, \nState: ")
                print_state(child_state)
                print()

            # Если новое состояние уже присутствует в очереди,
            # но такой узел имеет большую стоимость пути, чем текущий потомок,
            # то информация о таком узле в очереди обновляется
            for node in queue:
                if node.state == child_node.state and node.path_cost > child_node.path_cost:
                    node.depth = child_node.depth
                    node.parent_node = current_node
                    node.previous_action = child_node.previous_action
                    node.cost_estimation = node.cost_estimation - node.path_cost + child_node.path_cost
                    node.path_cost = child_node.path_cost
                    if DEBUG:
                        print("Узел в очереди с этим же состоянием заменен на этого потомка из-за оценки стоимости.")
                    break
                if child_node.cost_estimation > node.cost_estimation:
                    break

    if DEBUG:
        input("\nНажмите 'Enter' для продолжения...")

    # Сортировка в соответствии с выбранной функцией h в обратном порядке
    # (приоритет - состояние с наименьшей оценкой стоимости)
    queue = sorted(queue, key=lambda item: item.cost_estimation)

    # Рекурсивно переходим к обработке полученных потомков, удаляя их постепенно из очереди
    while queue:
        result_node, iterations = defining_sequences(queue.pop(0), visited_states, queue, iterations, h_flag,
                                                     greedy_flag)
        if result_node is not None:
            return result_node, iterations

    return None, iterations

import sys
from time import process_time

from node import Node
from basic_operations import print_info, check_final, state_hash, \
    get_followers, print_state, print_node, print_path, get_initial_state, get_finish_state, MOVES

sys.setrecursionlimit(1000000)  # Предел рекурсии
DEBUG = False

def h1(state, print_flag: bool):
    """
    Эвристическая функция h1: возвращает количество фишек, стоящих не на своем месте.
    :param state: текущее состояние игры.
    :param print_flag: Флаг вывода фишек и их присутствия/отусутствия на целевых позициях.
    :return: количество фишек, стоящих не на своем месте.
    """
    # Получаем целевое состояние игры
    target_state = get_finish_state()
    
    # Инициализируем счетчик фишек, не на своем месте
    misplaced_tiles = 0
    
    if print_flag:
        print("\nФишки:")
    # Проходим по каждой клетке текущего состояния
    for i in range(3):
        for j in range(3):
            current_tile = state[i][j]
            target_tile = target_state[i][j]
            # Проверяем, является ли текущая клетка пустой
            if current_tile != 0:
                if current_tile != target_tile:
                    if print_flag:
                        print(f"({current_tile}) - НЕ на своем месте")
                    misplaced_tiles += 1
                else:
                    if print_flag:
                        print(f"({current_tile}) + на своем месте")
    
    return misplaced_tiles


def h2(state: list, print_flag: bool) -> int:
    """
    Эвристическая функция h2: возвращает сумму расстояний каждой фишки до ее целевой позиции.
    :param state: Текущее состояние игры.
    :param print_flag: Флаг вывода расстояний фишек до целевых позиций.
    :return: Значение второй эвристической функции.
    """
    target_state = get_finish_state()  # Получаем целевое состояние
    total_distance = 0  # Инициализируем суммарное расстояние
    if print_flag:
        print("\nРасстояния:")
    # Проходим по всем клеткам текущего состояния
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:  # Пропускаем пустую ячейку
                # Ищем координаты фишки в целевом состоянии
                target_i, target_j = find_tile_position(target_state, tile)
                # Вычисляем расстояние между текущей позицией и целевой
                distance = abs(target_i - i) + abs(target_j - j)
                if print_flag:
                    print(f"({state[i][j]}) {distance}", end="  ")
                total_distance += distance

    return total_distance

def find_tile_position(state: list, tile: int) -> tuple:
    """
    Находит позицию фишки в состоянии.
    :param state: Состояние игры.
    :param tile: Фишка, позицию которой нужно найти.
    :return: Позиция фишки в виде кортежа (i, j).
    """
    for i in range(3):
        for j in range(3):
            if state[i][j] == tile:
                return i, j


def search(debug_flag: int, depth_limit: int = None, h_flag: int = None):
    """
    Поиск в глубину.
    :param debug_flag: Выбор пользователя относительно пошагового вывода поиска.
    :param depth_limit: Ограничение для поиска с ограничением глубины.
    :param h_flag: Флаг выбора эвристической функции.
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
    stack = [start_node]  # стек для хранения узлов
    result_node = None  # Переменная для хранения результата
    iterations = 0  # Счетчик итераций
    defining_sequences.limit_reached = False  # Ограничитель на рекурсию

    START_TIME = process_time()
    # Основной цикл алгоритма
    while stack:
        result_node, iterations = defining_sequences(stack.pop(), visited_states, stack, iterations, depth_limit, h_flag)
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

    # Если состояние уже посещалось, пропускаем его
    if state_hash_value in visited_states:
        return None, iterations

    visited_states.add(state_hash_value)  # Добавляем текущее состояние в множество посещенных

    # Проверка для ограниченного по глубине поиска
    if depth_limit is not None and current_node.depth >= depth_limit:
        if not defining_sequences.limit_reached:
            print("\nДостигнуто ограничение глубины!")
            stack.clear()  # Очищаем стек
            defining_sequences.limit_reached = True  # Меняем флаг достижения глубины
        return None, iterations

    new_states_dict = get_followers(current_node.current_state)  # Получаем новые состояния из текущего узла
   
    if h_flag == 1:
        # Сортировка с использованием h1 в обратном порядке, т.к. в приоритете состояние с наименьшим зн-м эвристической ф-ии
        new_states_sorted = sorted(new_states_dict.items(), key=lambda item: h1(item[1], print_flag = False), reverse=True)
    elif h_flag == 2:
        # Сортировка с использованием h2 в обратном порядкет.к. в приоритете состояние с наименьшим зн-м эвристической ф-ии
        new_states_sorted = sorted(new_states_dict.items(), key=lambda item: h2(item[1], print_flag = False), reverse=True)
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
                    print("\nЗначение эвристической функции h1:", h1(child_node.current_state, print_flag = True))
                elif h_flag == 2:
                    print("\n\nЗначение эвристической функции ----------------------> h2:", h2(child_node.current_state, print_flag = True))
                print()

            stack.append(child_node)  # Помещаем узел в стек
        elif DEBUG:
            print(f"Повторное состояние: \nAction = {MOVES[child_action]}, \nState: ")
            print_state(child_state)
            print()
    if DEBUG:
        input("Нажмите 'Enter' для продолжения...")

    # Рекурсивно переходим к обработке полученных потомков, удаляя их постепенно из очереди
    while stack:
        result_node, iterations = defining_sequences(stack.pop(), visited_states, stack, iterations, depth_limit, h_flag)
        if result_node is not None:
            return result_node, iterations

    return None, iterations

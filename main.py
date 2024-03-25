from tabulate import tabulate
from search_strategies import search
from basic_operations import get_initial_state, get_finish_state


def input_h():
    """
    Функция ввода эвристической функции.
    :return: Номер используемой эвристической функции.
    """
    h = input("\nЭвристическая функция h: (1/2)\n> ")
    while h != '1' and h != '2':
        print("Неправильный ввод, повторите попытку!\n")
        h = input("\nЭвристическая функция h: (1/2)\n> ")
    return h


def calculate_inversions(state):
    """
    Функция для подсчета порядка перестановки.
    :param state: Состояние, в котором будут считаться инверсии.
    :return: Общее количество инверсий в state.
    """
    inversions = 0  # Инициализация счетчика инверсий
    # Создание плоского списка состояния игры без пустых ячеек (значения 0)
    flattened_state = [cell for row in state for cell in row if cell != 0]
    # Перебор всех пар элементов в плоском списке
    for i in range(len(flattened_state)):
        for j in range(i + 1, len(flattened_state)):
            # Если порядок элементов в паре нарушен (более большой элемент идет перед меньшим),
            # увеличиваем счетчик инверсий
            if flattened_state[i] > flattened_state[j]:
                inversions += 1
    return inversions


def solution_exists(start_state, end_state):
    """
    Функция для проверки наличия решения.
    :param start_state: Корень дерева.
    :param end_state: Искомое состояние в дереве.
    :return: Существует ли путь от start_state к end_state.
    """
    # Вычисление количества инверсий для начального и конечного состояний
    start_inversions = calculate_inversions(start_state)
    end_inversions = calculate_inversions(end_state)
    # Проверка, имеют ли оба состояния одинаковый остаток от деления количества инверсий на 2
    if start_inversions % 2 == end_inversions % 2:
        return True  # Решение существует
    return False  # Решение не существует


def search_start(greedy_mode: bool):
    """
    Функция запуска поиска.
    :param greedy_mode: True, если будет запущен жадный поиск, False, если А*.
    """
    debug_flag = input("\nРежим пошагового вывода (Y/N):\n> ") == 'Y'
    h_flag = input_h()

    start_state = get_initial_state()
    end_state = get_finish_state()

    if solution_exists(start_state, end_state):
        print("Решение существует!")
        search(debug_flag, h_flag=int(h_flag), greedy_flag=greedy_mode)
    else:
        print("Решения не существует.")


if __name__ == '__main__':
    repeat = 'Y'
    while repeat.lower() == 'y':
        mode = input(tabulate(
            [["1", "Запустить А*"], ["2", "Запустить жадный поиск"], ["3", "Справка"]],
            headers=["№", "Действие"],
            tablefmt="grid")
                     + '\n> ')

        match mode:
            case '1':
                search_start(False)
            case '2':
                search_start(True)
            case '3':
                print(tabulate(
                    [["A*",
                      "\tСтратегия использует очередь с приоритетом, где первенство отдается тем узлам,\n"
                      "в которых значение аддитивной оценочной стоимости минимально.\n\nОценочная стоимость "
                      "вычисляется с помощью следующей формулы:\nf(n)=h(n)+g(n),\nгде h(n) - эвристическая "
                      "функция, g(n) - стоимость пути от начальной вершины до изучаемого узла.\nОсобенностью А* "
                      "является обязательное монотонное убывание значения f(n) от корня дерева к его потомкам."],
                     ["Жадный поиск",
                      "\tСтратегия использует очередь с приоритетом, где первенство отдается тем узлам,\n"
                      "в которых значение эвристической функции h(n) минимально.\n"],
                     ["h1",
                      "\tФункция, возвращающее общее количество фишек, стоящих не на своем месте."
                      ],
                     ["h2",
                      "\tФункция, возвращающая удаленность изучаемого состояния от конечного\n"
                      "с использованием манхэттенского расстояния."
                      ]],
                    headers=["Название", "Описание"],
                    tablefmt="grid"))
            case _:
                print("Некорректный ввод")
        repeat = input("\nПерезапуск? (Y/N)\n> ")

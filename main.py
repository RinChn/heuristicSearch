from tabulate import tabulate
from search_strategies import search
from basic_operations import get_initial_state, get_finish_state


def input_h() -> str:
    h = input("\nЭвристическая функция h: (1/2)\n> ")
    while h != '1' and h != '2':
        print("Неправильный ввод, повторите попытку!\n")
        h = input("\nЭвристическая функция h: (1/2)\n> ")
    return h


def calculate_inversions(state):
    """Функция для подсчета порядка перестановки."""
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
    return inversions  # Возвращаем общее количество инверсий в состоянии игры


def solution_exists(start_state, end_state):
    """Функция для проверки наличия решения."""
    # Вычисление количества инверсий для начального и конечного состояний
    start_inversions = calculate_inversions(start_state)
    end_inversions = calculate_inversions(end_state)
    # Проверка, имеют ли оба состояния одинаковый остаток от деления количества инверсий на 2
    if start_inversions % 2 == end_inversions % 2:
        return True  # Решение существует
    else:
        return False  # Решение не существует


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
                debug_flag = input("\nРежим пошагового вывода (Y/N):\n> ") == 'Y'
                h_flag = input_h()
                
                start_state = get_initial_state()
                end_state = get_finish_state()

                if solution_exists(start_state, end_state):
                    print("Решение существует!")
                    search(debug_flag, h_flag=int(h_flag))
                else:
                    print("Решения не существует.")
                    
            case '2':
                debug_flag = input("\nРежим пошагового вывода (Y/N):\n> ") == 'Y'
                h_flag = input_h()
                
                start_state = get_initial_state()
                end_state = get_finish_state()

                if solution_exists(start_state, end_state):
                    print("Решение существует!")
                    search(debug_flag, h_flag=int(h_flag), greedy_flag = True)
                else:
                    print("Решение не существует.")
                    
            case '3':
                print(tabulate(
                    [["A*",
                      "\tСтратегия использует очередь с приоритетом, где первенство отдается тем узлам,\n"
                      "в которых значение аддитивной оценочной стоимости минимально.\n\tОценочная стоимость "
                      "вычисл1яется с помощью следующей формулы:\nf(n)=h(n)+g(n),\nгде h(n) - эвристическая "
                      "функция, g(n) - стоимость пути от начальной вершиныдо изучаемого узла."],
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

from tabulate import tabulate
from search_strategies import search

if __name__ == '__main__':
    repeat = 'Y'
    while repeat == 'Y':
        mode = input(tabulate(
                         [["1", "DFS"], ["2", "DLS"], ["3", "Справка"]],
                         headers=["№", "Стратегия"],
                         tablefmt="grid")
                     + '\n> ')

        match mode:
            case '1':
                debug_flag = input("\nРежим пошагового вывода (Y/N):\n> ") == 'Y'
                h_flag = input("\nЭвристическая функция h: (1/2/N)\n> ")
                if h_flag == 'N':
                    search(debug_flag)
                elif h_flag == '1' or h_flag == '2':
                    search(debug_flag, h_flag=int(h_flag))
                else:
                    print("Некорректный ввод")
            case '2':
                debug_flag = input("\nРежим пошагового вывода (Y/N):\n> ") == 'Y'  
                depth_limit = int(input("Введите ограничение на глубину:\n> "))
                h_flag = input("\nЭвристическая функция h: (1/2/N)\n> ")
                if h_flag == 'N':
                    search(debug_flag, depth_limit)
                elif h_flag == '1' or h_flag == '2':
                    search(debug_flag, depth_limit, h_flag=int(h_flag))

                else:
                    print("Некорректный ввод")
            case '3':
                print(tabulate(
                         [["DFS",
                           "Поиск сначала в глубину всегда раскрывает одну из вершин на самом глубоком уровне дерева.\n"
                           "Останавливается, когда поиск достигает цели или заходит в тупик.\nВ последнем случае "
                           "выполняется возврат назад и раскрываются вершины на более верхних уровнях."],
                          ["DLS",
                           "Ограниченный по глубине поиск, чтобы избежать недостатков поиска в глубину, накладывает "
                           "ограничения\nна максимальную глубину пути.\nПоиск не оптимален. Если выбрано очень "
                           "малое ограничение глубины, данная стратегия даже неполна.\nВременная и емкостная сложность "
                           "аналогична поиску в глубину. Временная сложность O(b^L), где L – ограничение глубины.\n"
                           "Емкостная сложность – O(b*L)."],
                          ["h1",
                              "С помощью этой эвристической функции осуществляется сортировка состояний\nв соответствии"
                              " с количеством фишек в них, стоящих не на своем месте: от меньшего к большему."
                          ],
                          ["h2",
                              "С помощью этой эвристической функции осуществляется сортировка состояний\nв соответствии"
                              " с общей суммой расстояний удалённости каждой фишки от её финального состояния: "
                              "от меньшего к большему."
                          ]],
                         headers=["Название стратегии", "Описание"],
                         tablefmt="grid"))
            case _:
                print("Некорректный ввод")
        repeat = input("\nПерезапуск? (Y/N)\n > ")

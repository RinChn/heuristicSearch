class Node:
    """
    Класс представления узла.
    """
    current_state: list = None  # Текущее состояние
    parent_node: "Node" = None  # Указатель на родительский узел
    previous_action: tuple = None  # Действие, применённое к родительскому узлу для получения текущего узла
    path_cost: int = 0  # Стоимость пути от начального узла к данному
    depth: int = 0  # Глубина узла
    id: int = 0  # ID узла (его индекс в общем массиве узлов)
    heuristic_function: int = 0  # Значение эвристической функции узла
    
    nodes_count = 0  # Общее количество представителей класса

    def __init__(self, state: list, parent: "Node", action: tuple, cost: int, depth: int, f: int):
        """
        Конструктор класса.
        :param state: Текущее состояние.
        :param parent: Родительский узел.
        :param action: Действие, применённое к родительскому узлу.
        :param cost: Стоимость.
        :param depth: Глубина.
        """
        self.current_state = state
        self.parent_node = parent
        self.previous_action = action
        self.path_cost = cost
        self.depth = depth
        self.id = Node.nodes_count
        self.heuristic_function = f

        Node.nodes_count += 1

    @classmethod
    def get_nodes_count(cls) -> int:
        """
        Геттер количества узлов.
        :return: количество узлов.
        """
        return cls.nodes_count + 1

import unittest
from game import Game  # Импортируем класс Game из файла game.py
from player import Player  # Импортируем класс Player из файла player.py

class TestGameLogic(unittest.TestCase):
    def test_calculate_winner(self):
        """
        Проверка логики определения победителя.
        """
        # Создаем игроков с фиксированными выборами
        player1 = Player(player_id=1, name="Игрок 1", chat_id=1)
        player2 = Player(player_id=2, name="Игрок 2", chat_id=2)

        # Случай 1: Игрок 1 побеждает
        player1.choice = "камень"
        player2.choice = "ножницы"
        result = Game.calculate_winner(player1, player2)
        self.assertEqual(result, "🎉 Победил Игрок 1!")

        # Случай 2: Игрок 2 побеждает
        player1.choice = "ножницы"
        player2.choice = "камень"
        result = Game.calculate_winner(player1, player2)
        self.assertEqual(result, "🎉 Победил Игрок 2!")

        # Случай 3: Ничья
        player1.choice = "бумага"
        player2.choice = "бумага"
        result = Game.calculate_winner(player1, player2)
        self.assertEqual(result, "Ничья!")

    def test_invalid_choices(self):
        """
        Проверка обработки некорректных выборов игроков.
        """
        # Создаем игроков
        player1 = Player(player_id=1, name="Игрок 1", chat_id=1)
        player2 = Player(player_id=2, name="Игрок 2", chat_id=2)

        # Случай 1: Выбор одного из игроков равен None
        player1.choice = "камень"
        player2.choice = None
        result = Game.calculate_winner(player1, player2)
        self.assertEqual(result, "Ошибка: Выбор одного из игроков не установлен.")

        # Случай 2: Оба выбора равны None
        player1.choice = None
        player2.choice = None
        result = Game.calculate_winner(player1, player2)
        self.assertEqual(result, "Ошибка: Выбор одного из игроков не установлен.")

    def test_all_combinations(self):
        """
        Проверка всех возможных комбинаций выборов игроков.
        """
        # Создаем игроков
        player1 = Player(player_id=1, name="Игрок 1", chat_id=1)
        player2 = Player(player_id=2, name="Игрок 2", chat_id=2)

        # Список всех допустимых выборов
        choices = ["камень", "ножницы", "бумага"]

        # Проверяем все комбинации
        for p1_choice in choices:
            for p2_choice in choices:
                player1.choice = p1_choice
                player2.choice = p2_choice

                # Определяем ожидаемый результат
                if p1_choice == p2_choice:
                    expected_result = "Ничья!"
                elif (p1_choice == "камень" and p2_choice == "ножницы") or \
                     (p1_choice == "ножницы" and p2_choice == "бумага") or \
                     (p1_choice == "бумага" and p2_choice == "камень"):
                    expected_result = "🎉 Победил Игрок 1!"
                else:
                    expected_result = "🎉 Победил Игрок 2!"

                # Проверяем результат
                result = Game.calculate_winner(player1, player2)
                self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
import unittest
from player import Player  # Импортируем класс Player из файла player.py

class TestPlayer(unittest.TestCase):
    def setUp(self):
        """
        Подготовка данных перед каждым тестом.
        Создаем экземпляр класса Player для тестирования.
        """
        self.player = Player(player_id=1, name="Игрок 1", chat_id=12345)

    def test_initialization(self):
        """
        Проверка корректности инициализации объекта Player.
        """
        self.assertEqual(self.player.player_id, 1)
        self.assertEqual(self.player.name, "Игрок 1")
        self.assertEqual(self.player.chat_id, 12345)
        self.assertIsNone(self.player.choice)  # Выбор изначально должен быть None

    def test_set_choice_valid(self):
        """
        Проверка установки допустимого выбора.
        """
        result = self.player.set_choice("камень")
        self.assertTrue(result)  # Метод set_choice должен вернуть True
        self.assertEqual(self.player.get_choice(), "камень")  # Выбор должен быть установлен

        result = self.player.set_choice("ножницы")
        self.assertTrue(result)
        self.assertEqual(self.player.get_choice(), "ножницы")

        result = self.player.set_choice("бумага")
        self.assertTrue(result)
        self.assertEqual(self.player.get_choice(), "бумага")

    def test_set_choice_invalid(self):
        """
        Проверка установки недопустимого выбора.
        """
        result = self.player.set_choice("дерево")  # Недопустимый выбор
        self.assertFalse(result)  # Метод set_choice должен вернуть False
        self.assertIsNone(self.player.get_choice())  # Выбор не должен измениться

    def test_get_choice(self):
        """
        Проверка получения текущего выбора.
        """
        self.assertIsNone(self.player.get_choice())  # Изначально выбор равен None

        self.player.set_choice("камень")
        self.assertEqual(self.player.get_choice(), "камень")  # После установки выбор должен быть корректным

        self.player.set_choice("ножницы")
        self.assertEqual(self.player.get_choice(), "ножницы")

    def test_reset_choice(self):
        """
        Проверка сброса выбора игрока.
        """
        self.player.set_choice("камень")
        self.assertEqual(self.player.get_choice(), "камень")  # Выбор установлен

        self.player.set_choice(None)  # Сбрасываем выбор
        self.assertIsNone(self.player.get_choice())  # Выбор должен стать None


if __name__ == '__main__':
    unittest.main()
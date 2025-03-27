import unittest
from pykka import ActorRegistry
from player import Player
from actor_manager import ActorManager

class TestActors(unittest.TestCase):
    def setUp(self):
        """
        Подготовка данных перед каждым тестом.
        Создаем экземпляр ActorManager и регистрируем акторов.
        """
        self.actor_manager = ActorManager()
        self.player1 = Player(player_id=1, name="Игрок 1", chat_id=12345)
        self.player2 = Player(player_id=2, name="Игрок 2", chat_id=67890)

        # Создаем акторов для игроков
        self.actor1 = self.actor_manager.create_player_actor(self.player1.player_id, self.player1.name, self.player1.chat_id)
        self.actor2 = self.actor_manager.create_player_actor(self.player2.player_id, self.player2.name, self.player2.chat_id)

    def tearDown(self):
        """
        Очистка после каждого теста.
        Удаляем всех акторов из реестра Pykka.
        """
        ActorRegistry.stop_all()

    def test_create_and_retrieve_player_actor(self):
        """
        Проверка создания и получения акторов через ActorManager.
        """
        # Получаем актора по ID игрока
        retrieved_actor1 = self.actor_manager.get_player_actor(1)
        retrieved_actor2 = self.actor_manager.get_player_actor(2)

        self.assertIsNotNone(retrieved_actor1)
        self.assertIsNotNone(retrieved_actor2)

        # Проверяем, что акторы соответствуют ожидаемым игрокам
        player_data1 = retrieved_actor1.ask({'action': 'get_player_data'})
        player_data2 = retrieved_actor2.ask({'action': 'get_player_data'})

        self.assertEqual(player_data1['player_id'], 1)
        self.assertEqual(player_data1['name'], "Игрок 1")
        self.assertEqual(player_data1['chat_id'], 12345)

        self.assertEqual(player_data2['player_id'], 2)
        self.assertEqual(player_data2['name'], "Игрок 2")
        self.assertEqual(player_data2['chat_id'], 67890)

    def test_set_and_get_choice(self):
        """
        Проверка установки и получения выбора через акторов.
        """
        # Устанавливаем выбор для первого игрока
        response1 = self.actor1.ask({'action': 'set_choice', 'choice': 'камень'})
        self.assertTrue(response1['status'])  # Установка должна быть успешной

        # Проверяем, что выбор установлен корректно
        choice1 = self.actor1.ask({'action': 'get_choice'})['choice']
        self.assertEqual(choice1, 'камень')

        # Устанавливаем выбор для второго игрока
        response2 = self.actor2.ask({'action': 'set_choice', 'choice': 'ножницы'})
        self.assertTrue(response2['status'])

        # Проверяем, что выбор установлен корректно
        choice2 = self.actor2.ask({'action': 'get_choice'})['choice']
        self.assertEqual(choice2, 'ножницы')

    def test_invalid_choice_handling(self):
        """
        Проверка обработки недопустимых выборов через акторов.
        """
        # Пытаемся установить недопустимый выбор
        response = self.actor1.ask({'action': 'set_choice', 'choice': 'дерево'})
        self.assertFalse(response['status'])  # Установка должна быть неудачной

        # Проверяем, что выбор не изменился (остался None)
        choice = self.actor1.ask({'action': 'get_choice'})['choice']
        self.assertIsNone(choice)

    def test_remove_player_actor(self):
        """
        Проверка удаления акторов через ActorManager.
        """
        # Удаляем актора первого игрока
        self.actor_manager.remove_player_actor(1)

        # Пытаемся получить актора по ID
        retrieved_actor = self.actor_manager.get_player_actor(1)
        self.assertIsNone(retrieved_actor)  # Актор должен быть удален

        # Второй актор должен остаться
        retrieved_actor2 = self.actor_manager.get_player_actor(2)
        self.assertIsNotNone(retrieved_actor2)


if __name__ == '__main__':
    unittest.main()
import telebot

from game import Game
from player import Player


class BotManager:
    def __init__(self, api_token, actor_manager):
        self.bot = telebot.TeleBot(api_token)
        self.actor_manager = actor_manager
        self.game_queue = []

        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            user_name = message.from_user.first_name
            self.bot.reply_to(message, f"👋 Привет, {user_name}! 🎮\n"
                                       "Добро пожаловать в игру 'Камень, ножницы, бумага'!\n"
                                       "Чтобы присоединиться к игре, используйте команду /join.")

        @self.bot.message_handler(commands=['join'])
        def join_game(message):
            player_id = message.from_user.id
            chat_id = message.chat.id
            player_name = message.from_user.first_name

            if self.actor_manager.get_player_actor(player_id):
                self.bot.reply_to(message, "Вы уже зарегистрированы!")
                return

            # Создаем актор для игрока
            self.actor_manager.create_player_actor(player_id, player_name, chat_id)
            self.game_queue.append(player_id)

            self.bot.reply_to(message, f"{player_name}, вы успешно присоединились к игре! Ожидайте второго игрока...")

            print(f"Текущая очередь: {self.game_queue}")  # Отладочное сообщение

            # Если в очереди есть два игрока, начинаем игру
            if len(self.game_queue) >= 2:
                self.start_game()

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            player_id = message.from_user.id
            text = message.text.lower()

            player_actor = self.actor_manager.get_player_actor(player_id)
            if not player_actor:
                self.bot.reply_to(message, "Вы не зарегистрированы в игре. Используйте команду /join.")
                return

            # Устанавливаем выбор игрока
            response = player_actor.ask({'action': 'set_choice', 'choice': text})
            if not response['status']:
                self.bot.reply_to(message, "❌ Некорректный ввод! Пожалуйста, выберите: камень, ножницы или бумага.")
                return

            self.bot.reply_to(message, f"✅ Вы выбрали: {text}. Ждите выбора соперника...")

            # Проверяем, сделали ли оба игрока выбор
            opponent_id = self.find_opponent(player_id)
            if opponent_id:
                print(f"Игрок {player_id} нашел соперника {opponent_id}. Запускаем определение победителя.")
                self.determine_winner(player_id, opponent_id)
            else:
                print(f"Игрок {player_id} не нашел соперника. Ожидание...")

    def find_opponent(self, player_id):
        print(f"Поиск соперника для игрока {player_id}. Очередь: {self.game_queue}")
        for other_player_id in self.game_queue:
            if other_player_id != player_id:
                opponent_actor = self.actor_manager.get_player_actor(other_player_id)
                opponent_choice = opponent_actor.ask({'action': 'get_choice'})['choice']
                print(f"Проверка соперника {other_player_id}: choice={opponent_choice}")
                if opponent_choice:
                    print(f"Найден соперник: {other_player_id}")
                    return other_player_id
        print("Соперник еще не готов.")
        return None


    def start_game(self):
        if len(self.game_queue) < 2:
            print("Недостаточно игроков для начала игры.")
            return

        player1_id = self.game_queue[0]
        player2_id = self.game_queue[1]

        print(f"Игра началась между игроками {player1_id} и {player2_id}")

        player1_actor = self.actor_manager.get_player_actor(player1_id)
        player2_actor = self.actor_manager.get_player_actor(player2_id)

        self.bot.send_message(player1_actor.ask({'action': 'get_player_data'})['chat_id'],
                              "Игра началась! Выберите: камень, ножницы или бумага.")
        self.bot.send_message(player2_actor.ask({'action': 'get_player_data'})['chat_id'],
                              "Игра началась! Выберите: камень, ножницы или бумага.")

    def determine_winner(self, player1_id, player2_id):
        player1_actor = self.actor_manager.get_player_actor(player1_id)
        player2_actor = self.actor_manager.get_player_actor(player2_id)

        player1_data = player1_actor.ask({'action': 'get_player_data'})
        player2_data = player2_actor.ask({'action': 'get_player_data'})

        print(f"Данные игрока 1: {player1_data}")
        print(f"Данные игрока 2: {player2_data}")

        result = Game.calculate_winner(
            Player(player1_data['player_id'], player1_data['name'], player1_data['chat_id'], player1_data['choice']),
            Player(player2_data['player_id'], player2_data['name'], player2_data['chat_id'], player2_data['choice'])
        )

        self.bot.send_message(player1_data['chat_id'], result)
        self.bot.send_message(player2_data['chat_id'], result)

        # Удаляем игроков из очереди
        self.game_queue.remove(player1_id)
        self.game_queue.remove(player2_id)
        print(f"Игроки {player1_id} и {player2_id} удалены из очереди.")

        # Удаляем игроков из игры
        self.actor_manager.remove_player_actor(player1_id)
        self.actor_manager.remove_player_actor(player2_id)
        print(f"Игроки {player1_id} и {player2_id} удалены из игры.")

    def start_bot(self):
        self.bot.polling()
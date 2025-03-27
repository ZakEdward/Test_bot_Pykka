class Player:
    def __init__(self, player_id, name, chat_id, choice=None):
        self.player_id = player_id
        self.name = name
        self.chat_id = chat_id
        self.choice = choice  # Выбор игрока

    def set_choice(self, choice):
        if choice is None:
            # Сброс выбора
            self.choice = None
            return True
        elif choice in ['камень', 'ножницы', 'бумага']:
            # Установка допустимого выбора
            self.choice = choice
            return True
        else:
            # Недопустимый выбор
            return False

    def get_choice(self):
        return self.choice
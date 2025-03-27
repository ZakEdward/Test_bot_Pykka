class Game:
    ALLOWED_CHOICES = ['камень', 'ножницы', 'бумага']

    @staticmethod
    def calculate_winner(player1, player2):
        p1_choice = player1.get_choice()
        p2_choice = player2.get_choice()

        print(f"Сравнение выборов: Игрок 1 ({p1_choice}) vs Игрок 2 ({p2_choice})")

        if not p1_choice or not p2_choice:
            return "Ошибка: Выбор одного из игроков не установлен."

        if p1_choice == p2_choice:
            return "Ничья!"
        elif (p1_choice == 'камень' and p2_choice == 'ножницы') or \
             (p1_choice == 'ножницы' and p2_choice == 'бумага') or \
             (p1_choice == 'бумага' and p2_choice == 'камень'):
            return f"🎉 Победил {player1.name}!"
        else:
            return f"🎉 Победил {player2.name}!"
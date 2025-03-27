import pykka

from player import Player


class PlayerActor(pykka.ThreadingActor):
    def __init__(self, player):
        super().__init__()
        self.player = player

    def on_receive(self, message):
        if message['action'] == 'set_choice':
            success = self.player.set_choice(message['choice'])
            print(f"Игрок {self.player.player_id} установил выбор: {message['choice']}, статус: {success}")
            return {'status': success}
        elif message['action'] == 'get_choice':
            choice = self.player.get_choice()
            print(f"Игрок {self.player.player_id} вернул выбор: {choice}")
            return {'choice': choice}
        elif message['action'] == 'get_player_data':
            data = {
                'player_id': self.player.player_id,
                'name': self.player.name,
                'chat_id': self.player.chat_id,
                'choice': self.player.get_choice()
            }
            print(f"Игрок {self.player.player_id} вернул данные: {data}")
            return data

class ActorManager:
    def __init__(self):
        self.players = {}

    def create_player_actor(self, player_id, name, chat_id):
        player = Player(player_id, name, chat_id)
        actor = PlayerActor.start(player)
        self.players[player_id] = actor
        return actor

    def get_player_actor(self, player_id):
        return self.players.get(player_id)

    def remove_player_actor(self, player_id):
        if player_id in self.players:
            self.players[player_id].stop()
            del self.players[player_id]
from actor_manager import ActorManager
from bot_manager import BotManager

if __name__ == '__main__':
    API_TOKEN = 'YOUR_BOT_API_TOKEN'
    actor_manager = ActorManager()
    bot_manager = BotManager(API_TOKEN, actor_manager)
    bot_manager.start_bot()
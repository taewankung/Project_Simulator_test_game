#import bge
import json

class GameLogic:
    def __init__(self, game_client):
        self.status = 'wait'
        self.players = None
        self.player = None
        self.game_space = None

        self.game_space = None
        self.game_client = game_client

    def start_game(self):
        self.status = 'play'


    def initial_game(self, players, player, game_space):
        if players is None:
            return
        self.game_space = game_space
        self.players = players
        self.player = player
        self.game_client.game.ready()

    def synchronize(self, args):
        object_id = args.get('object_id', None)
        if object_id is None:
            return

        msg = json.dumps(args)
   #     bge.logic.sendMessage('remote', msg, object_id)


    def move_hero(self, x, y, player_id):
        hero_stat = self.game_space['heros'][player_id]
        hero_stat['target'] = dict(x=x,y=y)

        move_msg = json.dumps(dict(method='move_hero', x=x, y=y, player_id=player_id))
  #      bge.logic.sendMessage('remote', move_msg, hero_stat['name'].lower())


    def skill_action(self, skill, player_id):
        hero_stat = self.game_space['heros'][player_id]
        skill_msg = json.dumps(dict(method='skill_action', skill=skill, player_id=player_id))
 #       bge.logic.sendMessage('remote', skill_msg, hero_stat['name'].lower())
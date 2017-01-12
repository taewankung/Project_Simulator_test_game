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

        self.rev_message = ""

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

    def update_game(self,game_space):
        self.game_space = game_space

    def complete_command(self,msg):
        self.rev_message = msg
        print(str(self.player['username'])+':'+msg+' '+'complete')

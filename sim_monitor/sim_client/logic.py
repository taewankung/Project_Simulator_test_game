#import bge
import json
import logging
from sim_monitor.model.status import status
import os
import datetime

class GameLogic:
    def __init__(self, game_client):
        self.status = 'wait'
        self.players = None
        self.player = None
        self.game_space = None
        self.ex_file =None
        self.has_change_msg= False

        self.old_message=''
        self.counter_order = 0
        self.game_space = None
        self.game_client = game_client
        self.history_file = None
        self.rev_message =''
        self.tower_message =''
        self.alliance_message =''
        self.action_msg_history=[]
        self.alliance_msg_history=[]
        self.time_created_file = None
        self.end_message =''
        #  self.history_file = open(file_path+'../logging/'+self.player['username']+'_history.log','w')
#        self.logger = logging.basicConfig(filename=file_path+'../logging/'+self.player['username']+'history.log')
        #logging.basicConfig(filename=)

    def start_game(self):
        self.status = 'play'

    def initial_game(self, players, player, game_space):
        if players is None:
            return
        self.game_space = game_space
        self.players = players
        self.player = player
        self.game_client.game.ready()

    def create_file(self):
        now_compleated = datetime.datetime.now()
        if self.time_created_file == None:
            time_created_file = str(now_compleated)
            time_created_file = time_created_file.split(' ')
            self.time_created_file = time_created_file
        if self.history_file == None:
            file_path = os.path.dirname(__file__)
            self.history_file = open(file_path+'/../logging/{0}_{1}_{2}_{3}_history.log'\
                                                .format(self.player['username'],\
                                                str(self.ex_file),str(self.time_created_file[0]),\
                                                str(self.time_created_file[1])),'w')

            self.history_file.write('user name: {0}\nfile name: {1}\n'.format(self.player['username'],str(self.ex_file)))

    def synchronize(self, args):
        object_id = args.get('object_id', None)
        if object_id is None:
            return

        msg = json.dumps(args)
   #     bge.logic.sendMessage('remote', msg, object_id)

    def update_game(self,game_space):
        self.game_space = game_space

    def end_game(self,msg):
        self.status = 'end_game'
        self.end_message = msg
        status.connect =False
        print('msg:'+str(msg))
        if self.player["id"] in self.game_space["hero_" + str(self.player["team"])]:
            hero_status = self.game_space["hero_" + str(self.player["team"])][self.player["id"]]
            if  hero_status['death'] != 0:
                kda = (hero_status['kill'] + hero_status['assist']) / hero_status['death']*100
            else:
                kda = 100
                if hero_status['death'] ==0:
                    kda =0
            lasthit = hero_status['lasthit']
            level=0
            lasthit_level=''
            if kda >= 80:
                level = 'A'
            elif kda >= 75:
                level = 'B+'
            elif kda >= 70:
                level = 'B'
            elif kda > 65:
                level = 'C+'
            elif kda > 60:
                level = 'C'
            elif kda > 55:
                level = 'D+'
            elif kda > 50:
                level = 'D'
            else:
                level = 'E'
            if lasthit > 200:
                lasthit_level ='Execelent'
            elif lasthit > 100:
                lasthit_level ='Good'
            else:
                lasthit_level ='Bad'

            self.history_file.write('\nResult of Code:\n'.format(self.player['username'],kda))
            self.history_file.write('{0} kda: {1}\n'.format(self.player['username'],kda))
            self.history_file.write('level of kda:{0}\n'.format(level))
            self.history_file.write('\n{0} Lasthit: {1}\n'.format(self.player['username'],lasthit))
            self.history_file.write('level of Lasthit:{0}\n'.format(lasthit_level))

    def complete_command(self,msg):
        if self.old_message !=msg:
            self.old_message = msg
            print(self.counter_order)
            self.counter_order = 0
            self.has_change_msg = True
        else:
            self.has_change_msg = False
        self.rev_message = msg
        now_compleated = datetime.datetime.now()
        self.history_file.write(str(now_compleated)+str(' '+self.player['username'])+':'+msg+'\n')
        if msg not in self.action_msg_history:
            self.action_msg_history.append(msg)
        print(str(self.player['username'])+':'+msg)

    def rev_tower_message(self,msg):
        self.tower_message = msg
        now_compleated = datetime.datetime.now()
        self.history_file.write(str(now_compleated)+str(' '+self.player['username'])+':'+msg+'\n')
        print(str(self.player['username'])+':'+msg)

    def rev_alliance_message(self,msg):
        self.alliance_message = msg
        now_compleated = datetime.datetime.now()
        self.history_file.write(str(now_compleated)+str(' '+self.player['username'])+':'+msg+'\n')
        if msg not in self.alliance_msg_history:
            self.alliance_msg_history.append(msg)
        print('alliance: {0} {1}'.format(self.player['username'],msg))

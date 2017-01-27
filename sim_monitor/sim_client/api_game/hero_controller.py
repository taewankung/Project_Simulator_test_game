from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.model.status import status
from nagaclient import client
import time
'''
warning:
    if you want to use loop for ever you must be use timer.sleep(0.001)
    because loop forever can your disply program not optimize if not delay.
'''

class HeroController:
    '''
    The HeroController class is controlling the actor in serveral events.
    '''
    def __init__(self):
        self.ac = ApaimaneeMOBAClient()
        self.player = self.ac.game_logic.player
        self.connection_status = status.connect
#        print(self.ac.game_logic.game_space)
        if self.player["id"] in self.ac.game_logic.game_space["hero_"+str(self.player["team"])]:
            self.status = self.ac.game_logic.game_space["hero_"+str(self.player["team"])][self.player["id"]]
        self.rev_message = self.ac.game_logic.rev_message

    def update_status(self):
        '''
        This method use to update status from server for HeroController.
        '''
        if self.player["id"] in self.ac.game_logic.game_space["hero_"+str(self.player["team"])]:
            self.status = self.ac.game_logic.game_space["hero_"+str(self.player["team"])][self.player["id"]]
        self.connection_status = status.connect

    def update_message(self):
        '''
        This method use to update message from server for handle event when your hero found some event.
        '''
        self.rev_message = self.ac.game_logic.rev_message

    def buy_item(self,item,msg=''):
        self.ac.game_client.game.buy_item(item,msg)
        time.sleep(0.001)

    def use_item(self,item,msg=''):
        self.ac.game_client.game.use_item(item,msg)
        time.sleep(0.001)

    def attack(self, Enemy,msg=""):
        '''
        The attack method is controlling the actor to attack Enemy.

        type of parameter:
            Enemy is string
            msg is string
        '''
        self.ac.game_client.game.attack(Enemy,msg)
        time.sleep(0.001)

    def upgrade_skill(self,skill_num,msg="upgrade_skill"):
        '''
        The upgrade_skill is method which used to upgrade skill of hero.

        Note: If u don't upgrade skill,the hero will can't use skill because his skill has level 0.
        type of parameter:
            skill_num is integer
            msg is string
        '''
        if self.status["skill_point"] >0:
            self.ac.game_client.game.upgrade_skill(skill_num,msg)
        time.sleep(0.001)


    def use_skill(self,skill_num,target=None,msg="use_skill"):
        '''
        The use_skill method is controlling the actor use skill which actor
        have to target.
        type of parameter:
            skill_num is integer
            msg is string
        '''
        skill = self.status['skills']
        skill_level = self.status['skill_level'][skill_num]
        if skill_num in range(0,3) and self.status["skill_cooldown"][skill_num] <= 0\
                                   and skill[skill_num]['skill_type']!='buff_passive'\
                                   and self.status['current_mana'] >= skill[skill_num]['used_mana'][skill_level]:
            self.ac.game_client.game.use_skill(skill_num,target,msg)
        time.sleep(0.01)
#            print('used skill:{}'.format(self.status['skills'][skill_num]['name']))

    def move(self,pos_x,pos_y,msg="move"):
        '''
        The movement method move the actor.
        argument in function have 3 argument: pos_x,pos_y

        type of parameter:
            pos_x is integer or float for position x,
            pos_y is integer or float for position y,
            msg is string for message which want to server send when this function finish done.

        recommend:
            Server will send message "found enemy" when unit found enemy for you want to handle that event.
        '''
        #print("{0},{1}".format(self.status["pos_x"],self.status["pos_y"]))
        self.status = self.ac.game_logic.game_space["hero_"+str(self.player["team"])][self.player["id"]]
        self.ac.game_client.game.move_hero(x=pos_x, y=pos_y,msg=msg)

    def aliance_message(self,msg,args=dict()):
        '''
        The aliance_message is method for send message to hero in your team.
        argument in function have 1 argument: msg

        type of parameter:
            msg is string,

        recommend:
            Server will send message "found enemy" when unit found enemy for you want to handle that event.
        '''
        self.ac.game_client.game.aliance_message(msg,args)
        time.sleep(0.001)

    def get_position(self):
        self.update_status()
        return (self.status['pos_x'],self.status['pos_y'])

    def get_current_hp(self):
        '''
        This method return current_hp attibute  in Hero class.
        '''
        return self.status["current_hp"]

    def get_hp_percent(self):
        return (self.status["current_hp"]/self.status["max_hp"]*100)

    def get_max_mp(self):
        '''
        This method return mp attibute in Hero class.
        '''
        return self.status["max_mana"]

    def get_current_mp(self):
        '''
        This method return mp attibute in Hero class.
        '''
        return self.status["current_mana"]

    def get_max_mp(self):
        '''
        This method return mp attibute in Hero class.
        '''
        return self.status["max_mana"]

    def get_mp_percent(self):
        return (self.status["current_mana"]/self.status["max_mana"]*100)

    def get_item_in_hero(self):
        '''
            The get_item_in_hero method return the list of item in the actor who want
        to know.
        '''
        return self.status["item"]

    def get_near_enemy(self):
        return self.status['near_enemy_list']

    #  def get_enemy_hp(self,enemy):
        #  '''
                #  The get_enemy_hp method return hp in enemy in enemy_list attibute
            #  of Hero class.
            #  if enemy is not in enemy_list will return 0.
        #  '''
        #  pass

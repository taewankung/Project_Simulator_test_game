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
        self.item_price_dict=dict(ArmorBoot=450,
                                  AssasinGrove=1000,
                                  BladeBoot=500,
                                  Boot=500,
                                  Emeral=400,
                                  Grove=500,
                                  Knife=450,
                                  ManaPotion=100,
                                  Potion=100,
                                  Ruby=400,
                                  Sapphire=400,
                                  Shild=250,
                                  SoulBox=500,
                                  Sword=450)
        self.local_dict = dict(t1_base_left=(130,220),
                               t1_base_right=(170,190),
                               t1_tower_bot_level1=(820,150),
                               t1_tower_bot_level2=(470,130),
                               t1_tower_bot_level3=(260,140),
                               t1_tower_mid_level1=(400,420),
                               t1_tower_mid_level2=(295,330),
                               t1_tower_mid_level3=(220,260),
                               t1_tower_top_level1=(110,610),
                               t1_tower_top_level2=(110,445),
                               t1_tower_top_level3=(95,308),
                               t2_base_left=(850,780),
                               t2_base_right=(800,810),
                               t2_tower_bot_level1=(880,380),
                               t2_tower_bot_level2=(880,520),
                               t2_tower_bot_level3=(880,690),
                               t2_tower_mid_level1=(555,530),
                               t2_tower_mid_level2=(668,650),
                               t2_tower_mid_level3=(755,735),
                               t2_tower_top_level1=(210,885),
                               t2_tower_top_level2=(490,874),
                               t2_tower_top_level3=(720,850),
                              )
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
        '''
        This method use to buy item in the game.
        item in the game:
            ArmorBoot
            AssasinGrove
            BladeBoot
            Boot
            Emeral
            Grove
            Knife
            ManaPotion
            Potion
            Ruby
            Sapphire
            Shild
            SoulBox
            Sword

        Args:
            item(str): name of item
            msg(str): msg want to return if finish funtion
        '''

        str_item = ''
        item = item.split(' ')
        for i in item:
            str_item+=i
        item = str_item
        if item in self.item_price_dict and self.status['gold'] > self.item_price_dict[item]:
            self.ac.game_client.game.buy_item(item,msg)
        time.sleep(0.0001)

    def use_item(self,item,msg=''):
        '''
        The use_item method is controlling the hero to use item which in hero'

        Args:
            item(str): name of item
            msg(str): msg want to return if finish funtion
        '''
        item_name_list = [i['name'] for i in self.get_item_in_hero()]
        if item in  item_name_list:
            self.ac.game_client.game.use_item(item,msg)
            time.sleep(0.0001)

    def attack(self, Enemy,msg=""):
        '''
        The attack method is controlling the actor to attack Enemy.

        Args:
            Enemy(str): name of Enemy
            msg(str): msg want to return if finish funtion
        '''
        self.ac.game_client.game.attack(Enemy,msg)
        time.sleep(0.001)

    def upgrade_skill(self,skill_num,msg="upgrade_skill"):
        '''
        The upgrade_skill is method which used to upgrade skill of hero.
        Note: If u don't upgrade skill,the hero will can't use skill because his skill has level 0.

        Args:
            skill_num(int): skill number
            msg(str): msg want to return if finish funtion
        '''
        if self.status["skill_point"] >0:
            self.ac.game_client.game.upgrade_skill(skill_num,msg)
        time.sleep(0.001)


    def use_skill(self,skill_num,target=None,msg="use_skill"):
        '''
        The use_skill method is controlling the actor use skill which actor
        have to target.

        Args:
            skill_num (int): skill number
            target (str): use skill to  target
            msg (str): msg want to return if finish funtion
        '''
        skill = self.status['skills']
        skill_level = self.status['skill_level'][skill_num]
        if skill_num in range(0,3) and self.status["skill_cooldown"][skill_num] <= 0\
                                   and skill[skill_num]['skill_type']!='buff_passive'\
                                   and self.status['current_mana'] >= skill[skill_num]['used_mana'][skill_level]:
            self.ac.game_client.game.use_skill(skill_num,target,msg)
        time.sleep(0.001)
#            print('used skill:{}'.format(self.status['skills'][skill_num]['name']))

    def move(self,pos_x,pos_y,msg="move"):
        '''
        The movement method move the actor.
        argument in function have 3 argument: pos_x,pos_y

        Args:
            pos_x(int): integer or float for position x,
            pos_y(int): integer or float for position y,
            msg(str):   string for message which want to server send when this function finish done.

        recommend:
            Server will send message "found enemy" when unit found enemy for you want to handle that event.
        '''
        #print("{0},{1}".format(self.status["pos_x"],self.status["pos_y"]))
        self.status = self.ac.game_logic.game_space["hero_"+str(self.player["team"])][self.player["id"]]
        self.ac.game_client.game.move_hero(x=pos_x, y=pos_y,msg=msg)

    def move_to_local(self,target,msg=""):
        msg = 'move to {0}'.format(target)
        self.ac.game_client.game.move_hero(x=self.local_dict[target][0],y=self.local_dict[target][1])

    def move_follow(self,target,msg='follow'):
        self.ac.game_client.game.move_hero(x=target.pos_x,y=pos_y,msg=msg)

    def alliance_message(self,msg_to_team,msg_end_send='send message'):
        '''
        The alliance_message is method for send message to hero in your team.
        argument in function have 1 argument: msg

        Args:
            msg(str):   string for message which want to server send when this function finish done.

        recommend:
            Server will send message "found enemy" when unit found enemy for you want to handle that event.
        '''
        self.ac.game_client.game.alliance_message(msg_to_team,msg_end_send)
        time.sleep(0.001)

    def get_position(self):
        '''
        This method will return position of hero be Tuple (X,Y).

        Returns:
            position(tuple)
        '''
        self.update_status()
        return (self.status['pos_x'],self.status['pos_y'])

    def get_current_hp(self):
        '''
        This method return current_hp attibute  in Hero class.
        '''
        return self.status["current_hp"]

    def get_hp_percent(self):
        '''
        This method return the hp of your hero is percent.
        recomend:
            This percent use Float style (1% =0.01).
        event example to use:
            you want to your hero use item or change action if hp lower than 10%.
            you can use this method to check.
        '''
        return (self.status["current_hp"]/self.status["max_hp"])

    def get_max_mp(self):
        '''
        This method return mp or mana attibute in Hero class.

        '''
        return self.status["max_mana"]

    def get_current_mp(self):
        '''
        This method return current mp or mana attibute in Hero class.
        '''
        return self.status["current_mana"]

    def get_max_mp(self):
        '''
        This method return max mp or mana attibute in Hero class.
        '''
        return self.status["max_mana"]

    def get_mp_percent(self):
        '''
        This method return the hp of hero is percent.
        recomend:
            This percent use Float style (1% =0.01).
        event example to use:
            you want to your hero use item or change action if mana or mp lower than 10%.
            you can use this method to check.
        '''
        return (self.status["current_mana"]/self.status["max_mana"])

    def get_item_in_hero(self):
        '''
            The get_item_in_hero method return list of item in your hero.
        '''
        return self.status["item"]

    def get_near_enemy(self):
        '''
            This method will return lsit of enemys who are near your hero.
        '''
        return self.status['near_enemy_list']

    def get_gold(self):
        '''
            This method will return gold of hero.
        '''
        return self.status['gold']

    def alive(self):
        '''
        '''
        return self.status['alive']

    def get_level(self):
        return self.status['level']

    def get_current_exp(self):
        return self.status['current_exp']

    def get_max_exp(self):
        return self.status['max_exp']

    def get_skill_cooldown(self):
        return self.status['skill_cooldown']

    def get_kill(self):
        return self.status['kill']

    def get_death(self):
        return self.status['death']

    def get_team_list(self):
        return self.status['near_team_list']

    def count_near_enemy(self):
        return len(self.status['near_enemy_list'])

    def get_skill_point(self):
        return self.status['skill_point']

    def get_armor(self):
        return self.status['armor']

    def get_damage(self):
        return self.status['damage']

    def get_name(self):
        return self.status['name']
    #  def get_enemy_hp(self,enemy):
        #  '''
                #  The get_enemy_hp method return hp in enemy in enemy_list attibute
            #  of Hero class.
            #  if enemy is not in enemy_list will return 0.
        #  '''
        #  pass

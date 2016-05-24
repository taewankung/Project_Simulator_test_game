#import bge
import time
import datetime

import logging
import logging.config
import sys
import argparse
from .client_map import ApaimaneeMOBAClient

def initial_game():
    # print("arg:", sys.argv)
    parser = argparse.ArgumentParser(prog='ApaimaneeMOBA',
                                     description='Apaimanee MOBA Game')
    parser.add_argument('blend', nargs='?',
                        help='')
    parser.add_argument('--client_id', nargs='?', const='test_client_id',
                        default='test_client_id',
                        help='ApaimaneeMOBA client_id')
    parser.add_argument('--room_id', nargs='?', const='test_room_id',
                        default='test_room_id',
                        help='ApamneeMOBA room_id')
    parser.add_argument('--token', nargs='?', const='test_token',
                        default='test_token',
                        help='ApamneeMOBA token')
    parser.add_argument('--host', nargs='?', const='localhost',
                        default='localhost',
                        help='ApamneeMOBA API host')
    parser.add_argument('--port', nargs='?', const=1883,
                        default=1883,
                        help='ApamneeMOBA API port')
    parser.add_argument('--log', nargs='?', const='logging.conf',
                        default='logging.conf',
                        help='ApamneeMOBA API logging')



    args = parser.parse_args()

    logging.config.fileConfig(args.log)
    logger = logging.getLogger('apmn')

    logger.info('Apaimanee Game start')
    logger.info('Try to connect to host {} port {} client_id {} room_id {}'.format(args.host, args.port, args.client_id, args.room_id))


    ac = ApaimaneeMOBAClient(args.client_id,
                             args.host, int(args.port),
                             args.room_id)

    gc = ac.game_client
    gc.user.loggedin_info = dict(token=args.token)
    gc.room.current_room = dict(room_id=args.room_id)

    ac.connect()

    gc.game.initial()
    global send_initial
    send_initial = True
    logger.info('Apaimanee Game initial ready')


send_initial = False

def loading_scene():

    owner = {}
    if 'start_time' in owner:
        ac = ApaimaneeMOBAClient()
        if ac.game_logic.status == 'play':

            logger = logging.getLogger('apmn')
            logger.info('Play game')

            cont.activate(scene_act)

        diff_time = datetime.datetime.now() - start_time
        print('wait for play singnal', diff_time.seconds)
        if diff_time.seconds % 20 == 0:
            global send_initial
            if not send_initial:
                ac.game_client.game.initial()
                send_initial = True
        else:
           send_initial = False

        if diff_time > datetime.timedelta(minutes=2):
            print('time out')
            ac.disconnect()


    else:
        try:
            initial_game()

        except Exception as e:
            logger = logging.getLogger('apmn')
            print('Initial Fail:', e)
            logger.exception(e)
        owner['start_time'] = datetime.datetime.now()

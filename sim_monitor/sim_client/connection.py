#import bge
import time
import datetime
import os
import logging
import logging.config
import sys
import argparse
from .client_map import ApaimaneeMOBAClient

def initial_game():
    # print("arg:", sys.argv)
    parser = argparse.ArgumentParser(prog='Sim_map',
                                     description='Simulation of Moba game')
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
    parser.add_argument('--load', nargs='?', const='sim_monitor.sim_client.test',
                        default=str(os.getcwd())+'/sim_monitor/sim_client/test.py',
                        help='load file')


    args = parser.parse_args()

    logging.config.fileConfig(args.log)
    logger = logging.getLogger('Naga')

    logger.info('Apaimanee Game start')
    logger.info('Try to connect to host {} port {} client_id {} room_id {}'.format(args.host, args.port, args.client_id, args.room_id))


    ac = ApaimaneeMOBAClient(args.client_id,
                             args.host, int(args.port),
                             args.room_id)
    gc = ac.game_client
    gc.user.loggedin_info = dict(token=args.token)
    gc.room.current_room = dict(room_id=args.room_id)
    #  print(gc.user.loggedin_info)
    print(ac._client_id)
    ac.connect()
    gc.game.initial()
    global send_initial
    send_initial = True
    logger.info('Apaimanee Game initial ready')
    return args.load
send_initial = False

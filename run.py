#!/usr/bin/python

import logging
from api import Api

logger = logging.getLogger('urlCache')

def Args():
    pass
args = Args()

import argparse
parser = argparse.ArgumentParser(description='get info from ogame api',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--server', '-s', type=str, help='server like uni117.ogame.de')
parser.add_argument('--player', '-p', type=str, help='playername')
parser.add_argument('--alliance', '-a', type=str, help='alliance tag')
parser.add_argument('--quick', '-q', type=int, help='shortened output')
parser.add_argument('--find', '-f', type=int, help='lists $count matches (just the names)')
args = parser.parse_args()

api = Api(args.server, "var", quick=args.quick)

if args.find:
    find = args.find
    if find > 50:
        find = 50
    if find < 1:
        find = 1
    if args.player:
        api.findPlayer(args.player, find)
    elif args.alliance:
        api.findAlliance(args.alliance, find)
elif args.player:
    api.getPlayerString(args.player)
elif args.alliance:
    api.getAllianceString(args.alliance)
else:
    print "too few arguments"

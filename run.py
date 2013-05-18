#!/usr/bin/python

import argparse
import requests
from cache import FileCache
from helper import textextract
from datetime import datetime, timedelta
import logging
from lxml import etree
import sys

logger = logging.getLogger('urlCache')

parser = argparse.ArgumentParser(description='get info from ogame api',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--server', '-s', type=str, help='server like uni117.ogame.de')
parser.add_argument('--player', '-p', type=str, help='playername')
parser.add_argument('--alliance', '-a', type=str, help='alliance tag')
parser.add_argument('--quick', '-q', type=int, help='quick')
args = parser.parse_args()

cache = FileCache("var")

ogniter_mapping = {
        'uni117.ogame.de': 136
        }

def doApiRequest(server, type, append=""):
    type_to_update_intervall = {
            'playerData': timedelta(days=7),
            'alliances': timedelta(days=1),
            'players': timedelta(days=1),
            }
    api_data = cache.lookup(server+"_"+type+append.encode("base64"))
    need_download = False
    if not api_data:
        logger.info("Need download because %s is not cached")
        need_download = True
    else:
        timestamp = int(textextract(api_data, 'timestamp="', '"'))
        timestamp = datetime.fromtimestamp(timestamp)
        if timestamp + type_to_update_intervall[type] < datetime.now():
            logger.info("Need download because %s is more than 12h old" % (server+"_"+type))
            need_download = True
    if need_download:
        r = requests.get('http://'+server+'/api/'+type+'.xml'+append)
        cache.write(server+"_"+type+append.encode("base64"), r.text)
        api_data = r.text
    return api_data

def getLxmlRoot(data):
    # lxml seems to have a problem with unicode-strings so do this strange conversion
    data = bytes(bytearray(data, encoding="utf-8"))
    return etree.fromstring(data)


def getPlayerInfo(id=False, name=False):
    if not id:
        root = getLxmlRoot(doApiRequest(args.server, "players"))
        el = root.xpath(".//player[re:test(@name, '^"+name+"$', 'i')]",
                namespaces={"re": "http://exslt.org/regular-expressions"})
        if len(el) == 0:
            return (False, "No match")
        id = el[0].get("id")
    playerData = doApiRequest(args.server, "playerData", "?id="+str(id))
    if playerData == "Player not found.":
        return (False, "Player not found.")
    root = getLxmlRoot(playerData)

    player_info = {}

    dataEl = root.xpath("/playerData")[0]
    player_info["name"] = dataEl.get("name")
    player_info["id"] = dataEl.get("id")
    player_info["serverId"] = dataEl.get("serverId")
    player_info["timestamp"] = dataEl.get("timestamp")
    position = {}
    for posEl in root.xpath(".//position"):
        position[int(posEl.get("type"))] = {
                "position":int(posEl.text),
                "score":int(posEl.get("score")),
                }
        if posEl.get("ships"):
            position[int(posEl.get("type"))]["ships"] = posEl.get("ships")
    player_info["position"] = position

    planets = []
    for planEl in root.xpath(".//planet"):
        planets.append((planEl.get("coords"), planEl.get("name")))
    player_info["planets"] = planets

    ally = root.xpath(".//alliance")
    if len(ally) == 0:
        player_info["ally"] = False
    else:
        ally = ally[0]
        tag = ally.xpath(".//tag")[0].text
        name = ally.xpath(".//name")[0].text
        player_info["ally"] = {
                "tag": tag,
                "name": name,
                }
    return (True, player_info)

if args.player:
    (ret, player_info) = getPlayerInfo(name=args.player)
    if not ret:
        print player_info
        sys.exit(1)

    type_to_name = ["Total", "Economy", "Research", "Military", "Military Built", "Military Destroyed", "Military Lost", "Honor"]
    if args.quick:
        type = 0
        position = player_info["position"][type]
        print "%s: %04d - %d  " % (type_to_name[type], position["position"], position["score"]),
        if args.server in ogniter_mapping:
            print "http://www.ogniter.org/de/%d/player/%d" % (ogniter_mapping[args.server], int(player_info["id"]))
        else:
            print ""
    else:
        for type in player_info["position"]:
            position = player_info["position"][type]
            print "%s: %04d - %d" % (type_to_name[type].ljust(18), position["position"], position["score"])


    if args.quick:
        i = 0
        for planet in player_info["planets"]:
            i += 1
            print "%s %s  " % (planet[0].ljust(8), planet[1]),
            if i%2 == 0:
                print ""
        if i > 1 and i%2 != 0:
            print ""
    else:
        for planet in player_info["planets"]:
            print "%s %s" % (planet[0].ljust(8), planet[1])

    if not player_info["ally"]:
        print "No ally"
    else:
        print "%s - %s" % (player_info["ally"]["tag"], player_info["ally"]["name"])

elif args.alliance:
    root = getLxmlRoot(doApiRequest(args.server, "alliances"))
    el = root.xpath(".//alliance[re:test(@tag, '^"+args.alliance+"$', 'i')]",
            namespaces={"re": "http://exslt.org/regular-expressions"})
    if len(el) == 0:
        print "No match"
        sys.exit(1)
    el = el[0]
    for i in ["name", "homepage", "logo", "open"]:
        if el.get(i):
            print "%s: %s   " % (i, el.get(i)),
            if not args.quick:
                print ""
    if args.server in ogniter_mapping:
        print "http://www.ogniter.org/de/%d/alliance/%d" % (ogniter_mapping[args.server], int(el.get("id"))),
        if not args.quick:
            print ""
    if args.quick:
        print "players: %d" % (len(el.xpath(".//player")))
    players = []
    for playerEl in el.xpath(".//player"):
        (ret, player_info) = getPlayerInfo(id=playerEl.get("id"))
        if ret:
            players.append((player_info["name"], player_info["position"][0]["position"], player_info))
    players = sorted(players, key=lambda x: x[1])
    i = 0
    if args.quick:
        for player in players:
            i+=1
            print "%s %s %d %s   " % (str(i), player[0], player[1], player[2]["planets"][0][0]),
            if i%2==0:
                print ""
            if i == 4:
                break
    else:
        for player in players:
            i+=1
            print "%s %s %d %s" % (str(i).ljust(2), player[0], player[1], player[2]["planets"][0][0])


else:
    print "too few arguments"

#!/usr/bin/python

import requests
from cache import FileCache
from helper import textextract
from datetime import datetime, timedelta
import logging
from lxml import etree
import Levenshtein

logger = logging.getLogger('urlCache')





class Api(object):
    ogniter_mapping = {
            'uni117.ogame.de': 136
            }

    def __init__(self, server, cache_dir, quick=False):
        self.server = server
        self.cache = FileCache(cache_dir)
        self.quick = quick

    def _doApiRequest(self, type, append=""):
        type_to_update_intervall = {
                'playerData': timedelta(days=7),
                'alliances': timedelta(days=1),
                'players': timedelta(days=1),
                'highscore': timedelta(hours=1),
                }
        api_data = self.cache.lookup(self.server+"_"+type+append.encode("base64"))
        need_download = False
        if not api_data:
            logger.info("Need download because %s is not cached")
            need_download = True
        else:
            timestamp = int(textextract(api_data, 'timestamp="', '"'))
            timestamp = datetime.fromtimestamp(timestamp)
            if timestamp + type_to_update_intervall[type] < datetime.now():
                logger.info("Need download because %s is more than 12h old" % (self.server+"_"+type))
                need_download = True
        if need_download:
            r = requests.get('http://'+self.server+'/api/'+type+'.xml'+append)
            self.cache.write(self.server+"_"+type+append.encode("base64"), r.text)
            api_data = r.text
        return api_data

    def _getLxmlRoot(self, data):
        # lxml seems to have a problem with unicode-strings so do this strange conversion
        data = bytes(bytearray(data, encoding="utf-8"))
        return etree.fromstring(data)

    def _findMatch(self, elements, attr, name):
        name = name.lower()
        all_names = []
        for el in elements:
            all_names.append((el, Levenshtein.ratio(el.get(attr).decode("utf-8").lower(), name)))
        return sorted(all_names, key=lambda x: x[1], reverse = True)

    def getPlayerInfo(self, id=False, name=False, find=False):
        sim = 1.0
        if not id:
            root = self._getLxmlRoot(self._doApiRequest("players"))
            el, sim = self._findMatch(root.xpath(".//player"), "name", name)[0]
            if sim == 0.0:
                return (False, "No match")
            id = el.get("id")
        playerData = self._doApiRequest("playerData", "?id="+str(id))
        if playerData == "Player not found.":
            return (False, "Player not found.")
        root = self._getLxmlRoot(playerData)

        player_info = {}

        dataEl = root.xpath("/playerData")[0]
        player_info["name"] = dataEl.get("name")
        player_info["sim"] = sim
        player_info["id"] = dataEl.get("id")
        player_info["serverId"] = dataEl.get("serverId")
        player_info["timestamp"] = dataEl.get("timestamp")
        position = {}
        # position info is outdated - highscore.xml gets updated every hour - so better use this
        #for posEl in root.xpath(".//position"):
        #    position[int(posEl.get("type"))] = {
        #            "position":int(posEl.text),
        #            "score":int(posEl.get("score")),
        #            }
        #    if posEl.get("ships"):
        #        position[int(posEl.get("type"))]["ships"] = posEl.get("ships")
        #player_info["position"] = position
        for posType in (0, 1, 2, 3, 4, 5, 6, 7):
            highscoreRoot = self._getLxmlRoot(self._doApiRequest("highscore", "?category=1&type="+str(posType)))
            posEl = highscoreRoot.xpath(".//player[@id=%s]" % id)[0]
            position[posType] = {
                    "position":int(posEl.get("position")),
                    "score":int(posEl.get("score")),
                    }
            if posEl.get("ships"):
                position[posType]["ships"] = posEl.get("ships")
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
        # to get the playerstatus we have to retrieve the players.xml :/
        playersRoot = self._getLxmlRoot(self._doApiRequest("players"))
        playerEl = playersRoot.xpath(".//player[@id=%s]" % id)[0]
        player_info["status"] = playerEl.get("status")
        if not player_info["status"]:
            player_info["status"] = ""
        return (True, player_info)


    def findPlayer(self, name, find):
        retStr = []
        root = self._getLxmlRoot(self._doApiRequest("players"))
        matches = self._findMatch(root.xpath(".//player"), "name", name.strip())
        for i in range(0, find):
            el, sim = matches[i]
            retStr.append("%s - %.2f" % (el.get("name"), sim))
            if not self.quick or i%2 == 1:
                retStr.append("\n")
        return retStr

    def findAlliance(self, tag, find):
        retStr = []
        root = self._getLxmlRoot(self._doApiRequest("alliances"))
        matches = self._findMatch(root.xpath(".//alliance"), "tag", tag.strip())
        for i in range(0, find):
            el, sim = matches[i]
            retStr.append("%s - %.2f" % (el.get("tag"), sim))
            if not self.quick or i%2 == 1:
                retStr.append("\n")
        return retStr

    def getPlayerString(self, name):
        retStr = []
        (ret, player_info) = self.getPlayerInfo(name=name.strip())
        if not ret:
            retStr.append(player_info)
            return retStr
        if player_info["sim"] != 1.0:
            retStr.append("%s - similarity:%.2f\n" % (player_info["name"], player_info["sim"]))

        type_to_name = ["Total", "Economy", "Research", "Military", "Military Built", "Military Destroyed", "Military Lost", "Honor"]
        if self.quick:
            type = 0
            position = player_info["position"][type]
            if player_info["status"]:
                retStr.append("%s, " % player_info["status"])
            retStr.append("%s: %04d - %d  " % (type_to_name[type], position["position"], position["score"]))
            if self.server in self.ogniter_mapping:
                retStr.append("http://www.ogniter.org/de/%d/player/%d\n" % (self.ogniter_mapping[self.server], int(player_info["id"])))
            else:
                retStr.append("\n")
        else:
            if player_info["status"]:
                retStr.append("Status: %s\n" % player_info["status"])
            for type in player_info["position"]:
                position = player_info["position"][type]
                retStr.append("%s: %04d - %d\n" % (type_to_name[type].ljust(18), position["position"], position["score"]))
        if self.quick:
            i = 0
            for planet in player_info["planets"]:
                i += 1
                retStr.append("%s %s  " % (planet[0].ljust(8), planet[1]))
                if i%2 == 0:
                    retStr.append("\n")
            if i > 1 and i%2 != 0:
                retStr.append("\n")
        else:
            for planet in player_info["planets"]:
                retStr.append("%s %s\n" % (planet[0].ljust(8), planet[1]))
        if not player_info["ally"]:
            retStr.append("No ally\n")
        else:
            retStr.append("%s - %s\n" % (player_info["ally"]["tag"], player_info["ally"]["name"]))
        return retStr

    def getAllianceString(self, tag):
        retStr = []
        root = self._getLxmlRoot(self._doApiRequest("alliances"))
        el, sim = self._findMatch(root.xpath(".//alliance"), "tag", tag.strip())[0]
        if sim == 0.0:
            retStr.append("No match\n")
            return retStr
        if sim != 1.0:
            retStr.append("%s - similarity:%.2f\n" % (el.get("tag"), sim))
        for i in ["name", "homepage", "logo", "open"]:
            if el.get(i):
                retStr.append("%s: %s   " % (i, el.get(i)))
                if not self.quick:
                    retStr.append("\n")
        if self.server in self.ogniter_mapping:
            retStr.append("http://www.ogniter.org/de/%d/alliance/%d" % (self.ogniter_mapping[self.server], int(el.get("id"))))
            if not self.quick:
                retStr.append("\n")
        if self.quick:
            retStr.append("players: %d\n" % (len(el.xpath(".//player"))))
        players = []
        for playerEl in el.xpath(".//player"):
            (ret, player_info) = self.getPlayerInfo(id=playerEl.get("id"))
            if ret:
                players.append((player_info["name"], player_info["position"][0]["position"], player_info))
        players = sorted(players, key=lambda x: x[1])
        i = 0
        if self.quick:
            for player in players:
                i+=1
                retStr.append("%s %s %d %s   " % (str(i), player[0], player[1], player[2]["planets"][0][0]))
                if i%2==0:
                    retStr.append("\n")
                if i == 4:
                    break
        else:
            for player in players:
                i+=1
                retStr.append("%s %s %d %s\n" % (str(i).ljust(2), player[0], player[1], player[2]["planets"][0][0]))
        return retStr

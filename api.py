#!/usr/bin/python

import requests
from cache import FileCache
from helper import textextract
from datetime import datetime, timedelta
import logging
import os
try:
    from lxml import etree
except:
    import xml.etree.ElementTree as etree
    # cElementTree doesn't support xpath player[@id='123']
    #import cElementTree as etree
import Levenshtein
import time
from prettytable import PrettyTable



logger = logging.getLogger('urlCache')





class Api(object):
    ogniter_mapping = {
            'uni117.ogame.de': 136
            }
    highscore_type_to_name = ["Total", "Economy", "Research", "Military", "Military Lost", "Military Built", "Military Destr.", "Honor"]

    def __init__(self, server, cache_dir, quick=False):
        self.server = server
        self.cache = FileCache(cache_dir)
        self.quick = quick
        self.lxmlCache = {}
        # use session to reuse the connection
        self.requests = requests.Session()

    def _doApiRequest(self, type, append=""):
        type_to_update_intervall = {
                'playerData': timedelta(days=7),
                'alliances': timedelta(days=1),
                'players': timedelta(days=1),
                'highscore': timedelta(hours=1),
                }
        api_data = self.cache.lookup(self.server+"_"+type+append)
        need_download = False
        if not api_data:
            logger.info("Need download because %s is not cached")
            need_download = True
        else:
            try:
                # exception when response is "player not found"
                timestamp = int(textextract(api_data, 'timestamp="', '"'))
            except:
                timestamp = os.path.getmtime(self.cache.get_path(self.server+"_"+type+append))
            timestamp = datetime.fromtimestamp(timestamp)
            if timestamp + type_to_update_intervall[type] < datetime.now():
                logger.info("Need download because %s is more than 12h old" % (self.server+"_"+type))
                need_download = True
        if need_download:
            r = self.requests.get('http://'+self.server+'/api/'+type+'.xml'+append)
            self.cache.write(self.server+"_"+type+append, r.text)
            api_data = r.text
        return (need_download, type, append), api_data

    # call this if you want to cache many requests - works only for playerData
    # append must be an array
    def _doApiRequestAsync(self, type, appendList=[]):
        # also the newest grequests doesn't work with gevent >= 1.x - but don't know how to check this here
        try:
            import grequests
        except:
            return
        type_to_update_intervall = {
                'playerData': timedelta(days=7),
                }
        urlList = []
        for append in appendList:
            api_data = self.cache.lookup(self.server+"_"+type+append)
            need_download = False
            if not api_data:
                logger.info("Need download because %s is not cached")
                need_download = True
            else:
                try:
                    # exception when response is "player not found"
                    timestamp = int(textextract(api_data, 'timestamp="', '"'))
                except:
                    timestamp = int(time.time())
                timestamp = datetime.fromtimestamp(timestamp)
                if timestamp + type_to_update_intervall[type] < datetime.now():
                    logger.info("Need download because %s is more than 12h old" % (self.server+"_"+type))
                    need_download = True
            if need_download:
                urlList.append('http://'+self.server+'/api/'+type+'.xml'+append)

        if len(urlList):
            rs = (grequests.get(u, session=self.requests, timeout=3) for u in urlList)
            responses = grequests.map(rs)
            for r in responses:
                if r:
                    append = textextract(r.url, type+".xml", "")
                    self.cache.write(self.server+"_"+type+append, r.text)

    def _getLxmlRoot(self, apiRequestData):
        need_download = apiRequestData[0][0]
        type = apiRequestData[0][1]
        append = apiRequestData[0][2]
        data = apiRequestData[1]
        if type == "highscore" or type == "players" or type == "alliances":
            if not need_download:
                try:
                    return self.lxmlCache[type+append]
                except:
                    pass
            else:
                data = bytes(bytearray(data, encoding="utf-8"))
                self.lxmlCache[type+append] = etree.fromstring(data)
                return self.lxmlCache[type+append]

        # lxml seems to have a problem with unicode-strings so do this strange conversion
        data = bytes(bytearray(data, encoding="utf-8"))
        return etree.fromstring(data)

    def _findMatch(self, elements, attr, name):
        name = name.lower()
        all_names = []
        for el in elements:
            all_names.append((el, Levenshtein.ratio(el.get(attr).decode("utf-8").lower(), name)))
        return sorted(all_names, key=lambda x: x[1], reverse = True)

    def getPlayerInfo(self, id=False, name=False, addPositionInfo=True, addStatusInfo=True):
        sim = 1.0
        if not id:
            root = self._getLxmlRoot(self._doApiRequest("players"))
            el, sim = self._findMatch(root.findall(".//player"), "name", name)[0]
            if sim == 0.0:
                return (False, "No match")
            id = int(el.get("id"))
        data, playerData = self._doApiRequest("playerData", "?id=%d"%id)
        if playerData == "Player not found.":
            return (False, "Player not found.")
        root = self._getLxmlRoot((data, playerData))

        player_info = {}

        dataEl = root
        player_info["name"] = dataEl.get("name")
        player_info["sim"] = sim
        player_info["id"] = int(dataEl.get("id"))
        player_info["serverId"] = dataEl.get("serverId")
        player_info["timestamp"] = dataEl.get("timestamp")
        if addPositionInfo:
            position = {}
            # position info is outdated - highscore.xml gets updated every hour - so better use this
            #for posEl in root.findall(".//position"):
            #    if posEl.text is None:
            #        return (False, "This player has no highscore - either he is gamemaster, or banned")
            #    posType = int(posEl.get("type"))
            #    position[posType] = {
            #            "position":int(posEl.text),
            #            "score":int(posEl.get("score")),
            #            }
            #    if posType == 3:
            #        if posEl.get("ships"):
            #            position[posType]["ships"] = int(posEl.get("ships"))
            #        else:
            #            position[posType]["ships"] = 0
            for posType in (0, 1, 2, 3, 4, 5, 6, 7):
                highscoreRoot = self._getLxmlRoot(self._doApiRequest("highscore", "?category=1&type="+str(posType)))
                posEl = highscoreRoot.find(".//player[@id='%d']" % id)
                if posEl is None:
                    return (False, "This player has no highscore - either he is gamemaster, or banned")
                position[posType] = {
                        "position":int(posEl.get("position")),
                        "score":int(posEl.get("score")),
                        }
                if posType == 3:
                    if posEl.get("ships"):
                        position[posType]["ships"] = int(posEl.get("ships"))
                    else:
                        position[posType]["ships"] = 0
            player_info["position"] = position

        planets = []
        for planEl in root.findall(".//planet"):
            moonName = ""
            moonSize = 0
            moon = planEl.find(".//moon")
            if moon is not None:
                moonName = moon.get("name")
                moonSize = int(moon.get("size"))
            planets.append((planEl.get("coords"), planEl.get("name"), planEl.get("id"), moonName, moonSize))
        player_info["planets"] = planets

        ally = root.findall(".//alliance")
        if len(ally) == 0:
            player_info["ally"] = False
            player_info["allianceId"] = 0
        else:
            ally = ally[0]
            tag = ally.find(".//tag").text
            name = ally.find(".//name").text
            player_info["ally"] = {
                    "id": int(ally.get("id")),
                    "tag": tag,
                    "name": name,
                    }
            player_info["allianceId"] = int(ally.get("id"))
        # to get the playerstatus we have to retrieve the players.xml :/
        if addStatusInfo:
            playersRoot = self._getLxmlRoot(self._doApiRequest("players"))
            playerEl = playersRoot.find("player[@id='%d']" % id)
            player_info["status"] = playerEl.get("status")
            if not player_info["status"]:
                player_info["status"] = ""
        return (True, player_info)

    def getAllianceInfo(self, id=False, tag=False):
        sim = 1.0
        if not id:
            root = self._getLxmlRoot(self._doApiRequest("alliances"))
            el, sim = self._findMatch(root.findall(".//alliance"), "tag", tag)[0]
            if sim == 0.0:
                return (False, "No match")
            id = int(el.get("id"))
        else:
            root = self._getLxmlRoot(self._doApiRequest("alliances"))
            el = root.find(".//alliance[@id='%d']" % id)
        alliance_info = {
            "name": el.get("name"),
            "tag": el.get("tag"),
            "sim": sim,
            "id": int(el.get("id")),
            "homepage": el.get("homepage"),
            "logo": el.get("logo"),
            "open": bool(el.get("open")),
            "serverId": root.get("serverId"),
            "timestamp": root.get("timestamp"),
            }

        players = []
        for playerEl in el.findall(".//player"):
            players.append(int(playerEl.get("id")))
        alliance_info["players"] = players
        return (True, alliance_info)

    def listPlayers(self):
        root = self._getLxmlRoot(self._doApiRequest("players"))
        allEls = root.findall(".//player")
        ret = []
        for el in allEls:
            status = el.get("status")
            if status is None:
                status = ""
            ret.append({
                "id":int(el.get("id")),
                "status":status,
                })
        return (int(root.get("timestamp")), ret)

    def listHighscore(self, posType):
        root = self._getLxmlRoot(self._doApiRequest("highscore", "?category=1&type="+str(posType)))
        allPlayer = root.findall(".//player")
        ret = {}
        for posEl in allPlayer:
            position = {
                    "position":int(posEl.get("position")),
                    "score":int(posEl.get("score")),
                    }
            if posType == 3:
                if posEl.get("ships"):
                    position["ships"] = int(posEl.get("ships"))
                else:
                    position["ships"] = 0
            ret[int(posEl.get("id"))] = position
        return (int(root.get("timestamp")), ret)

    def listAlliances(self):
        root = self._getLxmlRoot(self._doApiRequest("alliances"))
        allEls = root.findall(".//alliance")
        ret = []
        for el in allEls:
            ret.append({
                "name": el.get("name"),
                "tag": el.get("tag"),
                "id": int(el.get("id")),
                "homepage": el.get("homepage"),
                "logo": el.get("logo"),
                "open": bool(el.get("open")),
                })
        return (int(root.get("timestamp")), ret)

    def findPlayer(self, name, find, justMatch=False):
        retStr = []
        root = self._getLxmlRoot(self._doApiRequest("players"))
        matches = self._findMatch(root.findall(".//player"), "name", name.strip())
        for i in range(0, find):
            el, sim = matches[i]
            if justMatch:
                return int(el.get("id")), el.get("name"), sim
            retStr.append("%s - %.2f" % (el.get("name"), sim))
            if not self.quick or i%2 == 1:
                retStr.append("\n")
            else:
                retStr.append(" ")
        return retStr

    def findAlliance(self, tag, find):
        retStr = []
        root = self._getLxmlRoot(self._doApiRequest("alliances"))
        matches = self._findMatch(root.findall(".//alliance"), "tag", tag.strip())
        for i in range(0, find):
            el, sim = matches[i]
            retStr.append("%s - %.2f" % (el.get("tag"), sim))
            if not self.quick or i%2 == 1:
                retStr.append("\n")
            else:
                retStr.append(" ")
        return retStr

    def getPlayerString(self, name):
        retStr = []
        (ret, player_info) = self.getPlayerInfo(name=name.strip())
        if not ret:
            retStr.append(player_info)
            return retStr
        if player_info["sim"] != 1.0:
            retStr.append("%s - similarity:%.2f\n" % (player_info["name"], player_info["sim"]))

        position = player_info["position"][0]
        if player_info["status"]:
            retStr.append("%s, " % player_info["status"])
        retStr.append("%04d/%d " % (position["position"], position["score"]))
        if self.server in self.ogniter_mapping:
            retStr.append("http://www.ogniter.org/de/%d/player/%d" % (self.ogniter_mapping[self.server], int(player_info["id"])))
        retStr.append("\n")
        if not self.quick:
            if player_info["status"]:
                retStr.append("Status: %s\n" % player_info["status"])
            t = PrettyTable(["Type", "Position", "Score", "Type2", "Position2", "Score2"])
            t.align["Type"] = "l"
            t.align["Position"] = "r"
            t.align["Score"] = "r"
            t.align["Type2"] = "l"
            t.align["Position2"] = "r"
            t.align["Score2"] = "r"
            for type in range(0,len(self.highscore_type_to_name),2):
                t.add_row([self.highscore_type_to_name[type], player_info["position"][type]["position"], player_info["position"][type]["score"],
                    self.highscore_type_to_name[type+1], player_info["position"][type+1]["position"], player_info["position"][type+1]["score"]])
            t.add_row(["ships", "", player_info["position"][3]["ships"],
                # defense is (economy+research+military)-total
                       "defense", "",
                       (player_info["position"][1]["score"]+player_info["position"][2]["score"]+player_info["position"][3]["score"]) -
                       player_info["position"][0]["score"]])
            t.set_style(11)
            t_str = t.get_string(border=False,header=False, padding_width=1).split("\n")
            new_t_str = []
            for line in t_str:
                new_t_str.append(line[1:])
            retStr.append("\n".join(new_t_str)+"\n")

        t = PrettyTable(["Coord", "M", "Name"])
        t.align["Coord"] = "l"
        t.align["Moon"] = "l"
        t.align["Name"] = "l"
        for planet in player_info["planets"]:
            moonInfo = ""
            if planet[4]:
                moonInfo = "M%d" % planet[4]
            t.add_row([planet[0], moonInfo, planet[1]])
        t.set_style(11)
        t_str = t.get_string(border=False, header=False, padding_width=1)
        # make the table horizontal wider
        tableRows = t_str.split("\n")
        if len(tableRows) > 1:
            # take lower half and append it to the upper half
            half = len(tableRows)/2
            for i in range(0, half):
                tableRows[i] += tableRows[i+1]
                del(tableRows[i+1])
            t_str = "\n".join(tableRows)
        t_str = t_str.split("\n")
        new_t_str = []
        for line in t_str:
            new_t_str.append(line[1:])
        retStr.append("\n".join(new_t_str)+"\n")


        if not player_info["ally"]:
            retStr.append("No ally")
        else:
            retStr.append("%s - %s" % (player_info["ally"]["tag"], player_info["ally"]["name"]))
        return retStr

    def getAllianceString(self, tag):
        retStr = []
        (ret, alliance_info) = self.getAllianceInfo(tag=tag.strip())
        if not ret:
            retStr.append(alliance_info)
            return retStr
        if alliance_info["sim"] != 1.0:
            retStr.append("%s - similarity:%.2f\n" % (alliance_info["tag"], alliance_info["sim"]))
        for i in ["name", "homepage", "logo", "open"]:
            if alliance_info[i]:
                retStr.append("%s: %s   " % (i, alliance_info[i]))
                if not self.quick:
                    retStr.append("\n")
        if self.server in self.ogniter_mapping:
            retStr.append("http://www.ogniter.org/de/%d/alliance/%d " % (self.ogniter_mapping[self.server], alliance_info["id"]))
            if not self.quick:
                retStr.append("\n")
        if self.quick:
            retStr.append("players: %d\n" % (len(alliance_info["players"])))
        players = []
        for playerId in alliance_info["players"]:
            (ret, player_info) = self.getPlayerInfo(id=playerId)
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

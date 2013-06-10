# coding=utf-8
import re
import api
# TODO get server from commandline
server = "uni117.ogame.de"
api = api.Api(server, "var", quick=True)

def handle_command(connection, e, command):
    target = e.target
    if e.type == "privmsg" or command.startswith("!help"):
        target = e.source.nick

    try:
        if command[0] != '!':
            return
        command = command[1:]
        print command
        retStr = realy_handle_command(command, connection=connection, target=target)
    except Exception, ex:
        target = e.target
        if e.type == "privmsg":
            target = e.source.nick
        try:
            #connection.privmsg(e.source.nick, u"Du hast einen Fehler verursacht: %s" % str(ex))
            connection.privmsg(target, u"Fehler, probier nochmal (Versuch 1/3)")
        except:
            pass
        print "error ", ex

    for line in retStr:
        connection.privmsg(target, line)

def realy_handle_command(command, connection=False, target=False):
    retStr = []
    s = re.search("^(?P<search>(a|f)?)(?P<type>(player)|(alliance)) (?P<name>.+)$", command)
    if s:
        if s.group("search") == "a":
            api.quick = False
        else:
            api.quick = True

        name = s.group("name").decode("utf-8")
        if s.group("type") == "player":
            if s.group("search") == "f":
                data = api.findPlayer(name, 6)
            else:
                data = api.getPlayerString(name)
        if s.group("type") == "alliance":
            if s.group("search") == "f":
                data = api.findAlliance(name, 6)
            else:
                data = api.getAllianceString(name)
        retStr = "".join(data).split("\n")

    elif command == "help":
        retStr.append(u"!player name - infos zu einem spieler")
        retStr.append(u"!alliance tag - infos zu einer allianz")
        retStr.append(u"!aplayer bzw. aalliance - gibt erweiterte infos")
        retStr.append(u"!fplayer bzw. falliance - gibt 6 spieler/allianz nach Ähnlichkeit zurück")
        retStr.append(u"!which met kris deut [plasma] [temp] [kurs] - gibt Vorschlag welche Mine am besten zu bauen ist - help which für mehr")
        retStr.append(u"!awhich same as which, but a bit more detailed")
        retStr.append(u"!diff playername [hours] - highscore diff")
        retStr.append(u"!inactive yourpos [radius] [duration] [minscore] [maxscore] - finds inactive")

    elif command == "help which":
        retStr.append(u"Beispielaufruf: !which 18 15 12 für met=18,kris=15 und deut=12 - plasmatech=0 und maximale temperatur=50 da nicht angegeben, kurs=2:1:1")
        retStr.append(u"Beispielaufruf: !which 18 15 12 3 45 3:2:1 nun ist plasma=3, temp=45 und der kurs 3:2:1")

    elif command.startswith("which ") or command.startswith("awhich"):
        args = command.split(" ")
        plasma = 0
        temp = 50
        mse = [2.0, 1.0, 1.0]
        buildings = {}
        if len(args) > 2:
            buildings[1] = int(args[1])
            buildings[2] = int(args[2])
        if len(args) > 3:
            buildings[3] = int(args[3])
        if len(args) > 4:
            plasma = int(args[4])
        if len(args) > 5:
            temp = int(args[5])
        if len(args) > 6:
            mse = []
            for i in args[6].split(":"):
                mse.append(float(i))
        import Constants
        if command.startswith("which "):
            bId = Constants.buildingTopList(buildings, {122:plasma}, temp, mse)[0]["bId"]
            retStr.append("Am besten baust du: %s" % Constants.buildLabels[bId])
        else:
            t = Constants.buildingTopList(buildings, {122:plasma}, temp, mse)
            i = 0
            for build in t:
                i+=1
                bId = build["bId"]
                atime = build["atime"]
                import datetime
                atime = str(datetime.timedelta(seconds=atime))
                retStr.append("%d: %s %s" % (i, Constants.buildLabels[bId], atime))

    elif command == "dbupdate":
        import db
        if connection:
            connection.privmsg(target, "updating db - this takes some time..")
        db.update(server)
        retStr.append("updated")

    elif command.startswith("dbquery"):
        import db
        try:
            res = db.query(command[8:])
        except Exception, ex:
            connection.privmsg(target, ex)
            if len(command[8:]) == 445:
                retStr.append("Your query can't be longer than 445 chars")
                retStr.append(command[8:])
            return
        retStr = res[:9]

    elif command.startswith("inactive") or command.startswith("ainactive"):
        args = command[9:].split(" ")
        import db
        amount = 6
        if command.startswith("ainactive"):
            args = command[10:].split(" ")
            amount = 12
        radius = 15
        duration = 60*60*24
        minScore = 5000
        maxScore = 9999999
        if len(args) < 1 or args[0].find(":") == -1:
            retStr.append("usage !inactive yourpos [radius] [duration] [minscore] [maxscore]")
            retStr.append("example !inactive 3:338 15 2 5000 20000 - sucht alle planeten zwischen 3:323 und 3:353 wo spieler 2Tage inaktive und zw. 5k und 20k punkte hat")
        else:
            if len(args) > 0:
                 position = args[0]
            if len(args) > 1:
                radius = int(args[1])
            if len(args) > 2:
                 duration = int(args[2]) * 60*60*24
            if len(args) > 3:
                minScore = int(args[3])
            if len(args) > 4:
                maxScore = int(args[4])
            retStr = "".join(db.listInactivityPlayer(position, radius, duration, minScore, maxScore, amount)).split("\n")
    elif command.startswith("diff"):
        args = command[9:].split(" ")
        import db
        hours = 12
        if len(args) < 1:
            retStr.append("usage !diff playername [hours]")
        else:
            if len(args) > 0:
                 player = args[0].decode("utf-8")
            if len(args) > 1:
                hours = int(args[1])
            retStr = db.highscoreChange(server, player, hours).split("\n")
    return retStr


if __name__ == "__main__":
    def Args():
        pass
    args = Args()

    import argparse
    parser = argparse.ArgumentParser(description='get info from ogame api db',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--command', '-c', type=str, help='command to execute')
    args = parser.parse_args()

    print "\n".join(realy_handle_command(args.command))

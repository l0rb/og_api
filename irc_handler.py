# coding=utf-8
import re
import api
reload(api)
api = api.Api("uni117.ogame.de", "var", quick=True)

def handle_command(connection, e, command):
    #    try:
    #        do_logging(connection, e, command)
    #    except:
    #        pass
    try:
        realy_handle_command(connection, e, command)
    except Exception, ex:
        target = e.target
        if e.type == "privmsg":
            target = e.source.nick
        try:
            connection.privmsg(target, u"Du hast einen Fehler verursacht: %s" % str(ex))
        except:
            pass
        print "error ", ex

def realy_handle_command(connection, e, command):
    #nick = e.source.nick
    #channel = e.target
    #e.type == pubmsg
    target = e.target
    if e.type == "privmsg":
        target = e.source.nick
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
        for line in "".join(data).split("\n"):
            connection.privmsg(target, line)
    elif command == "bot help":
        connection.privmsg(target, u"player name - infos zu einem spieler")
        connection.privmsg(target, u"alliance tag - infos zu einer allianz")
        connection.privmsg(target, u"aplayer bzw. aalliance - gibt erweiterte infos")
        connection.privmsg(target, u"fplayer bzw. falliance - gibt 6 spieler/allianz nach Ähnlichkeit zurück")
        connection.privmsg(target, u"which met kris deut [plasma] [temp] [kurs] - gibt Vorschlag welche Mine am besten zu bauen ist - help which für mehr")
    elif command == "help which":
        connection.privmsg(target, u"Beispielaufruf: which 18 15 12 für met=18,kris=15 und deut=12 - plasmatech=0 und maximale temperatur=50 da nicht angegeben, kurs=2:1:1")
        connection.privmsg(target, u"Beispielaufruf: which 18 15 12 3 45 3:2:1 nun ist plasma=3, temp=45 und der kurs 3:2:1")

    elif command.startswith("which "):
        args = command.split(" ")
        plasma = 0
        temp = 50
        mse = [2.0, 1.0, 1.0]
        if len(args) > 3:
            met = int(args[1])
            kris = int(args[2])
            deut = int(args[3])
        if len(args) > 4:
            plasma = int(args[4])
        if len(args) > 5:
            temp = int(args[5])
        if len(args) > 6:
            mse = []
            for i in args[6].split(":"):
                mse.append(float(i))
            print mse
        import Constants
        reload(Constants)
        bId = Constants.which(met, kris, deut, plasma, temp, mse)
        msg = "Am besten baust du: %s" % Constants.buildLabels[bId]
        connection.privmsg(target, msg)


# coding=utf-8
#import logging
#from datetime import datetime
#
##logging init
#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
#
#formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(name)s %(message)s')
#formatter_short = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s',
#        "%M:%S")
## filehandler
#
#name = "log"+datetime.now().strftime("%Y_%m_%d")
#hdlr = logging.FileHandler(name)
#
#hdlr.setFormatter(formatter)
#hdlr.setLevel(logging.CRITICAL)
#logger.addHandler(hdlr)
#
#def do_logging(connection, e, command):
#    if e.type == "pubmsg":
#        logger.critical(command)

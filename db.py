#!/usr/bin/python
import sqlite3
from api import Api
import datetime





def update(server, consoleOut=True):
    conn = sqlite3.connect('ogapi.sqlite')
    cur = conn.cursor()

    api = Api(server, "var")

    # alliance
    timestamp, allAlliances = api.listAlliances()
    cur.execute("DELETE FROM alliance")
    all = len(allAlliances)
    count = 0
    insertData = []
    print "updating alliance"
    for ally in allAlliances:
        count += 1
        print "%d/%d\r" % (count, all),
        insertData.append(
                (ally["id"], ally["tag"], ally["name"], ally["logo"], ally["homepage"], ally["open"]))

    cur.executemany("""INSERT INTO "alliance" ("id", "tag", "name", "logo", "homepage", "open") VALUES (?, ?, ?, ?, ?, ?)""",
            insertData)
    print ""


    # player + planets
    timestamp, allPlayers = api.listPlayers()

    # this is here to download all playerdata resources in parallel
    # I know I should perhaps make this a background task but this felt as easiest
    appendList = []
    count = 0
    all = len(allPlayers)
    print "updating player - async download"
    for playerData in allPlayers:
        id = playerData["id"]
        appendList.append("?id=%d"%id)
        if len(appendList) == 40:
            count += 40
            print "%d/%d\r"%(count,all),
            api._doApiRequestAsync("playerData", appendList)
            appendList = []
    print ""

    cur.execute("DELETE FROM player")
    cur.execute("DELETE FROM planet")
    count = 0
    insertData = []
    insertPlanetData = []
    print "updating player"
    playerStatus = {}
    for playerData in allPlayers:
        playerId = playerData["id"]
        count += 1
        res, player = api.getPlayerInfo(playerId, addPositionInfo=False, addStatusInfo=False)
        if not res:
            print "Some error occured with player %d %s" % (playerId, player)
            continue
        print "%d/%d\r" % (count, all),
        playerStatus[playerId] = playerData["status"]

        player["status"] = playerData["status"]
        insertData.append((player["id"], player["name"], player["allianceId"], player["status"]))
        for planet in player["planets"]:
            coord, pName, pId = planet
            coord = coord.split(":")
            insertPlanetData.append((player["id"], pId, pName, int(coord[0]), int(coord[1]), int(coord[2])))
    print ""

    cur.executemany("""INSERT INTO `player` (`id`, `name`, `allianceId`, `status`) VALUES (?, ?, ?, ?)""", insertData)
    cur.executemany("""INSERT INTO `planet` (`playerId`, `id`, `name`, `galaxy`, `system`, `position`) VALUES (?, ?, ?, ?, ?, ?)""",
            insertPlanetData)


    # highscore
    updateData = []
    allHighscore = {}
    for posType in range(0,8):
        timestamp, tmpHighscore = api.listHighscore(posType)
        allHighscore[posType] = tmpHighscore
    all = len(allHighscore[0])
    count = 0
    updateData = []
    print "updating highscore"
    cur.execute("DELETE FROM score_history WHERE `timestamp`=%d"% timestamp)
    for playerId in allHighscore[0]:
        count += 1
        print "%d/%d\r" % (count, all),
        try:
            status = playerStatus[playerId]
        except:
            status = "-"
        try:
            updateData.append((
                    allHighscore[3][playerId]["ships"],
                    status,
                    allHighscore[0][playerId]["position"],
                    allHighscore[1][playerId]["position"],
                    allHighscore[2][playerId]["position"],
                    allHighscore[3][playerId]["position"],
                    allHighscore[4][playerId]["position"],
                    allHighscore[5][playerId]["position"],
                    allHighscore[6][playerId]["position"],
                    allHighscore[7][playerId]["position"],
                    allHighscore[0][playerId]["score"],
                    allHighscore[1][playerId]["score"],
                    allHighscore[2][playerId]["score"],
                    allHighscore[3][playerId]["score"],
                    allHighscore[4][playerId]["score"],
                    allHighscore[5][playerId]["score"],
                    allHighscore[6][playerId]["score"],
                    allHighscore[7][playerId]["score"],
                    playerId,
                    timestamp))
        except:
            # when a new player registers it can happen that he is in
            # posType=0 but not in posType=3
            # since it is just a new player, don't do much about it
            print playerId
    print ""

    cur.executemany("""UPDATE `player` SET ships = ?, status=?, position0 = ?, position1 = ?, position2 = ?, position3 = ?, position4 = ?, position5 = ?,
            position6 = ?, position7 = ?, score0 = ?, score1 = ?, score2 = ?, score3 = ?, score4 = ?, score5 = ?, score6 = ?, score7 = ?  WHERE
            id = ? AND ?>0""", updateData)
    cur.executemany("""INSERT INTO score_history ( ships, status, position0, position1, position2, position3, position5, position4, position6,
    position7, score0, score1, score2, score3, score4, score5, score6, score7 , playerId , `timestamp`) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
    ?, ?, ?, ?, ?, ?, ?, ?, ?)""", updateData)
    highscoreTimestamp = timestamp



    # update score inactivity
    cur.execute("SELECT timestamp FROM score_inactivity WHERE timestamp=%d" % highscoreTimestamp)
    if cur.fetchone() is None:
        print "updating inactivity"
        # read existing data
        cur.execute("SELECT playerId, score_0, timestamp, duration FROM score_inactivity")
        data = cur.fetchall()
        scoreInactivity = {}
        for row in data:
            playerId, score_0, timestamp, duration = row
            scoreInactivity[playerId] = (score_0, timestamp, duration)
        # delete it
        cur.execute("DELETE FROM score_inactivity")
        # create insert
        updateData = []
        for playerId in allHighscore[0]:
            score = allHighscore[0][playerId]["score"]
            timestamp = highscoreTimestamp
            duration = 0
            score_0 = score
            try:
                score_0, timestamp, duration = scoreInactivity[playerId]
            except:
                pass
            if score <= score_0:
                duration += highscoreTimestamp-timestamp
            else:
                duration = 0
            updateData.append((playerId, score, duration, highscoreTimestamp))
        cur.executemany("""INSERT INTO `score_inactivity` (playerId, score_0, duration, timestamp) VALUES (?,?,?,?)""", updateData)

    conn.commit()
    conn.close()

def query(query):
    conn = sqlite3.connect('ogapi.sqlite')
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

def highscoreChange(server, player, hours=24):
    from prettytable import PrettyTable
    import time
    api = Api(server, "var")
    playerId, playerName, sim = api.findPlayer(player, 1, True)
    # the old data
    q = """SELECT timestamp, ships, position0, position1, position2, position3, position5, position4, position6,
            position7, score0, score1, score2, score3, score4, score5, score6, score7
            FROM score_history
            WHERE playerId=%d AND timestamp < %d
            ORDER BY timestamp DESC
            LIMIT 1
        """ % (playerId, time.time()-hours*60*60)
    rows = query(q)
    if len(rows) == 0:
        return "Not found"
    old = rows[0]
    #print old
    # the new data
    q = """SELECT timestamp, ships, position0, position1, position2, position3, position5, position4, position6,
            position7, score0, score1, score2, score3, score4, score5, score6, score7
            FROM score_history
            WHERE playerId=%d
            ORDER BY timestamp DESC
            LIMIT 1
        """ % playerId
    rows = query(q)
    if len(rows) == 0:
        return ""
    new = rows[0]
    #print new

    retStr = []
    if sim != 1.0:
        retStr.append("%s - similarity:%.2f\n" % (playerName, sim))
    retStr.append("Highscorediff: %dh\n" % round((new[0]-old[0])/(60*60)))

    t = PrettyTable(["Type", "Position", "Score", "Type2", "Position2", "Score2"])
    t.align["Type"] = "l"
    t.align["Position"] = "r"
    t.align["Score"] = "r"
    t.align["Type2"] = "l"
    t.align["Position2"] = "r"
    t.align["Score2"] = "r"
    for type in range(0,len(api.highscore_type_to_name),2):
        # 2+type = (skip timestamp,ships) = score
        # 10+type = (skip all of above (2+8 types))
        t.add_row([
            api.highscore_type_to_name[type], old[2+type]-new[2+type], new[10+type]-old[10+type],
            # everything +1
            api.highscore_type_to_name[type+1], old[2+type+1]-new[2+type+1], new[10+type+1]-old[10+type+1],
            ])
    t.add_row(["ships", "", new[1]-old[1],
        # defense is (economy+research+military)-total
               "defense", "", ((new[10+1]-old[10+1])+(new[10+2]-old[10+2])+(new[10+3]-old[10+3]))-(new[10+0]-old[10+0])])
    t.set_style(11)
    t_str = t.get_string(border=False,header=False, padding_width=1).split("\n")
    new_t_str = []
    for line in t_str:
        new_t_str.append(line[1:])
    retStr.append("\n".join(new_t_str)+"\n")

    return "".join(retStr)


def listInactivityPlayer(position, radius=15, duration=60*60*24, minScore=5000, maxScore=9999999, amount=50):
    import math
    from prettytable import PrettyTable
    from Constants import sysDurationEqualsGalaxy
    galaxy = int(position.split(":")[0])
    system = int(position.split(":")[1])
    minSys = system-radius
    maxSys = system+radius
    # when the radius is so big, that the flight to another galaxy has a shorter duration
    # look at the other galaxy too
    minGala= galaxy-math.floor(sysDurationEqualsGalaxy(radius))
    maxGala= galaxy+math.floor(sysDurationEqualsGalaxy(radius))
    q = """SELECT player.id, player.name, player.score0, score_inactivity.duration, planet.galaxy,planet.system,planet.position
    FROM player,planet,score_inactivity
    WHERE score_inactivity.playerId = player.id AND planet.playerId=player.id
    AND player.status NOT LIKE "%%i%%" AND player.status NOT LIKE "%%I%%" AND player.status NOT LIKE "%%v%%"
    AND score_inactivity.duration >= %d
    AND player.score0>%d AND player.score0<%d
    AND planet.galaxy>=%d AND planet.galaxy<=%d AND planet.system>=%d AND planet.system<=%d
    ORDER BY score_inactivity.duration DESC, player.score0 DESC, player.id
        """ % (duration, minScore, maxScore, minGala, maxGala, minSys, maxSys)
    rows = query(q)
    if len(rows) == 0:
        return ""

    newRows = []
    lastId = 0
    newRow = False
    i = 0
    for row in rows:
        id, name, score, duration, galaxy, system, position = row
        durTime = str(datetime.timedelta(seconds=duration))
        if id != lastId:
            if lastId != 0:
                newRows.append(newRow)
                i += 1
                if i == amount:
                    break
            newRow = [id, name, score, duration, ["%d:%d:%d" % (galaxy, system, position)]]
            lastId = id
        else:
            newRow[4].append("%d:%d:%d" % (galaxy, system, position))


    t = PrettyTable(["Name", "Score", "Duration", "Coords"])
    t.align["Name"] = "l"
    t.align["Score"] = "r"
    t.align["Duration"] = "r"
    t.align["Coords"] = "l"
    for row in newRows:
        id, name, score, duration, coords = row
        for i in range(0, len(coords)):
            coords[i] = coords[i].ljust(8)
        durTime = str(datetime.timedelta(seconds=duration))
        score = float(score)/1000
        if score < 20:
            score = round(score, 1)
        else:
            score = int(score)
        score = str(score)+"k"
        t.add_row([name, score, str(durTime).replace(" day, ", "d ")[:-6]+"h", " ".join(coords)])
    return t.get_string(border=False, header=False, padding_width=1)




if __name__ == "__main__":
    def Args():
        pass
    args = Args()

    import argparse
    parser = argparse.ArgumentParser(description='get info from ogame api db',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--server', '-s', type=str, help='server like uni117.ogame.de')
    parser.add_argument('--update', '-u', type=int, help='update the database')
    parser.add_argument('--query', '-q', type=str, help='run a readonly query on the db')
    parser.add_argument('--change', '-c', type=int, help='print highscoreChange with x hours')
    parser.add_argument('--player', '-p', type=unicode, help='playername')
    args = parser.parse_args()

    if args.update:
        update(args.server)
    if args.query:
        print query(args.query)
    if args.change:
        print highscoreChange(args.server, args.player, args.change)

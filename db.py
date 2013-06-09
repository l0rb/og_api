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
    for playerData in allPlayers:
        playerId = playerData["id"]
        count += 1
        res, player = api.getPlayerInfo(playerId, addPositionInfo=False, addStatusInfo=False)
        if not res:
            print "Some error occured with player %d %s" % (playerId, player)
            continue
        print "%d/%d\r" % (count, all),

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
            updateData.append((
                    allHighscore[3][playerId]["ships"],
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

    cur.executemany("""UPDATE `player` SET ships = ?, position0 = ?, position1 = ?, position2 = ?, position3 = ?, position4 = ?, position5 = ?,
            position6 = ?, position7 = ?, score0 = ?, score1 = ?, score2 = ?, score3 = ?, score4 = ?, score5 = ?, score6 = ?, score7 = ?  WHERE
            id = ? AND ?>0""", updateData)
    cur.executemany("""INSERT INTO score_history ( ships, position0, position1, position2, position3, position5, position4, position6,
    position7, score0, score1, score2, score3, score4, score5, score6, score7 , playerId , `timestamp`) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
    ?, ?, ?, ?, ?, ?, ?, ?)""", updateData)
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


def listInactivityPlayer(position, radius=15, duration=60*60*24, minScore=5000, maxScore=9999999):
    galaxy = int(position.split(":")[0])
    system = int(position.split(":")[1])
    minSys = system-radius
    maxSys = system+radius
    q = """SELECT player.id, player.name, player.score0, score_inactivity.duration, planet.galaxy,planet.system,planet.position
    FROM player,planet,score_inactivity
    WHERE score_inactivity.playerId = player.id AND planet.playerId=player.id
    AND player.status NOT LIKE "%%i%%" AND player.status NOT LIKE "%%I%%" AND player.status NOT LIKE "%%u%%"
    AND score_inactivity.duration >= %d
    AND player.score0>%d AND player.score0<%d
    AND planet.galaxy=%d AND planet.system>%d AND planet.system<%d
    ORDER BY score_inactivity.duration DESC, player.score0 DESC, player.id
        """ % (duration, minScore, maxScore, galaxy, minSys, maxSys)
    rows = query(q)
    lastId = 0
    retStr = []
    for row in rows:
        id, name, score, duration, galaxy, system, position = row
        durTime = str(datetime.timedelta(seconds=duration))
        if id != lastId:
            if id != 0:
                retStr.append("\n")
            retStr.append("%s (%d/%s) %d:%d:%d" % (name, score, durTime, galaxy, system, position))
            lastId = id
        else:
            retStr.append(" %d:%d:%d" % (galaxy, system, position))
    return retStr




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
    args = parser.parse_args()

    if args.update:
        update(args.server)
    if args.query:
        print query(args.query)

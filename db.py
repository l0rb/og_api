#!/usr/bin/python
import sqlite3
from api import Api
import atexit





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
    for ally in allAlliances:
        count += 1
        print "%d/%d\r" % (count, all),
        insertData.append(
                (ally["id"], ally["tag"], ally["name"], ally["logo"], ally["homepage"], ally["open"]))

    cur.executemany("""INSERT INTO "alliance" ("id", "tag", "name", "logo", "homepage", "open") VALUES (?, ?, ?, ?, ?, ?)""",
            insertData)


    # player + planets
    timestamp, allPlayers = api.listPlayers()

    # this is here to download all playerdata resources in parallel
    # I know I should perhaps make this a background task but this felt as easiest
    appendList = []
    count = 0
    all = len(allPlayers)
    for playerData in allPlayers:
        id = playerData["id"]
        appendList.append("?id=%d"%id)
        if len(appendList) == 40:
            count += 40
            print "%d/%d\r"%(count,all),
            api._doApiRequestAsync("playerData", appendList)
            appendList = []

    cur.execute("DELETE FROM player")
    cur.execute("DELETE FROM planet")
    count = 0
    insertData = []
    insertPlanetData = []
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
    cur.execute("DELETE FROM score_history WHERE `timestamp`=%d"% timestamp)
    for playerId in allHighscore[0]:
        count += 1
        print "%d/%d\r" % (count, all),
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

    cur.executemany("""UPDATE `player` SET ships = ?, position0 = ?, position1 = ?, position2 = ?, position3 = ?, position4 = ?, position5 = ?,
            position6 = ?, position7 = ?, score0 = ?, score1 = ?, score2 = ?, score3 = ?, score4 = ?, score5 = ?, score6 = ?, score7 = ?  WHERE
            id = ? AND ?>0""", updateData)
    cur.executemany("""INSERT INTO score_history ( ships, position0, position1, position2, position3, position5, position4, position6,
    position7, score0, score1, score2, score3, score4, score5, score6, score7 , playerId , `timestamp`) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
    ?, ?, ?, ?, ?, ?, ?, ?)""", updateData)


    conn.commit()
    conn.close()

def query(query):
    conn = sqlite3.connect('ogapi.sqlite')
    cur = conn.cursor()
    cur.execute(query)
    ret = []
    return cur.fetchall()



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

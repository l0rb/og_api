og_api
=====

python bindings for the ogame api
Reads player and alliance information

**Example:**

    ./run.py -s uni1.ogame.de -p testname
    ./run.py -s uni1.ogame.de -a tagname

when you add -q 1 it will print a shorter list



**Requirements:**
* argparse
* requests
* python 2.7
* levenshtein
* prettytable


**How it can be used in irc:**

With irssi and trigger.pl
The triggerlist can look like this:

    -publics -nocase -channels '#yourchan' -regexp '^aplayer ([0-9a-zA-Z]+[0-9a-zA-Z\-\.\ ]+)$' -command 'exec -o /home/balrok/irssi/og_api/run.py -s uni1.ogame.de -p "$1"' 
    -publics -nocase -channels '#yourchan' -regexp '^player ([0-9a-zA-Z]+[0-9a-zA-Z\-\.\ ]+)$' -command 'exec -o /home/balrok/irssi/og_api/run.py -s uni1.ogame.de -p "$1" -q 1' 
    -publics -nocase -channels '#yourchan' -regexp '^alliance ([0-9a-zA-Z]+[0-9a-zA-Z\-\.\ ]+)$' -command 'exec -o /home/balrok/irssi/og_api/run.py -s uni1.ogame.de -a "$1" -q 1' 
    -publics -nocase -channels '#yourchan' -regexp '^aalliance ([0-9a-zA-Z]+[0-9a-zA-Z\-\.\ ]+)$' -command 'exec -o /home/balrok/irssi/og_api/run.py -s uni1.ogame.de -a "$1"' 

This has a problem, that the regex must be defensive, so a user won't execute any bash scripts through escaping from "$1"

Another method is to use the provided ircbot.py
with dependency:
* irc (this is the actual name of the python library)

This ircbot will directly call the api and therefore doesn't need to be so defensive.
Also it supports automatic reloading of the irc_handler.py in which you will find most of the logic.


** db **
The database is done with sqlite and requires this python extension - also you need to copy the ogapi.example.sqlite to ogapi.sqlite

The layout of the table is this:

*planet*
* id int(11)
* playerId int(11)
* galaxy tinyint(3)
* system tinyint(3)
* position smallint(5)
* name varchar(255) 
* moonName text
* moonSize int

*alliance*
* id int
* tag text
* name text
* logo text NULL
* homepage text NULL
* open integer

*score_history*
* playerId integer
* timestamp integer
* ships integer
* status text (default is "-" for entries where one can't find a status)
* position0 integer
* score0 integer
* position1 integer
* score1 integer
* position2 integer
* score2 integer
* position3 integer
* position5 integer
* score4 integer
* position4 integer
* score3 integer
* score5 integer
* position6 integer
* score6 integer
* position7 integer
* score7 integer 

*player*
* id integer
* name text
* allianceId integer NULL
* status text
* ships integer NULL
* position0 integer NULL
* score0 integer NULL
* position1 integer NULL
* score1 integer NULL
* position2 integer NULL
* score2 integer NULL
* position3 integer NULL
* position5 integer NULL
* score4 integer NULL
* position4 integer NULL
* score3 integer NULL
* score5 integer NULL
* position6 integer NULL
* score6 integer NULL
* position7 integer NULL
* score7 integer NULL

Useful queries:
*top 5 alliances with less than 2 players*
* SELECT alliance.name, COUNT(alliance.id), SUM(player.score0) as s0sum FROM player,alliance WHERE player.allianceId=alliance.id GROUP BY alliance.id HAVING COUNT(alliance.id)<3 ORDER BY s0sum DESC LIMIT 5
* players in top 100 which are not military top 1200 (so they are miners)
* SELECT player.name,player.position0, alliance.name FROM player LEFT JOIN alliance ON alliance.id=player.allianceId WHERE position0<=100 AND position3>1200 ORDER BY position0
* score inactivity (players without "i" status but who did not have any score changes since 24h
* SELECT s1.playerId playerId, s1.timestamp-min(s2.timestamp) duration FROM score_history s1, score_history s2 WHERE 
s1.playerId=s2.playerId AND s1.timestamp=(SELECT timestamp from score_history ORDER BY timestamp DESC LIMIT 1) AND s1.score0=s2.score0
GROUP BY s1.playerId
HAVING s1.timestamp-60*60*24>min(s2.timestamp);
* select players near you with score_inactivity
* SELECT player.name, player.score0, score_inactivity.duration, planet.galaxy,planet.system,planet.position FROM player,planet, score_inactivity
WHERE score_inactivity.playerId = player.id AND planet.playerId=player.id AND
planet.galaxy=3 AND planet.system>323 AND planet.system<353;
ORDER BY score_inactivity.duration DESC, player.score0 DESC, player.id
* select inactive players near you
* SELECT player.name, player.status, planet.galaxy, planet.system, planet.position FROM player,planet WHERE planet.playerId=player.id AND
 planet.galaxy=1 AND planet.system>454 AND planet.system<494 AND (player.status LIKE "%i%" OR player.status LIKE "%I%") AND player.status
 NOT LIKE "%v%"

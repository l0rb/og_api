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

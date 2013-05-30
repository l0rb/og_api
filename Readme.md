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
* lxml
* python 2.7


**How it can be used in irc:**

With irssi and trigger.pl
The triggerlist can look like this:

    -publics -nocase -channels '#yourchan' -regexp '^aplayer ([0-9a-zA-Z]+[0-9a-zA-Z\-\.\ ]+)$' -command 'exec -o /home/balrok/irssi/og_api/run.py -s uni1.ogame.de -p "$1"' 
    -publics -nocase -channels '#yourchan' -regexp '^player ([0-9a-zA-Z]+[0-9a-zA-Z\-\.\ ]+)$' -command 'exec -o /home/balrok/irssi/og_api/run.py -s uni1.ogame.de -p "$1" -q 1' 
    -publics -nocase -channels '#yourchan' -regexp '^alliance ([0-9a-zA-Z]+[0-9a-zA-Z\-\.\ ]+)$' -command 'exec -o /home/balrok/irssi/og_api/run.py -s uni1.ogame.de -a "$1" -q 1' 
    -publics -nocase -channels '#yourchan' -regexp '^aalliance ([0-9a-zA-Z]+[0-9a-zA-Z\-\.\ ]+)$' -command 'exec -o /home/balrok/irssi/og_api/run.py -s uni1.ogame.de -a "$1"' 

This has a problem, that the regex is very defensive, so a user won't execute any bash scripts through escaping from "$1"


Another method is to use the ircbot.py which is provided

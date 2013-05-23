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


Please use it with caution and report any bugs you find :)
Also you might see, that not all possible playernames and alliance tags will work this is because I don't want to allow .*

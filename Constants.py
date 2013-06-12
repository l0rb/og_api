# coding=utf-8
from __future__ import division
from math import floor,ceil,e

# when you use vim, you can use this to replace bId with this constant
#'<,'>s/[0-9][0-9]*/\={ '1'  : 'METALMINE', '2'  : 'CRYSTALMINE', '3'  : 'DEUTERIUMSYNTHESIZER', '4'  : 'SOLARPLANT', '12' : 'FUSIONREACTOR', '14' : 'ROBOTICSFACTORY', '15' : 'NANITEFACTORY', '21' : 'SHIPYARD', '22' : 'METALSTORAGE', '23' : 'CRYSTALSTORAGE', '24' : 'DEUTERIUMTANK', '25' : 'METALHIDING', '26' : 'CRYSTALHIDING', '27' : 'DEUTERIUMHIDING', '31' : 'RESEARCHLAB', '33' : 'TERRAFORMER', '34' : 'ALLIANCEDEPOT', '41' : 'LUNARBASE', '42' : 'SENSORPHALANX', '43' : 'JUMPGATE', '44' : 'MISSILESILO', '106': 'ESPIONAGETECHNOLOGY', '108': 'COMPUTERTECHNOLOGY', '109': 'WEAPONSTECHNOLOGY', '110': 'SHIELDINGTECHNOLOGY', '111': 'ARMOURTECHNOLOGY', '113': 'ENERGYTECHNOLOGY', '114': 'HYPERSPACETECHNOLOGY', '115': 'COMBUSTIONDRIVE', '117': 'IMPULSEDRIVE', '118': 'HYPERSPACEDRIVE', '120': 'LASERTECHNOLOGY', '121': 'IONTECHNOLOGY', '122': 'PLASMATECHNOLOGY', '123': 'INTERGALACTICRESEARCHNETWORK', '124': 'ASTROPHYSICS', '199': 'GRAVITONTECHNOLOGY', '202': 'SMALLCARGO', '203': 'LARGECARGO', '204': 'LIGHTFIGHTER', '205': 'HEAVYFIGHTER', '206': 'CRUISER', '207': 'BATTLESHIP', '208': 'COLONYSHIP', '209': 'RECYCLER', '210': 'ESPIONAGEPROBE', '211': 'BOMBER', '212': 'SOLARSATELLITE', '213': 'DESTROYER', '214': 'DEATHSTAR', '215': 'BATTLECRUISER', '401': 'ROCKETLAUNCHER', '402': 'LIGHTLASER', '403': 'HEAVYLASER', '404': 'GAUSSCANNON', '405': 'IONCANNON', '406': 'PLASMATURRET', '407': 'SMALLSHIELDDOME', '408': 'LARGESHIELDDOME', '502': 'ANTIBALLISTICMISSILE', '503': 'INTERPLANETARYMISSILE' }[submatch(0)]/g


# constants for bids
METALMINE                    = 1
CRYSTALMINE                  = 2
DEUTERIUMSYNTHESIZER         = 3
SOLARPLANT                   = 4
FUSIONREACTOR                = 12
ROBOTICSFACTORY              = 14
NANITEFACTORY                = 15
SHIPYARD                     = 21
METALSTORAGE                 = 22
CRYSTALSTORAGE               = 23
DEUTERIUMTANK                = 24
METALHIDING                  = 25
CRYSTALHIDING                = 26
DEUTERIUMHIDING              = 27
RESEARCHLAB                  = 31
TERRAFORMER                  = 33
ALLIANCEDEPOT                = 34
LUNARBASE                    = 41
SENSORPHALANX                = 42
JUMPGATE                     = 43
MISSILESILO                  = 44
ESPIONAGETECHNOLOGY          = 106
COMPUTERTECHNOLOGY           = 108
WEAPONSTECHNOLOGY            = 109
SHIELDINGTECHNOLOGY          = 110
ARMOURTECHNOLOGY             = 111
ENERGYTECHNOLOGY             = 113
HYPERSPACETECHNOLOGY         = 114
COMBUSTIONDRIVE              = 115
IMPULSEDRIVE                 = 117
HYPERSPACEDRIVE              = 118
LASERTECHNOLOGY              = 120
IONTECHNOLOGY                = 121
PLASMATECHNOLOGY             = 122
INTERGALACTICRESEARCHNETWORK = 123
ASTROPHYSICS                 = 124
GRAVITONTECHNOLOGY           = 199
SMALLCARGO                   = 202
LARGECARGO                   = 203
LIGHTFIGHTER                 = 204
HEAVYFIGHTER                 = 205
CRUISER                      = 206
BATTLESHIP                   = 207
COLONYSHIP                   = 208
RECYCLER                     = 209
ESPIONAGEPROBE               = 210
BOMBER                       = 211
SOLARSATELLITE               = 212
DESTROYER                    = 213
DEATHSTAR                    = 214
BATTLECRUISER                = 215
ROCKETLAUNCHER               = 401
LIGHTLASER                   = 402
HEAVYLASER                   = 403
GAUSSCANNON                  = 404
IONCANNON                    = 405
PLASMATURRET                 = 406
SMALLSHIELDDOME              = 407
LARGESHIELDDOME              = 408
ANTIBALLISTICMISSILE         = 502
INTERPLANETARYMISSILE        = 503

buildLabels = {}
buildLabelsName = dict(zip(buildLabels.values(),buildLabels.keys()))

def loadLanguage(lang="de"):
    global buildLabels
    global buildLabelsName
    if lang == "de":
        buildLabels = {
                METALMINE  : u'Metallmine',
                CRYSTALMINE  : u'Kristallmine',
                DEUTERIUMSYNTHESIZER  : u'Deuterium-Synthetisierer',
                SOLARPLANT  : u'Solarkraftwerk',
                FUSIONREACTOR : u'Fusionskraftwerk',
                ROBOTICSFACTORY : u'Roboterfabrik',
                NANITEFACTORY : u'Nanitenfabrik',
                SHIPYARD : u'Raumschiffswerft',
                METALSTORAGE : u'Metallspeicher',
                CRYSTALSTORAGE : u'Kristallspeicher',
                DEUTERIUMTANK : u'Deuteriumtank',
                METALHIDING : u'Abgeschirmtes Metallversteck',
                CRYSTALHIDING : u'Unterirdisches Kristallversteck',
                DEUTERIUMHIDING : u'Meeresgrund Deuteriumversteck',
                RESEARCHLAB : u'Forschungslabor',
                TERRAFORMER : u'Terraformer',
                ALLIANCEDEPOT : u'Allianzdepot',
                MISSILESILO : u'Raketensilo',
                # research
                ESPIONAGETECHNOLOGY: u'Spionagetechnik',
                COMPUTERTECHNOLOGY: u'Computertechnik',
                WEAPONSTECHNOLOGY: u'Waffentechnik',
                SHIELDINGTECHNOLOGY: u'Schildtechnik',
                ARMOURTECHNOLOGY: u'Raumschiffpanzerung',
                ENERGYTECHNOLOGY: u'Energietechnik',
                HYPERSPACETECHNOLOGY: u'Hyperraumtechnik',
                COMBUSTIONDRIVE: u'Verbrennungstriebwerk',
                IMPULSEDRIVE: u'Impulstriebwerk',
                HYPERSPACEDRIVE: u'Hyperraumantrieb',
                LASERTECHNOLOGY: u'Lasertechnik',
                IONTECHNOLOGY: u'Ionentechnik',
                PLASMATECHNOLOGY: u'Plasmatechnik',
                INTERGALACTICRESEARCHNETWORK: u'Intergalaktisches Forschungsnetzwerk',
                ASTROPHYSICS: u'Astrophysik',
                GRAVITONTECHNOLOGY: u'Gravitonforschung',
                # shipyard
                SMALLCARGO: u'Kleiner Transporter',
                LARGECARGO: u'Großer Transporter',
                LIGHTFIGHTER: u'Leichter Jäger',
                HEAVYFIGHTER: u'Schwerer Jäger',
                CRUISER: u'Kreuzer',
                BATTLESHIP: u'Schlachtschiff',
                COLONYSHIP: u'Kolonieschiff',
                RECYCLER: u'Recycler',
                ESPIONAGEPROBE: u'Spionagesonde',
                BOMBER: u'Bomber',
                SOLARSATELLITE: u'Solarsatellit',
                DESTROYER: u'Zerstörer',
                DEATHSTAR: u'Todesstern',
                BATTLECRUISER: u'Schlachtkreuzer',
                ROCKETLAUNCHER: u'Raketenwerfer',
                LIGHTLASER: u'Leichtes Lasergeschütz',
                HEAVYLASER: u'Schweres Lasergeschütz',
                GAUSSCANNON: u'Gaußkanone',
                IONCANNON: u'Ionengeschütz',
                PLASMATURRET: u'Plasmawerfer',
                SMALLSHIELDDOME: u'Kleine Schildkuppel',
                LARGESHIELDDOME: u'Große Schildkuppel',
                ANTIBALLISTICMISSILE: u'Abfangrakete',
                INTERPLANETARYMISSILE: u'Interplanetarrakete',
            }
    elif lang == "se":
        buildLabels = {
                METALMINE  : u'Metallgruva',
                CRYSTALMINE  : u'Kristallgruva',
                DEUTERIUMSYNTHESIZER  : u'Deuteriumplattform',
                SOLARPLANT  : u'Solkraftverk',
                FUSIONREACTOR : u'Fusionskraftverk',
                ROBOTICSFACTORY : u'Robotfabrik',
                NANITEFACTORY : u'Nanofabrik',
                SHIPYARD : u'Skeppsvarv',
                METALSTORAGE : u'Metallager',
                CRYSTALSTORAGE : u'Kristallager',
                DEUTERIUMTANK : u'Deuteriumtank',
                METALHIDING : u'Skärmad Metall Håla',
                CRYSTALHIDING : u'Underjordisk Kristall håla',
                DEUTERIUMHIDING : u'Havsbotten Deuterium Håla',
                RESEARCHLAB : u'Forskningslabb',
                TERRAFORMER : u'Terraformare',
                ALLIANCEDEPOT : u'Alliansdepå',
                MISSILESILO : u'Missilsilo',
                # research
                ESPIONAGETECHNOLOGY: u'Spionageteknologi',
                COMPUTERTECHNOLOGY: u'Datorteknologi',
                WEAPONSTECHNOLOGY: u'Vapenteknologi',
                SHIELDINGTECHNOLOGY: u'Sköldteknologi',
                ARMOURTECHNOLOGY: u'Pansarteknologi',
                ENERGYTECHNOLOGY: u'Energiteknologi',
                HYPERSPACETECHNOLOGY: u'Hyperrymdteknologi',
                COMBUSTIONDRIVE: u'Raketmotor',
                IMPULSEDRIVE: u'Impulsmotor',
                HYPERSPACEDRIVE: u'Hyperrymdmotor',
                LASERTECHNOLOGY: u'Laserteknologi',
                IONTECHNOLOGY: u'Jonteknologi',
                PLASMATECHNOLOGY: u'Plasmateknologi',
                INTERGALACTICRESEARCHNETWORK: u'Intergalaktiskt forskningsnätverk',
                ASTROPHYSICS: u'Astrofysik',
                GRAVITONTECHNOLOGY: u'Gravitonteknologi',
                # shipyard
                SMALLCARGO: u'Litet transportskepp',
                LARGECARGO: u'Stort transportskepp',
                LIGHTFIGHTER: u'Litet jaktskepp',
                HEAVYFIGHTER: u'Stort jaktskepp',
                CRUISER: u'Kryssare',
                BATTLESHIP: u'Slagskepp',
                COLONYSHIP: u'Koloniskepp',
                RECYCLER: u'Återvinnare',
                ESPIONAGEPROBE: u'Spionsond',
                BOMBER: u'Bombare',
                SOLARSATELLITE: u'Solsatellit',
                DESTROYER: u'Flaggskepp',
                DEATHSTAR: u'Dödsstjärna',
                BATTLECRUISER: u'Jagare',
                ROCKETLAUNCHER: u'Raketramp',
                LIGHTLASER: u'Litet lasertorn',
                HEAVYLASER: u'Stort lasertorn',
                GAUSSCANNON: u'Gausskanon',
                IONCANNON: u'Jonkanon',
                PLASMATURRET: u'Plasmakanon',
                SMALLSHIELDDOME: u'Liten sköldkupol',
                LARGESHIELDDOME: u'Stor sköldkupol',
                ANTIBALLISTICMISSILE: u'Antiballistiska missiler',
                INTERPLANETARYMISSILE: u'Interplanetära missiler',
            }
    buildLabelsName = dict(zip(buildLabels.values(),buildLabels.keys()))

pageToBid = {
    'resources': [METALMINE,CRYSTALMINE,DEUTERIUMSYNTHESIZER,SOLARPLANT,FUSIONREACTOR,METALSTORAGE,CRYSTALSTORAGE,DEUTERIUMTANK,METALHIDING,CRYSTALHIDING,DEUTERIUMHIDING,],
    'station': [ROBOTICSFACTORY,NANITEFACTORY,SHIPYARD,RESEARCHLAB,TERRAFORMER,ALLIANCEDEPOT,MISSILESILO,],
    'research': [ ESPIONAGETECHNOLOGY, COMPUTERTECHNOLOGY, WEAPONSTECHNOLOGY, SHIELDINGTECHNOLOGY, ARMOURTECHNOLOGY, ENERGYTECHNOLOGY, HYPERSPACETECHNOLOGY, COMBUSTIONDRIVE, IMPULSEDRIVE, HYPERSPACEDRIVE, LASERTECHNOLOGY, IONTECHNOLOGY, PLASMATECHNOLOGY, INTERGALACTICRESEARCHNETWORK, ASTROPHYSICS, GRAVITONTECHNOLOGY,],
    'shipyard': [SMALLCARGO,LARGECARGO,LIGHTFIGHTER,HEAVYFIGHTER,CRUISER,BATTLESHIP,COLONYSHIP,RECYCLER,ESPIONAGEPROBE,BOMBER,SOLARSATELLITE,DESTROYER,DEATHSTAR,BATTLECRUISER,],
    'defense': [ ROCKETLAUNCHER, LIGHTLASER, HEAVYLASER, GAUSSCANNON, IONCANNON, PLASMATURRET, SMALLSHIELDDOME, LARGESHIELDDOME, ANTIBALLISTICMISSILE, INTERPLANETARYMISSILE,],
}

costs = {
    METALMINE           : (40      , 10      , 0      , 1.5),
    CRYSTALMINE         : (30      , 15      , 0      , 1.6),
    DEUTERIUMSYNTHESIZER: (150     , 50      , 0      , 1.5),
    SOLARPLANT          : (50      , 20      , 0      , 1.5),
    FUSIONREACTOR       : (500     , 200     , 100    , 1.8),
    ROBOTICSFACTORY     : (200     , 60      , 100    , 2.0),
    NANITEFACTORY       : (500000  , 250000  , 50000  , 2.0),
    SHIPYARD            : (200     , 100     , 50     , 2.0),
    METALSTORAGE        : (500     , 0       , 0      , 2.0),
    CRYSTALSTORAGE      : (500     , 250     , 0      , 2.0),
    DEUTERIUMTANK       : (500     , 500     , 0      , 2.0),
    METALHIDING         : (1150    , 0       , 0      , 2.3),
    CRYSTALHIDING       : (1150    , 575     , 0      , 2.3),
    DEUTERIUMHIDING     : (1150    , 575     , 0      , 2.3),
    RESEARCHLAB         : (100     , 200     , 100    , 2.0),
    TERRAFORMER         : (0       , 25000   , 50000  , 2.0),
    ALLIANCEDEPOT       : (10000   , 20000   , 0      , 2.0),
    LUNARBASE           : (10000   , 20000   , 10000  , 2.0),
    SENSORPHALANX       : (10000   , 20000   , 10000  , 2.0),
    JUMPGATE            : (1000000 , 2000000 , 1000000, 2.0),
    MISSILESILO         : (10000   , 10000   , 500    , 2.0),
    #research
    ESPIONAGETECHNOLOGY : (100     , 500     , 100    , 2.0),
    COMPUTERTECHNOLOGY  : (0       , 200     , 300    , 2.0),
    WEAPONSTECHNOLOGY   : (400     , 100     , 0      , 2.0),
    SHIELDINGTECHNOLOGY : (100     , 300     , 0      , 2.0),
    ARMOURTECHNOLOGY    : (500     , 0       , 0      , 2.0),
    ENERGYTECHNOLOGY    : (0       , 400     , 200    , 2.0),
    HYPERSPACETECHNOLOGY: (0       , 0       , 0      , 2.0), # is in getCosts
    COMBUSTIONDRIVE     : (200     , 0       , 300    , 2.0),
    IMPULSEDRIVE        : (1000    , 2000    , 300    , 2.0),
    HYPERSPACEDRIVE     : (5000    , 10000   , 3000   , 2.0),
    LASERTECHNOLOGY     : (100     , 50      , 0      , 2.0),
    IONTECHNOLOGY       : (500     , 150     , 50     , 2.0),
    PLASMATECHNOLOGY    : (1000    , 2000    , 500    , 2.0),
    INTERGALACTICRESEARCHNETWORK: (120000  , 200000  , 80000  , 2.0),
    ASTROPHYSICS        : (4000    , 8000    , 4000   , 2.0),
    GRAVITONTECHNOLOGY  : (0       , 0       , 0      , 2.0),
    #fleet
    SMALLCARGO          : (2000    , 2000    , 0      ),
    LARGECARGO          : (6000    , 6000    , 0      ),
    LIGHTFIGHTER        : (3000    , 1000    , 0      ),
    HEAVYFIGHTER        : (6000    , 4000    , 0      ),
    CRUISER             : (20000   , 7000    , 2000   ),
    BATTLESHIP          : (45000   , 15000   , 0      ),
    COLONYSHIP          : (10000   , 20000   , 10000  ),
    RECYCLER            : (10000   , 6000    , 2000   ),
    ESPIONAGEPROBE      : (0       , 1000    , 0      ),
    BOMBER              : (500     , 50000   , 25000  ),
    SOLARSATELLITE      : (0       , 2000    , 500    ),
    DESTROYER           : (60000   , 50000   , 15000  ),
    DEATHSTAR           : (5000000 , 4000000 , 1000000),
    BATTLECRUISER       : (30000   , 40000   , 15000  ),
    #deff
    ROCKETLAUNCHER      : (2000    , 0       , 0)       ,
    LIGHTLASER          : (1500    , 500     , 0)       ,
    HEAVYLASER          : (6000    , 2000    , 0)       ,
    GAUSSCANNON         : (20000   , 15000   , 2000)    ,
    IONCANNON           : (2000    , 6000    , 0)       ,
    PLASMATURRET        : (50000   , 50000   , 30000)   ,
    SMALLSHIELDDOME     : (10000   , 10000   , 0)       ,
    LARGESHIELDDOME     : (50000   , 50000   , 0)       ,
    ANTIBALLISTICMISSILE: (8000    , 0       , 2000)    ,
    INTERPLANETARYMISSILE: (12500   , 2500    , 10000)   ,
}
def isBuilding(bId):
    return 0<bId<100
def isResearch(bId):
    return 100<bId<200
def isFleet(bId):
    return 200<bId<300
def isDeff(bId):
    return 400<bId<600


def getCosts(bId, lvl):
    c = costs[bId]
    if isBuilding(bId) or isResearch(bId):
        if bId == ASTROPHYSICS:
            return {
                    'metal': 100*floor(0.5+40*pow(1.75,lvl-1)),
                    'crystal': 100*floor(0.5+80*pow(1.75,lvl-1)),
                    'deuterium': 100*floor(0.5+40*pow(1.75,lvl-1)),
                    }
        return {
                'metal': floor(c[0]*pow(c[3], lvl)),
                'crystal': floor(c[1]*pow(c[3], lvl)),
                'deuterium': floor(c[2]*pow(c[3], lvl)),
                }
    else:
        return {
                'metal': c[0],
                'crystal': c[1],
                'deuterium': c[2],
                }

def getStorage(bId, level):
    res = {"metal":0, "crystal":0, "deuterium":0, "energy":0}
    if bId == METALSTORAGE:
        res["metal"] = int(floor(2.5 * pow(e, 20 * level / 33.0)) * 5000)
    elif bId == CRYSTALSTORAGE:
        res["crystal"] = int(floor(2.5 * pow(e, 20 * level / 33.0)) * 5000)
    elif bId == DEUTERIUMTANK:
        res["deuterium"] = int(floor(2.5 * pow(e, 20 * level / 33.0)) * 5000)
    return res

def getHiding(bId, level, mtemp=50):
    res = {"metal":0, "crystal":0, "deuterium":0, "energy":0}
    if bId == METALHIDING:
        res["metal"] = int(floor(600 * level * pow(1.1, level)))
    elif bId == CRYSTALHIDING:
        res["crystal"] = int(floor(600 * level * pow(1.1, level)))
    elif bId == DEUTERIUMHIDING:
        res["deuterium"] = int(floor(400 * level * pow(1.1, level * (1.44-0.004*mtemp))))
    return res

def addRes(res1, res2):
    return {k:(res1[k] + res2[k]) for k in res1}
def subRes(res1, res2):
    return {k:(res1[k] - res2[k]) for k in res1}



def to_mse(metal=0, crystal=0, deuterium=0, energy=0, mse=None):
    if not mse: mse = [2.0, 1.0, 1.0]
    m = metal
    k = crystal * (mse[0]/mse[1])
    d = deuterium * (mse[0]/mse[2])
    e = energy * 0 # TODO can we add energy to this formula?
    return round(m+k+d+e)

def production(bId, level, research=None, mtemp=50):
    if research is None: research = {PLASMATECHNOLOGY:0, ENERGYTECHNOLOGY:0}
    res = {"metal":0, "crystal":0, "deuterium":0, "energy":0}
    if bId == METALMINE:
        plasma_metbonus= 0.01 # 1% per level
        res["metal"] = int(floor(30*level*pow(1.1,level) * (1+plasma_metbonus*research[122])) + 30)
        res["energy"] = int(ceil(10*level*pow(1.1,level)) * -1)
    elif bId == CRYSTALMINE:
        plasma_krisbonus= 0.0066 # 0.66% per level
        res["crystal"] = int(floor( (20*level*pow(1.1,level)) * (1+plasma_krisbonus*research[122]) ) + 15)
        res["energy"] = int(ceil(10*level*pow(1.1,level)) * -1)
    elif bId == DEUTERIUMSYNTHESIZER:
        res["deuterium"] = int(floor(10*level*pow(1.1,level)*(1.44-0.004*mtemp)))
        res["energy"] = int(ceil(20*level*pow(1.1,level)) * -1)
    elif bId == SOLARPLANT:
        res["energy"] = int(floor(20*level*pow(1.1,level)))
    elif bId == FUSIONREACTOR:
        res["energy"] = int(floor(30*level*pow(1.05+research[ENERGYTECHNOLOGY]*0.01,level)))
        res["deuterium"] = int(ceil(10*level*pow(1.1,level)) * -1)
    elif bId == SOLARSATELLITE:
        res["energy"] = int(floor((mtemp+140) / 6) * level)
    return res

def gain(bId, level, research=None, mtemp=50):
    if research is None: research = {PLASMATECHNOLOGY:0, ENERGYTECHNOLOGY:0}
    pNew = production(bId, level, research, mtemp)
    pOld = production(bId, level-1, research, mtemp)
    return subRes(pNew, pOld)

def atime(level, bId, research=None, mtemp=50, mse=None):
    """ Return time in seconds after which the mine with the given level
    has paid off itself. """
    if not mse: mse = [2.0, 1.0, 1.0]
    if research is None: research = {PLASMATECHNOLOGY:0, ENERGYTECHNOLOGY:0}
    cost_mse = to_mse(mse=mse, **getCosts(bId, level))
    gain_mse = to_mse(mse=mse, **gain(bId, level, research, mtemp))
    return round((cost_mse / gain_mse) * 3600)

def buildingTopList(buildings, research=None, temp=50, mse=None):
    if not mse: mse = [2.0, 1.0, 1.0]
    if research is None: research = {PLASMATECHNOLOGY:0, ENERGYTECHNOLOGY:0}
    t= []
    for bId in buildings:
        if bId > 3 or bId < 1:
            continue
        lvl = buildings[bId]
        t.append({'bId': bId, 'atime': atime(lvl+1,bId,research,temp, mse=mse)})
    return sorted(t, key=lambda x: x["atime"])


battleStats = {
        #shipId: (0:attack, 1:shield, 2:hull, 3:rapidfire)
        SMALLCARGO:     (5, 10, 4000,   {ESPIONAGEPROBE: 5, SOLARSATELLITE: 5}),
        LARGECARGO:     (5, 25, 12000,  {ESPIONAGEPROBE: 5, SOLARSATELLITE: 5}),
        LIGHTFIGHTER:   (50, 10, 4000,  {ESPIONAGEPROBE: 5, SOLARSATELLITE: 5}),
        HEAVYFIGHTER:   (150, 25, 10000,{SMALLCARGO:3,ESPIONAGEPROBE: 5, SOLARSATELLITE: 5}),
        CRUISER:        (400, 50, 27000,{LIGHTFIGHTER:6,ROCKETLAUNCHER:10,ESPIONAGEPROBE: 5, SOLARSATELLITE: 5}),
        BATTLESHIP:     (1000, 200, 60000,{ESPIONAGEPROBE: 5, SOLARSATELLITE: 5}),
        COLONYSHIP:     (50, 100, 30000,{ESPIONAGEPROBE: 5, SOLARSATELLITE: 5}),
        RECYCLER:       (1, 10000, 16000,{ESPIONAGEPROBE: 5, SOLARSATELLITE: 5}),
        ESPIONAGEPROBE: (0, 0, 1000, {}),
        BOMBER:         (1000,500,75000, {LIGHTLASER:20,ROCKETLAUNCHER:20,HEAVYLASER:10,IONCANNON:10,ESPIONAGEPROBE:5,SOLARSATELLITE:5}),
        DESTROYER:      (2000,500,110000, {LIGHTLASER:10,BATTLECRUISER:2,ESPIONAGEPROBE:5,SOLARSATELLITE:5}),
        DEATHSTAR:      (200000,50000,9000000,{SOLARSATELLITE:1250,ESPIONAGEPROBE:1250,COLONYSHIP:250,SMALLCARGO:250,LARGECARGO:250,RECYCLER:250,
            LIGHTFIGHTER:200,HEAVYFIGHTER:100,CRUISER:33,BATTLESHIP:30,BOMBER:25,BATTLECRUISER:15,DESTROYER:5,ROCKETLAUNCHER:200,LIGHTLASER:200,
            HEAVYLASER:100,IONCANNON:100,GAUSSCANNON:50}),
        BATTLECRUISER:  (700, 400, 70000, {ESPIONAGEPROBE:5,SOLARSATELLITE:5,SMALLCARGO:3,LARGECARGO:3,HEAVYFIGHTER:4,CRUISER:4,BATTLESHIP:7}),
        SOLARSATELLITE: (1, 1, 2000, {}),
        # TODO defense buildings
}


shipStats = {
    #shipId: (0:research, 1:baseSpeed, 2:fuel, 3:(improvedResearch, improvedMinlevel, improvedBaseSpeed, improvedFuel), 4:exp_value, 5:cargo)
        SMALLCARGO:     (COMBUSTIONDRIVE, 5000,      10, (IMPULSEDRIVE,5,10000,20), 12, 5000),
        LARGECARGO:     (COMBUSTIONDRIVE, 7500,      50, (0,0,0,0),        47,25000),
        LIGHTFIGHTER:   (COMBUSTIONDRIVE, 12500,     20, (0,0,0,0),        12,   50),
        HEAVYFIGHTER:   (IMPULSEDRIVE,    10000,     75, (0,0,0,0),       110,  100),
        CRUISER:        (IMPULSEDRIVE,    15000,    300, (0,0,0,0),        47,  800),
        BATTLESHIP:     (HYPERSPACEDRIVE, 10000,    500, (0,0,0,0),       160, 1500),
        COLONYSHIP:     (IMPULSEDRIVE,    2500,    1000, (0,0,0,0),        40, 7500),
        RECYCLER:       (COMBUSTIONDRIVE, 2000,     300, (0,0,0,0),        16,20000),
        ESPIONAGEPROBE: (COMBUSTIONDRIVE, 100000000,  1, (0,0,0,0),         1,    0),
        BOMBER:         (IMPULSEDRIVE,    4000,    1000, (HYPERSPACEDRIVE,8,5000,1000),75,  500),
        DESTROYER:      (HYPERSPACEDRIVE, 5000,    1000, (0,0,0,0),       110, 2000),
        DEATHSTAR:      (HYPERSPACEDRIVE, 100,        1, (0,0,0,0),      9000,1000000),
        BATTLECRUISER:  (HYPERSPACEDRIVE, 10000,    250, (0,0,0,0),        70,  750),
}

def distance(coord1, coord2):
    if coord1[0] != coord2[0]:
        return abs(coord1[0]-coord2[0]) * 20000
    if coord1[1] != coord2[1]:
        return abs(coord1[1]-coord2[1]) * 95 + 2700
    if coord1[2] != coord2[2]:
        return abs(coord1[2]-coord2[2]) * 5 + 1000
    return 5

def speed(shipId, research):
    # find if this ship has an improved speed
    rId, rMinLvl, baseSpeed = shipStats[shipId][3][:3]
    if rId == 0 or rId not in research or rMinLvl > research[rId]:
        # take normal speed
        rId, baseSpeed = shipStats[shipId][:2]
    try:
        lvl = research[rId]
    except KeyError:
        return 0
    if rId == COMBUSTIONDRIVE:
        return round(baseSpeed * (1 + 0.1 * lvl))
    if rId == IMPULSEDRIVE:
        return round(baseSpeed * (1 + 0.2 * lvl))
    if rId == HYPERSPACEDRIVE:
        return round(baseSpeed * (1 + 0.3 * lvl))

# speedfactor is how many percent of speed is used
# speeduni is wether the universe is double or quadruple speed
def duration(speed, distance, speedFactor=1, speedUni=1):
    if speed == 0:
        return 999999999
    return round(3500 / speedFactor * (distance * 10 / speed)**0.5 + 10)

# convenience funtion for duration calculation in one go
def easyDuration(coord1, coord2, shipId, research, speedFactor=1, speedUni=1):
    dist = distance(coord1, coord2)
    sp = speed(shipId, research)
    return duration(sp, dist, speedFactor, speedUni)

# calculates the res which will end in the specified cargo
# it is expected that resources are the lootable resources
# so that they are already divided by 2
def getFilledCargo(resources, availableCargo):
    res = {"metal":0, "crystal":0, "deuterium":0, "energy":0}
    if availableCargo == 0:
        return 0,res
    # to explain it: the algo works for each resource type the same,
    # only a constant changes. In the first step it is: m:3,c:2,d:1
    # and second step it is m:2,c:1
    for step in (0,1):
        # mse is for this special constant
        mse = {"metal":3.0,"crystal":2.0,"deuterium":1.0}
        for i in mse:
            mse[i] -= step # second step has 2:1:0
        for r in ("metal", "crystal", "deuterium"):
            if mse[r] == 0:
                break
            # we can't make changes to resources, so calculate it by the diff
            # with our token res
            actualResource = resources[r]-res[r]
            # useCargo is the maximum amount of res we can take with use
            useCargo = int(ceil(availableCargo/mse[r]))
            if actualResource > useCargo:
                res[r] += useCargo
                availableCargo -= useCargo
                if availableCargo == 0:
                    return 0, res
            else:
                availableCargo -= actualResource
                res[r] += actualResource
    return availableCargo, res
    # following was simplified but is kept up so it can be understood
    ## 1. maximum 1/3 of cargo gets filled with metal
    #if resources["metal"] > ceil(availableCargo/3.0):
    #    res["metal"] += int(ceil(availableCargo/3.0))
    #    availableCargo -= int(ceil(availableCargo/3.0))
    #else:
    #    availableCargo -= resources["metal"]
    #    res["metal"] += resources["metal"]
    ## 1/2 of the available cargo gets filled with crystal
    #if resources["crystal"] > ceil(availableCargo/2.0):
    #    res["crystal"] += int(ceil(availableCargo/2.0))
    #    availableCargo -= int(ceil(availableCargo/2.0))
    #else:
    #    availableCargo -= resources["crystal"]
    #    res["crystal"] += resources["crystal"]
    ## now every deuterium available gets loaded on
    #if resources["deuterium"] > availableCargo:
    #    res["deuterium"] += availableCargo
    #    return 0, res
    #else:
    #    availableCargo -= resources["deuterium"]
    #    res["deuterium"] += resources["deuterium"]
    ## load half of the cargo with metal
    #if resources["metal"]-res["metal"] > ceil(availableCargo/2.0):
    #    res["metal"] += int(ceil(availableCargo/2.0))
    #    availableCargo -= int(ceil(availableCargo/2.0))
    #else:
    #    availableCargo -= resources["metal"]-res["metal"]
    #    res["metal"] += resources["metal"]-res["metal"]
    ## now every crystal available gets loaded on
    #if resources["crystal"]-res["crystal"] > availableCargo:
    #    res["crystal"] += availableCargo
    #    return 0, res
    #else:
    #    availableCargo -= resources["crystal"]-res["crystal"]
    #    res["crystal"] += resources["crystal"]-res["crystal"]
    #return availableCargo, res










if __name__ == "__main__":
    assert(production(METALMINE, 20)["metal"] == 4066)
    assert(production(CRYSTALMINE, 18)["crystal"] == 2016)
    assert(production(DEUTERIUMSYNTHESIZER, 15, mtemp=48)["deuterium"] == 781)
    assert(production(SOLARPLANT, 19)["energy"] == 2324)
    assert(production(FUSIONREACTOR, 13)["energy"] == 735)
    assert(production(FUSIONREACTOR, 13)["deuterium"] == -449)
    assert(production(FUSIONREACTOR, 13, {ENERGYTECHNOLOGY:7})["energy"] == 1701)

    assert(to_mse(metal = 1000) == 1000)
    assert(to_mse(metal = 1000, crystal = 1000) == 3000)
    assert(to_mse(metal = 1000, crystal = 1000, deuterium = 1000) == 5000)

    for met in range(0,7):
        for kris in range(0,15):
            assert(buildingTopList({1:met,2:kris,3:0}, {122:6}, 27)[0]["bId"] ==
                buildingTopList({1:met,2:kris}, {122:6}, 27)[0]["bId"])

    assert(buildingTopList({1:18,2:15,3:12}, {122:6}, 27)[0]["bId"] == 2)
    assert(buildingTopList({1:18,2:16,3:12}, {122:6}, 27)[0]["bId"] == 3)
    assert(buildingTopList({1:18,2:16,3:13}, {122:6}, 27)[0]["bId"] == 1)
    assert(buildingTopList({1:19,2:16,3:13}, {122:6}, 27)[0]["bId"] == 3)
    assert(buildingTopList({1:19,2:17,3:13}, {122:6}, 27)[0]["bId"] == 3)
    assert(buildingTopList({1:19,2:17,3:14}, {122:6}, 27)[0]["bId"] == 1)
    assert(buildingTopList({1:20,2:17,3:14}, {122:6}, 27)[0]["bId"] == 3)
    assert(buildingTopList({1:20,2:17,3:15}, {122:6}, 27)[0]["bId"] == 1)
    assert(buildingTopList({1:21,2:17,3:15}, {122:6}, 27)[0]["bId"] == 2)

    assert(getCosts(METALMINE, 22) == {"metal":299273, "crystal":74818, "deuterium":0})
    assert(getCosts(CRYSTALMINE, 19) == {"metal":226673, "crystal":113336, "deuterium":0})
    assert(getCosts(DEUTERIUMSYNTHESIZER, 16) == {"metal":98526, "crystal":32842, "deuterium":0})
    assert(getCosts(SOLARPLANT, 23) == {"metal":561137, "crystal":224454, "deuterium":0})
    assert(getCosts(FUSIONREACTOR, 13) == {"metal":1041148, "crystal":416459, "deuterium":208229})


    assert(distance((1,4,3), (1,4,7)) == 1020)
    assert(distance((1,5,3), (1,7,3)) == 2890)
    assert(distance((1,5,2), (1,7,14)) == 2890)
    assert(distance((1,5,3), (3,7,5)) == 40000)
    assert(distance((1,105,8), (3,427,5)) == 40000)
    assert(distance((2,5,3), (3,227,5)) == 20000)
    assert(distance((1,10,3), (1,193,5)) == 20085)
    assert(distance((1,10,3), (1,403,5)) == 40035)

    assert(speed(LIGHTFIGHTER, {COMBUSTIONDRIVE:4}) == 17500)
    assert(speed(LIGHTFIGHTER, {}) == 0)
    assert(speed(SMALLCARGO, {COMBUSTIONDRIVE:15}) == 12500)
    assert(speed(SMALLCARGO, {COMBUSTIONDRIVE:15,IMPULSEDRIVE:7}) == 24000)
    assert(speed(SMALLCARGO, {COMBUSTIONDRIVE:15,IMPULSEDRIVE:5}) == 20000)
    assert(speed(SMALLCARGO, {COMBUSTIONDRIVE:15,IMPULSEDRIVE:4}) == 12500)
    assert(speed(LARGECARGO, {COMBUSTIONDRIVE:15,IMPULSEDRIVE:4}) == 18750)
    assert(duration(18750, 1020) == 2591)

    assert(getFilledCargo({"metal":300000,"crystal":250000,"deuterium":50000}, 600000) ==
            (25000, {'crystal': 250000, 'energy': 0, 'metal': 275000, 'deuterium': 50000}))

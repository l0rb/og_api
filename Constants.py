# coding=utf-8
from __future__ import division

buildings = [
    ('metalMine'                    ,1   ,(60      , 15      , 0))       ,
    ('crystalMine'                  ,2   ,(48      , 24      , 0))       ,
    ('deuteriumSynthesizer'         ,3   ,(225     , 75      , 0))       ,
    ('solarPlant'                   ,4   ,(75      , 30      , 0))       ,
    ('fusionReactor'                ,12  ,(900     , 360     , 180))     ,
    ('roboticsFactory'              ,14  ,(400     , 120     , 200))     ,
    ('naniteFactory'                ,15  ,(1000000 , 500000  , 100000))  ,
    ('shipyard'                     ,21  ,(400     , 200     , 100))     ,
    ('metalStorage'                 ,22  ,(2000    , 0       , 0))       ,
    ('crystalStorage'               ,23  ,(2000    , 1000    , 0))       ,
    ('deuteriumTank'                ,24  ,(2000    , 2000    , 0))       ,
    ('metalHiding'                  ,25  ,(2645    , 0       , 0))       ,
    ('crystalHiding'                ,26  ,(2645    , 1322    , 0))       ,
    ('deuteriumHiding'              ,27  ,(2645    , 2645    , 0))       ,
    ('researchLab'                  ,31  ,(200     , 400     , 200))     ,
    ('terraformer'                  ,33  ,(0       , 50000   , 100000))  ,
    ('allianceDepot'                ,34  ,(20000   , 40000   , 0))       ,
    ('lunarBase'                    ,41  ,(20000   , 40000   , 20000))   ,
    ('sensorPhalanx'                ,42  ,(20000   , 40000   , 20000))   ,
    ('jumpGate'                     ,43  ,(2000000 , 4000000 , 2000000)) ,
    ('missileSilo'                  ,44  ,(20000   , 20000   , 1000))    ,
    ]

research = [
    ('espionageTechnology'          ,106 ,(200     , 1000    , 200))     ,
    ('computerTechnology'           ,108 ,(0       , 400     , 600))     ,
    ('weaponsTechnology'            ,109 ,(800     , 200     , 0))       ,
    ('shieldingTechnology'          ,110 ,(200     , 600     , 0))       ,
    ('armourTechnology'             ,111 ,(1000    , 0       , 0))       ,
    ('energyTechnology'             ,113 ,(0       , 900     , 400))     ,
    ('hyperspaceTechnology'         ,114 ,(0       , 4000    , 2000))    ,
    ('combustionDrive'              ,115 ,(400     , 0       , 600))     ,
    ('impulseDrive'                 ,117 ,(2000    , 4000    , 600))     ,
    ('hyperspaceDrive'              ,118 ,(10000   , 20000   , 6000))    ,
    ('laserTechnology'              ,120 ,(200     , 100     , 0))       ,
    ('ionTechnology'                ,121 ,(1000    , 300     , 100))     ,
    ('plasmaTechnology'             ,122 ,(2000    , 4000    , 100))     ,
    ('intergalacticResearchNetwork' ,123 ,(240000  , 400000  , 160000))  ,
    ('astrophysics'                 ,124 ,(4000    , 8000    , 4000))    ,
    ('gravitonTechnology'           ,199 ,(0       , 0       , 0))       ,
]

shipyard = [
    ('smallCargo'                   ,202 ,(2000    , 2000    , 0)        , 5000    , 20)   ,
    ('largeCargo'                   ,203 ,(6000    , 6000    , 0)        , 25000   , 50)   ,
    ('lightFighter'                 ,204 ,(3000    , 1000    , 0)        , 50      , 20)   ,
    ('heavyFighter'                 ,205 ,(6000    , 4000    , 0)        , 100     , 75)   ,
    ('cruiser'                      ,206 ,(20000   , 7000    , 2000)     , 800     , 300)  ,
    ('battleShip'                   ,207 ,(45000   , 15000   , 0)        , 1500    , 500)  ,
    ('colonyShip'                   ,208 ,(10000   , 20000   , 10000)    , 7500    , 1000) ,
    ('recycler'                     ,209 ,(10000   , 6000    , 2000)     , 20000   , 300)  ,
    ('espionageProbe'               ,210 ,(0       , 1000    , 0)        , 1       , 1)    ,
    ('bomber'                       ,211 ,(500     , 50000   , 25000)    , 15000   , 1000) ,
    ('solarSatellite'               ,212 ,(0       , 2000    , 500)      , 0       , 0)    ,
    ('destroyer'                    ,213 ,(60000   , 50000   , 15000)    , 2000    , 1000) ,
    ('deathStar'                    ,214 ,(5000000 , 4000000 , 1000000)  , 1000000 , 1)    ,
    ('battlecruiser'                ,215 ,(30000   , 40000   , 15000)    , 750     , 250)  ,
    ('rocketLauncher'               ,401 ,(2000    , 0       , 0))       ,
    ('lightLaser'                   ,402 ,(1500    , 500     , 0))       ,
    ('heavyLaser'                   ,403 ,(6000    , 2000    , 0))       ,
    ('gaussCannon'                  ,404 ,(20000   , 15000   , 2000))    ,
    ('ionCannon'                    ,405 ,(2000    , 6000    , 0))       ,
    ('plasmaTurret'                 ,406 ,(50000   , 50000   , 30000))   ,
    ('smallShieldDome'              ,407 ,(10000   , 10000   , 0))       ,
    ('largeShieldDome'              ,408 ,(50000   , 50000   , 0))       ,
    ('antiBallisticMissile'         ,502 ,(8000    , 0       , 2000))    ,
    ('interplanetaryMissile'        ,503 ,(12500   , 2500    , 10000))   ,
]

buildLabels = {
        1  : u'Metallmine',
        2  : u'Kristallmine',
        3  : u'Deuterium-Synthetisierer',
        4  : u'Solarkraftwerk',
        12 : u'Fusionskraftwerk',
        14 : u'Roboterfabrik',
        15 : u'Nanitenfabrik',
        21 : u'Raumschiffswerft',
        22 : u'Metallspeicher',
        23 : u'Kristallspeicher',
        24 : u'Deuteriumtank',
        25 : u'Abgeschirmtes Metallversteck',
        26 : u'Unterirdisches Kristallversteck',
        27 : u'Meeresgrund Deuteriumversteck',
        31 : u'Forschungslabor',
        33 : u'Terraformer',
        34 : u'Allianzdepot',
        44 : u'Raketensilo',
        # research
        106: u'Spionagetechnik',
        108: u'Computertechnik',
        109: u'Waffentechnik',
        110: u'Schildtechnik',
        111: u'Raumschiffpanzerung',
        113: u'Energietechnik',
        114: u'Hyperraumtechnik',
        115: u'Verbrennungstriebwerk',
        117: u'Impulstriebwerk',
        118: u'Hyperraumantrieb',
        120: u'Lasertechnik',
        121: u'Ionentechnik',
        122: u'Plasmatechnik',
        123: u'Intergalaktisches Forschungsnetzwerk',
        124: u'Astrophysik',
        199: u'Gravitonforschung',
        # shipyard
        202: u'Kleiner Transporter',
        203: u'Großer Transporter',
        204: u'Leichter Jäger',
        205: u'Schwerer Jäger',
        206: u'Kreuzer',
        207: u'Schlachtschiff',
        208: u'Kolonieschiff',
        209: u'Recycler',
        210: u'Spionagesonde',
        211: u'Bomber',
        212: u'Solarsatellit',
        213: u'Zerstörer',
        214: u'Todesstern',
        215: u'Schlachtkreuzer',
        401: u'Raketenwerfer',
        402: u'Leichtes Lasergeschütz',
        403: u'Schweres Lasergeschütz',
        404: u'Gaußkanone',
        405: u'Ionengeschütz',
        406: u'Plasmawerfer',
        407: u'Kleine Schildkuppel',
        408: u'Große Schildkuppel',
        502: u'Abfangrakete',
        503: u'Interplanetarrakete',
    }
buildLabelsName = dict(zip(buildLabels.values(),buildLabels.keys()))

pageToBid = {
    'resources': [1,2,3,4,12,22,23,24,25,26,27,],
    'station': [14,15,21,31,33,34,44,],
    'research': [ 106, 108, 109, 110, 111, 113, 114, 115, 117, 118, 120, 121, 122, 123, 124, 199,],
    'shipyard': [202,203,204,205,206,207,208,209,210,211,212,213,214,215,],
    'defense': [ 401, 402, 403, 404, 405, 406, 407, 408, 502, 503,],
}

costs = {
    1  : (40      , 10      , 0      , 1.5),
    2  : (30      , 15      , 0      , 1.6),
    3  : (150     , 50      , 0      , 1.5),
    4  : (50      , 20      , 0      , 1.5),
    12 : (900     , 360     , 180    , 1.5),
    14 : (400     , 120     , 200    , 1.5),
    15 : (1000000 , 500000  , 100000 , 1.5),
    21 : (400     , 200     , 100    , 1.5),
    22 : (2000    , 0       , 0      , 1.5),
    23 : (2000    , 1000    , 0      , 1.5),
    24 : (2000    , 2000    , 0      , 1.5),
    25 : (2645    , 0       , 0      , 1.5),
    26 : (2645    , 1322    , 0      , 1.5),
    27 : (2645    , 2645    , 0      , 1.5),
    31 : (200     , 400     , 200    , 1.5),
    33 : (0       , 50000   , 100000 , 1.5),
    34 : (20000   , 40000   , 0      , 1.5),
    41 : (20000   , 40000   , 20000  , 1.5),
    42 : (20000   , 40000   , 20000  , 1.5),
    43 : (2000000 , 4000000 , 2000000, 1.5),
    44 : (20000   , 20000   , 1000   , 1.5),
    #research
    106: (200     , 1000    , 200    , 2.0),
    108: (0       , 400     , 600    , 2.0),
    109: (800     , 200     , 0      , 2.0),
    110: (200     , 600     , 0      , 2.0),
    111: (1000    , 0       , 0      , 2.0),
    113: (0       , 900     , 400    , 2.0),
    114: (0       , 4000    , 2000   , 2.0),
    115: (400     , 0       , 600    , 2.0),
    117: (2000    , 4000    , 600    , 2.0),
    118: (10000   , 20000   , 6000   , 2.0),
    120: (200     , 100     , 0      , 2.0),
    121: (1000    , 300     , 100    , 2.0),
    122: (2000    , 4000    , 100    , 2.0),
    123: (240000  , 400000  , 160000 , 2.0),
    124: (4000    , 8000    , 4000   , 2.0),
    199: (0       , 0       , 0      , 2.0),
    #fleet
    202: (2000    , 2000    , 0      ),
    203: (6000    , 6000    , 0      ),
    204: (3000    , 1000    , 0      ),
    205: (6000    , 4000    , 0      ),
    206: (20000   , 7000    , 2000   ),
    207: (45000   , 15000   , 0      ),
    208: (10000   , 20000   , 10000  ),
    209: (10000   , 6000    , 2000   ),
    210: (0       , 1000    , 0      ),
    211: (500     , 50000   , 25000  ),
    212: (0       , 2000    , 500    ),
    213: (60000   , 50000   , 15000  ),
    214: (5000000 , 4000000 , 1000000),
    215: (30000   , 40000   , 15000  ),
    #deff
    401: (2000    , 0       , 0)       ,
    402: (1500    , 500     , 0)       ,
    403: (6000    , 2000    , 0)       ,
    404: (20000   , 15000   , 2000)    ,
    405: (2000    , 6000    , 0)       ,
    406: (50000   , 50000   , 30000)   ,
    407: (10000   , 10000   , 0)       ,
    408: (50000   , 50000   , 0)       ,
    502: (8000    , 0       , 2000)    ,
    503: (12500   , 2500    , 10000)   ,
}
def isBuilding(bId):
    return 0<bId<100
def isResearch(bId):
    return 100<bId<200
def isFleet(bId):
    return 200<bId<300
def isDeff(bId):
    return 400<bId<600

plasma_metbonus= 0.01 # 1% per level
plasma_krisbonus= 0.0066 # 0.66% per level

from math import floor
def getCosts(bId, lvl):
    if isBuilding(bId) or isResearch(bId):
        c = costs[bId]
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


def to_mse(metal=0, crystal=0, deuterium=0, mse=[2.0,1.0,1.0]):
    m = metal
    k = crystal * (mse[0]/mse[1])
    d = deuterium * (mse[0]/mse[2])
    return round(m+k+d)

# TODO floor or ceil? (one display in ogame shows floor, 2 other show ceil)
def prod_met(level=1,plasma=0):
   return floor( (30*level*pow(1.1,level)) * (1+plasma_metbonus*plasma) ) + 30

def prod_met_gain(level=1,plasma=0):
   m1= prod_met(level-1,plasma)
   m2= prod_met(level,plasma)
   return m2-m1

# TODO floor or ceil? (one display in ogame shows floor, 2 other show ceil)
def prod_kris(level=1,plasma=0):
    return floor( (20*level*pow(1.1,level)) * (1+plasma_krisbonus*plasma) ) + 15

def prod_kris_gain(level=1,plasma=0):
   k1= prod_kris(level-1,plasma)
   k2= prod_kris(level,plasma)
   return k2-k1

# TODO floor or ceil? (one display in ogame shows floor, 2 other show ceil)
def prod_deut(level=1,mtemp=50):
   return floor( 10*level*pow(1.1,level)*(-0.004*mtemp+1.44) )

def prod_deut_gain(level=1,mtemp=0):
   d1= prod_deut(level-1,mtemp)
   d2= prod_deut(level,mtemp)
   return d2-d1

def atime(level, bId, plasma=0, mtemp=50, mse=[2.0,1.0,1.0]):
    """ Return time in seconds after which the mine with the given level
    has paid off itself. """
    c = getCosts(bId, level-1)
    if bId == 1:
        p = to_mse(metal=prod_met_gain(level,plasma), mse=mse)
    elif bId == 2:
        p = to_mse(crystal=prod_kris_gain(level,plasma), mse=mse)
    elif bId == 3:
        p = to_mse(deuterium=prod_deut_gain(level,mtemp), mse=mse)
    return round((to_mse(mse=mse, **c) / p )*3600 )

def which(mlevel, klevel, dlevel, plasma=0, mtemp=50, mse=[2.0,1.0,1.0]):
   t= {}
   t[1] = atime(mlevel+1,1,plasma, mse=mse)
   t[2] = atime(klevel+1,2,plasma, mse=mse)
   t[3] = atime(dlevel+1,3,mtemp=mtemp, mse=mse)
   return min(t, key=t.get)


def buildingTopList(buildings, research=0, temp=50, mse=[2.0,1.0,1.0]):
    t= []
    try:
        plasma = research[122]
    except:
        plasma = 0
    for bId in buildings:
        lvl = buildings[bId]
        t.append({'bId': bId, 'atime': atime(lvl+1,bId,plasma,temp, mse=mse)})
    t = sorted(t, key=lambda x: x["atime"])
    return t
















if __name__ == "__main__":
    assert(prod_kris(18) == 2016)
    assert(prod_met(20) == 4066)
    assert(prod_deut(15, 48) == 781)
    assert(to_mse(metal = 1000) == 1000)
    assert(to_mse(metal = 1000, crystal = 1000) == 3000)
    assert(to_mse(metal = 1000, crystal = 1000, deuterium = 1000) == 5000)
    assert(which(18,15,12,6,27) == 2)
    assert(which(18,16,12,6,27) == 3)
    assert(which(18,16,13,6,27) == 1)
    assert(which(19,16,13,6,27) == 2)
    assert(which(19,17,13,6,27) == 3)
    assert(which(19,17,14,6,27) == 1)
    assert(which(20,17,14,6,27) == 3)
    assert(which(20,17,15,6,27) == 1)
    assert(which(21,17,15,6,27) == 2)


    assert(buildingTopList({1:18,2:15,3:12}, {122:6}, 27)[0]["bId"] == 2)
    assert(buildingTopList({1:18,2:16,3:12}, {122:6}, 27)[0]["bId"] == 3)
    assert(buildingTopList({1:18,2:16,3:13}, {122:6}, 27)[0]["bId"] == 1)
    assert(buildingTopList({1:19,2:16,3:13}, {122:6}, 27)[0]["bId"] == 2)
    assert(buildingTopList({1:19,2:17,3:13}, {122:6}, 27)[0]["bId"] == 3)
    assert(buildingTopList({1:19,2:17,3:14}, {122:6}, 27)[0]["bId"] == 1)
    assert(buildingTopList({1:20,2:17,3:14}, {122:6}, 27)[0]["bId"] == 3)
    assert(buildingTopList({1:20,2:17,3:15}, {122:6}, 27)[0]["bId"] == 1)
    assert(buildingTopList({1:21,2:17,3:15}, {122:6}, 27)[0]["bId"] == 2)

    assert(getCosts(1, 22) == {"metal":299273, "crystal":74818, "deuterium":0})
    assert(getCosts(2, 19) == {"metal":226673, "crystal":113336, "deuterium":0})
    assert(getCosts(3, 16) == {"metal":98526, "crystal":32842, "deuterium":0})
    assert(getCosts(4, 23) == {"metal":561137, "crystal":224454, "deuterium":0})

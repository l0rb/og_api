import re
import os
import logging
import atexit
import cPickle as pickle

log = logging.getLogger('urlCache')


# contains a list of {'class'..,'check'..,'noDefault'} where class is the cacheclass and check is a function
# which decides if we use this specific cache. The decission is made based on configuration or wether a cache-folder/file
# already exists
# the last item in the list is the most important
# noDefault is a bool which defines if we should use this cache when no other caches match
cacheList = []


class BaseCache(object): # interface for all my caches
    def remove(self, section):
        pass
    def lookup(self, section):
        return None
    def pyLookup(self, section):
        return pickle.loads(self.lookup(section))
    def pyLookupDefault(self, section, default):
        r = self.lookup(section)
        if r is None:
            return default
        return pickle.loads(r)
    def lookupDefault(self, section, default):
        r = self.lookup(section)
        if r is None:
            return default
        return r
    def write(self, section, data):
        pass
    def pyWrite(self, section, data):
        data = pickle.dumps(data, 0)
        self.write(section, data)
    def allKeys(self):
        return [i for i in self.iterKeys()]
    def iterKeys(self):
        for i in self.iterKeyValues():
            yield i[0]
    def iterKeyValues(self):
        yield None
    def count(self):
        c = 0
        for i in self.iterKeys():
            c+=1
        return c
    def __repr__(self):
        return self.__class__.__name__+':'+self.key

import codecs
FILENAME_MAX_LENGTH = 100 # maxlength of filenames
# the filecache has also some additional interface methods
class FileCache(BaseCache):
    def __init__(self, dir, subdirs = []):
        ''' subdirs must be an array '''
        for i in xrange(0, len(subdirs)):
            dir = os.path.join(dir, self.create_filename(subdirs[i]))
        self.path = dir
        self.key = dir
        # create the path only if we write something there, thats why those variables getting set
        if os.path.isdir(self.path) is False:
            self.create_path = True
        else:
            self.create_path = False

    @staticmethod
    def create_filename(s):
        return re.sub('[^a-zA-Z0-9]','_',s)

    def get_path(self, section, create = False):
        if self.create_path:
            if create:
                try:
                    os.makedirs(self.path)
                except:
                    pass
            else:
                return None
        self.create_path = False
        return os.path.join(self.path, section)

    def iterKeys(self):
        for root, subFolders, files in os.walk(self.path):
            cleanRoot = root.replace(self.path+'/', '')
            for file in files:
                yield os.path.join(cleanRoot, file)
    def iterKeyValues(self):
        for root, subFolders, files in os.walk(self.path):
            cleanRoot = root.replace(self.path+'/', '')
            for file in files:
                f = os.path.join(cleanRoot, file)
                yield (f, codecs.open(self.path+"/"+f, 'r', 'utf-8').readlines())

    def remove(self, section):
        import shutil
        file = self.get_path(section)
        if file and os.path.isfile(file):
            os.remove(file)
        else:
            shutil.rmtree(file)

    def lookup(self, section):
        file = self.get_path(section)
        if file and os.path.isfile(file):
            log.debug('using cache [%s] path: %s' % (section, file))
            f = codecs.open(file, 'r', 'utf-8')
            return ''.join(f.readlines())
        return None

    def lookup_size(self, section):
        file = self.get_path(section)
        if file and os.path.isfile(file):
            return os.path.getsize(file)
        return None

    def read_stream(self, section):
        file = self.get_path(section)
        if file:
            return open(file, 'rb')
        return None

    def truncate(self, section, x):
        file = self.get_path(section)
        if file:
            a = open(file, 'r+b')
            a.truncate(x)

    def get_stream(self, section):
        file = self.get_path(section, True)
        return open(file, 'wb')

    def get_append_stream(self, section):
        file = self.get_path(section, True)
        return open(file, 'ab')

    def write(self, section, data):
        file = self.get_path(section, True)
        open(file, 'w').writelines(data.encode('utf-8'))


# below this i define several database caches - so they don't support append_stream and so on.. i won't store so big data inside

try:
    from kyotocabinet import DB, Visitor
except:
    pass
else:
    dbList = {}

    @atexit.register
    def close():
        for dir in dbList:
            db = dbList[dir]
            db.close()

    class KyotoCache(BaseCache):
        def __init__(self, dir, subdirs = []):
            if dir not in dbList:
                dbList[dir] = DB()
                dbList[dir].open(dir+".kch", DB.OWRITER | DB.OCREATE)
            self.db = dbList[dir]
            self.key = "/".join(subdirs)
        def lookup(self, section):
            ret = self.db.get(self.key+"/"+section)
            return ret
        def write(self, section, data):
            self.db.set(self.key+"/"+section, data)
        def remove(self, section):
            self.db.remove(self.key+"/"+section)
        def iterKeys(self):
            for i in self.db:
                yield i
        def iterKeyValues(self):
            cur = self.db.cursor()
            cur.jump()
            def printproc(key, value):
                return Visitor.NOP
            while True:
                cur.step()
                if cur.get_key() == None:
                    break
                yield (cur.get_key(), cur.get_value())
        def count(self):
            return self.db.count()

    def isKyotoCache(namespace):
        return os.path.exists(namespace+".kch")
    cacheList.append({'class':KyotoCache, 'check':isKyotoCache})

    class KyotoCacheComp(KyotoCache): # with compression
        def __init__(self, dir, subdirs = []):
            dir+="_zlib"
            if dir not in dbList:
                dbList[dir] = DB()
                dbList[dir].open(dir+".kch#ops=c#log="+dir+".log#logkinds=debu#zcomp=zlib", DB.OWRITER | DB.OCREATE)
            self.db = dbList[dir]
            self.key = "/".join(subdirs)

    def isKyotoCacheComp(namespace):
        return os.path.exists(namespace+"_zlib.kch")
    cacheList.append({'class':KyotoCacheComp, 'check':isKyotoCacheComp})

try:
    import lib.leveldb as leveldb
except:
    pass
else:
    dbList = {}
    class LevelCache(BaseCache):
        def __init__(self, dir, subdirs = []):
            dir+=".ldb"
            if dir not in dbList:
                dbList[dir] = leveldb.LevelDB(dir)
            self.db = dbList[dir]
            self.key = "/".join(subdirs)

        def lookup(self, section):
            ret = self.db.Get(self.key+"/"+section)
            return ret
        def write(self, section, data):
            self.db.Put(self.key+"/"+section, data)
        def remove(self, section):
            self.db.Delete(self.key+"/"+section)

        def iterKeys(self):
            for i in self.db.RangeIter(include_value=False):
                yield i
        def iterKeyValues(self):
            for i in self.db.RangeIter():
                yield i

    def isLevelCache(namespace):
        return os.path.isdir(namespace+".ldb")
    cacheList.append({'class':LevelCache, 'check':isLevelCache})



try:
    from hypertable.thriftclient import ThriftClient
    #from hyperthrift.gen.ttypes import *
except:
    pass
else:

    class HypertableCache(BaseCache):
        clientCache = None
        def __init__(self, dir, subdirs = []):
            if HypertableCache.clientCache == None:
                HypertableCache.clientCache = ThriftClient("localhost", 38080)
            self.client = HypertableCache.clientCache
            self.key = "/".join(subdirs)
            if not self.client.exists_namespace("flashget_"+dir):
                self.client.create_namespace("flashget_"+dir)
            self.namespace = self.client.open_namespace("flashget_"+dir)
            if not self.client.exists_table(self.namespace, "cache"):
                sections = ['data', 'redirect']
                self.client.hql_query(self.namespace, 'CREATE TABLE cache('+','.join(sections)+')');

        def lookup(self, section):
            key = self.key.replace('"', '\\"')
            res = self.client.hql_query(self.namespace, 'select '+section+' FROM cache WHERE row="'+key+'" REVS 1 NO_ESCAPE')
            if res.cells == []:
                return None
            return res.cells[0].value

        def write(self, section, data):
            key = self.key.replace('"', '\\"')
            if key == '':
                return None
            self.client.hql_query(self.namespace, 'INSERT INTO cache VALUES ("%s", "%s", \'%s\')' % (key, section, data.replace("\\", "\\\\").replace("'", "\\'").replace("\x00", "")));

        def remove(self, section):
            key = self.key.replace('"', '\\"')
            if section is None:
                section = '*'
            self.client.hql_query(self.namespace, 'DELETE %s FROM cache WHERE ROW="%s"' % (section, key))

        def iterKeyValues(self):
            res = self.client.hql_exec(self.namespace, 'select * FROM cache REVS 1', 0, 1)
            scanner = res.scanner
            while True:
                cells = self.client.next_row_as_arrays(scanner)
                if not len(cells): break
                key = cells[0][0]
                section = cells[0][1]
                data = cells[0][3]
                #timestamp = cells[0][4]
                yield (key+"/"+section, data)
            self.client.close_scanner(scanner)


# a factory, which will create the class based on cachelist
class Cache(object):
    _dirToCache = {} # internal mapping from dir to cache
    def __new__(cls, dir, subdirs=[]):
        cls = None
        if dir in Cache._dirToCache:
            cls = Cache._dirToCache[dir]
        if not cls:
            for i in cacheList[::-1]:
                if i['check'](dir):
                    cls = i['class']
                    break
            else:
                log.debug("no cache exists for %s" % dir)
                # no cache found yet chose a default cache
                for i in cacheList[::-1]:
                    if 'noDefault' in i and i['noDefault']:
                        continue
                    cls = i['class']
            if cls == None:
                raise Exception("No Cache is available")
        log.debug("using cache %s" % cls.__name__)
        Cache._dirToCache[dir] = cls
        return cls(dir, subdirs)

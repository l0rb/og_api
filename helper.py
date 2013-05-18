# vim: set fileencoding=utf-8 :

def textextract(data, startstr, endstr, startpos = 0):
    ''' extracts a text from data, which is between startstr and endstr
        if startstr is '' it will extract from the beginning of data
        if endstr   is '' it will extract until the end of data
        the optional parameter startpos will indicate the startposition from where startstr will be searched
        and if startpos is something else than 0 it will return a tuple of the extracted string and the endposition of this string '''
    if startstr == '':
        pos1 = startpos
    else:
        pos1 = data.find(startstr, startpos)
        if pos1 < 0:
            return None
        pos1 += len(startstr)

    if endstr == '':
        return data[pos1:]
    pos2 = data.find(endstr, pos1)
    if pos2 < 0:
        return None
    if startpos != 0:
        return (data[pos1:pos2], pos2)
    return data[pos1:pos2]

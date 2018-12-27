from logger import error, info
from enum import Enum

def parseUrl(url, absUrl):
    assert absUrl.startswith('http://') or absUrl.startswith('https://'), absUrl
    assert url.startswith('http://') or url.startswith('https://') or url.startswith('/'), url
    rooturl = toFileName(absUrl, '', False) 
    assert rooturl 
    
    if url.startswith('/'):
        if absUrl.endswith('/'):
            src = absUrl[:-1] + url
        else:
            src = absUrl + url
    else:
        src = url

    src = removeAnchor(src)
    dst = toFileName(removeAnchor(url), rooturl, False)
    # url, filename
    return src, dst

def removeAnchor(url):
    idx = url.rfind('#')
    if idx < 0:
        return url
    else:
        return url[:idx]

def toFileName(url, absUrl = '', addIndex = True):
    if absUrl != '':
        rooturl = toFileName(absUrl, '', False)
        if not rooturl.endswith('/'):
            rooturl = rooturl + '/'

    if addIndex:
        if url.count('/') == 2:
            dst = url + '/index.html'
        elif url.endswith('/'):
            dst = url + 'index.html'
        else:
            dst = url
    else:
        dst = url

    if dst.startswith('http://'):
        dst = dst[7:]
    elif dst.startswith('https://'):
        dst = dst[8:]
    elif dst.startswith('/'):
        dst = dst[1:]
    
    return dst

class RespType(Enum):
    PAGE = 1
    URL = 2

async def requestUrl(url):
    import aiohttp
    async with aiohttp.ClientSession(raise_for_status=True) as client_session:
        async with client_session.get(url, raise_for_status=False) as resp:
            if isHTMLfile(resp.headers):
                await client_session.close()
                text = await resp.text()
                return RespType.PAGE, text
            else:
                return RespType.URL, resp


def isHTMLfile(headers):
    return "content-type" in headers and (headers["content-type"] == "text/html" or headers["content-type"].startswith("text/html;"))


def isValidHref(ref):
    if removeAnchor(ref) == '': 
        return False 
    elif ref.startswith('/'):
        return True
    elif ref.startswith('http://'):
        return True
    elif ref.startswith('https://'):
        return True
    else:
        return False

def makeDir(path):
    import os
    import pathlib
    assert path.rfind('/') > 0, path
    dir = path[:path.rfind('/')]
    if os.path.exists(dir):
        if os.path.isfile(dir):
            handleFileExists(dir)
        elif not os.path.isdir(dir):
            raise Exception('is special file')
    else:
        pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

def handleFileExists(path):
    import os
    import magic
    import aiofile
    assert os.path.isfile(path)
    if magic.from_file(path) != 'text/html':
        raise Exception('path is not html file')
    tname = '.' + path[path.rfind('/')+1:] + '.tmp'
    os.rename(path, tname)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    os.rename(tname, path + '/index.html')

def handleDirExists(path):
    return path + '/index.html'

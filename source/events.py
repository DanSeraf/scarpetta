from collections import namedtuple
import aiohttp
import json
from queue import PriorityQueue

from config import globalConfig
from parse import *
from logger import error, info

class EventQueue(PriorityQueue):
    def get(self, *args, **kwargs):
        assert self.empty, 'queue should not be empty'
        return super().get(*args, **kwargs)

    def put(self, event):
        super().put((-event.tp, event))
    
def uuid(s):
    from uuid import uuid3, NAMESPACE_DNS
    return uuid3(NAMESPACE_DNS, s)

Base = namedtuple('Base', ['uuid', 'parent'])

# methods for insertion in priority queue
class Event:
    def __lt__(self, other):
        return False

class RequestEvent(Event):
    def __init__(self, url = None, parent = None):
        assert url is not None
        self.base = Base(uuid(url), None if parent is None else parent)
        self.url = url
        self.tp = 1
        self.over = False
        info('request event '+str(self.base.uuid)+': '+url)

    async def resolve(self):
        resp_type, response = await requestUrl(self.url)
        if resp_type is RespType.PAGE:
            return [HTMLEvent(content = response, url = self.url, parent = self.base.uuid)]
        elif resp_type is RespType.URL:
            return [ToFileEvent(content = (resp_type, response), url = self.url, parent = self.base.uuid)]
        else:
            assert False
    
    def toJsonString(self):
        d = {}
        d['url'] = self.url
        return json.dumps(d)

class HTMLEvent(Event):
    def __init__(self, content = None, url = None, parent = None):
        assert url is not None and content is not None and parent is not None
        self.base = Base(uuid(url + content), parent)
        self.tp = 2
        self.content = content
        self.url = url
        info('html event '+str(self.base.uuid)+': '+url)

    async def resolve(self):
        from bs4 import BeautifulSoup as Soup
        soup = Soup(self.content, 'html.parser')
        events = []
        for link in soup.find_all('a'):
            if not 'href' in link.attrs:
                continue
            ref = link['href']
            if isValidHref(ref):
                url, fname = parseUrl(ref, self.url)
                events.append(RequestEvent(url, parent = self.base.uuid))
                link['href'] = fname
        events.append(ToFileEvent(content = (RespType.PAGE, str(soup)), url = self.url, parent = self.base.uuid))
        return events

    def toJsonString(self):
        d = {}
        d['url'] = self.url
        return json.dumps(d)

class ToFileEvent(Event):
    def __init__(self, content = None, url = None, parent = None):
        assert url is not None and content is not None and parent is not None
        assert type(content) is tuple and type(content[0]) is RespType
        self.content = content
        self.tp = 3
        self.fname = globalConfig()['project_dir'] + toFileName(url)
        self.base = Base(uuid(self.fname), parent)
        self.url = url
        info('to file event '+str(self.base.uuid)+': '+self.fname)

    async def resolve(self):
        from os.path import exists, isfile, isdir
        from aiofile import AIOFile
        fname = self.fname
        if exists(fname) and not isfile(fname):
            if isdir(self.fname):
                fname = handleDirExists(fname)
            else:
                raise Exception('special file') 
        else:
            makeDir(fname)
        
        resp_type, response = self.content
        if resp_type == RespType.PAGE: 
            async with AIOFile(fname, 'w') as fb:
                await fb.write(response)
        else:
            async with AIOFile(fname, 'wb') as fb:
                async with aiohttp.ClientSession() as client_session:
                    async with client_session.get(self.url) as resp:
                        async for data in resp.content.iter_any():
                            await fb.write(data)

        return []
 
    def toJsonString(self):
        d = {}
        d['url'] = self.url
        d['fname'] = self.fname
        return json.dumps(d)

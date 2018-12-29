import sqlite3

from logger import debug
from enum import Enum
from events import *

class DataBase:
    def __init__(self, path):
        import os 
        if os.path.exists(path):
            return
        else:
            self.conn = sqlite3.connect(path)
            c = self.conn.cursor()

            c.execute('''CREATE TABLE Event
                         (type integer, over integer, resolved integer, uuid text not null unique, parent text, data text not null)''')
            
            self.conn.commit()

    def _doQuery(self, q):
        debug(q)
        c = self.conn.cursor()
        c.execute(q)
        self.conn.commit()

    def insert(self, event):
        over = event.over if type(event) is RequestEvent else "NULL"
        resolved = 0
        parent = "NULL" if event.base.parent is None else "'" + str(event.base.parent) + "'"
        query = '''INSERT INTO Event (type, over, resolved, uuid, parent, data) VALUES (%s, %s, %s,'%s', %s, '%s')''' % (event.tp, over, resolved, str(event.base.uuid), parent, event.toJsonString())  
        self._doQuery(query)
        self.updateParent(event.base.uuid)

    def setResolved(self, event):
        query = '''UPDATE Event SET resolved = 1 WHERE uuid = '%s' ''' % event.base.uuid
        self._doQuery(query)
    
    def isResolved(self, event):
        query = '''SELECT EXISTS(SELECT 1 FROM Event WHERE uuid = '%s' and resolved = 1)''' % event.base.uuid
        debug('RESOLVED_EVENT: ' + query)
        c = self.conn.cursor()
        c.execute(query)
        resp = bool(c.fetchone()[0])
        debug(resp)
        return resp

    def updateParent(self, p_uuid):
        if p_uuid == '':
            return

        query = '''UPDATE Event SET over = 1 WHERE uuid = '%s' ''' % p_uuid
        self._doQuery(query)

    def test(self, event):
        query = '''SELECT EXISTS(SELECT 1 FROM Event WHERE uuid = '%s')''' % event.base.uuid
        c = self.conn.cursor()
        c.execute(query)
        resp = bool(c.fetchone()[0])
        return resp

from events import *
from config import parseCLI, globalConfig
import os

async def main(db):
    from logger import error, info
    import aiohttp

    queue = EventQueue()
    event = RequestEvent(globalConfig()['url'])
    queue.put(event)

    while(not queue.empty()):
        _, ev = queue.get()
        if db.isResolved(ev):
            continue
        else:
            db.insert(ev)

        try:
            next_evs = await ev.resolve()
        except aiohttp.ClientError as e:
            error(e)
         
        db.setResolved(ev)
        for e in next_evs:
            if not db.test(e):
                queue.put(e)

if __name__ == '__main__':
    import asyncio
    from sys import argv
    from database import DataBase
    parseCLI(argv[1:])
    db = DataBase(globalConfig()['project_dir'] + 'scarpetta.db')
    asyncio.get_event_loop().run_until_complete(main(db))



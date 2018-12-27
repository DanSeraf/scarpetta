from events import *
from config import parseCLI, globalConfig
import os

DEBUG = False

async def main():
    from logger import error, info
    events = [RequestEvent(globalConfig()['url'])]
    while(len(events) > 0):
        tmp = []
        for i, ev in enumerate(events):
            events.pop(i)
            if DEBUG:
                res = await ev.resolve()
                tmp.extend(res)
            else:
                try:
                    res = await ev.resolve()
                    tmp.extend(res)
                except Exception as e:
                    error(e)
        events.extend(tmp)

if __name__ == '__main__':
    import asyncio
    import uvloop
    import sys
    import logging
    logging.basicConfig(level=logging.DEBUG)
    parseCLI(sys.argv[1:])
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()



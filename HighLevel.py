import AutoSave
import AutoSaveAll
import logging
import Follower
import asyncio
from _thread import start_new_thread
from time import sleep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########## task for follower
async def StartFollower():
    with open('LoginFollow.txt', 'rt') as f:
        ownername, username, password = f.read().strip().splitlines()
        Follower.FollowerClient(name=username, password=password, ownername= ownername).start()
    
########## task for my replays
async def StartReplay():
    with open('Login.txt', 'rt') as f:
        username, password = f.read().strip().splitlines()
    AutoSave.ReplayClient(name=username, password=password).start()

########## task for my replays
async def StartAutosaveAll():
    with open('Login.txt', 'rt') as f:
        username, password = f.read().strip().splitlines()
    AutoSaveAll.ReplayClient(name=username, password=password).start(autologin=False)
 
with open('Login.txt', 'rt') as f:
    username, password = f.read().strip().splitlines()   
    AutoSaveAll.ReplayClient(name=username, password=password).start(autologin=False)

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(StartAutosaveAll())
    asyncio.ensure_future(StartFollower())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()



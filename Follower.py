
# -*- coding: utf-8 -*-
"""
An example client that joins any rooms that its
specified owner does.
"""
import showdown
import logging
import warnings
import asyncio
from showdown.utils import strip_prefix
from pprint import pprint
import numpy as np

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# with open('LoginFollow.txt', 'rt') as f:
#         ownername, username, password = f.read().strip().splitlines()
        
        
class FollowerClient(showdown.Client):
    def __init__(self, ownername, **kwargs):
        showdown.Client.__init__(self, **kwargs)
        self.owner = showdown.User(ownername, client=self)

    ######### join room
    async def on_query_response(self, response_type, data):
        # logger.info(data)
        if response_type == 'userdetails':
            user_rooms = set(map(strip_prefix, data.get('rooms') or {}))
            bot_rooms = set(self.rooms)
            for room in user_rooms - bot_rooms:
                await self.join(room)
            for room in bot_rooms - user_rooms:
                await self.leave(room)

    @showdown.Client.on_interval(interval=3)
    async def get_owner_details(self): 
        await self.owner.request_user_details()


    async def on_room_init(self, room_obj):
        if isinstance(room_obj, showdown.room.Battle):
            await asyncio.sleep(3)
            await room_obj.say('Good luck ' + self.owner.id)
            
    ######### mimick on pm
    async def on_private_message(self, pm):
        with open('ConversationLog.txt', 'a+') as f:
                f.write("r\n" + pm.author.id + ':' + pm.content)    
        if pm.recipient == self and 'error' not in pm.content:
            await asyncio.sleep(np.random.chisquare(2.8))
            

            if 'copy' in pm.content:
                await pm.reply('I am not')
                with open('ConversationLog.txt', 'a+') as f:
                    f.write("r\n" + pm.recipient.id + ' : I am not')  
            else:
                await pm.reply(pm.content)
                with open('ConversationLog.txt', 'a+') as f:
                    f.write("r\n" + pm.recipient.id + ' : ' + pm.content)  

# FollowerClient(name=username, password=password, ownername= ownername).start()
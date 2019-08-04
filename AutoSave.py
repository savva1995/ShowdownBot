
# -*- coding: utf-8 -*-
"""
An example client that challenges a player to 
a random battle when PM'd, or accepts any
random battle challenge.
"""
import showdown
import logging
import asyncio
from pprint import pprint

class ReplayClient(showdown.Client):
    roomCurrent = None
    async def on_query_response(self, response_type, data):
        if response_type == 'roomlist':
            for battle_id in set(data['rooms']):
                p1 = data['rooms'].get(battle_id).get('p1')
                p2 = data['rooms'].get(battle_id).get('p2')
                if (p2 == self.Id or p1 == self.id) and battle_id not in self.rooms:
                    await self.join(battle_id)

    @showdown.Client.on_interval(interval=3)
    async def check_ou(self): 
        await self.query_battles(battle_format='gen2ou', lifespan=3)
    
    async def on_receive(self, room_id, inp_type, params):
        if inp_type == 'win':
            await self.save_replay(room_id)
            

    async def on_room_init(self, room_obj):
        if isinstance(room_obj, showdown.room.Battle):
            await asyncio.sleep(3)
            await room_obj.say('Have a wonderful day.')
            self.roomCurrent = room_obj
            # await room_obj.forfeit()
            # await room_obj.leave()

    async def on_room_deinit(self, room_obj):
        if isinstance(room_obj, showdown.room.Battle):
            await asyncio.sleep(3)
            await self.save_replay(room_obj.id)



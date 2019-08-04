import showdown
import logging

class ReplayClient(showdown.Client):
    async def on_query_response(self, response_type, data):
        if response_type == 'roomlist':
            for battle_id in set(data['rooms']) - set(self.rooms) :
                if len(self.rooms) < 100 or 'gen2ou' in battle_id: #### only join 100 rooms at a time
                    await self.join(battle_id)

    async def on_receive(self, room_id, inp_type, params):
        if inp_type == 'win':
            with open('Battle Logs/' + room_id + '.txt', 'wt') as f:
                f.write('\n'.join(self.rooms[room_id].logs))
            await self.save_replay(room_id)
            
    @showdown.Client.on_interval(interval=3)
    async def check_ou(self): 
        await self.query_battles(lifespan=3, min_elo=1700) # battle_format='gen2ou', 
        await self.query_battles(battle_format='gen2ou', lifespan=3) # it seems to only return 100 so do this to make sure we get gen 2


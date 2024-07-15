import asyncio

from .main import BasesClass
from ..generator import style_one
from ..tools.git import ImageCache
from ..model.card import ZZZeroCard
from ..tools.settings import save_card

class Card(BasesClass):
    
    
    async def get_data(self, id: int) -> list:
        await self.get_list_agent()
        
        data = [] #strategy_wiki
        self.list_id = []
        self.character_name = []
        self.character_id = []
        self.wiki = self.data_list.data.avatar_wiki
        for key in self.data_list.data.avatar_list:
            self.character_name.append(key.name_mi18n)
            self.character_id.append(key.id)
            
        for key in self.data_list.data.avatar_list:
            if id != 0 and int(id) == int(key.id):
                await self.get_agent(id=id)
                data.append(self.data.data.avatar_list[0])
                break
            elif id == 0:
                await self.get_agent(id=key.id)
                
                data.append(self.data.data.avatar_list[0])
                
        for key in self.data_list.data.avatar_list:
            self.list_id.append(key.full_name_mi18n)

        return data
    
    async def create(self, id: int = 0, style: int = 1):
        
        await ImageCache.set_assets_download(self.asset_save)
        
        if style != 1:
            style = 1
            
        data = await self.get_data(id)

        card = []
        for key in data:
            
            card.append(style_one.StyleOne(self).start(key, self.list_id, wiki = self.wiki))
        
        card = await asyncio.gather(*card)
        
        if self.save:
            for key in card:
                await save_card(self.uid, key["card"], key["id"])

        result = {
            "settings": {
                "uid": self.uid,
                "lang": self.lang,
                "save": self.save,
                "style": style
            },
            "card": card,
            "character_name": self.character_name,
            "character_id":  self.character_id
        }
        
        return ZZZeroCard(**result)
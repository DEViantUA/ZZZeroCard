from pydantic import BaseModel, Field
from PIL import Image
from typing import List ,Optional,Final, Union





class Setting(BaseModel):
    uid: int
    lang: Optional[str]
    save: bool
    style: int

class Card(BaseModel):
    id: int
    name: Optional[str]
    rarity: str
    profession: int
    card: Union[Image.Image,list]
    icon: str
    size: Optional[tuple]
    color: Optional[tuple]

    class Config:
        arbitrary_types_allowed = True

class ZZZeroCard(BaseModel):
    settings: Setting
    card: Union[List[Card], Image.Image]
    character_id: list
    character_name: list
    
    class Config:
        arbitrary_types_allowed = True
    
    def __str__(self):
        return f"card={self.card} character_name = {self.character_name} character_id={self.character_id}"
    
    def get_charter(self, setting = False, name = False):
        if setting:
            card_ids = [str(card.id) for card in self.card]

            if name:
                return {name: id for id, name in zip(self.character_id, self.character_name) if id in card_ids}
            return {id: name for id, name in zip(self.character_id, self.character_name) if id in card_ids}
        
        if name:
            return {name: id for id, name in zip(self.character_id, self.character_name)}
        
        return {id: name for id, name in zip(self.character_id, self.character_name)}
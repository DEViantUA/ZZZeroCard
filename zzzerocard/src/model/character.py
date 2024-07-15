from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Union

from pydantic import BaseModel, Field


class Property(BaseModel):
    property_name: str
    property_id: int
    base: Optional[Union[str, int]] = Field("")
    add: Optional[Union[str, int]] = Field("")
    final: Optional[Union[str, int]] = Field("")

class Item(BaseModel):
    title: str
    text: str

class Skill(BaseModel):
    level: int
    skill_type: int
    items: List[Item]

class Rank(BaseModel):
    id: int
    name: str
    desc: str
    pos: int
    is_unlocked: bool
    
class MainProperty(BaseModel):
    property_name: str
    property_id: int
    base: str
    add: Optional[Union[str, int]] = Field("")
    final: Optional[Union[str, int]] = Field("")


class EquipSuit(BaseModel):
    suit_id: int
    name: str
    own: int
    desc1: str
    desc2: str


class EquipItem(BaseModel):
    id: int
    level: int
    name: str
    icon: str
    rarity: str
    properties: List[Property]
    main_properties: List[MainProperty]
    equip_suit: EquipSuit
    equipment_type: int

class Weapon(BaseModel):
    id: int
    level: int
    name: str
    star: int
    icon: str
    rarity: str
    properties: List[Property]
    main_properties: List[MainProperty]
    talent_title: str
    talent_content: str
    profession: int

class AvatarListItem(BaseModel):
    id: int
    level: int
    name_mi18n: str
    full_name_mi18n: str
    element_type: int
    camp_name_mi18n: str
    avatar_profession: int
    rarity: str
    group_icon_path: str
    hollow_icon_path: str
    equip: List[EquipItem]
    weapon: Optional[Weapon]
    properties: List[Property]
    skills: List[Skill]
    rank: int
    ranks: List[Rank]

class Data(BaseModel):
    avatar_list: List[AvatarListItem]
    equip_wiki: Mapping[int, str]
    weapon_wiki: Mapping[int, str]
    avatar_wiki: Mapping[int, str]
    strategy_wiki: Mapping[int, str]


class CharacterInfo(BaseModel):
    retcode: int
    message: str
    data: Data

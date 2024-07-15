from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Component(BaseModel):
    component_id: str
    layout: str
    data: str
    style: str


class Module(BaseModel):
    name: str
    is_poped: bool
    components: List[Component]
    id: str
    is_customize_name: bool
    is_abstract: bool
    is_show_switch: bool
    switch: bool
    desc: str
    repeated: bool
    is_submodule: bool
    origin_module_id: str
    without_border: bool
    can_delete: bool
    is_hidden: bool


class ValueType(BaseModel):
    id: str
    value: str
    mi18n_key: str
    icon: str
    enum_string: str


class Key(BaseModel):
    key: str
    text: str
    values: List
    mi18n_key: str
    is_multi_select: bool
    id: str
    is_hidden: bool
    updated_at: str


class AgentAttackType(BaseModel):
    values: List[str]
    value_types: List[ValueType]
    key: Optional[Key]


class ValueType1(BaseModel):
    id: str
    value: str
    mi18n_key: str
    icon: str
    enum_string: str

class AgentFaction(BaseModel):
    values: List[str]
    value_types: List[ValueType1]
    key: Optional[Key]

class ValueType2(BaseModel):
    id: str
    value: str
    mi18n_key: str
    icon: str
    enum_string: str

class AgentRarity(BaseModel):
    values: List[str]
    value_types: List[ValueType2]
    key: Optional[Key]


class ValueType3(BaseModel):
    id: str
    value: str
    mi18n_key: str
    icon: str
    enum_string: str


class AgentSpecialties(BaseModel):
    values: List[str]
    value_types: List[ValueType3]
    key: Optional[Key]


class ValueType4(BaseModel):
    id: str
    value: str
    mi18n_key: str
    icon: str
    enum_string: str

class AgentStats(BaseModel):
    values: List[str]
    value_types: List[ValueType4]
    key: Optional[Key]


class FilterValues(BaseModel):
    agent_attack_type: Optional[AgentAttackType]
    agent_faction: Optional[AgentFaction]
    agent_rarity: Optional[AgentRarity]
    agent_specialties: Optional[AgentSpecialties]
    agent_stats: Optional[AgentStats]


class PostExt(BaseModel):
    post_id: str
    post_user_name: str
    post_time: str
    post_avatar_url: str
    url: str


class Ext(BaseModel):
    fe_ext: str
    post_ext: PostExt
    server_ext: str
    personalized_color: str
    scrolling_text: str


class Page(BaseModel):
    id: str
    name: str
    desc: str
    icon_url: str
    header_img_url: str
    modules: List[Module]
    filter_values: FilterValues
    menu_id: str
    menu_name: str
    version: str
    langs: List
    template_layout: Any
    edit_lock_status: str
    correct_lock_status: str
    menus: List
    template_id: str
    ext: Ext
    alias_name: str
    lang: str
    beta: bool
    page_type: str
    menu_style: str


class Data(BaseModel):
    page: Page

class WikiInfo(BaseModel):
    retcode: int
    message: str
    data: Data

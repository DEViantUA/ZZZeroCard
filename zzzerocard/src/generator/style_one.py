import asyncio
from ..components.main import BasesClass
from ..model.character import AvatarListItem
from ..tools import git
from ..tools.settings import (icon_properties_relict,
                            color_rang,
                            icon_properties_character,
                            element_icon,
                            split_long_words
                        )

from ..tools.pill import (get_download_img,
                        apply_opacity,
                        hex_to_rgba,
                        recolor_image,
                        get_dark_pixel_color,
                        create_image_with_text_v2,
                        get_font,
                        get_text_size_frame,
                        get_light_pixel_color,
                        light_level,
                    )
from PIL import ImageChops, Image, ImageDraw

_of = git.ImageCache()
_of.set_mapping(1)


async def get_stars(rarity:int) -> Image.Image:
    frame = {
        5: lambda: _of.stars_five,
        4: lambda: _of.stars_four,
        3: lambda: _of.stars_three,
        2: lambda: _of.stars_two,
        1: lambda: _of.stars_one
    }
    frame_func = frame.get(rarity, lambda: _of.stars_one)
    return await frame_func()

async def get_const(rank:int) -> Image.Image:
    frame = {
        6: lambda: _of.const_6,
        5: lambda: _of.const_5,
        4: lambda: _of.const_4,
        3: lambda: _of.const_3,
        2: lambda: _of.const_2,
        1: lambda: _of.const_1,
        0: lambda: _of.const_0
    }
    frame_func = frame.get(rank, lambda: _of.const_0)
    return await frame_func()

async def get_rank_icon(rank:str) -> Image.Image:
    frame = {
        "S": lambda: _of.rank_s,
        "A": lambda: _of.rank_a,
        "B": lambda: _of.rank_b
    }
    frame_func = frame.get(rank, lambda: _of.rank_b)
    return await frame_func()

def adjust_list(ids: list, cID: int) -> list:
    if len(ids) < 12:
        while len(ids) < 12:
            ids += ids[:12 - len(ids)]
    else:
        try:
            cID_index = ids.index(cID)
        except ValueError:
            raise ValueError("cID not found in the list")
        
        if cID_index + 4 > len(ids):
            ids = ids[cID_index:] + ids[:12 - len(ids[cID_index:])]
        else:
            ids = ids[cID_index:cID_index + 4] + ids[:12 - 4]

    return ids


class StyleOne:
    
    def __init__(self, BaseSelf: BasesClass) -> None:
        self.base_self = BaseSelf
    
    async def create_character_list(self) -> Image.Image:
        items_id = adjust_list(self.items_id, self.avatar.full_name_mi18n)

        background = await _of.character_list
        background = background.copy()
        
        items = {}
        
        position = [
            (1,2),
            (109,2),
            (215,2),
            
            (43,144),
            (151,144),
            (257,144),
            
            (87,288),
            (195,288),
            (301,288),
            
            (128,430),
            (236,430),
            (342,430),
        ]
        
        i = 0
        for key in items_id:
            if not key in items:
                                    
                link = next(filter(lambda x: x["name"] == key, self.page_id.get("data").get("list")), None)
                if link is None:
                    continue
                         
                items[key] = link["icon_url"]
                
            icon = await get_download_img(items[key], size=(143,139))
            if self.avatar.full_name_mi18n != key:
                icon = icon.convert("LA").convert("RGBA")
                
            background.alpha_composite(icon, position[i])
            
            
            i += 1    
        
        return background
        
    async def create_background(self, wiki) -> Image.Image:
        
        background = await _of.background
        zzz_text = await _of.zzz_text
        zzz_frame = await _of.zzz_text_frame
        splash_one = await _of.splash_one
        splash_two = await _of.splash_two
        overlay_splash = await _of.overlay_splash
        
        wave_down = await _of.wave_down
        wave_line = await _of.wave_line
        wave_up = await _of.wave_up
        texture_line = await _of.texture_line
        pixel = await _of.pixel
        
        background = background.copy().convert("RGBA")

        icon = await get_download_img(wiki.data.page.header_img_url, size=(1481,1481))
        icon = await apply_opacity(icon.convert("LA").convert("RGBA"), opacity= 0.5)
        background.alpha_composite(icon, (-80,-199))
        
        character_list = await self.create_character_list()
        background.alpha_composite(character_list.resize((718,843)), (-80,-16))

        zzz_text = zzz_text.copy()
        zzz_frame = await recolor_image(zzz_frame.copy(),self.color[:3])
        zzz_text.alpha_composite(zzz_frame)
        background.alpha_composite(zzz_text, (564,-37))
        
        
        splash_one = await recolor_image(splash_one.copy(), self.color[:3])
        background.alpha_composite(splash_one)
        
        splash_two = await recolor_image(splash_two.copy(), self.color[:3])
        splash_two = ImageChops.overlay(splash_two.copy(), overlay_splash.convert("RGBA"))
        background.alpha_composite(splash_two)
        

        wave_down = await recolor_image(wave_down.copy(), await get_dark_pixel_color(self.color[:3]))
        background.alpha_composite(wave_down)
        
        wave_up = await recolor_image(wave_up.copy(), self.color[:3])
        background.alpha_composite(wave_up)
        
        background.alpha_composite(wave_line)
        
        icon = await get_download_img(wiki.data.page.header_img_url, size=(874,874))
        
        icon_d = await recolor_image(icon.copy(), (0,0,0))
        icon_c = await recolor_image(icon.copy(), self.color[:3])
        
        background.alpha_composite(icon_d, (-75,-25))
        background.alpha_composite(icon_c, (-65,-24))
        background.alpha_composite(icon, (-70,-25))
        
        level_c = await create_image_with_text_v2(f"LEVEL: {self.avatar.level}", 75, 800, color=self.color)
        level_d = await recolor_image(level_c.copy(), (0,0,0))
        level = Image.new("RGBA", (level_c.width + 10, level_c.height + 10), (0,0,0,0))
        level.alpha_composite(level_d)
        level.alpha_composite(level_d, (5,3))
        level.alpha_composite(level_c, (3,1))
        
        #level = level.rotate(20, expand=True)
        background.alpha_composite(level,(39,707))
        
        background.alpha_composite(texture_line)
        background.alpha_composite(pixel)
        
        return background
        
    async def create_relict(self) -> list:
        relict_list = []
        relict_icon = await _of.relict_icon
        relict_level = await _of.relict_level
        relict_stats = await _of.relict_stats
        font_20 = await get_font(20)
        
        sets_relict = {}
        
        for key in self.avatar.equip:

            relict_icon = relict_icon.copy()
            relict_level = await recolor_image(relict_level.copy(), self.text_color[:3])
            relict_stats: Image.Image = await recolor_image(relict_stats.copy(), color_rang.get(key.rarity))
            relict_up = await _of.relict_up
            relict_up = relict_up.copy()
            relict = Image.new("RGBA", (195,195), (0,0,0,0))
            
            icon = await get_download_img(key.icon, size=(110,110))
            
            relict_icon.alpha_composite(icon, (43,0))
            relict.alpha_composite(relict_icon, (0,0))
            main_icon = await get_download_img(icon_properties_relict.get(str(key.main_properties[0].property_id)), size=(30,30))
            relict_stats.alpha_composite(main_icon, (0,1))
            draw = ImageDraw.Draw(relict_stats)
            draw.text((32,10), str(key.main_properties[0].base), font = font_20, fill = (255,255,255,255))

            draw = ImageDraw.Draw(relict_level)
            x = int(font_20.getlength(f"+{key.level}")/2)
            draw.text((24-x,6), f"+{key.level}", font = font_20, fill = (27,27,27,255))
            
            relict_up.alpha_composite(relict_stats,(6,73))
            relict_up.alpha_composite(relict_level,(141,77))
            
            
            x = 6
            y = 115
            draw = ImageDraw.Draw(relict_up)
            for i, prop in enumerate(key.properties):

                prop_icon = await get_download_img(icon_properties_relict.get(str(prop.property_id)), size=(30,30))
                prop_icon = await recolor_image(prop_icon, self.text_color[:3])

                relict_up.alpha_composite(prop_icon,(x,y))
                
                draw.text((x + 40, y + 7), prop.base, font = font_20, fill = self.text_color)

                y = 151 
                
                if i == 1:
                    x = 109
                    y = 115
                
                
            relict.alpha_composite(relict_up)
            
            relict_list.append(relict)
            
            
            if not key.equip_suit.suit_id in sets_relict:
                if key.equip_suit.own > 1:
                    sets_relict[key.equip_suit.suit_id] = {"name": key.equip_suit.name, "value": key.equip_suit.own}


        return relict_list, sets_relict
    
    async def create_stats_skill(self) -> Image.Image:
                
        background_skill = await _of.skill
        
        
        stats = await _of.stats
        stats = stats.copy()
        stats_background_overlay = await _of.stats_background_overlay
        stats_background_up = await _of.stats_background_up
        stats_background_up_shadow = await _of.stats_background_up_shadow
        
        stats_background_up = await recolor_image(stats_background_up.copy(), self.color[:3])
        stats_background_up.alpha_composite(stats_background_overlay)
        stats_background_up_shadow.alpha_composite(stats_background_up)
        
        stats.alpha_composite(stats_background_up_shadow,(0,74))
        font_24 = await get_font(24)
        font_18 = await get_font(18)
        x = 15
        
        skill = background_skill.copy()
        for key in self.avatar.skills:
            draw = ImageDraw.Draw(skill)
            if len(str(key.level)) == 1:
                key.level = f"0{key.level}"
            draw.text((x,50), str(key.level), font = font_24, fill = (255,255,255,255))
            x += 109
        
        stats.alpha_composite(skill,(48,99))
        
        stats_frame = await _of.stats_frame
        xx = 34
        y = 224
        
        for i, key in enumerate(self.avatar.properties):
            frame = stats_frame.copy()
            icon = await get_download_img(icon_properties_character.get(str(key.property_id)), size= (57,57))
            frame.alpha_composite(icon,(3,29))
            text = split_long_words(key.property_name)
            name = await create_image_with_text_v2(text, 16, 95, (255,255,255,255))
            draw = ImageDraw.Draw(frame)
            font_24 = await get_font(18)
            x = int(font_18.getlength(str(key.final))/2)
            draw.text((32-x,12), str(key.final), font = font_18, fill = (255,255,255,255))
            frame.alpha_composite(name,(64,32))

            stats.alpha_composite(frame, (xx,y))
            xx += 177
            
            if i in [3, 7]:
                xx = 34
                y += 125
        
        return stats
    
    async def build(self, background:Image.Image,
        relict_list: list,
        sets: list,
        stats:Image.Image,
        weapon:Image.Image,
        organization:Image.Image,
        rank_background:Image.Image,
        elements_icon:Image.Image,
        constant:Image.Image
    ) -> Image.Image:

        x = 774
        y = 18
        for i, key in enumerate(relict_list):
            background.alpha_composite(key.resize((163,165)), (x,y))
            
            i += 1
            y += 176
            if i == 3:
                x = 953
                y = 18
        
        position = [
            (809,546),
            (718,586),
            (817,632),
        ]
                
        for i, key in enumerate(sets):
            background.alpha_composite(key, position[i])
        
        
        background.alpha_composite(stats,(1155,50))
        background.alpha_composite(weapon, (1535,530))
        
        logo = await _of.logo
        background.alpha_composite(logo.resize((295,71)),(1591,735))
        
        background.alpha_composite(organization, (15,101))
        background.alpha_composite(rank_background,(32,297))
        background.alpha_composite(elements_icon,(32,380))
        background.alpha_composite(constant,(32,214))
        
        background.alpha_composite(self.name,(485,687))
        background.alpha_composite(self.name_white,(499,691))
        background.alpha_composite(self.name_color,(491,689))
        
        #background.save(f"{self.avatar.name_mi18n}.png")
        
        return background

    async def create_sets(self, sets):
        #background = await _of.relict_stats
        
        sets_one = await _of.sets_one
        
        sets_one = await recolor_image(sets_one.copy(), self.color[:3])
        sets_two = await _of.sets_two
        
        sets_one.alpha_composite(sets_two)
        sets_three = await _of.sets_three
        
        sets_three = await recolor_image(sets_three.copy(), self.color[:3])
        sets_one.alpha_composite(sets_three)
        
        sets_four = await _of.sets_four
        sets_one.alpha_composite(sets_four)
        
        sets_itog = []
        
        for key in sets:
            bg = sets_one.copy()
            text = f'{sets[key]["name"]} [{sets[key]["value"]}/4]'
            text_font, x = await get_text_size_frame(text, 16, 317)
            
            draw = ImageDraw.Draw(bg)
            draw.text((int(170-x/2), 13), text, font = text_font, fill = self.text_color)
            
            sets_itog.append(bg)
            
        return sets_itog
    
    async def weapon(self) -> Image.Image:
        if self.avatar.weapon is None:
            return Image.new("RGBA",(1,1),(0,0,0,0))
        icon = await get_download_img(self.avatar.weapon.icon, size=(112,112))
        weapon_shadow = await _of.weapon_shadow
        weapon_shadow = weapon_shadow.copy()
        background_weapon = await _of.background_weapon
        weapon_overlay = await _of.weapon_overlay
        weapon_up = await _of.weapon_up
        weapon_text = await _of.weapon_text

        background_weapon = await recolor_image(background_weapon.copy(), self.color[:3])
        
        #weapon_text_rarity = await recolor_image(weapon_text.copy(), color_rang.get(self.avatar.weapon.rarity))
        #weapon_text = await recolor_image(weapon_text.copy(), (0,0,0))    
        weapon_shadow.alpha_composite(background_weapon)
        #weapon_shadow.alpha_composite(weapon_text, (-3,0))
        weapon_shadow.alpha_composite(weapon_text)
        weapon_shadow.alpha_composite(weapon_up)
        
        
        background = Image.new("RGBA", (379,169), (0,0,0,0))
        weapon_shadow = weapon_shadow.resize((379,169))
        weapon_shadow.alpha_composite(weapon_overlay)
        
        background.alpha_composite(weapon_shadow)
        
        
        #rank_icon  = await get_rank_icon(self.avatar.weapon.rarity)
        
        #background.alpha_composite(rank_icon.copy().resize((64,60)), (0,17))
        background.alpha_composite(icon, (13,44))
        
        stars = await get_stars(self.avatar.weapon.star)
        background.alpha_composite(stars.resize((76,27)), (31,127))
        
        name = await create_image_with_text_v2(self.avatar.weapon.name, 18, 228, (255,255,255,255))

        name_line = Image.new("RGBA", (2,name.height), color_rang.get(self.avatar.weapon.rarity))
        
        background.alpha_composite(name_line,(127,51))
        background.alpha_composite(name,(129,51))
        
        draw = ImageDraw.Draw(background)
        font_19 = await get_font(19)
        
        main_icon = await get_download_img(icon_properties_relict.get(str(self.avatar.weapon.main_properties[0].property_id)), size=(24,24))
        main_icon = await recolor_image(main_icon, self.text_color)
        main_value = self.avatar.weapon.main_properties[0].base
        background.alpha_composite(main_icon,(129,103))
        draw.text((158,108), str(main_value), font = font_19, fill = (255,255,255,255))
        
        main_icon = await get_download_img(icon_properties_relict.get(str(self.avatar.weapon.properties[0].property_id)), size=(24,24))
        main_icon = await recolor_image(main_icon, self.text_color)
        main_value = self.avatar.weapon.properties[0].base
        background.alpha_composite(main_icon,(231,103))
        draw.text((260,108), str(main_value), font = font_19, fill = (255,255,255,255))
        
        level = await create_image_with_text_v2(f"LEVEL: {self.avatar.weapon.level}", 19, 175, (255,255,255,255))
        
        background.alpha_composite(level,(int(356-level.width),130))
        
        return background
    
    async def create_organization(self) -> Image.Image:
        
        organization = Image.new("RGBA", (116,113), (0,0,0,0))
        
        icon = await get_download_img(self.avatar.group_icon_path, size=(107,107))
        icon_d = await recolor_image(icon.copy(), (0,0,0))
        icon_c = await recolor_image(icon.copy(), self.color[:3])
        
        organization.alpha_composite(icon_d, (0,6))
        organization.alpha_composite(icon_c, (5,2))
        organization.alpha_composite(icon, (9,0))
        
        
        return organization
    
    async def information_icon(self) -> Image.Image:
        frame = await _of.frame_info
        background = await _of.background_info
        background: Image.Image = await recolor_image(background.copy(), self.color[:3])
        background.alpha_composite(frame)
        
        rank_background = background.copy()
        element_background = background.copy()
        #profession_background = background.copy()
        elements_icon = await get_download_img(element_icon.get(self.avatar.element_type), size=(55,55))
        rank_icon = await get_rank_icon(self.avatar.rarity)
        
        rank_background.alpha_composite(rank_icon.resize((64,60)), (10,11))
        element_background.alpha_composite(elements_icon, (14,14))
                
        return rank_background, element_background
    
    async def create_constant_icon(self) -> Image.Image:
        frame = await _of.frame_info
        background = await _of.background_info
        
        background = await recolor_image(background.copy(), (0,0,0))
        frame = await recolor_image(frame.copy(), self.text_color[:3])
        
        icon = await get_const(self.avatar.rank)
        icon = await recolor_image(icon, self.text_color[:3])
        background.alpha_composite(frame)
        background.alpha_composite(icon.resize((55,55)), (14,14))
        
        return background

    async def create_name(self) -> None:
        text = self.avatar.name_mi18n.upper()
        size = await get_text_size_frame(text,117,955, True)
        self.name = await create_image_with_text_v2(text, size, max_width=955, color= (0,0,0,255))
        
        self.name_white = await recolor_image(self.name, (255,255,255))
        self.name_color = await recolor_image(self.name, self.color[:3])        
               
    async def start(self, avatar: AvatarListItem, items_id: list, wiki: dict):
                
        self.items_id = items_id
        self.avatar = avatar
        self.page_id = await self.base_self.get_wiki_page()
        self.wiki = wiki
                    
        link = next(filter(lambda x: x["name"] == avatar.full_name_mi18n, self.page_id.get("data").get("list")), None)
        if link is None:
            link = {"entry_page_id": self.wiki.get(avatar.id).replace("https://wiki.hoyolab.com/pc/zzz/entry/","")}
        wiki = await self.base_self.get_wiki_info(link.get("entry_page_id"))
        
        
        if self.base_self.color_user is None:
            color_user = None
        else:
            color_user = self.base_self.color_user.get(str(avatar.id))
            
        if color_user is None:
            if wiki.data.page.ext.personalized_color == "":
                self.color = hex_to_rgba("#3b3b3b")
            else:
                self.color = hex_to_rgba(wiki.data.page.ext.personalized_color)
                ll = await light_level(self.color)
                if ll > 0.40:
                    self.color = await get_dark_pixel_color(self.color)
        else:
            self.color = color_user
            
        self.text_color = await get_light_pixel_color(self.color, up= True)
        
        
        task =  [
                    self.create_background(wiki),
                    self.create_stats_skill(),
                    self.weapon(),
                    self.create_organization(),
                    self.create_constant_icon(),
                    self.create_name()
                ]
        
        background, stats, weapon, organization,constant, _ = await asyncio.gather(*task)
        
        relict_list, sets_relict = await self.create_relict()
        sets = await self.create_sets(sets_relict)
        rank_background, elements_icon = await self.information_icon()
        
        card = await self.build(background, relict_list,sets, stats, weapon, organization,rank_background, elements_icon, constant)
    
    
        return {
            "id": avatar.id,
            "name": avatar.name_mi18n,
            "rarity": avatar.rarity,
            "profession": avatar.avatar_profession,
            "icon": avatar.hollow_icon_path,
            "card": card,
            "size": card.size,
            "color": self.color
        }
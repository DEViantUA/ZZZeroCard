# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image
import os
import threading
from pathlib import Path
from io import BytesIO

from .http import AioSession
from .cache import Cache

lock = threading.Lock()

_caches = Cache.get_cache()

assets = Path(__file__).parent.parent / 'assets'

_BASE_URL = 'https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/main/assets/'

font = str(assets / 'font' / 'zzz_font.otf')


def determine_font_path_automatically(font_file = 'Times New Roman.ttf'):
    font_dirs = [
        '/usr/share/fonts',          
        '/usr/local/share/fonts',    
        '/Library/Fonts',           
    ]
        
    for font_dir in font_dirs:
        font_path = os.path.join(font_dir, font_file)
        if os.path.isfile(font_path):
            return font_path

    return None

async def change_font(font_path = None):
    global font
    if font_path is None:
        font = str(assets / 'font' / 'zzz_font.otf')
    else:
        font_path = os.path.abspath(font_path)
        if os.path.isfile(font_path):
            font = font_path 
        else:
            font_path = determine_font_path_automatically(font_path)
            if font_path is None:
                font = str(assets / 'font' / 'zzz_font.otf')

style_one = {
    "background": 'style_one/background/background.png',
    "overlay_splash": 'style_one/background/overlay_splash.png',
    "pixel": 'style_one/background/pixel.png',
    "splash_one": 'style_one/background/splash_one.png',
    "splash_two": 'style_one/background/splash_two.png',
    "texture_line": 'style_one/background/texture_line.png',
    "wave_down": 'style_one/background/wave_down.png',
    "wave_line": 'style_one/background/wave_line.png',
    "wave_up": 'style_one/background/wave_up.png',
    "zzz_text": 'style_one/background/zzz_text.png',
    "zzz_text_frame": 'style_one/background/zzz_text_frame.png',
    "character_list": 'style_one/background/character_list.png',
    
    
    "background_info": 'style_one/info/background_info.png',
    "frame_info": 'style_one/info/frame_info.png',
    

    "relict_icon": 'style_one/relict/icon.png',
    "relict_level": 'style_one/relict/level.png',
    "sets": 'style_one/relict/sets.png',
    "relict_stats": 'style_one/relict/stats.png',
    "relict_up": 'style_one/relict/up.png',
    
    
    "sets_one": 'style_one/relict/sets_one.png',
    "sets_two": 'style_one/relict/sets_two.png',
    "sets_three": 'style_one/relict/sets_three.png',
    "sets_four": 'style_one/relict/sets_four.png',
    
    
    "stats": 'style_one/stats/stats.png',
    "stats_background_overlay": 'style_one/stats/stats_background_overlay.png',
    "stats_background_up": 'style_one/stats/stats_background_up.png',
    "stats_background_up_shadow": 'style_one/stats/stats_background_up_shadow.png',
    "stats_frame": 'style_one/stats/stats_frame.png',
    "skill": 'style_one/stats/skill.png',
    
    "weapon_shadow": 'style_one/weapon/weapon_shadow.png',
    "background_weapon": 'style_one/weapon/background_weapon.png',
    "weapon_overlay": 'style_one/weapon/weapon_overlay.png',
    "weapon_up": 'style_one/weapon/weapon_up.png',
    "weapon_text": 'style_one/weapon/weapon_text.png',

    "const_0": 'style_one/const/const_1.png',
    "const_1": 'style_one/const/const_1.png',
    "const_2": 'style_one/const/const_2.png',
    "const_3": 'style_one/const/const_3.png',
    "const_4": 'style_one/const/const_4.png',
    "const_5": 'style_one/const/const_5.png',
    "const_6": 'style_one/const/const_6.png',
    
}

total_style = {
    "stars_one": 'stars/one.png',
    "stars_two": 'stars/two.png',
    "stars_three": 'stars/three.png',
    "stars_four": 'stars/four.png',
    "stars_five": 'stars/five.png',
    "logo": 'logo.png',
    
    "rank_s": 'rank_icon/s.png',
    "rank_a": 'rank_icon/a.png',
    "rank_b": 'rank_icon/b.png',
}

class ImageCache:
    
    _assets_download = False
    _mapping = {}
            
    @classmethod
    async def set_assets_download(cls, download = False):
        cls._assets_download = download
    
    @classmethod
    def set_mapping(cls,style):
        if style == 1:
            cls._mapping = style_one
        
    @classmethod
    async def _load_image(cls, name):
        
        try:
            image = _caches[name]
        except KeyError:
            try:
                _caches[name] = image = Image.open(assets / name)
                return _caches[name]
            except Exception as e:
                pass
        
        try:
            _caches[name] = image = Image.open(assets / name)
            return _caches[name]
        except Exception as e:
            pass
        
        url = _BASE_URL + name
        if url in _caches:
            return _caches[name]
        else:
            image_data = await AioSession.get(url, response_format= "bytes")
            image = Image.open(BytesIO(image_data))
            _caches[name] = image
        
        if cls._assets_download:
            file_path = assets / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(str(assets / name))
        
        return image

    async def __getattr__(cls, name):
        if name in cls._mapping:
            return await cls._load_image(cls._mapping[name])
        else:
            if name in total_style:
                return await cls._load_image(total_style[name]) 
            else:
                raise AttributeError(f"'{cls.__class__.__name__}' object has no attribute '{name}'")
import datetime
import aiofiles
import os
import io
from PIL import Image

SUPPORT_LANG = {
    "cn": "zh-cn",
    "cht": "zh-tw",
    "de": "de-de",
    "en": "en-us",
    "es": "es-es",
    "fr": "fr-fr",
    "id": "id-id",
    "it": "it-it",
    "ja": "ja-jp",
    "ko": "ko-kr",
    "pt": "pt-pt",
    "ru": "ru-ru",
    "th": "th-th",
    "vi": "vi-vn",
    "tr": "tr",
}

CHARACTER = "https://sg-act-nap-api.hoyolab.com/event/game_record_zzz/api/zzz/avatar/info"
WIKI = "https://sg-wiki-api-static.hoyolab.com/hoyowiki/zzz/wapi/entry_page"
WIKI_CHARACTER = "https://sg-wiki-api.hoyolab.com/hoyowiki/zzz/wapi/get_entry_page_list"


icon_urls = {
    "impact": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-impact-icon.6d9c9282.png",
    "weapon_suit": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/weapon-suit-icon.f75f0d28.png"
}

icon_properties_character = {
    "1": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-hp-icon.59cb16ef.png",
    "2": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-atk-icon.7e5f0cb6.png",
    "3": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-def-icon.a927965c.png",
    "4": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-impact-icon.6d9c9282.png",
    "5": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-crit-rate-icon.810d1d8e.png",
    "6": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-crit-dmg-icon.b896fc9e.png",
    "7": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-anomaly-mastery-icon.f4fc5970.png", 
    "8": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-anomaly-proficiency-icon.38adc36b.png",
    "9": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-pen-ratio-icon.90bc6385.png",
    "10": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-energy-regen-icon.2ec55369.png"
}

icon_properties_relict = {
    "11103": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-hp-icon.59cb16ef.png",
    "11102": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-hp-icon.59cb16ef.png",
    "12103": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-atk-icon.7e5f0cb6.png",
    "12102": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-atk-icon.7e5f0cb6.png",
    "12101": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-atk-icon.7e5f0cb6.png",
    "13103": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-def-icon.a927965c.png",
    "13102": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-def-icon.a927965c.png",
    "20103": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-crit-rate-icon.810d1d8e.png",
    "21103": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-crit-dmg-icon.b896fc9e.png",
    "23203": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-pen-ratio-icon.90bc6385.png",
    "23103": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-pen-ratio-icon.90bc6385.png",
    "31203": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-anomaly-proficiency-icon.38adc36b.png",
    "31903":"https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-anomaly-proficiency-icon.38adc36b.png",
    "31503": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-impact-icon.6d9c9282.png",
    "30502": "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/prop-energy-regen-icon.2ec55369.png",
}


color_rang = {
    "S": (255,198,99),
    "A": (183,99,255),
    "B": (99,180,255),
}


element_icon = {
    205: "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/attribute-ether-icon.9a1e42a1.png",
    203: "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/attribute-electric-icon.ad4c441f.png",
    202: "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/attribute-ice-icon.5c85742d.png",
    201: "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/attribute-fire-icon.aeddecee.png",
    200: "https://act.hoyolab.com/app/mihoyo-zzz-game-record/images/attribute-physical-icon.a657c07a.png",
}



def split_long_words(text, max_length=7):
    words = text.split()
    result = []

    for word in words:
        if len(word) > max_length:
            split_word = '-\n'.join([word[i:i+max_length] for i in range(0, len(word), max_length)])
            result.append(split_word)
        else:
            result.append(word)
    
    return ' '.join(result)


def get_color_user(color):
    processed_dict = {}
    for key, value in color.items():
        if isinstance(value, tuple):
            if len(value) >= 3 and len(value) <= 4:
                if all(0 <= x <= 255 for x in value):
                    processed_dict[key] = value
    if processed_dict != {}:
        return processed_dict
    
    return None

async def save_card(uid, image_data, name):
    data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M")
    path = os.getcwd()
    
    try:
        os.makedirs(f'{path}/CardZZZero/{uid}', exist_ok=True)
    except FileExistsError:
        pass
    
    file_name = f"{path}/CardZZZero/{uid}/{name}_{data}.png"
    
    async with aiofiles.open(file_name, 'wb') as file:
        if isinstance(image_data, Image.Image):
            img_bytes = io.BytesIO()
            image_data.save(img_bytes, format='PNG')
            await file.write(img_bytes.getvalue())
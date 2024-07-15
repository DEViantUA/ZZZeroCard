# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import json
from PIL import ImageFont,Image,ImageDraw
from .. import cache, git

_caches = cache.Cache.get_cache()

async def get_font(size):
    return ImageFont.truetype(git.font, size)

async def get_text_size_frame(text,font_size,frame_width, return_size = False):    
    font = await get_font(font_size)

    while font.getlength(text) > frame_width:
        font_size -= 1
        font = await get_font(font_size)
    if return_size:
        return font_size
    return font,font.getlength(text)


async def create_image_with_text(text, font_size, max_width=336, color=(255, 255, 255, 255), alg="Left"):
    cache_key = json.dumps((text, font_size, max_width, color, alg), sort_keys=True)
    if cache_key in _caches:
        return _caches[cache_key]
    
    font = await get_font(font_size)

    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
            temp_width = font.getmask(temp_text).getbbox()[2]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)

    width = 0
    height = 0
    for line in lines:
        line_width = font.getmask(' '.join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(' '.join(line)).getbbox()[3]

    img = Image.new('RGBA', (min(width, max_width), height + (font_size)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    
    y_text = 0
    for line_num, line in enumerate(lines):
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        if alg == "center" and line_num > 0:
            x_text = (max_width - text_width) // 2
        else:
            x_text = 0
        draw.text((x_text, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height + 5
        
    _caches[cache_key] = img
    
    return img


def calculate_text_size(text, font, max_width):
    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
            temp_width = font.getbbox(temp_text)[2] - font.getbbox(temp_text)[0]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)

    max_line_width = max(font.getbbox(' '.join(line))[2] - font.getbbox(' '.join(line))[0] for line in lines)
    total_height = sum(font.getbbox(' '.join(line))[3] - font.getbbox(' '.join(line))[1] for line in lines) + (len(lines) - 1) * 5

    return lines, min(max_line_width, max_width), total_height


async def create_image_with_text_v2(text: str, font_size: int, max_width: int = 336, color: tuple = (255, 255, 255, 255), padding_default:tuple = (0,0), alg: str = "Left") -> Image.Image:
    cache_key = json.dumps((text, font_size, max_width, color, alg), sort_keys=True)
    if cache_key in _caches:
        return _caches[cache_key]
    
    font = await get_font(font_size)

    lines, width, height = calculate_text_size(text, font, max_width)

    padding = 5
    img_width = width + 2 * padding + padding_default[0]
    img_height = height + 2 * padding + padding_default[1]

    img = Image.new('RGBA', (img_width, img_height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    y_text = padding
    for line in lines:
        line_text = ' '.join(line)
        bbox = font.getbbox(line_text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if alg.lower() == "center":
            x_text = (img_width - text_width) // 2
        else:
            x_text = padding
        draw.text((x_text, y_text), line_text, font=font, fill=color)
        y_text += text_height + 5

    _caches[cache_key] = img
    
    return img
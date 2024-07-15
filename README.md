<img src = "https://raw.githubusercontent.com/DEViantUA/ZZZeroCard/main/ReadMe/ZZZBANNER.png" >


# ZZZeroCard

Module for creating cards with characters from the game Zenless zone zero!

----

* [Telegram](https://t.me/enkacardchat)
* [Patreon](https://www.patreon.com/deviantapi)
-----
### Install:

```bash
pip install zzzerocard
```

### Launch:

```py
import zzzerocard
import asyncio 


cookies = {
    "ltoken_v2": "YOU_LTOKEN",
    "ltmid_v2": "YOU_LTMID",
    "ltuid_v2": "YOU_LTUID"
}


#Setting the module settings

client = zzzerocard.ZZZeroCard(
      lang="en", #Language in which you need to receive information
      asset_save= True, #Save card assets | Speeds up creation, takes up storage space
      boost_speed= True, #Save character resources | Speeds up creation, takes up storage space
      cookie= cookies, #information about your cookies from the HoYoLab website
      uid=184551462, #Your game UID
      server= "prod_gf_jp", #ID Server | prod_gf_eu - Europe
      color = {"1181": (88,57,57,255)}, #Set character color
      save= False #Should I save the result?
    )

async def main():
    async with client:
        data = await client.create() 
        print(data)

asyncio.run(m())
```

### Resultat:

<details>
<summary>Resultat Style 1</summary>
 
[![Adaptation][1]][1]
 
[1]: https://github.com/DEViantUA/ZZZeroCard/blob/main/ReadMe/Style_one.png

</details>

# Thank the author for the code: 
* **Patreon**: https://www.patreon.com/deviantapi
* **Ko-Fi**: https://ko-fi.com/dezzso

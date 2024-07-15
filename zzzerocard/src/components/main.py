import abc
from .api import ZZZeroCardAPI
from ..tools.settings import SUPPORT_LANG, WIKI
from ..model.character import CharacterInfo
from ..model.wiki import WikiInfo
from ...src.tools.pill import image_control
from ...src.tools import settings

class BasesClass(abc.ABC):
    
    def __init__(self, 
                lang:str = "en",
                cookie: dict = {},
                server: str =  "prod_gf_eu",
                uid: int= 1502457277,
                asset_save: bool = False,
                boost_speed: bool = True,
                color: tuple = None,
                save: bool = False
            ) -> None:
        
        """Main class

        Args:
            lang (str, optional): Set the language for the module
            cookie (bool, optional): Save assets to device, fills device storage. Defaults to False.
        """
        self.lang: str = lang
        self.cookie: dict = cookie
        self.server: str = server
        self.uid: int = uid
        self.asset_save: bool = asset_save
        self.boost_speed: bool = boost_speed
        self.save = save
        
        if isinstance(color, dict):
            self.color_user = settings.get_color_user(color)
            
        image_control._boost_speed = self.boost_speed
        super().__init__()
        
        self.check_lang()
        
        self.client: ZZZeroCardAPI = ZZZeroCardAPI(lang=self.lang, uid = self.uid, server = self.server, cookies= self.cookie)
        
    def check_lang(self) -> None:
        if not self.lang in SUPPORT_LANG.keys():
            self.lang = "en-us"
        else:
            self.lang = SUPPORT_LANG.get(self.lang)
        
    def create_headers(self) -> dict:
        return self.client._build_headers()    
        
    
    async def get_agent(self, id: int) -> CharacterInfo:
        data = await self.client.request(id=[id])
        self.data = CharacterInfo(**data)
        
    
    async def get_list_agent(self) -> CharacterInfo:
        data =  await self.client.request()
        self.data_list = CharacterInfo(**data)
    
    
    async def get_wiki_page(self):
        data = await self.client.request_wiki_page()
        return data
        
    
    async def get_wiki_info(self, id:int) -> WikiInfo:
        data =  await self.client.request(id = [id], url = WIKI)
        return WikiInfo(**data)
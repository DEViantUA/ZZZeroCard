import aiohttp
from datetime import datetime
from ..tools.settings import CHARACTER, WIKI_CHARACTER
from ..tools import http

class ZZZeroCardAPI:
    def __init__(self, 
                lang="ru-ru", 
                uid="1502457277",
                server: str = "prod_gf_eu",
                cookies: dict = None
                ) -> None:
        
        self.lang = lang
        self.uid = uid
        self.server = server
        self.cookies = cookies
    
    
    async def request_wiki_page(self, url: str = WIKI_CHARACTER) -> dict:
        params = {
            "filters": [],
            "menu_id": "8",
            "page_num": 1,
            "page_size": 50,
            "use_es": "true"
        }
        
        headers = self._build_headers()
        response = await http.AioSession.post(url, headers=headers, params=params, response_format="json")

        if response is None:
            raise TypeError(response.get("message"))
        
        if response.get("retcode") != 0:
            raise TypeError(response.get("message"))
        
        return response
    
    
    async def request(self, id: list = [], url: str = CHARACTER) -> dict:
        params = {
            "need_wiki": "true",
            "server": self.server,
            "role_id": self.uid
        }
        
        if id != []:
            params["id_list[]"] = [str(key) for key in id]
            params["entry_page_id"] = str(id[0])
        
        headers = self._build_headers()
        
        response = await http.AioSession.get(url, headers=headers, params=params, response_format="json")

        if response.get("retcode") != 0:
            raise #TypeError(response.get("message"))
        
        return response
        
    
    def _build_headers(self) -> dict:
        return {
            "Dnt": "1",
            "Origin": "https://act.hoyolab.com",
            "Priority": "u=1, i",
            "Referer": "https://act.hoyolab.com/",
            "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "X-Rpc-Device_fp": "38d7f1c41171b",
            "X-Rpc-Device_id": "aabb12f1-c8cc-4113-99e1-9bc2d7ad583d",
            "X-Rpc-Lang": self.lang,
            "X-Rpc-Language": self.lang,
            "X-Rpc-Page": "v1.0.20_#/zzz/roles/1031/detail",
            "X-Rpc-Platform": "4",
            "X-Rpc-Wiki_app": "zzz",
            "Cookie": self._build_cookie_string()
        }
    
    def _build_cookie_string(self) -> str:
        DEVICEFP_SEED_TIME = int(datetime.now().timestamp() * 1000)
        fixed_cookies = {
            "_MHYUUID": self.cookies.get('_MHYUUID', ''),
            "HYV_LOGIN_PLATFORM_OPTIONAL_AGREEMENT": self.cookies.get('HYV_LOGIN_PLATFORM_OPTIONAL_AGREEMENT', ''),
            "DEVICEFP_SEED_ID": self.cookies.get('DEVICEFP_SEED_ID', ''),
            "DEVICEFP_SEED_TIME": DEVICEFP_SEED_TIME,
            "_ga_V5D1BW264Z": self.cookies.get('_ga_V5D1BW264Z', ''),
            "hoyolab_color_scheme": self.cookies.get('hoyolab_color_scheme', ''),
            "account_mid_v2": self.cookies.get('ltmid_v2', ''),
            "account_id_v2": self.cookies.get('ltuid_v2', ''),
            "ltoken_v2": self.cookies.get('ltoken_v2', ''),
            "ltmid_v2": self.cookies.get('ltmid_v2', ''),
            "ltuid_v2": self.cookies.get('ltuid_v2', ''),
            "HYV_LOGIN_PLATFORM_LOAD_TIMEOUT": self.cookies.get('HYV_LOGIN_PLATFORM_LOAD_TIMEOUT', ''),
            "_ga_Z2CH03T4VN": self.cookies.get('_ga_Z2CH03T4VN', ''),
            "_ga_CYB6ETZXPE": self.cookies.get('_ga_CYB6ETZXPE', ''),
            "_ga_27EG203DM0": self.cookies.get('_ga_27EG203DM0', ''),
            "_ga_F08558F5L1": self.cookies.get('_ga_F08558F5L1', ''),
            "_ga_Y5SZ86WZQH": self.cookies.get('_ga_Y5SZ86WZQH', ''),
            "_ga_SBYZMHZRMJ": self.cookies.get('_ga_SBYZMHZRMJ', ''),
            "_ga_1CHR121QPG": self.cookies.get('_ga_1CHR121QPG', ''),
            "_ga_DLRHD8PLDD": self.cookies.get('_ga_DLRHD8PLDD', ''),
            "_ga_JTLS2F53NR": self.cookies.get('_ga_JTLS2F53NR', ''),
            "_ga_GFC5HN79FG": self.cookies.get('_ga_GFC5HN79FG', ''),
            "_ga": self.cookies.get('_ga', ''),
            "_ga_GEYW4HC0FV": self.cookies.get('_ga_GEYW4HC0FV', ''),
            "_ga_PDXBNGQFCP": self.cookies.get('_ga_PDXBNGQFCP', ''),
            "DEVICEFP": self.cookies.get('DEVICEFP', ''),
            "mi18nLang": self.cookies.get('mi18nLang', ''),
            "e_nap_token": self.cookies.get('e_nap_token', ''),
            "HYV_LOGIN_PLATFORM_TRACKING_MAP": self.cookies.get('HYV_LOGIN_PLATFORM_TRACKING_MAP', ''),
            "HYV_LOGIN_PLATFORM_LIFECYCLE_ID": self.cookies.get('HYV_LOGIN_PLATFORM_LIFECYCLE_ID', ''),
        }
        return "; ".join([f"{key}={value}" for key, value in fixed_cookies.items() if value])
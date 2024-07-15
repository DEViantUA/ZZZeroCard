from .src.components import card
from .src.tools import cache, http


class ZZZeroCard(card.Card):
    async def __aenter__(self):
        cache.Cache.get_cache(maxsize = 1000, ttl = 300)
        await http.AioSession.enter()
        
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await http.AioSession.exit(exc_type, exc, tb)